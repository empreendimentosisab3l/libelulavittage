"""
Sync produtos Caliente -> Supabase Postgres.

Standalone, sem Flask. Roda no GitHub Actions (cron diario + workflow_dispatch).

Estrategia: sitemap completo (descobre TODOS os IDs) -> fetch por produto -> hash check
para escrever apenas o que mudou.

Variaveis de ambiente:
  DATABASE_URL   (obrigatorio) - postgresql://... do Supabase Transaction Pooler
  MODO           (opcional)    - 'full' ou 'incremental'. Default: 'incremental'

`incremental` e `full` rodam a mesma estrategia (sitemap completo); a diferenca e que
`full` ignora o hash e regrava tudo (use para forcar reset apos mudanca de schema).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import psycopg2
import psycopg2.extras
import requests


CALIENTE_URL = "https://calientelingerie.com.br/c/calientelingerie/17996842783"
SITEMAP_URL = "https://calientelingerie.com.br/sitemap.xml"
PRODUCT_URL = "https://calientelingerie.com.br/produto/{pid}/17996842783?ajax=ajax"
CDN_PREFIX = "https://arquivos.facilzap.app.br/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

MAX_WORKERS = 5
REQUEST_TIMEOUT = 20
DEFAULT_MARGEM = 105.0
DEFAULT_WHATSAPP = "43996048712"


def get_conn(database_url: str) -> psycopg2.extensions.connection:
    conn = psycopg2.connect(database_url, connect_timeout=15)
    conn.autocommit = False
    return conn


def load_config(conn) -> dict:
    """Carrega tabela configuracoes em um dict {chave: valor}."""
    with conn.cursor() as cur:
        cur.execute("SELECT chave, valor FROM configuracoes")
        return {row[0]: row[1] for row in cur.fetchall()}


def load_existing_index(conn) -> dict:
    """{url_original (str) -> {'id', 'data_hash'}}"""
    with conn.cursor() as cur:
        cur.execute("SELECT id, url_original, data_hash FROM produtos")
        return {
            str(row[1]): {"id": row[0], "data_hash": row[2]}
            for row in cur.fetchall()
            if row[1]
        }


def calc_hash(preco, imagens_str, tamanhos_str, cores_str, destaque) -> str:
    raw = f"{preco}-{imagens_str}-{tamanhos_str}-{cores_str}-{destaque}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def aplicar_margem(preco_original: float, margem_pct: float) -> float:
    return preco_original * (1 + margem_pct / 100)


def gerar_link_whatsapp(nome: str, preco_venda: float, numero: str) -> str:
    msg = (
        f"Ola! Tenho interesse no produto:\n*{nome}*\n"
        f"Preco: R$ {preco_venda:.2f}\n\nGostaria de mais informacoes!"
    )
    return f"https://wa.me/55{numero}?text={urllib.parse.quote(msg)}"


def fetch_sitemap_ids() -> list[str]:
    resp = requests.get(SITEMAP_URL, timeout=30)
    resp.raise_for_status()
    return sorted(set(re.findall(r"/produto/(\d+)", resp.text)))


def fetch_product(pid: str) -> dict | None:
    try:
        r = requests.get(PRODUCT_URL.format(pid=pid), headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def parse_product(pid: str, item: dict) -> dict | None:
    """Converte o JSON da API Caliente no nosso shape de banco."""
    nome = item.get("nome")
    if not nome:
        return None

    try:
        preco_original = float(item.get("preco", 0))
    except (TypeError, ValueError):
        preco_original = 0.0

    categoria = item.get("categoria_nome") or "Lingerie"

    imagens_lista = item.get("imagens", []) or []
    imagens = [
        img if str(img).startswith("http") else f"{CDN_PREFIX}{img}"
        for img in imagens_lista if img
    ]
    imagens_str = ",".join(imagens)

    tamanhos_set, cores_set = set(), set()
    variacoes = item.get("variacoes") or {}
    disponibilidade = item.get("disponibilidade") or {}
    estoque = item.get("estoque") or {}

    def add_variacao(var_data):
        if not var_data:
            return
        var_nome = (var_data.get("nome") or "").strip()
        var_cor = var_data.get("cor")
        if var_cor and str(var_cor).strip():
            cores_set.add(var_nome)
        else:
            if var_nome.lower().startswith("tamanho "):
                tamanhos_set.add(var_nome[8:].strip())
            elif var_nome:
                tamanhos_set.add(var_nome)

    def stock_for(var_id):
        try:
            return int(estoque.get(var_id, 0))
        except (TypeError, ValueError):
            return 0

    if isinstance(variacoes, dict) and isinstance(disponibilidade, dict) and disponibilidade:
        for var_id in disponibilidade.keys():
            if stock_for(var_id) > 0:
                add_variacao(variacoes.get(var_id))
    elif isinstance(variacoes, dict):
        for var_id, var_data in variacoes.items():
            if stock_for(var_id) > 0:
                add_variacao(var_data)

    m = re.search(r"\((.*?)\)", nome)
    if m and len(m.group(1)) < 30:
        cores_set.add(m.group(1))

    tamanhos_str = ", ".join(sorted(tamanhos_set))
    cores_str = ", ".join(sorted(cores_set))
    destaque = str(item.get("destaque", "0")) == "1"

    return {
        "url_original": str(pid),
        "nome": nome,
        "preco_original": preco_original,
        "categoria": categoria,
        "imagens_str": imagens_str,
        "tamanhos_str": tamanhos_str,
        "cores_str": cores_str,
        "destaque": destaque,
    }


UPSERT_SQL = """
INSERT INTO produtos (
    nome, preco_original, preco_venda, categoria, descricao,
    imagens, tamanhos, cores, data_hash, link_whatsapp,
    url_original, destaque, ativo, data_criacao, data_atualizacao
) VALUES (
    %(nome)s, %(preco_original)s, %(preco_venda)s, %(categoria)s, %(descricao)s,
    %(imagens)s, %(tamanhos)s, %(cores)s, %(data_hash)s, %(link_whatsapp)s,
    %(url_original)s, %(destaque)s, TRUE, %(now)s, %(now)s
)
ON CONFLICT (url_original) DO UPDATE SET
    nome = EXCLUDED.nome,
    preco_original = EXCLUDED.preco_original,
    preco_venda = EXCLUDED.preco_venda,
    categoria = EXCLUDED.categoria,
    imagens = EXCLUDED.imagens,
    tamanhos = EXCLUDED.tamanhos,
    cores = EXCLUDED.cores,
    data_hash = EXCLUDED.data_hash,
    link_whatsapp = EXCLUDED.link_whatsapp,
    destaque = EXCLUDED.destaque,
    ativo = TRUE,
    data_atualizacao = EXCLUDED.data_atualizacao
"""

UPDATE_SQL = """
UPDATE produtos SET
    nome = %(nome)s,
    preco_original = %(preco_original)s,
    preco_venda = %(preco_venda)s,
    categoria = %(categoria)s,
    imagens = %(imagens)s,
    tamanhos = %(tamanhos)s,
    cores = %(cores)s,
    data_hash = %(data_hash)s,
    link_whatsapp = %(link_whatsapp)s,
    destaque = %(destaque)s,
    ativo = TRUE,
    data_atualizacao = %(now)s
WHERE id = %(id)s
"""

INSERT_SQL = """
INSERT INTO produtos (
    nome, preco_original, preco_venda, categoria, descricao,
    imagens, tamanhos, cores, data_hash, link_whatsapp,
    url_original, destaque, ativo, data_criacao, data_atualizacao
) VALUES (
    %(nome)s, %(preco_original)s, %(preco_venda)s, %(categoria)s, %(descricao)s,
    %(imagens)s, %(tamanhos)s, %(cores)s, %(data_hash)s, %(link_whatsapp)s,
    %(url_original)s, %(destaque)s, TRUE, %(now)s, %(now)s
)
"""


def sync(database_url: str, modo: str = "incremental") -> dict:
    print(f"[sync] modo={modo}")
    started = time.time()

    print("[sync] baixando sitemap...")
    ids = fetch_sitemap_ids()
    total = len(ids)
    print(f"[sync] sitemap: {total} IDs unicos")

    conn = get_conn(database_url)
    try:
        config = load_config(conn)
        margem = float(config.get("margem_lucro", DEFAULT_MARGEM))
        whatsapp = config.get("numero_whatsapp", DEFAULT_WHATSAPP)
        print(f"[sync] config: margem={margem}% whatsapp={whatsapp}")

        existing = load_existing_index(conn)
        print(f"[sync] existentes no banco: {len(existing)}")

        stats = {"processados": 0, "criados": 0, "atualizados": 0,
                 "sem_mudanca": 0, "erros": 0, "puladas": 0}

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futures = {pool.submit(fetch_product, pid): pid for pid in ids}

            with conn.cursor() as cur:
                for fut in as_completed(futures):
                    pid = futures[fut]
                    stats["processados"] += 1

                    if stats["processados"] % 50 == 0:
                        print(f"[sync] {stats['processados']}/{total} "
                              f"(criados={stats['criados']} atualizados={stats['atualizados']} "
                              f"unchanged={stats['sem_mudanca']} erros={stats['erros']})")
                        conn.commit()

                    try:
                        item = fut.result()
                        if not item:
                            stats["erros"] += 1
                            continue

                        parsed = parse_product(pid, item)
                        if not parsed:
                            stats["puladas"] += 1
                            continue

                        new_hash = calc_hash(
                            parsed["preco_original"], parsed["imagens_str"],
                            parsed["tamanhos_str"], parsed["cores_str"],
                            parsed["destaque"],
                        )

                        prev = existing.get(parsed["url_original"])
                        if modo != "full" and prev and prev["data_hash"] == new_hash:
                            stats["sem_mudanca"] += 1
                            continue

                        preco_venda = aplicar_margem(parsed["preco_original"], margem)
                        params = {
                            "nome": parsed["nome"],
                            "preco_original": parsed["preco_original"],
                            "preco_venda": preco_venda,
                            "categoria": parsed["categoria"],
                            "descricao": f"{parsed['nome']} - {parsed['categoria']}",
                            "imagens": parsed["imagens_str"],
                            "tamanhos": parsed["tamanhos_str"],
                            "cores": parsed["cores_str"],
                            "data_hash": new_hash,
                            "link_whatsapp": gerar_link_whatsapp(parsed["nome"], preco_venda, whatsapp),
                            "url_original": parsed["url_original"],
                            "destaque": parsed["destaque"],
                            "now": datetime.now(timezone.utc),
                        }

                        if prev:
                            params["id"] = prev["id"]
                            cur.execute(UPDATE_SQL, params)
                            stats["atualizados"] += 1
                        else:
                            cur.execute(INSERT_SQL, params)
                            stats["criados"] += 1

                    except Exception as exc:
                        stats["erros"] += 1
                        conn.rollback()
                        print(f"[sync] erro em {pid}: {exc}", file=sys.stderr)

        conn.commit()

        # Log final
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO logs_scraping
                    (data_execucao, produtos_novos, produtos_atualizados, status, erros)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    datetime.now(timezone.utc),
                    stats["criados"],
                    stats["atualizados"],
                    "sucesso" if stats["erros"] == 0 else "parcial",
                    None if stats["erros"] == 0 else f"{stats['erros']} produtos com erro",
                ),
            )
        conn.commit()

        elapsed = time.time() - started
        print(f"[sync] concluido em {elapsed:.1f}s: {stats}")
        return stats

    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modo", choices=["full", "incremental"],
                        default=os.environ.get("MODO", "incremental"))
    args = parser.parse_args()

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("ERRO: DATABASE_URL nao definida no ambiente", file=sys.stderr)
        sys.exit(2)

    stats = sync(database_url, modo=args.modo)
    if stats["erros"] > 0 and (stats["criados"] + stats["atualizados"]) == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

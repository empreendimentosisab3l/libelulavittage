import sys
import os
sys.path.insert(0, os.getcwd())

from src.main import app
from src.models.produto import Produto, db

print("="*70)
print("RELATÓRIO DE COBERTURA - SCRAPER CALIENTE LINGERIE")
print("="*70)

with app.app_context():
    # Total no nosso banco
    total_nosso_banco = Produto.query.filter_by(ativo=True).count()

    # Total na loja (descoberto pela análise HTML)
    total_loja_caliente = 554

    # Calcular cobertura
    cobertura_percentual = (total_nosso_banco / total_loja_caliente) * 100
    produtos_faltando = total_loja_caliente - total_nosso_banco

    print(f"\nESTATISTICAS:")
    print(f"   Total de produtos na Caliente: {total_loja_caliente}")
    print(f"   Total no nosso banco:          {total_nosso_banco}")
    print(f"   Produtos faltando:             {produtos_faltando}")
    print(f"   Cobertura:                     {cobertura_percentual:.1f}%")

    # Análise por categoria
    print(f"\nPRODUTOS POR CATEGORIA (nosso banco):")
    categorias = db.session.query(
        Produto.categoria,
        db.func.count(Produto.id)
    ).filter_by(ativo=True).group_by(Produto.categoria).order_by(
        db.func.count(Produto.id).desc()
    ).all()

    total_categorias = 0
    for categoria, count in categorias:
        print(f"   {categoria:.<40} {count:>3} produtos")
        total_categorias += count

    print(f"   {'TOTAL':.<40} {total_categorias:>3} produtos")

    # Análise de gap
    print(f"\nANALISE DO GAP ({produtos_faltando} produtos faltando):")
    print(f"   Possiveis causas:")
    print(f"   - Produtos sem nome/categoria compativel com nossa busca")
    print(f"   - Produtos inativos ou ocultos na loja")
    print(f"   - Variacoes de produtos (cores/tamanhos) contados separadamente")
    print(f"   - Termos de busca nao cobertos pela nossa estrategia")

    # Recomendações
    print(f"\nRECOMENDACOES PARA MELHORAR COBERTURA:")
    print(f"   1. Adicionar mais termos de busca especificos")
    print(f"   2. Buscar por cores (preto, branco, vermelho, azul, etc)")
    print(f"   3. Buscar por tamanhos (P, M, G, GG, etc)")
    print(f"   4. Buscar por marcas/linhas especificas")
    print(f"   5. Testar combinacoes de 3 letras alem de 2")

    # Métricas de sucesso
    print(f"\nMETRICAS:")
    if cobertura_percentual >= 70:
        status = "EXCELENTE"
    elif cobertura_percentual >= 50:
        status = "BOA"
    elif cobertura_percentual >= 30:
        status = "RAZOAVEL"
    else:
        status = "PRECISA MELHORAR"

    print(f"   Status da cobertura: {status}")
    print(f"   Cobrimos {cobertura_percentual:.1f}% do catalogo!")

    # Sugestões de termos adicionais
    print(f"\nSUGESTOES DE TERMOS ADICIONAIS:")
    termos_sugeridos = [
        # Cores
        'preto', 'branco', 'vermelho', 'azul', 'rosa', 'verde',
        'amarelo', 'roxo', 'laranja', 'nude', 'bege', 'cinza',
        # Estilos
        'renda', 'transparente', 'aveludado', 'estampado',
        # Tamanhos
        'pequeno', 'medio', 'grande',
        # Ocasiões
        'noite', 'dia', 'especial', 'romântico',
        # Características
        'bojo', 'sem bojo', 'meia taça', 'push up', 'aro',
        # Tecidos
        'cotton', 'elastano', 'poliamida', 'viscose'
    ]

    print(f"   Cores: preto, branco, vermelho, azul, rosa, nude, etc")
    print(f"   Estilos: transparente, aveludado, estampado, etc")
    print(f"   Tamanhos: P, M, G, GG, etc")
    print(f"   Tecidos: cotton, elastano, poliamida, etc")

    print("\n" + "="*70)
    print("CONCLUSAO")
    print("="*70)
    print(f"Nossa estrategia atual captura {cobertura_percentual:.1f}% do catalogo,")
    print(f"o que e um resultado {status}!")
    print(f"\nPara chegar mais perto de 100%, recomendamos:")
    print(f"- Adicionar os termos sugeridos acima")
    print(f"- Executar o scraper novamente")
    print(f"- Monitorar o aumento na cobertura")
    print("="*70)

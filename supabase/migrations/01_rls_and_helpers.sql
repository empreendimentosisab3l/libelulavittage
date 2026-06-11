-- ============================================================
-- Migração 01 — RLS, policies e function auxiliar
-- Aplicar no SQL Editor do Supabase (projeto lingerie-store)
-- ============================================================

-- 1) Habilita RLS nas 3 tabelas (advisor de segurança vai parar de gritar)
ALTER TABLE public.produtos        ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.configuracoes   ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.logs_scraping   ENABLE ROW LEVEL SECURITY;

-- 2) PRODUTOS — qualquer visitante (anon) lê produtos ativos
DROP POLICY IF EXISTS "produtos_select_publico" ON public.produtos;
CREATE POLICY "produtos_select_publico"
  ON public.produtos
  FOR SELECT
  TO anon, authenticated
  USING (ativo = true);

-- Escrita só via service_role (scraper no GitHub Actions / admin via auth)
-- Não precisa policy: service_role bypassa RLS por padrão.

-- 3) CONFIGURACOES — leitura pública apenas das chaves seguras
DROP POLICY IF EXISTS "configuracoes_select_publico" ON public.configuracoes;
CREATE POLICY "configuracoes_select_publico"
  ON public.configuracoes
  FOR SELECT
  TO anon, authenticated
  USING (chave IN ('numero_whatsapp', 'margem_lucro', 'mensagem_padrao'));

-- 4) LOGS_SCRAPING — nada público, só service_role
-- (sem policy = ninguém lê via anon/authenticated)

-- 5) Function para listar categorias distintas (substitui /api/categorias)
CREATE OR REPLACE FUNCTION public.get_categorias()
RETURNS TABLE(categoria text)
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT DISTINCT categoria
  FROM public.produtos
  WHERE ativo = true AND categoria IS NOT NULL
  ORDER BY categoria;
$$;

GRANT EXECUTE ON FUNCTION public.get_categorias() TO anon, authenticated;

-- 6) Índices úteis (catálogo fica mais rápido)
CREATE INDEX IF NOT EXISTS idx_produtos_ativo_destaque_id
  ON public.produtos (ativo, destaque DESC, id DESC);

CREATE INDEX IF NOT EXISTS idx_produtos_categoria
  ON public.produtos (categoria) WHERE ativo = true;

CREATE INDEX IF NOT EXISTS idx_produtos_nome_busca
  ON public.produtos USING gin (to_tsvector('portuguese', nome));

import { supabase } from './supabase'

const DEFAULT_WHATSAPP = '5543996048712'
const DEFAULT_MENSAGEM = 'Olá! Tenho interesse no produto:'

let configCache = null
let configCachePromise = null

export async function getConfig() {
  if (configCache) return configCache
  if (configCachePromise) return configCachePromise

  configCachePromise = (async () => {
    const { data, error } = await supabase
      .from('configuracoes')
      .select('chave, valor')

    if (error) {
      console.warn('[configuracoes] erro ao carregar, usando defaults:', error.message)
      configCache = { numero_whatsapp: DEFAULT_WHATSAPP, mensagem_padrao: DEFAULT_MENSAGEM }
      return configCache
    }

    const map = Object.fromEntries((data || []).map(row => [row.chave, row.valor]))
    configCache = {
      numero_whatsapp: map.numero_whatsapp || DEFAULT_WHATSAPP,
      mensagem_padrao: map.mensagem_padrao || DEFAULT_MENSAGEM,
      margem_lucro: map.margem_lucro
    }
    return configCache
  })()

  return configCachePromise
}

export function normalizeWhatsappNumber(num) {
  const digits = String(num || '').replace(/\D/g, '')
  return digits.startsWith('55') ? digits : `55${digits}`
}

export function formatarWhatsapp(num) {
  const d = normalizeWhatsappNumber(num).slice(2)
  return d.length === 11 ? `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}` : d
}

function gerarLinkWhatsapp(produto, config) {
  const numero = normalizeWhatsappNumber(config?.numero_whatsapp || DEFAULT_WHATSAPP)
  const preco = Number(produto.preco_venda || 0).toFixed(2)
  const msg = `Olá! Tenho interesse no produto:\n*${produto.nome}*\nPreço: R$ ${preco}\n\nGostaria de mais informações!`
  return `https://wa.me/${numero}?text=${encodeURIComponent(msg)}`
}

function rowToProduto(row, config) {
  const imagens = typeof row.imagens === 'string'
    ? row.imagens.split(',').map(s => s.trim()).filter(Boolean)
    : (row.imagens || [])
  const tamanhos = typeof row.tamanhos === 'string'
    ? row.tamanhos.split(',').map(s => s.trim()).filter(Boolean)
    : (row.tamanhos || [])

  return {
    ...row,
    imagens,
    tamanhos,
    link_whatsapp: gerarLinkWhatsapp(row, config)
  }
}

export async function listarProdutos({ page = 1, perPage = 24, categoria, busca } = {}) {
  const config = await getConfig()
  const from = (page - 1) * perPage
  const to = from + perPage - 1

  let query = supabase
    .from('produtos')
    .select('*', { count: 'exact' })
    .eq('ativo', true)
    .order('destaque', { ascending: false })
    .order('id', { ascending: false })
    .range(from, to)

  if (categoria) query = query.ilike('categoria', `%${categoria}%`)
  if (busca) query = query.ilike('nome', `%${busca}%`)

  const { data, error, count } = await query
  if (error) throw error

  const total = count || 0
  return {
    produtos: (data || []).map(row => rowToProduto(row, config)),
    total,
    pages: Math.max(1, Math.ceil(total / perPage)),
    current_page: page,
    per_page: perPage
  }
}

export async function obterProduto(id) {
  const config = await getConfig()
  const { data, error } = await supabase
    .from('produtos')
    .select('*')
    .eq('id', id)
    .maybeSingle()

  if (error) throw error
  if (!data) return null
  return rowToProduto(data, config)
}

export async function listarCategorias() {
  const { data, error } = await supabase.rpc('get_categorias')
  if (error) {
    console.warn('[categorias] RPC falhou, fallback:', error.message)
    const { data: fallback } = await supabase
      .from('produtos')
      .select('categoria')
      .eq('ativo', true)
      .not('categoria', 'is', null)
    const set = new Set((fallback || []).map(r => r.categoria))
    return Array.from(set).sort()
  }
  return (data || []).map(r => r.categoria)
}

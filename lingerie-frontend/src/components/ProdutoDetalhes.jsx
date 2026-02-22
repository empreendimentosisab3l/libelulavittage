import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ShoppingCart, ArrowLeft, ChevronLeft, ChevronRight, Plus, Minus } from 'lucide-react'
import { Button } from './ui/button'
import { useCart } from '../context/CartContext'

const ProdutoDetalhes = ({ apiBaseUrl }) => {
  const { id } = useParams()
  const { addToCart } = useCart()
  const [produto, setProduto] = useState(null)
  const [loading, setLoading] = useState(true)
  const [imagemAtual, setImagemAtual] = useState(0)
  const [selectedVariacoes, setSelectedVariacoes] = useState({})

  useEffect(() => {
    // Scroll to top instantly when product changes
    window.scrollTo(0, 0)
    carregarProduto()
  }, [id])

  const carregarProduto = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${apiBaseUrl}/produtos/${id}`)
      const data = await response.json()
      setProduto(data)
      setSelectedVariacoes({})
    } catch (error) {
      console.error('Erro ao carregar produto:', error)
    } finally {
      setLoading(false)
    }
  }

  const proximaImagem = () => {
    if (produto?.imagens?.length > 1) {
      setImagemAtual((prev) =>
        prev === produto.imagens.length - 1 ? 0 : prev + 1
      )
    }
  }

  const imagemAnterior = () => {
    if (produto?.imagens?.length > 1) {
      setImagemAtual((prev) =>
        prev === 0 ? produto.imagens.length - 1 : prev - 1
      )
    }
  }

  const getVariacoes = () => {
    const baseCode = produto.id?.toString().padStart(8, '0') || '00000000'

    // Usar tamanhos dinâmicos da API (vindos do fornecedor)
    const tamanhosDaAPI = Array.isArray(produto.tamanhos) && produto.tamanhos.length > 0
      ? produto.tamanhos
      : typeof produto.tamanhos === 'string' && produto.tamanhos.trim()
        ? produto.tamanhos.split(', ')
        : ['Tamanho Único']

    return tamanhosDaAPI.map((tamanho, index) => ({
      id: `FZ${baseCode}.${index + 1}`,
      tamanho,
      preco: produto.preco_venda
    }))
  }

  const handleQuantityChange = (variacaoId, tamanho, delta) => {
    setSelectedVariacoes(prev => {
      const current = prev[variacaoId] || 0
      const newValue = Math.max(0, current + delta)

      if (newValue === 0) {
        const { [variacaoId]: _, ...rest } = prev
        return rest
      }

      return {
        ...prev,
        [variacaoId]: newValue
      }
    })
  }

  const handleAddToCart = () => {
    Object.entries(selectedVariacoes).forEach(([variacaoId, quantidade]) => {
      const variacao = getVariacoes().find(v => v.id === variacaoId)
      for (let i = 0; i < quantidade; i++) {
        addToCart(produto, variacaoId, variacao.tamanho)
      }
    })

    setSelectedVariacoes({})
    alert('Peças adicionadas à sua seleção!')
  }

  const getTotalItems = () => {
    return Object.values(selectedVariacoes).reduce((sum, qty) => sum + qty, 0)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0a0a0a]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-[#c9a96e] mx-auto"></div>
          <p className="mt-4 text-gray-400">Preparando sua experiência...</p>
        </div>
      </div>
    )
  }

  if (!produto) {
    return (
      <div className="container mx-auto px-4 py-8 bg-[#0a0a0a] min-h-screen">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white mb-4 font-display">
            Peça não encontrada
          </h1>
          <Link to="/catalogo">
            <Button>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar à Coleção
            </Button>
          </Link>
        </div>
      </div>
    )
  }

  const imagemPrincipal = produto.imagens && produto.imagens.length > 0
    ? produto.imagens[imagemAtual]
    : '/placeholder-product.jpg'

  return (
    <div className="container mx-auto px-4 py-8 bg-[#0a0a0a] min-h-screen">
      {/* Breadcrumb */}
      <nav className="mb-8">
        <Link
          to="/catalogo"
          className="text-[#c9a96e] hover:text-[#b8986e] flex items-center"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Voltar à Coleção
        </Link>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Galeria de Imagens */}
        <div>
          <div className="relative aspect-square mb-4 bg-[#1a1a1a] rounded-lg overflow-hidden border border-[#c9a96e]/20">
            <img
              src={imagemPrincipal}
              alt={produto.nome}
              className="w-full h-full object-cover"
              onError={(e) => {
                e.target.src = '/placeholder-product.jpg'
              }}
            />

            {/* Navegação da galeria */}
            {produto.imagens && produto.imagens.length > 1 && (
              <>
                <button
                  onClick={imagemAnterior}
                  className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white rounded-full p-2 shadow-md transition-all"
                >
                  <ChevronLeft className="h-6 w-6" />
                </button>
                <button
                  onClick={proximaImagem}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white rounded-full p-2 shadow-md transition-all"
                >
                  <ChevronRight className="h-6 w-6" />
                </button>

                {/* Indicadores */}
                <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
                  {produto.imagens.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setImagemAtual(index)}
                      className={`w-3 h-3 rounded-full transition-all ${index === imagemAtual
                          ? 'bg-white'
                          : 'bg-white/50 hover:bg-white/75'
                        }`}
                    />
                  ))}
                </div>
              </>
            )}
          </div>

          {/* Miniaturas */}
          {produto.imagens && produto.imagens.length > 1 && (
            <div className="grid grid-cols-4 gap-2">
              {produto.imagens.slice(0, 4).map((imagem, index) => (
                <button
                  key={index}
                  onClick={() => setImagemAtual(index)}
                  className={`aspect-square rounded-lg overflow-hidden border-2 transition-all ${index === imagemAtual
                      ? 'border-[#c9a96e]'
                      : 'border-[#1a1a1a] hover:border-[#c9a96e]/50'
                    }`}
                >
                  <img
                    src={imagem}
                    alt={`${produto.nome} - ${index + 1}`}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.src = '/placeholder-product.jpg'
                    }}
                  />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Informações do Produto */}
        <div>
          <div className="mb-4">
            <span className="text-sm text-gray-400 bg-[#1a1a1a] px-3 py-1 rounded-full border border-[#c9a96e]/20">
              {produto.categoria}
            </span>
          </div>

          <h1 className="text-3xl font-bold text-white mb-6 font-display">
            {produto.nome}
          </h1>

          <div className="mb-8">
            {produto.preco_original && produto.preco_venda && produto.preco_venda > produto.preco_original && (
              <div className="text-lg text-gray-500 line-through mb-1">
                De: R$ {(produto.preco_venda * 1.3).toFixed(2)}
              </div>
            )}
            <div className="flex items-baseline gap-2">
              <span className="text-sm text-gray-400">Por:</span>
              <span className="text-4xl font-bold text-[#c9a96e]">
                R$ {produto.preco_venda?.toFixed(2)}
              </span>
            </div>
          </div>

          {/* Seleção de Tamanhos e Quantidades */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-4 text-white">Selecione seu Tamanho</h3>

            <div className="space-y-3">
              {getVariacoes().map((variacao) => (
                <div
                  key={variacao.id}
                  className="flex items-center justify-between p-4 border border-[#c9a96e]/20 rounded-lg hover:border-[#c9a96e] transition-colors bg-[#1a1a1a]"
                >
                  <div className="flex-1">
                    <div className="font-semibold text-white">
                      Tamanho {variacao.tamanho}
                    </div>
                    <div className="text-sm text-gray-400">
                      R$ {variacao.preco.toFixed(2)}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      Código: {variacao.id}
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => handleQuantityChange(variacao.id, variacao.tamanho, -1)}
                      className="w-8 h-8 rounded-full bg-[#0a0a0a] hover:bg-black flex items-center justify-center transition-colors border border-[#c9a96e]/30 text-white"
                      disabled={!selectedVariacoes[variacao.id]}
                    >
                      <Minus className="h-4 w-4" />
                    </button>

                    <span className="w-8 text-center font-semibold text-white">
                      {selectedVariacoes[variacao.id] || 0}
                    </span>

                    <button
                      onClick={() => handleQuantityChange(variacao.id, variacao.tamanho, 1)}
                      className="w-8 h-8 rounded-full bg-[#c9a96e] hover:bg-[#b8986e] text-white flex items-center justify-center transition-colors"
                    >
                      <Plus className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {produto.descricao && (
            <div className="mb-8">
              <h3 className="text-lg font-semibold mb-3 text-white">Descrição</h3>
              <p className="text-gray-400 leading-relaxed">
                {produto.descricao}
              </p>
            </div>
          )}

          {/* Botão de Adicionar ao Carrinho */}
          <div className="space-y-4">
            <Button
              size="lg"
              className="w-full bg-[#c9a96e] hover:bg-[#b8986e] text-lg py-6 disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={handleAddToCart}
              disabled={getTotalItems() === 0}
            >
              <ShoppingCart className="h-5 w-5 mr-3" />
              {getTotalItems() === 0
                ? 'Escolha seu tamanho para continuar'
                : `Adicionar à Seleção (${getTotalItems()} ${getTotalItems() === 1 ? 'peça' : 'peças'})`
              }
            </Button>

            <div className="text-center text-sm text-gray-500">
              Suas peças serão reservadas. Finalize via WhatsApp.
            </div>
          </div>

          {/* Informações Adicionais */}
          <div className="mt-8 p-6 bg-[#1a1a1a] rounded-lg border border-[#c9a96e]/20">
            <h3 className="font-semibold mb-3 text-white">Benefícios Exclusivos</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>• Consultoria exclusiva via WhatsApp</li>
              <li>• Entrega em todo o Brasil</li>
              <li>• Qualidade premium garantida</li>
              <li>• Embalagem sofisticada e discreta</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProdutoDetalhes

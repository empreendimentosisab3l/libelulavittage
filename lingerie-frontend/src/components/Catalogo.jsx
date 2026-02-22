import { useState, useEffect, useMemo, memo } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { ShoppingCart, Filter, X } from 'lucide-react'
import { Button } from './ui/button'
import AddToCartModal from './AddToCartModal'
import ProductSkeleton from './ProductSkeleton'

const PER_PAGE = 24

const Catalogo = ({ categorias, apiBaseUrl }) => {
  const [searchParams] = useSearchParams()
  const [produtos, setProdutos] = useState([])
  const [loading, setLoading] = useState(true)
  const [loadingMore, setLoadingMore] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [totalProdutos, setTotalProdutos] = useState(0)
  const [showFilters, setShowFilters] = useState(false)

  // Sincronizar filtros com URL params
  const filtros = useMemo(() => ({
    categoria: searchParams.get('categoria') || '',
    busca: searchParams.get('busca') || ''
  }), [searchParams])

  useEffect(() => {
    // Reset quando filtros mudam
    setProdutos([])
    setCurrentPage(1)
    carregarProdutos(1, true)
  }, [filtros.categoria, filtros.busca])

  const carregarProdutos = async (page = 1, reset = false) => {
    try {
      if (reset) {
        setLoading(true)
      } else {
        setLoadingMore(true)
      }

      const params = new URLSearchParams()
      params.append('page', page.toString())
      params.append('per_page', PER_PAGE.toString())
      if (filtros.categoria) params.append('categoria', filtros.categoria)
      if (filtros.busca) params.append('busca', filtros.busca)

      const response = await fetch(`${apiBaseUrl}/produtos?${params}`)
      const data = await response.json()

      const novosProdutos = data.produtos || []

      if (reset) {
        setProdutos(novosProdutos)
      } else {
        setProdutos(prev => [...prev, ...novosProdutos])
      }

      setTotalPages(data.pages || 1)
      setTotalProdutos(data.total || 0)
      setCurrentPage(page)

    } catch (error) {
      console.error('Erro ao carregar produtos:', error)
    } finally {
      setLoading(false)
      setLoadingMore(false)
    }
  }

  const carregarMais = () => {
    if (currentPage < totalPages) {
      carregarProdutos(currentPage + 1, false)
    }
  }

  const aplicarFiltro = (tipo, valor) => {
    const params = new URLSearchParams(searchParams)

    if (valor) {
      params.set(tipo, valor)
    } else {
      params.delete(tipo)
    }

    window.location.href = `/catalogo?${params.toString()}`
  }

  const limparFiltros = () => {
    window.location.href = '/catalogo'
  }

  return (
    <div className="container mx-auto px-4 py-8 bg-[#0a0a0a] min-h-screen">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6 gap-4">
        <h1 className="text-2xl md:text-3xl font-bold text-white font-display">
          Nossa Coleção
        </h1>

        <Button
          variant="outline"
          onClick={() => setShowFilters(!showFilters)}
          className="lg:hidden w-full sm:w-auto"
        >
          <Filter className="h-4 w-4 mr-2" />
          {showFilters ? 'Ocultar Filtros' : 'Mostrar Filtros'}
        </Button>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar - Filtros */}
        <aside className={`w-full lg:w-64 flex-shrink-0 ${showFilters ? 'block' : 'hidden lg:block'}`}>
          <div className="bg-[#1a1a1a] p-4 md:p-6 rounded-lg shadow-md sticky top-20 border border-[#c9a96e]/20">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">Filtros</h3>
              <button
                onClick={() => setShowFilters(false)}
                className="lg:hidden text-gray-400 hover:text-white"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Filtro por categoria */}
            <div className="mb-6">
              <h4 className="font-medium mb-3 text-sm uppercase text-[#c9a96e]">Categoria</h4>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                <label className="flex items-center cursor-pointer hover:bg-[#0a0a0a] p-2 rounded transition-colors text-white">
                  <input
                    type="radio"
                    name="categoria"
                    value=""
                    checked={filtros.categoria === ''}
                    onChange={(e) => aplicarFiltro('categoria', e.target.value)}
                    className="mr-3 text-[#c9a96e] focus:ring-[#c9a96e] bg-[#0a0a0a] border-[#c9a96e]/30"
                  />
                  <span className="text-sm">Todas as Categorias</span>
                </label>
                {categorias.map((categoria) => (
                  <label key={categoria} className="flex items-center cursor-pointer hover:bg-[#0a0a0a] p-2 rounded transition-colors text-white">
                    <input
                      type="radio"
                      name="categoria"
                      value={categoria}
                      checked={filtros.categoria === categoria}
                      onChange={(e) => aplicarFiltro('categoria', e.target.value)}
                      className="mr-3 text-[#c9a96e] focus:ring-[#c9a96e] bg-[#0a0a0a] border-[#c9a96e]/30"
                    />
                    <span className="text-sm">{categoria}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Busca */}
            <div className="mb-6">
              <h4 className="font-medium mb-3 text-sm uppercase text-[#c9a96e]">Encontrar</h4>
              <input
                type="text"
                placeholder="Buscar peça..."
                value={filtros.busca}
                onChange={(e) => aplicarFiltro('busca', e.target.value)}
                className="w-full px-3 py-2 text-sm border border-[#c9a96e]/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#c9a96e] bg-[#0a0a0a] text-white placeholder-gray-500"
              />
            </div>

            {(filtros.categoria || filtros.busca) && (
              <Button
                variant="outline"
                onClick={limparFiltros}
                className="w-full text-sm"
              >
                Limpar Filtros
              </Button>
            )}
          </div>
        </aside>

        {/* Grid de produtos */}
        <main className="flex-1 min-w-0">
          {loading ? (
            <>
              <div className="mb-4 text-sm text-gray-400 px-1">
                Preparando sua experiência...
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-4 md:gap-6">
                {[...Array(PER_PAGE)].map((_, i) => (
                  <ProductSkeleton key={i} />
                ))}
              </div>
            </>
          ) : produtos.length > 0 ? (
            <>
              <div className="mb-4 text-sm text-gray-400 px-1">
                {produtos.length} de {totalProdutos} produto{totalProdutos !== 1 ? 's' : ''}
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-4 md:gap-6">
                {produtos.map((produto) => (
                  <ProductCard key={produto.id} produto={produto} />
                ))}
              </div>

              {currentPage < totalPages && (
                <div className="text-center mt-8">
                  <Button
                    onClick={carregarMais}
                    disabled={loadingMore}
                    className="bg-[#c9a96e] hover:bg-[#b8986e] px-8"
                  >
                    {loadingMore ? 'Carregando...' : 'Descobrir Mais Peças'}
                  </Button>
                  <p className="text-sm text-gray-500 mt-2">
                    Mostrando {produtos.length} de {totalProdutos} produtos
                  </p>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-12 px-4">
              <p className="text-gray-400 text-base md:text-lg mb-4">
                Nenhuma peça encontrada. Experimente ajustar os filtros.
              </p>
              <Button onClick={limparFiltros}>
                Limpar Filtros
              </Button>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

const ProductCard = memo(({ produto }) => {
  const [showModal, setShowModal] = useState(false)
  const imagemPrincipal = useMemo(() =>
    produto.imagens && produto.imagens.length > 0
      ? produto.imagens[0]
      : '/placeholder-product.jpg',
    [produto.imagens]
  )

  return (
    <>
      <div className="bg-[#1a1a1a] rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-all border border-transparent hover:border-[#c9a96e]">
        <Link to={`/produto/${produto.id}`}>
          <div className="aspect-square overflow-hidden bg-[#0a0a0a]">
            <img
              src={imagemPrincipal}
              alt={produto.nome}
              className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
              loading="lazy"
              onError={(e) => {
                e.target.src = '/placeholder-product.jpg'
              }}
            />
          </div>
        </Link>

        <div className="p-4">
          <Link to={`/produto/${produto.id}`}>
            <h3 className="font-semibold text-white mb-2 hover:text-[#c9a96e] transition-colors line-clamp-2 break-words min-h-[3rem]">
              {produto.nome}
            </h3>
          </Link>

          <div className="mb-3">
            <span className="text-xs text-gray-400 bg-[#0a0a0a] px-2 py-1 rounded inline-block break-words max-w-full border border-[#c9a96e]/20">
              {produto.categoria}
            </span>
          </div>

          <div className="mb-3">
            <span className="text-xl md:text-2xl font-bold text-[#c9a96e]">
              R$ {produto.preco_venda?.toFixed(2)}
            </span>
          </div>

          <Button
            className="w-full bg-[#c9a96e] hover:bg-[#b8986e] text-sm"
            onClick={() => setShowModal(true)}
          >
            <ShoppingCart className="h-4 w-4 mr-2" />
            <span className="truncate">Adicionar ao Carrinho</span>
          </Button>
        </div>
      </div>

      {showModal && (
        <AddToCartModal
          produto={produto}
          isOpen={showModal}
          onClose={() => setShowModal(false)}
        />
      )}
    </>
  )
})

ProductCard.displayName = 'ProductCard'

export default Catalogo


import { useState, useEffect, useMemo, memo } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { ShoppingCart, Filter, X } from 'lucide-react'
import { Button } from './ui/button'
import AddToCartModal from './AddToCartModal'

const Catalogo = ({ categorias, apiBaseUrl }) => {
  const [searchParams] = useSearchParams()
  const [produtos, setProdutos] = useState([])
  const [loading, setLoading] = useState(true)
  const [showFilters, setShowFilters] = useState(false)

  // Sincronizar filtros com URL params
  const filtros = useMemo(() => ({
    categoria: searchParams.get('categoria') || '',
    busca: searchParams.get('busca') || ''
  }), [searchParams])

  useEffect(() => {
    carregarProdutos()
  }, [filtros.categoria, filtros.busca])

  const carregarProdutos = async () => {
    try {
      setLoading(true)

      const params = new URLSearchParams()
      params.append('all', 'true')  // Carregar todos os produtos
      if (filtros.categoria) params.append('categoria', filtros.categoria)
      if (filtros.busca) params.append('busca', filtros.busca)

      const response = await fetch(`${apiBaseUrl}/produtos?${params}`)
      const data = await response.json()
      setProdutos(data.produtos || [])

    } catch (error) {
      console.error('Erro ao carregar produtos:', error)
    } finally {
      setLoading(false)
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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-pink-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando produtos...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6 gap-4">
        <h1 className="text-2xl md:text-3xl font-bold text-gray-800">
          Catálogo de Produtos
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
          <div className="bg-white p-4 md:p-6 rounded-lg shadow-md sticky top-20">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Filtros</h3>
              <button
                onClick={() => setShowFilters(false)}
                className="lg:hidden text-gray-500 hover:text-gray-700"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Filtro por categoria */}
            <div className="mb-6">
              <h4 className="font-medium mb-3 text-sm uppercase text-gray-700">Categoria</h4>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                <label className="flex items-center cursor-pointer hover:bg-gray-50 p-2 rounded transition-colors">
                  <input
                    type="radio"
                    name="categoria"
                    value=""
                    checked={filtros.categoria === ''}
                    onChange={(e) => aplicarFiltro('categoria', e.target.value)}
                    className="mr-3 text-pink-600 focus:ring-pink-500"
                  />
                  <span className="text-sm">Todas as Categorias</span>
                </label>
                {categorias.map((categoria) => (
                  <label key={categoria} className="flex items-center cursor-pointer hover:bg-gray-50 p-2 rounded transition-colors">
                    <input
                      type="radio"
                      name="categoria"
                      value={categoria}
                      checked={filtros.categoria === categoria}
                      onChange={(e) => aplicarFiltro('categoria', e.target.value)}
                      className="mr-3 text-pink-600 focus:ring-pink-500"
                    />
                    <span className="text-sm">{categoria}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Busca */}
            <div className="mb-6">
              <h4 className="font-medium mb-3 text-sm uppercase text-gray-700">Buscar</h4>
              <input
                type="text"
                placeholder="Nome do produto..."
                value={filtros.busca}
                onChange={(e) => aplicarFiltro('busca', e.target.value)}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
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
          {produtos.length > 0 ? (
            <>
              <div className="mb-4 text-sm text-gray-600 px-1">
                {produtos.length} produto{produtos.length !== 1 ? 's' : ''} encontrado{produtos.length !== 1 ? 's' : ''}
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-4 md:gap-6">
                {produtos.map((produto) => (
                  <ProductCard key={produto.id} produto={produto} />
                ))}
              </div>
            </>
          ) : (
            <div className="text-center py-12 px-4">
              <p className="text-gray-600 text-base md:text-lg mb-4">
                Nenhum produto encontrado com os filtros aplicados.
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
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
        <Link to={`/produto/${produto.id}`}>
          <div className="aspect-square overflow-hidden bg-gray-100">
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
            <h3 className="font-semibold text-gray-800 mb-2 hover:text-pink-600 transition-colors line-clamp-2 break-words min-h-[3rem]">
              {produto.nome}
            </h3>
          </Link>

          <div className="mb-3">
            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded inline-block break-words max-w-full">
              {produto.categoria}
            </span>
          </div>

          <div className="mb-3">
            <span className="text-xl md:text-2xl font-bold text-pink-600">
              R$ {produto.preco_venda?.toFixed(2)}
            </span>
          </div>

          <Button
            className="w-full bg-pink-600 hover:bg-pink-700 text-sm"
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


import { useState, memo, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { ShoppingCart, MessageCircle, User } from 'lucide-react'
import { Button } from './ui/button'
import AddToCartModal from './AddToCartModal'
import ProductSkeleton from './ProductSkeleton'
import { useCart } from '../context/CartContext'

const Home = ({ produtos, onOpenCart, loading }) => {
  const { getCartCount } = useCart()

  return (
    <div>
      {/* Hero Section */}
      <section
        className="relative bg-cover bg-center bg-no-repeat text-white min-h-[70vh] md:min-h-[80vh] flex items-center justify-center"
        style={{
          backgroundImage: 'url(/hero-bg.jpg)',
        }}
      >
        {/* Overlay suave com gradiente */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-black/40 to-black/60"></div>

        {/* Header elements - Top right */}
        <div className="absolute top-6 right-6 flex items-center gap-4 z-20">
          {/* Cart Button */}
          <button
            onClick={onOpenCart}
            className="relative p-2 hover:bg-white/10 rounded-full transition-colors"
          >
            <ShoppingCart className="h-6 w-6 text-white drop-shadow-lg" />
            {getCartCount() > 0 && (
              <span className="absolute -top-1 -right-1 bg-[#c9a96e] text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center shadow-lg">
                {getCartCount()}
              </span>
            )}
          </button>

          {/* Login Link */}
          <Link
            to="/admin"
            className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-full transition-all duration-300 border border-white/20"
          >
            <User className="h-5 w-5" />
            <span className="text-sm font-medium">Minha Conta</span>
          </Link>
        </div>

        <div className="container mx-auto px-4 text-center relative z-10">
          {/* Logo centralizado */}
          <div className="mb-12 md:mb-16">
            <img
              src="/logo.png"
              alt="Libélula Vittage"
              className="h-20 md:h-32 mx-auto drop-shadow-2xl"
              onError={(e) => {
                e.target.style.display = 'none'
                e.target.nextElementSibling.style.display = 'block'
              }}
            />
            <h1 className="text-5xl md:text-7xl font-light tracking-wide mt-4 hidden font-display">
              Libélula Vittage
            </h1>
          </div>

          {/* Menu de categorias */}
          <nav className="mb-8 md:mb-12">
            <ul className="flex flex-wrap justify-center gap-4 md:gap-8 text-sm md:text-base uppercase tracking-wider">
              <li>
                <Link to="/catalogo?categoria=Sutiã" className="hover:text-[#c9a96e] transition-colors duration-300 drop-shadow-md">
                  Sutiã
                </Link>
              </li>
              <li>
                <Link to="/catalogo?categoria=Calcinhas" className="hover:text-[#c9a96e] transition-colors duration-300 drop-shadow-md">
                  Calcinhas
                </Link>
              </li>
              <li>
                <Link to="/catalogo?categoria=Conjuntos" className="hover:text-[#c9a96e] transition-colors duration-300 drop-shadow-md">
                  Conjuntos
                </Link>
              </li>
              <li>
                <Link to="/catalogo" className="hover:text-[#c9a96e] transition-colors duration-300 drop-shadow-md">
                  Lançamentos
                </Link>
              </li>
            </ul>
          </nav>

          {/* CTA */}
          <div className="mt-12">
            <Link to="/catalogo">
              <Button
                size="lg"
                className="bg-transparent hover:bg-[#c9a96e] text-white hover:text-black text-base md:text-lg px-12 py-4 shadow-2xl backdrop-blur-sm border-2 border-[#c9a96e] transition-all duration-300 hover:scale-105 tracking-wider uppercase"
              >
                Explorar Coleção
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 bg-[#0a0a0a]">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-white font-display">
            Seleção Exclusiva
          </h2>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {[...Array(8)].map((_, i) => (
                <ProductSkeleton key={i} />
              ))}
            </div>
          ) : produtos.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {produtos.map((produto) => (
                <ProductCard key={produto.id} produto={produto} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-400 text-lg">
                Nossa coleção está sendo atualizada. Volte em breve para descobrir peças exclusivas.
              </p>
            </div>
          )}

          <div className="text-center mt-12">
            <Link to="/catalogo">
              <Button size="lg" className="bg-transparent border-2 border-[#c9a96e] text-[#c9a96e] hover:bg-[#c9a96e] hover:text-black tracking-wider uppercase">
                Descobrir a Coleção
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="py-16 bg-[#1a1a1a]">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-8 text-white font-display">
              A Arte da Elegância
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="p-6">
                <div className="w-16 h-16 bg-[#c9a96e]/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <MessageCircle className="h-8 w-8 text-[#c9a96e]" />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-white">Consultoria Exclusiva</h3>
                <p className="text-gray-400">
                  Assessoria personalizada para encontrar a peça perfeita para você
                </p>
              </div>
              <div className="p-6">
                <div className="w-16 h-16 bg-[#c9a96e]/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl text-[#c9a96e]">&#10022;</span>
                </div>
                <h3 className="text-xl font-semibold mb-3 text-white">Qualidade Premium</h3>
                <p className="text-gray-400">
                  Tecidos nobres e acabamento impecável em cada detalhe
                </p>
              </div>
              <div className="p-6">
                <div className="w-16 h-16 bg-[#c9a96e]/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl text-[#c9a96e]">&#9992;</span>
                </div>
                <h3 className="text-xl font-semibold mb-3 text-white">Entrega Discreta</h3>
                <p className="text-gray-400">
                  Embalagem sofisticada e envio discreto para todo o Brasil
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
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
      <div className="bg-[#1a1a1a] rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-all hover:border-[#c9a96e] border border-transparent">
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

export default Home


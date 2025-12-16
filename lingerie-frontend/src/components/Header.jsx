import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Search, ShoppingBag, Menu, X, Settings, ShoppingCart } from 'lucide-react'
import { Button } from './ui/button'
import { useCart } from '../context/CartContext'
import Cart from './Cart'

const Header = ({ categorias }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [isCartOpen, setIsCartOpen] = useState(false)
  const { getCartCount } = useCart()

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchTerm.trim()) {
      window.location.href = `/catalogo?busca=${encodeURIComponent(searchTerm)}`
    }
  }

  return (
    <header className="bg-white/95 backdrop-blur-sm shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4">
        {/* Top bar */}
        <div className="flex items-center justify-between py-3 md:py-4">
          {/* Logo */}
          <Link to="/" className="flex items-center">
            <img
              src="/logo02.png"
              alt="Libélula Village"
              className="h-10 md:h-14 transition-all duration-300"
              onError={(e) => {
                e.target.style.display = 'none'
                e.target.nextElementSibling.style.display = 'block'
              }}
            />
            <span className="text-xl md:text-2xl font-light text-gray-800 hidden tracking-wide" style={{ fontFamily: 'cursive' }}>
              Libélula Village
            </span>
          </Link>

          {/* Search bar - Desktop */}
          <form onSubmit={handleSearch} className="hidden md:flex items-center flex-1 max-w-md mx-8">
            <div className="relative w-full">
              <input
                type="text"
                placeholder="Buscar produtos..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
              />
              <Button
                type="submit"
                className="absolute right-0 top-0 h-full px-4 bg-pink-600 hover:bg-pink-700 rounded-l-none"
              >
                <Search className="h-4 w-4" />
              </Button>
            </div>
          </form>

          {/* Actions */}
          <div className="hidden md:flex items-center gap-2">
            {/* Cart Button */}
            <button
              onClick={() => setIsCartOpen(true)}
              className="relative p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <ShoppingCart className="h-6 w-6 text-gray-700" />
              {getCartCount() > 0 && (
                <span className="absolute -top-1 -right-1 bg-pink-600 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                  {getCartCount()}
                </span>
              )}
            </button>

            {/* Admin Link */}
            <Link to="/admin">
              <Button variant="ghost" size="sm">
                <Settings className="h-5 w-5" />
              </Button>
            </Link>
          </div>

          {/* Mobile buttons */}
          <div className="flex md:hidden items-center gap-2">
            {/* Cart Button Mobile */}
            <button
              onClick={() => setIsCartOpen(true)}
              className="relative p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <ShoppingCart className="h-6 w-6 text-gray-700" />
              {getCartCount() > 0 && (
                <span className="absolute -top-1 -right-1 bg-pink-600 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                  {getCartCount()}
                </span>
              )}
            </button>

            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Navigation - Desktop */}
        <nav className="hidden md:block border-t border-gray-200">
          <div className="flex items-center justify-center py-4 gap-6 lg:gap-8 flex-wrap">
            <Link
              to="/"
              className="text-gray-700 hover:text-pink-600 font-medium transition-colors text-sm"
            >
              Início
            </Link>
            <Link
              to="/catalogo"
              className="text-gray-700 hover:text-pink-600 font-medium transition-colors text-sm"
            >
              Catálogo
            </Link>
            <Link
              to="/catalogo?categoria=Lingerie"
              className="text-gray-700 hover:text-pink-600 font-medium transition-colors text-sm"
            >
              Lingerie
            </Link>
            <Link
              to="/catalogo?categoria=Conjuntos"
              className="text-gray-700 hover:text-pink-600 font-medium transition-colors text-sm"
            >
              Conjuntos
            </Link>
            <Link
              to="/catalogo?categoria=Calcinhas"
              className="text-gray-700 hover:text-pink-600 font-medium transition-colors text-sm"
            >
              Calcinhas
            </Link>
            <Link
              to="/catalogo?categoria=Cropped"
              className="text-gray-700 hover:text-pink-600 font-medium transition-colors text-sm"
            >
              Cropped
            </Link>
            <Link
              to="/catalogo?categoria=Plus Size"
              className="text-gray-700 hover:text-pink-600 font-medium transition-colors text-sm"
            >
              Plus Size
            </Link>
            <Link
              to="/catalogo?categoria=Body"
              className="text-gray-700 hover:text-pink-600 font-medium transition-colors text-sm"
            >
              Body
            </Link>
          </div>
        </nav>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-200 py-4">
            {/* Mobile search */}
            <form onSubmit={handleSearch} className="mb-4">
              <div className="flex">
                <input
                  type="text"
                  placeholder="Buscar produtos..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
                />
                <Button
                  type="submit"
                  className="px-4 bg-pink-600 hover:bg-pink-700 rounded-l-none"
                >
                  <Search className="h-4 w-4" />
                </Button>
              </div>
            </form>

            {/* Mobile navigation */}
            <nav>
              <ul className="space-y-2">
                <li>
                  <Link
                    to="/"
                    className="block py-2 text-gray-700 hover:text-pink-600 font-medium"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Início
                  </Link>
                </li>
                <li>
                  <Link
                    to="/catalogo"
                    className="block py-2 text-gray-700 hover:text-pink-600 font-medium"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Todos os Produtos
                  </Link>
                </li>
                {categorias.map((categoria) => (
                  <li key={categoria}>
                    <Link
                      to={`/catalogo?categoria=${encodeURIComponent(categoria)}`}
                      className="block py-2 text-gray-700 hover:text-pink-600 font-medium"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      {categoria}
                    </Link>
                  </li>
                ))}
                <li className="pt-2 border-t border-gray-200">
                  <Link
                    to="/admin"
                    className="block py-2 text-gray-700 hover:text-pink-600 font-medium flex items-center"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <Settings className="h-4 w-4 mr-2" />
                    Admin
                  </Link>
                </li>
              </ul>
            </nav>
          </div>
        )}
      </div>

      {/* Cart Modal */}
      <Cart isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
    </header>
  )
}

export default Header


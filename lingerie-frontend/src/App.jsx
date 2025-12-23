import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { CartProvider } from './context/CartContext'
import Header from './components/Header'
import Home from './components/Home'
import Catalogo from './components/Catalogo'
import ProdutoDetalhes from './components/ProdutoDetalhes'
import AdminPanel from './components/AdminPanel'
import Footer from './components/Footer'
import Cart from './components/Cart'
import ProductSkeleton from './components/ProductSkeleton'
import './App.css'

function App() {
  const [produtos, setProdutos] = useState([])
  const [categorias, setCategorias] = useState([])
  const [loading, setLoading] = useState(true)
  const [isCartOpen, setIsCartOpen] = useState(false)

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api'

  useEffect(() => {
    carregarDados()
  }, [])

  const carregarDados = async () => {
    try {
      setLoading(true)
      
      // Carregar produtos
      const produtosResponse = await fetch(`${API_BASE_URL}/produtos`)
      const produtosData = await produtosResponse.json()
      setProdutos(produtosData.produtos || [])
      
      // Carregar categorias
      const categoriasResponse = await fetch(`${API_BASE_URL}/categorias`)
      const categoriasData = await categoriasResponse.json()
      setCategorias(categoriasData.categorias || [])
      
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        {/* Hero Section Skeleton */}
        <div className="bg-gradient-to-b from-gray-300 to-gray-200 h-[70vh] md:h-[80vh] flex items-center justify-center animate-pulse">
          <div className="text-center">
            <div className="h-20 md:h-32 w-32 md:w-48 bg-white/30 rounded-lg mx-auto mb-8"></div>
            <div className="h-8 w-64 bg-white/30 rounded mx-auto"></div>
          </div>
        </div>

        {/* Products Skeleton */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <div className="h-10 w-64 bg-gray-200 rounded mx-auto mb-12 animate-pulse"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {[...Array(8)].map((_, i) => (
                <ProductSkeleton key={i} />
              ))}
            </div>
          </div>
        </section>
      </div>
    )
  }

  return (
    <CartProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route
              path="/"
              element={<Home produtos={produtos.slice(0, 8)} categorias={categorias} onOpenCart={() => setIsCartOpen(true)} />}
            />
            <Route
              path="/catalogo"
              element={
                <>
                  <Header categorias={categorias} onOpenCart={() => setIsCartOpen(true)} />
                  <Catalogo
                    categorias={categorias}
                    apiBaseUrl={API_BASE_URL}
                  />
                  <Footer />
                </>
              }
            />
            <Route
              path="/produto/:id"
              element={
                <>
                  <Header categorias={categorias} onOpenCart={() => setIsCartOpen(true)} />
                  <ProdutoDetalhes apiBaseUrl={API_BASE_URL} />
                  <Footer />
                </>
              }
            />
            <Route
              path="/admin"
              element={
                <>
                  <Header categorias={categorias} onOpenCart={() => setIsCartOpen(true)} />
                  <AdminPanel apiBaseUrl={API_BASE_URL} />
                  <Footer />
                </>
              }
            />
          </Routes>

          {/* Global Cart - renders at app level outside all stacking contexts */}
          <Cart isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
        </div>
      </Router>
    </CartProvider>
  )
}

export default App


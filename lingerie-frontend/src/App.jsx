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
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-pink-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando produtos...</p>
        </div>
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


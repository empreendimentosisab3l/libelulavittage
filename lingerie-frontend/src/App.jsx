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
import { startKeepAlive, stopKeepAlive } from './utils/keepAlive'
import './App.css'

function App() {
  const [produtos, setProdutos] = useState([])
  const [categorias, setCategorias] = useState([])
  const [loading, setLoading] = useState(true)
  const [isCartOpen, setIsCartOpen] = useState(false)

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api'

  useEffect(() => {
    carregarDados()

    // Start keep-alive service to prevent backend from sleeping
    startKeepAlive()

    // Cleanup on unmount
    return () => {
      stopKeepAlive()
    }
  }, [])

  const carregarDados = async () => {
    try {
      setLoading(true)

      // Carregar produtos e categorias em paralelo
      const [produtosResponse, categoriasResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/produtos?per_page=8`),
        fetch(`${API_BASE_URL}/categorias`)
      ])

      const [produtosData, categoriasData] = await Promise.all([
        produtosResponse.json(),
        categoriasResponse.json()
      ])

      setProdutos(produtosData.produtos || [])
      setCategorias(categoriasData.categorias || [])

    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <CartProvider>
      <Router>
        <div className="min-h-screen bg-[#0a0a0a]">
          <Routes>
            <Route
              path="/"
              element={<Home produtos={produtos} categorias={categorias} loading={loading} onOpenCart={() => setIsCartOpen(true)} />}
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


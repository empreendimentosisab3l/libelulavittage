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
import { listarProdutos, listarCategorias } from './lib/produtos'
import './App.css'

function App() {
  const [produtos, setProdutos] = useState([])
  const [categorias, setCategorias] = useState([])
  const [loading, setLoading] = useState(true)
  const [isCartOpen, setIsCartOpen] = useState(false)

  useEffect(() => {
    carregarDados()
  }, [])

  const carregarDados = async () => {
    try {
      setLoading(true)
      const [produtosResult, categoriasResult] = await Promise.all([
        listarProdutos({ page: 1, perPage: 8 }),
        listarCategorias()
      ])
      setProdutos(produtosResult.produtos)
      setCategorias(categoriasResult)
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
                  <Catalogo categorias={categorias} />
                  <Footer />
                </>
              }
            />
            <Route
              path="/produto/:id"
              element={
                <>
                  <Header categorias={categorias} onOpenCart={() => setIsCartOpen(true)} />
                  <ProdutoDetalhes />
                  <Footer />
                </>
              }
            />
            <Route
              path="/admin"
              element={
                <>
                  <Header categorias={categorias} onOpenCart={() => setIsCartOpen(true)} />
                  <AdminPanel />
                  <Footer />
                </>
              }
            />
          </Routes>

          <Cart isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
        </div>
      </Router>
    </CartProvider>
  )
}

export default App

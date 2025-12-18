import { createContext, useContext, useState, useEffect } from 'react'

const CartContext = createContext()

export const useCart = () => {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart deve ser usado dentro de um CartProvider')
  }
  return context
}

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState(() => {
    try {
      const savedCart = localStorage.getItem('lingerie-cart')
      return savedCart ? JSON.parse(savedCart) : []
    } catch (error) {
      console.error('Erro ao carregar carrinho do localStorage:', error)
      return []
    }
  })

  useEffect(() => {
    try {
      localStorage.setItem('lingerie-cart', JSON.stringify(cartItems))
    } catch (error) {
      console.error('Erro ao salvar carrinho no localStorage:', error)
    }
  }, [cartItems])

  const addToCart = (produto, variacaoId, tamanho) => {
    setCartItems(prevItems => {
      const existingItemIndex = prevItems.findIndex(
        item => item.produto.id === produto.id && item.variacaoId === variacaoId
      )

      if (existingItemIndex > -1) {
        const newItems = [...prevItems]
        newItems[existingItemIndex].quantidade += 1
        return newItems
      }

      // Normalize product data - ensure imagens is always a string
      const normalizedProduto = {
        ...produto,
        imagens: Array.isArray(produto.imagens)
          ? produto.imagens.join(',')
          : (produto.imagens || '')
      }

      return [...prevItems, {
        produto: normalizedProduto,
        variacaoId,
        tamanho,
        quantidade: 1
      }]
    })
  }

  const removeFromCart = (produtoId, variacaoId) => {
    setCartItems(prevItems =>
      prevItems.filter(item =>
        !(item.produto.id === produtoId && item.variacaoId === variacaoId)
      )
    )
  }

  const updateQuantity = (produtoId, variacaoId, quantidade) => {
    if (quantidade <= 0) {
      removeFromCart(produtoId, variacaoId)
      return
    }

    setCartItems(prevItems =>
      prevItems.map(item =>
        item.produto.id === produtoId && item.variacaoId === variacaoId
          ? { ...item, quantidade }
          : item
      )
    )
  }

  const clearCart = () => {
    setCartItems([])
  }

  const getCartTotal = () => {
    return cartItems.reduce((total, item) => {
      return total + (item.produto.preco_venda * item.quantidade)
    }, 0)
  }

  const getCartCount = () => {
    return cartItems.reduce((count, item) => count + item.quantidade, 0)
  }

  const value = {
    cartItems,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    getCartTotal,
    getCartCount
  }

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  )
}

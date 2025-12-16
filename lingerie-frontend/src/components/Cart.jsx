import { useState } from 'react'
import { X, Plus, Minus, ShoppingCart, Trash2, MessageCircle } from 'lucide-react'
import { useCart } from '../context/CartContext'

const Cart = ({ isOpen, onClose }) => {
  const { cartItems, updateQuantity, removeFromCart, clearCart, getCartTotal } = useCart()
  const [whatsappNumber, setWhatsappNumber] = useState('43996048712')

  if (!isOpen) return null

  const handleSendWhatsApp = () => {
    if (cartItems.length === 0) return

    const baseUrl = window.location.origin
    let message = '🛍️ *Olá! Gostaria de fazer um pedido:*\n\n'

    cartItems.forEach((item, index) => {
      const produtoUrl = `${baseUrl}/produto/${item.produto.id}`
      message += `${index + 1}. *${item.produto.nome}*\n`
      message += `   Tamanho: ${item.tamanho}\n`
      message += `   Quantidade: ${item.quantidade}\n`
      message += `   Preço unitário: R$ ${item.produto.preco_venda.toFixed(2)}\n`
      message += `   Subtotal: R$ ${(item.produto.preco_venda * item.quantidade).toFixed(2)}\n`
      message += `   Código: ${item.variacaoId}\n`
      message += `   🔗 Link: ${produtoUrl}\n\n`
    })

    message += `💰 *Total do Pedido: R$ ${getCartTotal().toFixed(2)}*\n\n`
    message += '📦 Aguardo retorno para finalizar o pedido!'

    const encodedMessage = encodeURIComponent(message)
    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodedMessage}`

    window.open(whatsappUrl, '_blank')
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-end sm:items-center justify-center">
      <div className="bg-white w-full sm:max-w-2xl sm:rounded-lg max-h-[95vh] sm:max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <ShoppingCart className="h-6 w-6 text-pink-600" />
            <h2 className="text-xl font-bold text-gray-800">
              Meu Carrinho ({cartItems.length})
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {cartItems.length === 0 ? (
            <div className="text-center py-12">
              <ShoppingCart className="h-24 w-24 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500 text-lg">Seu carrinho está vazio</p>
              <p className="text-gray-400 text-sm mt-2">
                Adicione produtos ao carrinho para continuar
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {cartItems.map((item) => (
                <CartItem
                  key={`${item.produto.id}-${item.variacaoId}`}
                  item={item}
                  onUpdateQuantity={updateQuantity}
                  onRemove={removeFromCart}
                />
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        {cartItems.length > 0 && (
          <div className="sticky bottom-0 bg-white border-t p-4 space-y-3">
            <div className="flex justify-between items-center text-lg font-bold">
              <span>Total:</span>
              <span className="text-pink-600">R$ {getCartTotal().toFixed(2)}</span>
            </div>

            <button
              onClick={handleSendWhatsApp}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
            >
              <MessageCircle className="h-5 w-5" />
              Finalizar Pedido via WhatsApp
            </button>

            <button
              onClick={clearCart}
              className="w-full bg-gray-200 hover:bg-gray-300 text-gray-700 py-2 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
            >
              <Trash2 className="h-4 w-4" />
              Limpar Carrinho
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

const CartItem = ({ item, onUpdateQuantity, onRemove }) => {
  const subtotal = item.produto.preco_venda * item.quantidade

  return (
    <div className="flex gap-4 bg-gray-50 p-4 rounded-lg">
      <img
        src={item.produto.imagens?.[0] || '/placeholder-product.jpg'}
        alt={item.produto.nome}
        className="w-24 h-24 object-cover rounded-lg"
        onError={(e) => {
          e.target.src = '/placeholder-product.jpg'
        }}
      />

      <div className="flex-1">
        <h3 className="font-semibold text-gray-800 mb-1">
          {item.produto.nome}
        </h3>
        <div className="text-sm text-gray-600 mb-2">
          <div>Tamanho: {item.tamanho}</div>
          <div className="text-xs text-gray-400">Cód: {item.variacaoId}</div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <button
              onClick={() => onUpdateQuantity(item.produto.id, item.variacaoId, item.quantidade - 1)}
              className="w-7 h-7 rounded-full bg-white hover:bg-gray-200 flex items-center justify-center transition-colors border"
            >
              <Minus className="h-3 w-3" />
            </button>

            <span className="w-8 text-center font-semibold">
              {item.quantidade}
            </span>

            <button
              onClick={() => onUpdateQuantity(item.produto.id, item.variacaoId, item.quantidade + 1)}
              className="w-7 h-7 rounded-full bg-pink-600 hover:bg-pink-700 text-white flex items-center justify-center transition-colors"
            >
              <Plus className="h-3 w-3" />
            </button>
          </div>

          <button
            onClick={() => onRemove(item.produto.id, item.variacaoId)}
            className="text-red-500 hover:text-red-700 p-2"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>

        <div className="mt-2 text-right">
          <div className="text-sm text-gray-600">
            R$ {item.produto.preco_venda.toFixed(2)} cada
          </div>
          <div className="text-lg font-bold text-pink-600">
            R$ {subtotal.toFixed(2)}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Cart

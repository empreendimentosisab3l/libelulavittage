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
    let message = '*Olá! Gostaria de finalizar minha seleção:*\n\n'

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
    message += 'Aguardo seu contato para finalizar minha compra.'

    const encodedMessage = encodeURIComponent(message)
    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodedMessage}`

    window.open(whatsappUrl, '_blank')
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-end sm:items-center justify-center" style={{ zIndex: 99999 }}>
      <div className="bg-[#1a1a1a] w-full sm:max-w-2xl sm:rounded-lg max-h-[95vh] sm:max-h-[90vh] flex flex-col shadow-2xl border border-[#c9a96e]/20">
        {/* Header */}
        <div className="sticky top-0 bg-[#1a1a1a] border-b border-[#c9a96e]/20 p-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <ShoppingCart className="h-6 w-6 text-[#c9a96e]" />
            <h2 className="text-xl font-bold text-white font-display">
              Sua Seleção ({cartItems.length})
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-[#0a0a0a] rounded-full transition-colors text-white"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {cartItems.length === 0 ? (
            <div className="text-center py-12">
              <ShoppingCart className="h-24 w-24 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400 text-lg">Sua seleção está aguardando</p>
              <p className="text-gray-500 text-sm mt-2">
                Explore nossa coleção e escolha suas peças favoritas
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
          <div className="sticky bottom-0 bg-[#1a1a1a] border-t border-[#c9a96e]/20 p-4 space-y-3">
            <div className="flex justify-between items-center text-lg font-bold text-white">
              <span>Total:</span>
              <span className="text-[#c9a96e]">R$ {getCartTotal().toFixed(2)}</span>
            </div>

            <button
              onClick={handleSendWhatsApp}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
            >
              <MessageCircle className="h-5 w-5" />
              Concluir Compra via WhatsApp
            </button>

            <button
              onClick={clearCart}
              className="w-full bg-[#0a0a0a] hover:bg-black text-gray-400 py-2 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors border border-[#c9a96e]/20"
            >
              <Trash2 className="h-4 w-4" />
              Limpar Seleção
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

const CartItem = ({ item, onUpdateQuantity, onRemove }) => {
  const subtotal = item.produto.preco_venda * item.quantidade

  // Handle both array and string formats for images
  let imagemUrl = '/placeholder-product.jpg'
  if (item.produto.imagens) {
    if (Array.isArray(item.produto.imagens)) {
      imagemUrl = item.produto.imagens[0] || '/placeholder-product.jpg'
    } else if (typeof item.produto.imagens === 'string') {
      imagemUrl = item.produto.imagens.split(',')[0].trim() || '/placeholder-product.jpg'
    }
  }

  return (
    <div className="bg-[#0a0a0a] p-3 sm:p-4 rounded-lg border border-[#c9a96e]/20">
      <div className="flex gap-3 sm:gap-4">
        <img
          src={imagemUrl}
          alt={item.produto.nome}
          className="w-20 h-20 sm:w-24 sm:h-24 object-cover rounded-lg flex-shrink-0"
          onError={(e) => {
            e.target.src = '/placeholder-product.jpg'
          }}
        />

        <div className="flex-1 min-w-0">
          <div className="flex justify-between items-start gap-2 mb-2">
            <h3 className="font-semibold text-white text-sm sm:text-base line-clamp-2">
              {item.produto.nome}
            </h3>
            <button
              onClick={() => onRemove(item.produto.id, item.variacaoId)}
              className="text-red-500 hover:text-red-400 p-1 flex-shrink-0"
              title="Remover item"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>

          <div className="text-sm text-gray-400 mb-2 space-y-1">
            <div className="flex items-center gap-2">
              <span className="font-medium">Tamanho:</span>
              <span className="bg-[#1a1a1a] px-2 py-0.5 rounded text-xs font-semibold text-white border border-[#c9a96e]/20">{item.tamanho}</span>
            </div>
            <div className="text-xs text-gray-500">Código: {item.variacaoId}</div>
          </div>

          <div className="flex items-center justify-between mt-3 pt-3 border-t border-[#c9a96e]/20">
            <div className="flex items-center gap-2">
              <button
                onClick={() => onUpdateQuantity(item.produto.id, item.variacaoId, item.quantidade - 1)}
                className="w-7 h-7 rounded-full bg-[#1a1a1a] hover:bg-[#2a2a2a] flex items-center justify-center transition-colors border border-[#c9a96e]/30 text-white"
                disabled={item.quantidade <= 1}
              >
                <Minus className="h-3 w-3" />
              </button>

              <span className="w-8 text-center font-semibold text-white">
                {item.quantidade}
              </span>

              <button
                onClick={() => onUpdateQuantity(item.produto.id, item.variacaoId, item.quantidade + 1)}
                className="w-7 h-7 rounded-full bg-[#c9a96e] hover:bg-[#b8986e] text-white flex items-center justify-center transition-colors"
              >
                <Plus className="h-3 w-3" />
              </button>
            </div>

            <div className="text-right">
              <div className="text-xs text-gray-500">
                {item.quantidade}x R$ {item.produto.preco_venda.toFixed(2)}
              </div>
              <div className="text-base sm:text-lg font-bold text-[#c9a96e]">
                R$ {subtotal.toFixed(2)}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Cart

import { useState } from 'react'
import { X, Plus, Minus, ShoppingCart } from 'lucide-react'
import { useCart } from '../context/CartContext'

const AddToCartModal = ({ produto, isOpen, onClose }) => {
  const { addToCart } = useCart()
  const [selectedVariacoes, setSelectedVariacoes] = useState({})

  if (!isOpen) return null

  const handleQuantityChange = (variacaoId, tamanho, delta) => {
    setSelectedVariacoes(prev => {
      const current = prev[variacaoId] || 0
      const newValue = Math.max(0, current + delta)

      if (newValue === 0) {
        const { [variacaoId]: _, ...rest } = prev
        return rest
      }

      return {
        ...prev,
        [variacaoId]: newValue
      }
    })
  }

  const handleAddToCart = () => {
    Object.entries(selectedVariacoes).forEach(([variacaoId, quantidade]) => {
      const variacao = getVariacaoInfo(variacaoId)
      for (let i = 0; i < quantidade; i++) {
        addToCart(produto, variacaoId, variacao.tamanho)
      }
    })

    setSelectedVariacoes({})
    onClose()
  }

  const getVariacaoInfo = (variacaoId) => {
    // Buscar tamanho da lista dinâmica do produto
    const tamanhosDaAPI = Array.isArray(produto.tamanhos) && produto.tamanhos.length > 0
      ? produto.tamanhos
      : typeof produto.tamanhos === 'string' && produto.tamanhos.trim()
        ? produto.tamanhos.split(', ')
        : ['Tamanho Único']

    const parts = variacaoId.split('.')
    const index = parseInt(parts[1]) - 1
    return {
      tamanho: tamanhosDaAPI[index] || 'Único',
      id: variacaoId
    }
  }

  const getTotalItems = () => {
    return Object.values(selectedVariacoes).reduce((sum, qty) => sum + qty, 0)
  }

  // Variações de tamanho dinâmicas (vindas do fornecedor via API)
  const getVariacoes = () => {
    const baseCode = produto.id?.toString().padStart(8, '0') || '00000000'

    const tamanhosDaAPI = Array.isArray(produto.tamanhos) && produto.tamanhos.length > 0
      ? produto.tamanhos
      : typeof produto.tamanhos === 'string' && produto.tamanhos.trim()
        ? produto.tamanhos.split(', ')
        : ['Tamanho Único']

    return tamanhosDaAPI.map((tamanho, index) => ({
      id: `FZ${baseCode}.${index + 1}`,
      tamanho,
      preco: produto.preco_venda
    }))
  }

  const variacoes = getVariacoes()

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 z-50 flex items-center justify-center p-4">
      <div className="bg-[#1a1a1a] rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-[#c9a96e]/20">
        <div className="sticky top-0 bg-[#1a1a1a] border-b border-[#c9a96e]/20 p-4 flex justify-between items-center">
          <h2 className="text-xl font-bold text-white font-display">{produto.nome}</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-[#0a0a0a] rounded-full transition-colors text-white"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        <div className="p-6">
          <div className="mb-6">
            <img
              src={produto.imagens?.[0] || '/placeholder-product.jpg'}
              alt={produto.nome}
              className="w-full h-64 object-cover rounded-lg"
              onError={(e) => {
                e.target.src = '/placeholder-product.jpg'
              }}
            />
          </div>

          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4 text-white">Selecione seu Tamanho</h3>

            <div className="space-y-3">
              {variacoes.map((variacao) => (
                <div
                  key={variacao.id}
                  className="flex items-center justify-between p-4 border border-[#c9a96e]/20 rounded-lg hover:border-[#c9a96e] transition-colors bg-[#0a0a0a]"
                >
                  <div className="flex-1">
                    <div className="font-semibold text-white">
                      Tamanho {variacao.tamanho}
                    </div>
                    <div className="text-sm text-gray-400">
                      R$ {variacao.preco.toFixed(2)}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      # {variacao.id}
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => handleQuantityChange(variacao.id, variacao.tamanho, -1)}
                      className="w-8 h-8 rounded-full bg-[#1a1a1a] hover:bg-[#2a2a2a] flex items-center justify-center transition-colors border border-[#c9a96e]/30 text-white"
                      disabled={!selectedVariacoes[variacao.id]}
                    >
                      <Minus className="h-4 w-4" />
                    </button>

                    <span className="w-8 text-center font-semibold text-white">
                      {selectedVariacoes[variacao.id] || 0}
                    </span>

                    <button
                      onClick={() => handleQuantityChange(variacao.id, variacao.tamanho, 1)}
                      className="w-8 h-8 rounded-full bg-[#c9a96e] hover:bg-[#b8986e] text-white flex items-center justify-center transition-colors"
                    >
                      <Plus className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="border-t border-[#c9a96e]/20 pt-4">
            <button
              onClick={handleAddToCart}
              disabled={getTotalItems() === 0}
              className="w-full bg-[#c9a96e] hover:bg-[#b8986e] disabled:bg-gray-700 disabled:cursor-not-allowed text-white py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
            >
              <ShoppingCart className="h-5 w-5" />
              Adicionar à Seleção ({getTotalItems()} {getTotalItems() === 1 ? 'peça' : 'peças'})
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AddToCartModal

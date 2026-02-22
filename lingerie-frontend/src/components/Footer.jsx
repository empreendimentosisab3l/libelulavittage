import { MessageCircle, Mail, MapPin } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-[#0a0a0a] text-white py-12 border-t border-[#c9a96e]/20">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Sobre */}
          <div>
            <h3 className="text-xl font-bold mb-4 font-display text-[#c9a96e]">Libélula Vittage</h3>
            <p className="text-gray-400 mb-4">
              Lingerie de luxo para mulheres que celebram sua feminilidade.
              Peças exclusivas selecionadas com requinte e sofisticação.
            </p>
            <div className="flex space-x-4">
              <a
                href="https://wa.me/5511999999999"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[#c9a96e] hover:text-[#b8986e] transition-colors"
              >
                <MessageCircle className="h-6 w-6" />
              </a>
            </div>
          </div>

          {/* Links Rápidos */}
          <div>
            <h3 className="text-xl font-bold mb-4 font-display">Navegue</h3>
            <ul className="space-y-2">
              <li>
                <a href="/" className="text-gray-400 hover:text-[#c9a96e] transition-colors">
                  Início
                </a>
              </li>
              <li>
                <a href="/catalogo" className="text-gray-400 hover:text-[#c9a96e] transition-colors">
                  Coleção
                </a>
              </li>
              <li>
                <a href="/catalogo?categoria=Lingerie" className="text-gray-400 hover:text-[#c9a96e] transition-colors">
                  Lingerie
                </a>
              </li>
              <li>
                <a href="/catalogo?categoria=Conjuntos" className="text-gray-400 hover:text-[#c9a96e] transition-colors">
                  Conjuntos
                </a>
              </li>
            </ul>
          </div>

          {/* Contato */}
          <div>
            <h3 className="text-xl font-bold mb-4 font-display">Fale Conosco</h3>
            <div className="space-y-3">
              <div className="flex items-center">
                <MessageCircle className="h-5 w-5 mr-3 text-[#c9a96e]" />
                <span className="text-gray-400">WhatsApp: (11) 99999-9999</span>
              </div>
              <div className="flex items-center">
                <Mail className="h-5 w-5 mr-3 text-[#c9a96e]" />
                <span className="text-gray-400">contato@libelulavittage.com</span>
              </div>
              <div className="flex items-center">
                <MapPin className="h-5 w-5 mr-3 text-[#c9a96e]" />
                <span className="text-gray-400">Enviamos para todo o Brasil</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-[#c9a96e]/20 mt-8 pt-8 text-center">
          <p className="text-gray-500">
            © 2024 Libélula Vittage. Todos os direitos reservados.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer


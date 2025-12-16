import { MessageCircle, Mail, MapPin } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Sobre */}
          <div>
            <h3 className="text-xl font-bold mb-4">Boutique Lingerie</h3>
            <p className="text-gray-300 mb-4">
              Sua boutique online especializada em lingerie de qualidade. 
              Oferecemos produtos cuidadosamente selecionados com atendimento personalizado.
            </p>
            <div className="flex space-x-4">
              <a 
                href="https://wa.me/5511999999999" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-green-400 hover:text-green-300 transition-colors"
              >
                <MessageCircle className="h-6 w-6" />
              </a>
            </div>
          </div>

          {/* Links Rápidos */}
          <div>
            <h3 className="text-xl font-bold mb-4">Links Rápidos</h3>
            <ul className="space-y-2">
              <li>
                <a href="/" className="text-gray-300 hover:text-white transition-colors">
                  Início
                </a>
              </li>
              <li>
                <a href="/catalogo" className="text-gray-300 hover:text-white transition-colors">
                  Catálogo
                </a>
              </li>
              <li>
                <a href="/catalogo?categoria=Lingerie" className="text-gray-300 hover:text-white transition-colors">
                  Lingerie
                </a>
              </li>
              <li>
                <a href="/catalogo?categoria=Conjuntos" className="text-gray-300 hover:text-white transition-colors">
                  Conjuntos
                </a>
              </li>
            </ul>
          </div>

          {/* Contato */}
          <div>
            <h3 className="text-xl font-bold mb-4">Contato</h3>
            <div className="space-y-3">
              <div className="flex items-center">
                <MessageCircle className="h-5 w-5 mr-3 text-green-400" />
                <span className="text-gray-300">WhatsApp: (11) 99999-9999</span>
              </div>
              <div className="flex items-center">
                <Mail className="h-5 w-5 mr-3 text-blue-400" />
                <span className="text-gray-300">contato@boutiquelingerie.com</span>
              </div>
              <div className="flex items-center">
                <MapPin className="h-5 w-5 mr-3 text-red-400" />
                <span className="text-gray-300">Enviamos para todo o Brasil</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p className="text-gray-400">
            © 2024 Boutique Lingerie. Todos os direitos reservados.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer


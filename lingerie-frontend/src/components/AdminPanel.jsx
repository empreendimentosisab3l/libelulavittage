import { useState, useEffect } from 'react'
import { Database, Package, Github, ExternalLink } from 'lucide-react'
import { Button } from './ui/button'
import { supabase } from '../lib/supabase'
import { listarCategorias } from '../lib/produtos'

const AdminPanel = () => {
  const [stats, setStats] = useState({ total: 0, categorias: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    carregarDados()
  }, [])

  const carregarDados = async () => {
    try {
      setLoading(true)
      const [{ count }, categorias] = await Promise.all([
        supabase
          .from('produtos')
          .select('*', { count: 'exact', head: true })
          .eq('ativo', true),
        listarCategorias()
      ])
      setStats({ total: count || 0, categorias: categorias.length })
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2 font-display">Painel Administrativo</h1>
          <p className="text-gray-400">Visão geral do catálogo</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-[#1a1a1a] rounded-lg border border-[#c9a96e]/20 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-400 font-medium">Produtos ativos</h3>
              <Package className="h-8 w-8 text-[#c9a96e]" />
            </div>
            <p className="text-4xl font-bold text-white">
              {loading ? '...' : stats.total}
            </p>
          </div>

          <div className="bg-[#1a1a1a] rounded-lg border border-[#c9a96e]/20 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-400 font-medium">Categorias</h3>
              <Database className="h-8 w-8 text-[#c9a96e]" />
            </div>
            <p className="text-4xl font-bold text-white">
              {loading ? '...' : stats.categorias}
            </p>
          </div>
        </div>

        <div className="bg-[#1a1a1a] rounded-lg border border-[#c9a96e]/20 p-8 mb-8">
          <h2 className="text-2xl font-bold text-white mb-4 font-display">Operações</h2>
          <p className="text-gray-400 mb-6">
            O catálogo é sincronizado automaticamente pelo GitHub Actions (1x/dia).
            Para gerenciar produtos manualmente ou disparar uma sincronização agora, use os atalhos abaixo.
          </p>

          <div className="space-y-3">
            <a
              href="https://github.com/empreendimentosisab3l/libelulavittage/actions"
              target="_blank"
              rel="noreferrer"
              className="flex items-center justify-between bg-[#0a0a0a] hover:bg-[#222] border border-[#c9a96e]/20 hover:border-[#c9a96e] transition-colors rounded-lg p-4"
            >
              <div className="flex items-center">
                <Github className="h-5 w-5 mr-3 text-[#c9a96e]" />
                <div>
                  <div className="text-white font-semibold">Disparar sincronização agora</div>
                  <div className="text-sm text-gray-400">Abre o GitHub Actions — clique em "Run workflow"</div>
                </div>
              </div>
              <ExternalLink className="h-4 w-4 text-gray-500" />
            </a>

            <a
              href="https://supabase.com/dashboard/project/oqezrudjiphggsphncxi/editor"
              target="_blank"
              rel="noreferrer"
              className="flex items-center justify-between bg-[#0a0a0a] hover:bg-[#222] border border-[#c9a96e]/20 hover:border-[#c9a96e] transition-colors rounded-lg p-4"
            >
              <div className="flex items-center">
                <Database className="h-5 w-5 mr-3 text-[#c9a96e]" />
                <div>
                  <div className="text-white font-semibold">Editar produtos e configurações</div>
                  <div className="text-sm text-gray-400">Abre o Supabase Table Editor</div>
                </div>
              </div>
              <ExternalLink className="h-4 w-4 text-gray-500" />
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminPanel

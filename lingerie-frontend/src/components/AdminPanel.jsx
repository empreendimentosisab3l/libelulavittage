import { useState, useEffect, useRef } from 'react'
import { RefreshCw, Database, CheckCircle, AlertCircle, TrendingUp, Package, Search, Globe, Info } from 'lucide-react'
import { Button } from './ui/button'

const AdminPanel = ({ apiBaseUrl }) => {
  const [stats, setStats] = useState(null)
  const [lastLog, setLastLog] = useState(null)
  const [loading, setLoading] = useState(false)
  const [scraping, setScraping] = useState(false)
  const [message, setMessage] = useState(null)
  const [strategy, setStrategy] = useState('keyword') // 'keyword' or 'sitemap'

  // Progress Bar State
  const [progress, setProgress] = useState({ percentage: 0, message: '' })
  const progressIntervalRef = useRef(null)

  useEffect(() => {
    carregarDados()
    return () => stopPolling()
  }, [])

  const carregarDados = async () => {
    try {
      // Carregar estatísticas de produtos
      const produtosResponse = await fetch(`${apiBaseUrl}/produtos`)
      const produtosData = await produtosResponse.json()

      // Carregar último log de scraping
      const logResponse = await fetch(`${apiBaseUrl}/scraper/status`)
      const logData = await logResponse.json()

      setStats({
        total: produtosData.total || 0,
        pages: produtosData.pages || 0
      })

      setLastLog(logData)
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    }
  }

  const startPolling = () => {
    stopPolling() // Ensure cleanup first
    progressIntervalRef.current = setInterval(async () => {
      try {
        const response = await fetch(`${apiBaseUrl}/scraper/progress`)
        const data = await response.json()

        setProgress({
          percentage: data.percentage,
          message: data.message
        })

        if (data.status === 'completed' || data.status === 'error') {
          stopPolling()
          setScraping(false)

          if (data.status === 'completed') {
            setMessage({
              type: 'success',
              text: data.message
            })
            await carregarDados()
          } else {
            setMessage({
              type: 'error',
              text: `Erro: ${data.message}`
            })
          }
        }

      } catch (error) {
        console.error("Polling error", error)
      }
    }, 1000)
  }

  const stopPolling = () => {
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current)
      progressIntervalRef.current = null
    }
  }

  const executarScraper = async () => {
    try {
      setScraping(true)
      setMessage(null)
      setProgress({ percentage: 0, message: 'Iniciando...' })

      const response = await fetch(`${apiBaseUrl}/scraper/executar`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ strategy })
      })
      const data = await response.json()

      if (response.ok) {
        // Scraper started successfully in background
        startPolling()
      } else {
        // Check if it's "Already Running" error
        if (response.status === 400 && data.erro && data.erro.includes('execução')) {
          console.log('Scraper already running, attaching to process...')
          startPolling()
        } else {
          setScraping(false)
          setMessage({
            type: 'error',
            text: `Erro: ${data.erro || 'Falha ao iniciar scraper'}`
          })
        }
      }
    } catch (error) {
      setScraping(false)
      setMessage({
        type: 'error',
        text: `Erro: ${error.message}`
      })
    }
  }

  const limparProdutos = async () => {
    if (!confirm('Tem certeza que deseja deletar TODOS os produtos? Esta ação não pode ser desfeita!')) {
      return
    }

    try {
      setLoading(true)
      const response = await fetch(`${apiBaseUrl}/config/limpar-produtos`, {
        method: 'POST'
      })

      const data = await response.json()

      if (response.ok) {
        setMessage({
          type: 'success',
          text: data.mensagem || 'Produtos deletados com sucesso!'
        })
        await carregarDados()
      } else {
        setMessage({
          type: 'error',
          text: `Erro: ${data.erro || 'Falha ao limpar produtos'}`
        })
      }
    } catch (error) {
      setMessage({
        type: 'error',
        text: `Erro: ${error.message}`
      })
    } finally {
      setLoading(false)
    }
  }

  const formatarData = (dataISO) => {
    if (!dataISO) return 'N/A'
    const data = new Date(dataISO)
    return data.toLocaleString('pt-BR')
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2 font-display">Painel Administrativo</h1>
          <p className="text-gray-400">Gerencie o scraper e produtos da loja</p>
        </div>

        {/* Message Alert */}
        {message && (
          <div className={`mb-6 p-4 rounded-lg flex items-start ${message.type === 'success' ? 'bg-green-900/30 border border-green-500/30' : 'bg-red-900/30 border border-red-500/30'
            }`}>
            {message.type === 'success' ? (
              <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5" />
            ) : (
              <AlertCircle className="h-5 w-5 text-red-400 mr-3 mt-0.5" />
            )}
            <p className={message.type === 'success' ? 'text-green-300' : 'text-red-300'}>
              {message.text}
            </p>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-[#1a1a1a] rounded-lg border border-[#c9a96e]/20 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-400 font-medium">Total de Produtos</h3>
              <Package className="h-8 w-8 text-[#c9a96e]" />
            </div>
            <p className="text-4xl font-bold text-white">{stats?.total || 0}</p>
            <p className="text-sm text-gray-500 mt-2">{stats?.pages || 0} páginas no catálogo</p>
          </div>

          <div className="bg-[#1a1a1a] rounded-lg border border-[#c9a96e]/20 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-400 font-medium">Último Scraping</h3>
              <Database className="h-8 w-8 text-[#c9a96e]" />
            </div>
            {lastLog && lastLog.data_execucao ? (
              <>
                <p className="text-lg font-semibold text-white">
                  {lastLog.produtos_novos || 0} novos
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  {formatarData(lastLog.data_execucao)}
                </p>
              </>
            ) : (
              <p className="text-gray-500">Nenhum scraping executado</p>
            )}
          </div>

          <div className="bg-[#1a1a1a] rounded-lg border border-[#c9a96e]/20 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-400 font-medium">Status</h3>
              <TrendingUp className="h-8 w-8 text-green-500" />
            </div>
            <p className={`text-lg font-semibold ${lastLog?.status === 'sucesso' ? 'text-green-400' : 'text-red-400'
              }`}>
              {lastLog?.status === 'sucesso' ? 'Operacional' : lastLog?.status || 'N/A'}
            </p>
            <p className="text-sm text-gray-500 mt-2">
              {lastLog?.produtos_atualizados || 0} atualizados
            </p>
          </div>
        </div>

        {/* Actions */}
        <div className="bg-[#1a1a1a] rounded-lg border border-[#c9a96e]/20 p-8 mb-8">
          <h2 className="text-2xl font-bold text-white mb-6 font-display">Ações</h2>

          <div className="space-y-6">
            {/* Executar Scraper */}
            <div className="border-b border-[#c9a96e]/10 pb-6">
              <h3 className="text-lg font-semibold text-white mb-4">Executar Scraper</h3>

              {/* Strategy Selector */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div
                  className={`border rounded-lg p-4 cursor-pointer transition-all ${strategy === 'keyword' ? 'border-[#c9a96e] bg-[#c9a96e]/10 ring-2 ring-[#c9a96e]/30' : 'border-[#333] hover:border-[#c9a96e]/50'}`}
                  onClick={() => !scraping && setStrategy('keyword')}
                >
                  <div className="flex items-center mb-2">
                    <Search className={`h-5 w-5 mr-2 ${strategy === 'keyword' ? 'text-[#c9a96e]' : 'text-gray-500'}`} />
                    <span className={`font-semibold ${strategy === 'keyword' ? 'text-[#c9a96e]' : 'text-gray-300'}`}>Varredura Rápida</span>
                  </div>
                  <p className="text-sm text-gray-400">Busca por palavras-chave (conjunto, sutiã, etc). Mais rápido, mas cobre apenas ~50% do catálogo.</p>
                </div>

                <div
                  className={`border rounded-lg p-4 cursor-pointer transition-all ${strategy === 'sitemap' ? 'border-[#c9a96e] bg-[#c9a96e]/10 ring-2 ring-[#c9a96e]/30' : 'border-[#333] hover:border-[#c9a96e]/50'}`}
                  onClick={() => !scraping && setStrategy('sitemap')}
                >
                  <div className="flex items-center mb-2">
                    <Globe className={`h-5 w-5 mr-2 ${strategy === 'sitemap' ? 'text-[#c9a96e]' : 'text-gray-500'}`} />
                    <span className={`font-semibold ${strategy === 'sitemap' ? 'text-[#c9a96e]' : 'text-gray-300'}`}>Varredura Completa</span>
                  </div>
                  <p className="text-sm text-gray-400">Baixa TUDO via Sitemap. Garante 100% de cobertura, incluindo Cores e Tamanhos.</p>
                </div>

                <div
                  className={`border rounded-lg p-4 cursor-pointer transition-all ${strategy === 'smart_update' ? 'border-blue-500 bg-blue-500/10 ring-2 ring-blue-500/30' : 'border-[#333] hover:border-blue-500/50'}`}
                  onClick={() => !scraping && setStrategy('smart_update')}
                >
                  <div className="flex items-center mb-2">
                    <Package className={`h-5 w-5 mr-2 ${strategy === 'smart_update' ? 'text-blue-400' : 'text-gray-500'}`} />
                    <span className={`font-semibold ${strategy === 'smart_update' ? 'text-blue-400' : 'text-gray-300'}`}>Atualização Inteligente</span>
                    <span className="ml-2 px-2 py-0.5 text-xs bg-blue-500/20 text-blue-400 rounded-full font-medium">Auto</span>
                  </div>
                  <p className="text-sm text-gray-400">Verifica o banco. Só baixa produtos novos ou incompletos. Extremamente rápido.</p>
                </div>
              </div>

              {scraping ? (
                <div className="w-full max-w-xl">
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-[#c9a96e]">{progress.message || 'Processando...'}</span>
                    <span className="text-sm font-medium text-[#c9a96e]">{progress.percentage}%</span>
                  </div>
                  <div className="w-full bg-[#333] rounded-full h-2.5">
                    <div
                      className="bg-[#c9a96e] h-2.5 rounded-full transition-all duration-500"
                      style={{ width: `${progress.percentage}%` }}
                    ></div>
                  </div>

                  <div className="mt-4 flex items-center text-sm text-blue-400 bg-blue-500/10 border border-blue-500/20 p-3 rounded-md">
                    <Info className="h-4 w-4 mr-2" />
                    <p>O processo continua rodando mesmo se você sair desta página.</p>
                  </div>
                </div>
              ) : (
                <Button
                  onClick={executarScraper}
                  disabled={scraping}
                  size="lg"
                >
                  <RefreshCw className={`h-5 w-5 mr-2 ${scraping ? 'animate-spin' : ''}`} />
                  {scraping ? 'Executando Scraper...' : `Iniciar Scraper (${strategy === 'keyword' ? 'Rápido' : strategy === 'sitemap' ? 'Completo' : 'Inteligente'})`}
                </Button>
              )}

            </div>

            {/* Limpar Produtos */}
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Limpar Produtos</h3>
              <p className="text-gray-400 mb-4">
                Remove TODOS os produtos do banco de dados.
                <br />
                <span className="text-sm text-red-400">Atenção: Esta ação não pode ser desfeita!</span>
              </p>
              <Button
                onClick={limparProdutos}
                disabled={loading || scraping}
                variant="outline"
                className="border-red-500 text-red-400 hover:bg-red-500/10"
                size="lg"
              >
                <Database className="h-5 w-5 mr-2" />
                {loading ? 'Limpando...' : 'Limpar Todos os Produtos'}
              </Button>
            </div>
          </div>
        </div>

        {/* Último Log Detalhado */}
        {lastLog && lastLog.data_execucao && (
          <div className="bg-[#1a1a1a] rounded-lg border border-[#c9a96e]/20 p-8">
            <h2 className="text-2xl font-bold text-white mb-6 font-display">Último Scraping - Detalhes</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm text-gray-500 mb-1">Data de Execução</p>
                <p className="text-lg font-semibold text-white">{formatarData(lastLog.data_execucao)}</p>
              </div>

              <div>
                <p className="text-sm text-gray-500 mb-1">Status</p>
                <p className={`text-lg font-semibold ${lastLog.status === 'sucesso' ? 'text-green-400' : 'text-red-400'
                  }`}>
                  {lastLog.status}
                </p>
              </div>

              <div>
                <p className="text-sm text-gray-500 mb-1">Produtos Novos</p>
                <p className="text-lg font-semibold text-white">{lastLog.produtos_novos}</p>
              </div>

              <div>
                <p className="text-sm text-gray-500 mb-1">Produtos Atualizados</p>
                <p className="text-lg font-semibold text-white">{lastLog.produtos_atualizados}</p>
              </div>
            </div>

            {lastLog.erros && (
              <div className="mt-6">
                <p className="text-sm text-gray-500 mb-2">Erros</p>
                <div className="bg-red-900/20 border border-red-500/30 rounded p-4">
                  <p className="text-red-300 font-mono text-sm">{lastLog.erros}</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminPanel

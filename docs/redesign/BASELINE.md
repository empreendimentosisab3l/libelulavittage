# Libélula Vittage — ponto de partida

- Data: 23/10/2026, America/Sao_Paulo.
- Repositório: `empreendimentosisab3l/libelulavittage`.
- `main` limpa no clone, sem arquivos modificados ou não rastreados.
- Commit de partida: `55b2e98facf0e8bafba3e194bebe614ffdaef0a4`.
- Branch de trabalho: `redesign-premium`.
- A produção só poderá mudar após aprovação expressa do preview.

## Contratos preservados

Rotas `/`, `/catalogo`, `/produto/:id`, `/admin`; componentes React atuais; consultas Supabase em `src/lib/produtos.js`; cliente em `src/lib/supabase.js`; armazenamento `lingerie-cart`; identificação `produto.id` + `variacaoId`; códigos `FZ<id com 8 dígitos>.<índice do tamanho + 1>`; número do WhatsApp via `getConfig()`; mensagem com nome, tamanho, quantidade, preço unitário, subtotal, código, link e total.

Não alterar Flask, scraper, schema ou GitHub Action. Não executar o sync manualmente durante a pesquisa. A leitura do scraper confirmou que `cores` já existe; normalmente a cor também aparece entre parênteses no nome e cada cor tem ID próprio. Uma troca de cor pode apontar ao produto real correspondente, sem coluna nova nem recoloração da foto.

## Limites desta primeira entrega

Somente protótipos de home em `lingerie-frontend/public/direcoes/` e documentação. Nenhum componente de produção é redesenhado antes da escolha. Produtos dos estudos são uma fotografia dos dados públicos em 23/10, não uma nova fonte de estoque. Links de produto abrem a página React existente. A sacola do estudo explica esse limite e leva ao catálogo; não é o novo carrinho.

As credenciais públicas do frontend em produção foram usadas apenas em `.env.local`, ignorado pelo Git, para compilar a loja existente. Nenhuma chave de serviço foi solicitada, exposta ou adicionada ao repositório. Não foi encontrada chave de geração nas variáveis de ambiente da sessão. Vercel CLI não está autenticada; tentar o deployment automático da branch pelo GitHub. Nunca usar `--prod` nem promover um preview sem aprovação.

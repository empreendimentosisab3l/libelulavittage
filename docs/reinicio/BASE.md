# Reinício criativo — 23/10/2026

O usuário pediu para ignorar os estudos anteriores e começar do zero. Esta branch nasce de main, sem importar os protótipos antigos.

- Branch: codex/redesign-from-zero.
- Base: 55b2e98facf0e8bafba3e194bebe614ffdaef0a4. Árvore limpa antes da criação.
- Etapa: três propostas independentes para escolha. Não é o redesign final.
- Contratos: manter src/lib, formato dos dados, lingerie-cart, /produto/:id, /admin, WhatsApp via getConfig, Flask, scraper e sync.
- Dados: fotografia de produtos públicos consultada em 23/10. Não usar essa fotografia como estoque na implementação final.

## Diagnóstico novo
A primeira tela atual não mostra uma peça comprável nem seu preço. Minha Conta aponta ao admin. Cart.jsx formata com ponto e omite o campo cor. O redesign precisa mostrar desejo e oferta juntos e manter a passagem ao WhatsApp.

## Pesquisa
- https://fleurdumal.com/ — categorias, campanhas e Shop the Feed: unir descoberta editorial e tráfego social.
- https://www.agentprovocateur.com/ — coleções e atendimento: atmosfera de marca com navegação explícita.
- https://www.natori.com/ — guia/quiz para sutiã: orientação de tamanho próxima da escolha.
- https://www.savagex.com/ — oferta evidente; não adotar complexidade de membership.
- https://www.hopeoficial.com.br/ e https://www.valisere.com.br/ — nomes de categorias familiares ao público brasileiro.
- https://www.awwwards.com/websites/fashion/ — pesquisa de ritmo e composição editorial.
- https://www.squared-media.nl/en/cases/wooz — case do próprio estúdio: loja 3D sobre checkout convencional. Aqui o 3D terá papel atmosférico, não será navegação obrigatória.
- https://www.behance.net/gallery/252991551/Belle-Etoile-Lingerie-Store-UXUI-design — referência aberta no navegador, não copiar assets.
- https://baymard.com/research-articles/apparel-size-information — dúvidas de tamanho devem ser resolvidas junto ao seletor.
- FWA retornou sem conteúdo legível e Intimissimi BR falhou na pesquisa; não afirmar inspeção concluída.

## Hipóteses inéditas
1. Teatro Rubi: palco de cetim, título em duas escalas e fotografia central suspensa. Composição simétrica e dramática, coleção clara em seguida.
2. Galeria Noturna: fotografia ocupando metade da tela, tipografia condensada por espaçamento, navegação lateral e seleção numerada. Composição assimétrica, preto e metal claro.
3. Jardim Íntimo: abertura de revista em papel, par de fotos desencontradas, botânica linear própria, verde oliva e rosa antigo. Ritmo íntimo e diurno.

A escolha define o style guide posterior. Nenhuma direção está aprovada. Guia de banda/bojo, política de troca, entrega discreta e depoimentos continuam pendentes de dados reais. Sem inventar popularidade ou colunas.

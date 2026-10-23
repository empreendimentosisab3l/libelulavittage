# Verificação — etapa de escolha da direção

23/10/2026. Esta etapa entrega três protótipos de home, não o redesign completo aprovado.

## Resultado

- `npm ci --no-audit --no-fund` concluído.
- `node --check` nos dois módulos dos estudos: passou.
- `npm run build`: passou. Bundle React `index-BjwCG_PE.js`, idêntico ao nome do bundle servido no site de partida. Nenhum arquivo em `src/`, Flask, scraper ou `.github/` foi alterado.
- `git diff --cached --check`: sem erros.
- `main` remota reconfirmada em `55b2e98facf0e8bafba3e194bebe614ffdaef0a4` após o primeiro push.
- Deploy da branch `redesign-premium` confirmado pelo status GitHub/Vercel. Primeiro deployment de estudos: `fc0775dc14a9eadd50708e4a6333d3ea517a3430`, ambiente **Preview**, deployment GitHub `7288930250`.
- URL desse preview: https://libelulavittage-mbifxdblp-lucas-projects-a37e0716.vercel.app/direcoes/index.html
- O preview remoto redireciona ao login Vercel. Não foi desativada a proteção nem declarada inspeção visual remota concluída. Prints e verificações visuais foram feitos no servidor local.

## Inspeção visual

Viewport medido no navegador em 375 × 812 e 1440 × 1000. A captura do navegador exclui partes de sua moldura/barra; por isso o bitmap tem dimensão diferente do viewport CSS. O relatório e as pranchas identificam **viewport**, não tamanho do arquivo.

Três aberturas, três coleções, três editoriais e três áreas de atendimento capturados em cada largura. Fotos reais verificadas, nenhuma imagem quebrada observada. Sem transbordamento horizontal nas três direções em 375 px após correção da decoração botânica de Romance. Ofertas observadas na faixa fixa: Mariana Preto/Vermelho/Marfim, `De R$ 111,93 / Por R$ 86,10`. Menu móvel e diálogo de sacola do estudo abrem e fecham. Links usam os IDs reais de produto e as rotas existentes. Logs da última verificação do estudo Cetim: sem erros ou avisos.

Pranchas `*-comparativo.jpg` mostram abertura desktop e móvel. `*-qa-mobile.jpg` reúnem a abertura e as três seções móveis. Os JPGs individuais preservam as capturas retornadas pelo navegador, sem recriar a interface.

## Movimento e limites da etapa

Os estudos Noir e Cetim incluem uma malha WebGL nativa com deslocamento 3D e iluminação; o módulo é carregado após a primeira pintura. Poster SVG local, redução de malha/DPR no celular, pausa fora da tela, descarte de recursos, detecção de aparelho limitado, economia de dados e preferência de reduzir movimento. Romance foi propositalmente estudada como alternativa de menor dependência de efeito; sua cena, se escolhida, ainda será definida.

No navegador de inspeção, a preferência de movimento provocou fallback estático (`data-motion="static-user-preference"` e canvas oculto pelo CSS de redução de movimento). A abertura, foto e oferta permaneceram visíveis. Os prints são estáticos. **O movimento WebGL ainda precisa de validação em um dispositivo/ambiente com animação habilitada, além do refinamento após a escolha.**

Não foram executados nesta etapa: Lighthouse do redesign final, testes de checkout novo, persistência de migração do carrinho, filtros novos com centenas de itens, matriz completa de acessibilidade ou teste de mensagem nova. Esses componentes ainda não foram alterados. Permanecem requisitos da implementação após a escolha e da aprovação final do preview.

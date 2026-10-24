# Verificação dos novos estudos

- Build Vite passou. JavaScript validado com node --check.
- 24 capturas: abertura, coleção, editorial e atendimento de cada direção, com viewport CSS 375 × 812 e 1440 × 1000.
- Imagens e pranchas em prints/. Capturas do navegador podem ter escala diferente do viewport CSS.
- Nenhum transbordamento horizontal detectado nos 24 estados. Nenhuma imagem carregada com erro detectada.
- Inspeção visual das pranchas: ajuste do posicionamento do título desktop Rubi e da escala do título Noturna móvel. Fotos reais e ofertas visíveis. Barra móvel mantém preço e escolha acessíveis.
- No navegador de inspeção, o módulo de tecido escolheu static-preference-or-device. Os prints mostram o fallback. Há malha WebGL implementada, mas sua animação ainda não foi validada neste ambiente; não apresentar como cena 3D final aprovada.
- Esta etapa não altera src, dependências, /admin, Flask, sync ou scraper. O build React conserva o bundle index-BjwCG_PE.js da base.
- Checkout, filtros e Lighthouse do redesign completo serão validados depois da escolha, quando os componentes forem implementados. Não foram declarados como testados nesta entrega de conceitos.
- Dados públicos obtidos em 23/10/2026, usados como amostra visual. Na aplicação final, consultar o Supabase pelo código existente.

## Preview

- Commit publicado: 1b9de71a893c5ac3c43f4a6e16b6a05fed78cbb1.
- Deployment GitHub 7291868637, ambiente Preview, status success.
- https://libelulavittage-68xcg881n-lucas-projects-a37e0716.vercel.app/conceitos/index.html
- Acesso remoto redirecionou ao login Vercel. Nenhuma proteção foi removida. Inspeção visual realizada no preview local.
- Fotos redimensionadas e comprimidas, sem recolorir as peças: 12,5 MB para 3,0 MB no conjunto de 18 arquivos. Imagens abaixo da abertura usam lazy loading.
- Menu móvel abriu e fechou. O teste inicial com URL /conceitos/ caiu no roteador React; usar /conceitos/index.html conforme o link entregue.
- Build repetido após os ajustes passou. Arquivos de produção e integrações sem diferenças em relação à main.

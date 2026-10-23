# Pesquisa e auditoria — 23/10/2026

## O que atrapalha a venda hoje

1. A abertura vende uma fotografia genérica, sem peça identificada ou preço. “Minha Conta” conduz ao admin.
2. O header muda entre home e catálogo. A logo preta quase desaparece no fundo preto do catálogo.
3. Em 375 px o catálogo tem uma única coluna. A listagem pública observada tem 595 produtos; 24 por carregamento. A cliente percorre muitas telas para comparar poucas opções.
4. A busca do catálogo atribui `window.location.href` no `onChange`: recarrega por tecla. O estado de carregamento/erro pode parecer uma coleção vazia.
5. A página do produto só revela preço e tamanhos depois da galeria; apresenta uma longa lista de contadores e códigos técnicos, sem guia de medidas, sem troca de cor, sem botão fixo. Adicionar abre `alert` e não oferece continuação clara para o carrinho.
6. Valores com ponto quebram a continuidade com os Stories. “De/Por” aparece no produto, mas não nos cards da home ou catálogo.
7. O WhatsApp omite a cor como campo, apesar de o dado existir, e usa `toFixed` diretamente. A quantidade e o carrinho persistente devem ser preservados.
8. Textos como “peças reservadas”, “exclusivas” ou garantias amplas precisam corresponder à operação real. Não criar escassez, popularidade, avaliações ou promessa de prazo.

Inspeção: home, catálogo e produto 4930 no navegador em 375 px; código integral dos componentes de compra, contexto de carrinho e lib de produtos. Leitura apenas do sync e workflow. Fotos reais de Mariana em seis cores e outras famílias. A edição de `/admin` não faz parte do escopo.

## Referências e decisões derivadas

Fontes acessadas em 23/10/2026. A descrição abaixo separa o que foi observado da decisão de projeto; não representa um ranking nem comprova conversão das referências.

| Fonte primária | Observação | Aplicação à Libélula |
| --- | --- | --- |
| [Belle Etoile, Kristina B., Behance](https://www.behance.net/gallery/252991551/Belle-Etoile-Lingerie-Store-UXUI-design) | Página aberta no navegador: cetim vermelho, escala de didone, molduras e camadas de cenografia. Inclui vídeo Vimeo incorporado. | Contraste vinho/marfim e ritmo editorial, usando as nossas próprias fotos reais e tecido feito em código. Não copiar imagens, tipografia comercial ou layout literal. |
| [Agent Provocateur — lingerie](https://www.agentprovocateur.com/us_en/lingerie) e [private fittings](https://www.agentprovocateur.com/us_en/private-fittings) | Organiza famílias, estilos, bandas/bojos e cores. Atendimento pessoal participa da proposta premium. | Navegação por intenção e família; atendimento WhatsApp como concierge, próximo à compra. |
| [Fleur du Mal](https://fleurdumal.com/) | Home aberta no navegador: campanha em grande escala, acesso claro à coleção, cores nos produtos, quick view, feed comprável e ajuda de tamanho. | Campanha emocional seguida de fotos e preço; ligação com Stories/Instagram. Poucas peças na home; catálogo dedicado mantém a escala. |
| [Savage X Fenty](https://www.savagex.com/) | Conteúdo público apresenta categorias, novidades e regras de benefícios/membership. | Clareza do caminho para a peça. Não importar a complexidade de assinatura nem a poluição de promoções. |
| [Natori](https://www.natori.com/) | Navegação pública inclui estilos, “The Bra Guide”, “Measure Your Bra Size” e quiz. | Fit é parte da decisão de compra. Colocar ajuda imediatamente ao lado do tamanho, com medidas corretas do fornecedor. |
| [Intimissimi — guia de tamanho](https://www.intimissimi.com/pt/product-guide-size.html) | Distingue contorno de tórax de copa e apresenta tabelas por sistema/país. A home BR não foi retornada pela ferramenta de pesquisa; a fonte efetivamente consultada é o guia PT. | Não copiar conversão estrangeira para P/M/G da Caliente. Separar explicação de como medir de uma recomendação de tamanho verificada. |
| [HOPE](https://www.hopeoficial.com.br/) | Navegação pública conhecida por tipo de peça; frete, troca e condições são explicitados. | Familiaridade brasileira de categorias e linguagem direta; nossa política precisa ser confirmada antes de publicá-la. |
| [Valisere](https://www.valisere.com.br/) e [coleção preta](https://www.valisere.com.br/lingerie-preta) | Produtos exibem tamanhos, preços brasileiros, bojos B/C em modelos específicos e ação de sacola. | Preço e seleção claros sem remover o posicionamento editorial. |
| [Awwwards — Finely Crafted](https://www.awwwards.com/sites/finely-crafted) e [exemplo de shopping WebGL](https://www.awwwards.com/inspiration_search/varnish/?page=2) | Pesquisa indexada relaciona moda, transições, WebGL e experiências de compra. O acesso a algumas páginas de cases/categoria falhou; não tratar como auditoria de desempenho desses sites. | Usar uma cena curta de atmosfera, nunca navegação obrigatória em canvas ou loader que bloqueia a loja. |
| [FWA — feed oficial](https://thefwa.com/rss/) | Feed consultado apresenta projetos de interação e Three.js; não foi obtido um case verificável de lingerie/e-commerce com desempenho móvel comparável. | Referência de ambição de interação, não evidência de que uma experiência premiada converta ou rode bem em celular intermediário. |
| [Baymard — informações de tamanho](https://baymard.com/research-articles/apparel-size-information) | Pesquisa aponta dúvida de tamanho como causa de abandono e recomenda medidas, equivalências e orientação acessível na página de produto. | Guia perto do seletor, sem adivinhar equivalência de banda/copa para a fornecedora. |
| [MDN — WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices) | Orientações para limites de recursos e custo do desenho. | DPR limitado, malha pequena, sem pós-processamento, sem textura pesada, pausa fora da tela e fallback automático. |

## As três hipóteses visuais

- **01 Noir intimista:** salão noturno, preto quente, ouro antigo, foto em arco e grande área de silêncio. Ouro do site atual preservado como referência, não como obrigação. Preto sustenta atmosfera; a seleção tem papel claro para leitura e comparação de fotos.
- **02 Cetim editorial:** marfim, vinho profundo, didone grande e foto real emoldurada sobre cetim WebGL. Alternância de papel claro e páginas vinho; peça, oferta e ação ficam explícitas. Recomendação inicial do designer: é a hipótese de maior assinatura de marca.
- **03 Romance natural:** marfim, rosé seco, Cormorant, botânica desenhada e foto em abertura oval. Um ritual pessoal mais solar e acolhedor. Menor dependência de efeito para funcionar.

Escolha aberta ao usuário. Não documentar uma dessas como aprovada nem aplicar no React antes da resposta.

## Dados a confirmar na etapa de produto

- Tabela oficial da Caliente com busto, sob busto/banda, bojo e equivalência dos tamanhos por modelo/família. Não existe nos campos lidos.
- Política real de troca e condições de entrega discreta, prazo, pagamento e frete.
- Depoimentos reais e autorização de uso, se houver. Não adicionar seção vazia na loja nem depoimentos fictícios; manter componente preparado na implementação posterior.
- Histórico real para “mais pedidos da semana”. Sem fonte, usar “seleção Libélula”, sem alegação de popularidade.
- Associação de família e conjunto deve ser sustentada por nomes/itens existentes. Não prometer componentes complementares se o catálogo só tiver conjunto completo.
- Preços públicos incluem mais de duas casas em alguns itens (ex.: 75.645 e 87.945). Os estudos usam `Intl.NumberFormat` sem alterar os dados. A implementação de compra precisará de regra de centavos única para não divergir entre card, total e WhatsApp.

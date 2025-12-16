# 🛍️ Loja Virtual de Lingerie

Sistema completo de e-commerce para revenda de lingerie com integração ao WhatsApp.

## 📦 Conteúdo do Projeto

- **lingerie-backend/** - Backend Flask com API REST
- **lingerie-frontend/** - Frontend React com interface moderna

## ⚙️ Configurações Atuais

- **WhatsApp:** 43996048712
- **Margem de Lucro:** 105%
- **8 produtos** de exemplo

## 🚀 Como Usar

### Backend (Flask)

1. Entre na pasta do backend:
```bash
cd lingerie-backend
```

2. Crie um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:
```bash
python setup_config.py
```

5. Inicie o servidor:
```bash
python src/main.py
```

O backend estará rodando em: `http://localhost:5001`

### Frontend (React)

1. Entre na pasta do frontend:
```bash
cd lingerie-frontend
```

2. Instale as dependências:
```bash
npm install
# ou
pnpm install
```

3. Configure a URL da API:
   - Edite o arquivo `src/App.jsx`
   - Altere a linha `const API_BASE_URL` para apontar para seu backend

4. Inicie o servidor de desenvolvimento:
```bash
npm run dev
# ou
pnpm run dev
```

5. Para build de produção:
```bash
npm run build
# ou
pnpm run build
```

## 🔧 Endpoints da API

### Produtos
- `GET /api/produtos` - Lista todos os produtos
- `GET /api/produtos/:id` - Busca produto por ID
- `GET /api/categorias` - Lista todas as categorias

### Scraper
- `POST /api/scraper/executar` - Executa o scraper e cria produtos de exemplo
- `GET /api/scraper/status` - Status do último scraping
- `GET /api/scraper/logs` - Logs de scraping

### Configuração
- `POST /api/config/setup` - Configura WhatsApp e margem de lucro
- `POST /api/config/limpar-produtos` - Deleta todos os produtos
- `POST /api/config/atualizar-produtos` - Atualiza links do WhatsApp

## 📱 Funcionalidades

### ✅ Implementadas
- Catálogo de produtos com filtros
- Sistema de busca
- Detalhes do produto com galeria de imagens
- Integração com WhatsApp
- Aplicação automática de margem de lucro
- Sistema de categorias
- Design responsivo (mobile e desktop)
- API REST completa

### 🔄 Para Implementar
- Scraper real do site da Caliente Lingerie
- Painel administrativo
- Sistema de favoritos
- Analytics de vendas
- Cupons de desconto

## 🎨 Tecnologias Utilizadas

### Backend
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-CORS 4.0.0
- SQLite (banco de dados)

### Frontend
- React 18
- React Router DOM
- TailwindCSS
- Vite

## 📝 Estrutura de Arquivos

### Backend
```
lingerie-backend/
├── src/
│   ├── models/
│   │   └── produto.py          # Modelos do banco de dados
│   ├── routes/
│   │   ├── produtos.py         # Rotas de produtos
│   │   ├── scraper.py          # Rotas do scraper
│   │   └── config.py           # Rotas de configuração
│   └── main.py                 # Arquivo principal do Flask
├── requirements.txt            # Dependências Python
└── setup_config.py            # Script de configuração inicial
```

### Frontend
```
lingerie-frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Cabeçalho
│   │   ├── Home.jsx            # Página inicial
│   │   ├── Catalogo.jsx        # Página de catálogo
│   │   ├── ProdutoDetalhes.jsx # Detalhes do produto
│   │   └── Footer.jsx          # Rodapé
│   └── App.jsx                 # Componente principal
├── index.html                  # HTML principal
└── package.json                # Dependências Node.js
```

## 🔐 Segurança

- CORS habilitado para comunicação frontend-backend
- Validação de dados nas rotas da API
- Sanitização de URLs e parâmetros

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique os logs do backend
- Verifique o console do navegador (F12)
- Teste as rotas da API usando curl ou Postman

## 📄 Licença

Este projeto foi desenvolvido para uso pessoal/comercial.

---

**Desenvolvido com ❤️ por Manus AI**


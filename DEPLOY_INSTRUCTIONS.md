# 📝 Instruções de Deploy - Loja de Lingerie

## 1️⃣ Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Nome do repositório: `loja-lingerie`
3. Descrição: "E-commerce completo de lingerie com Flask e React"
4. Marque como **Público** ou **Privado** (sua escolha)
5. **NÃO** inicialize com README, .gitignore ou licença
6. Clique em "Create repository"

## 2️⃣ Enviar Código para o GitHub

Depois de criar o repositório, execute estes comandos no terminal:

```bash
cd "C:\Users\Lucas\Documents\loja-lingerie-completa"
git remote add origin https://github.com/SEU-USUARIO/loja-lingerie.git
git branch -M main
git push -u origin main
```

**Substitua `SEU-USUARIO` pelo seu nome de usuário do GitHub!**

## 3️⃣ Deploy no Render (Backend)

### 3.1 Criar conta no Render
1. Acesse: https://render.com
2. Clique em "Get Started for Free"
3. Faça login com sua conta do GitHub

### 3.2 Criar Web Service para o Backend
1. No dashboard do Render, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub `loja-lingerie`
4. Configure:
   - **Name**: `loja-lingerie-backend`
   - **Region**: Oregon (US West) - mais próximo do Brasil
   - **Branch**: `main`
   - **Root Directory**: `lingerie-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT src.main:app`
   - **Instance Type**: `Free`

5. Clique em "Create Web Service"
6. **IMPORTANTE**: Anote a URL gerada (ex: `https://loja-lingerie-backend.onrender.com`)

### 3.3 Configurar Variáveis de Ambiente (Backend)
1. No painel do serviço criado, vá em "Environment"
2. Adicione:
   - `SECRET_KEY` = `sua-chave-secreta-aqui-123456`
   - `FLASK_ENV` = `production`

## 4️⃣ Deploy no Vercel (Frontend)

### 4.1 Criar conta no Vercel
1. Acesse: https://vercel.com
2. Clique em "Sign Up"
3. Faça login com sua conta do GitHub

### 4.2 Importar Projeto
1. No dashboard do Vercel, clique em "Add New..."
2. Selecione "Project"
3. Importe o repositório `loja-lingerie`
4. Configure:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `lingerie-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 4.3 Configurar Variável de Ambiente (Frontend)
1. Antes de fazer deploy, clique em "Environment Variables"
2. Adicione:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://loja-lingerie-backend.onrender.com/api`
   - (Use a URL do backend que você anotou no passo 3.2)

3. Clique em "Deploy"
4. Aguarde o build terminar (2-3 minutos)
5. **IMPORTANTE**: Anote a URL gerada (ex: `https://loja-lingerie.vercel.app`)

## 5️⃣ Configurar CORS (Backend)

Agora que você tem a URL do frontend, precisa atualizar o CORS:

1. No Render, vá no seu serviço de backend
2. Vá em "Environment"
3. Adicione a variável:
   - `FRONTEND_URL` = `https://loja-lingerie.vercel.app`
   - (Use a URL do frontend que você anotou no passo 4.3)

## 6️⃣ Testar a Aplicação

1. Acesse a URL do frontend: `https://loja-lingerie.vercel.app`
2. O site deve carregar normalmente
3. Se houver problemas:
   - Verifique os logs no Render (Backend)
   - Verifique os logs no Vercel (Frontend)
   - Abra o console do navegador (F12) para ver erros

## 🔄 Atualizações Futuras

Sempre que você fizer alterações no código:

```bash
cd "C:\Users\Lucas\Documents\loja-lingerie-completa"
git add .
git commit -m "Descrição das alterações"
git push
```

O Render e o Vercel farão o deploy automaticamente!

## 📱 URLs da Aplicação

Após o deploy, suas URLs serão:

- **Frontend**: https://loja-lingerie.vercel.app
- **Backend API**: https://loja-lingerie-backend.onrender.com/api
- **Admin Panel**: https://loja-lingerie.vercel.app/admin

## ⚠️ Importante - Banco de Dados

O Render usa armazenamento efêmero. Isso significa que:
- Os dados do SQLite serão perdidos quando o servidor reiniciar
- Para produção, considere usar PostgreSQL (Render oferece plano gratuito)

## 🆘 Problemas Comuns

### "Failed to fetch" ou "Network Error"
- Verifique se a variável `VITE_API_URL` está correta no Vercel
- Verifique se o backend está rodando no Render

### Backend demora para responder
- O plano gratuito do Render "dorme" após 15 minutos de inatividade
- A primeira requisição pode demorar 30-60 segundos

### Imagens não carregam
- Verifique se as URLs das imagens estão corretas
- Use URLs absolutas, não relativas

## 📞 Suporte

Se tiver problemas, verifique:
1. Logs do Render: https://dashboard.render.com
2. Logs do Vercel: https://vercel.com/dashboard
3. Console do navegador (F12)

---

**Desenvolvido com ❤️ por Manus AI**

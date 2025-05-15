# Guia Didático: Deploy Manual do Backend no Render

Olá! Conforme conversamos, preparei este guia passo a passo para ajudá-lo a fazer o deploy do `auth_service` e do banco de dados PostgreSQL manualmente na plataforma Render. Isso lhe dará um controle mais direto sobre o processo.

**Antes de começar:**
*   Certifique-se de que você tem uma conta no Render ([https://render.com/](https://render.com/)) e que está logado.
*   Tenha o código do projeto "Auge Invest" com o `render.yaml` corrigido (que também estou enviando) no seu repositório GitHub.

## Parte 1: Criando o Banco de Dados PostgreSQL no Render

1.  **Acesse o Dashboard do Render:** Após logar, você estará no seu dashboard.
2.  **Crie um Novo Banco de Dados:**
    *   Clique no botão "**New +**" (Novo).
    *   Selecione "**PostgreSQL**".
3.  **Configure seu Banco de Dados:**
    *   **Name (Nome):** Dê um nome para seu banco, por exemplo, `auge-auth-db` (o mesmo nome que usamos no `render.yaml` é uma boa prática, mas pode ser outro se preferir).
    *   **Region (Região):** Escolha uma região. "Frankfurt" é uma boa opção se você estiver na Europa ou se seus usuários estiverem lá. Caso contrário, escolha a mais próxima de você ou dos seus usuários.
    *   **PostgreSQL Version (Versão do PostgreSQL):** Selecione a versão `15` (ou a mais recente estável disponível).
    *   **Plan (Plano):** Selecione o plano "**Free**" para começar. Você sempre pode fazer upgrade depois.
    *   **IP Allow List (Lista de IPs Permitidos):** Para facilitar no início, você pode deixar em branco (o que permite acesso de qualquer IP) ou adicionar `0.0.0.0/0`. Para produção, você pode restringir isso depois.
4.  **Crie o Banco de Dados:**
    *   Clique em "**Create Database**".
    *   O Render começará a provisionar seu banco de dados. Isso pode levar alguns minutos.
5.  **Anote a URL de Conexão Interna:**
    *   Assim que o banco estiver "Available" (Disponível), vá para a página do seu banco de dados no Render.
    *   Na seção "Info" ou "Connect", você encontrará a "**Internal Connection String**" (ou "Internal Database URL"). Copie esta URL. Ela será algo como `postgresql://user:password@host:port/database_name`.
    *   **Guarde esta URL com segurança!** Você a usará para configurar o `auth_service`.

## Parte 2: Criando o Serviço Web para o `auth_service` no Render

1.  **Volte para o Dashboard do Render.**
2.  **Crie um Novo Serviço Web:**
    *   Clique no botão "**New +**" (Novo).
    *   Selecione "**Web Service**".
3.  **Conecte seu Repositório GitHub:**
    *   Escolha "**Build and deploy from a Git repository**".
    *   Se for a primeira vez, você precisará conectar sua conta GitHub ao Render e autorizar o acesso ao repositório `AugeCapital/Auge-Invest`.
    *   Selecione o repositório `AugeCapital/Auge-Invest` da lista.
4.  **Configure seu Serviço Web:**
    *   **Name (Nome):** Dê um nome para seu serviço, por exemplo, `auge-auth-service`.
    *   **Region (Região):** Idealmente, escolha a mesma região do seu banco de dados para menor latência.
    *   **Branch:** Selecione a branch do seu repositório que contém o código mais recente (geralmente `main` ou `master`).
    *   **Root Directory (Diretório Raiz):** **Muito importante!** Configure como `backend/auth_service`. Isso diz ao Render para procurar o código do `auth_service` nesta subpasta.
    *   **Environment (Ambiente):** Selecione "**Python**".
    *   **Build Command (Comando de Build):** Render geralmente detecta `requirements.txt`. O comando padrão `pip install -r requirements.txt` deve funcionar. Se precisar, pode ser `pip install --upgrade pip && pip install -r requirements.txt`.
    *   **Start Command (Comando de Início):** Use `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. A variável `$PORT` é fornecida pelo Render.
    *   **Plan (Plano):** Selecione o plano "**Free**".
5.  **Configurações Avançadas (Advanced Settings) - Variáveis de Ambiente:**
    *   Antes de criar o serviço, clique em "**Advanced**" ou procure a seção de "**Environment Variables**".
    *   Adicione as seguintes variáveis de ambiente:
        *   `PYTHON_VERSION`: `3.11.0` (ou a versão Python que estamos usando).
        *   `AUTH_DATABASE_URL`: Cole aqui a "**Internal Connection String**" do banco de dados PostgreSQL que você copiou na Parte 1, Passo 5.
        *   `AUTH_SECRET_KEY`: Clique em "**Generate**" para que o Render crie uma chave secreta segura para você, ou cole uma chave forte que você mesmo gerou (deve ser uma string longa e aleatória).
        *   `AUTH_ACCESS_TOKEN_EXPIRE_MINUTES`: `30` (ou o valor que definimos).
        *   (Opcional, mas recomendado para o futuro) `CORS_ORIGINS`: Se você já sabe a URL do seu frontend na Vercel (ex: `https://auge-invest.vercel.app`), adicione-a aqui. Se tiver múltiplas, separe por vírgula (ex: `https://auge-invest.vercel.app,http://localhost:3000`). Por enquanto, pode deixar em branco se o backend não estiver configurado para exigir CORS específico.
6.  **Crie o Serviço Web:**
    *   Clique em "**Create Web Service**".
    *   O Render começará o processo de build e deploy do seu `auth_service`. Você pode acompanhar os logs na página do serviço.
    *   Isso pode levar alguns minutos.
7.  **Verifique o Deploy e Obtenha a URL Pública:**
    *   Se o deploy for bem-sucedido, o status do serviço mudará para "Live" ou "Deployed".
    *   Na página do seu serviço web no Render, você encontrará a **URL pública** do seu `auth_service` (algo como `https://auge-auth-service.onrender.com`).
    *   Teste o endpoint de health check acessando `SUA_URL_PUBLICA/ping` no navegador. Você deve ver `{"message":"Auth Service is running!"}`.

## Parte 3: Atualizando o Frontend na Vercel

1.  **Copie a URL Pública do `auth_service`** que você obteve no Render.
2.  **Vá para o seu projeto na Vercel.**
3.  **Acesse as Configurações (Settings) do projeto.**
4.  **Vá para Variáveis de Ambiente (Environment Variables).**
5.  **Atualize (ou adicione, se usou um placeholder) a variável `NEXT_PUBLIC_API_URL`:**
    *   **Nome:** `NEXT_PUBLIC_API_URL`
    *   **Valor:** Cole a URL pública do seu `auth_service` no Render (ex: `https://auge-auth-service.onrender.com`).
6.  **Salve e faça Redeploy do seu projeto na Vercel** para que ele use a nova URL da API.

**Após esses passos:**
*   Seu `auth_service` estará rodando no Render e acessível publicamente.
*   Seu frontend na Vercel estará configurado para se comunicar com este `auth_service`.
*   Você poderá testar o fluxo de cadastro e login na sua aplicação "Auge Invest"!

Sei que são muitos passos, mas tente segui-los com calma. Se encontrar qualquer problema ou mensagem de erro em alguma etapa, me diga exatamente qual é a mensagem e em qual passo ocorreu, que eu te ajudo a resolver.

Boa sorte com o deploy! Estou aqui para ajudar.

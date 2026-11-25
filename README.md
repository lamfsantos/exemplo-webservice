# 🎬 Desafio Técnico Mobile: Catálogo de Obras & Avaliações

Bem-vindo ao desafio técnico prático de desenvolvimento mobile! Este projeto simula um teste real de contratação para uma vaga de **Desenvolvedor(a) Mobile (Flutter / Kotlin / React Native / Swift)**.

Você deverá construir um aplicativo conectado a uma API RESTful em produção para visualização de catálogo, avaliações colaborativas e gerenciamento de favoritos.

---

## 📌 1. Visão Geral do Desafio

O objetivo é desenvolver um aplicativo mobile fluido, bem arquitetado e resiliente que consuma os serviços fornecidos por esta API.

### 📱 Escopo do Aplicativo (Requisitos do App)
1. **Autenticação (Login):**
   - Tela de login com validação de campos (e-mail e senha).
   - Armazenamento seguro do token JWT (ex: `flutter_secure_storage`, `EncryptedSharedPreferences`, etc.).
   - Logout (limpeza do token e redirecionamento para tela de login).
2. **Catálogo de Obras (Home):**
   - Listagem paginada (Scroll infinito ou paginação por páginas).
   - Barra de busca textual por título (`search`).
   - Filtros rápidos por categoria (`category`: Ação, Ficção Científica, Animação, Drama, Aventura, Terror, Comédia, Séries).
   - Cada card deve exibir: Pôster da obra, Título, Ano, Categoria, Nota Média (`average_rating`) e ícone indicativo se está favoritado (`is_favorite`).
3. **Detalhes da Obra:**
   - Exibição em destaque do pôster em alta resolução, sinopse e nota média.
   - Botão interativo para favoritar / desfavoritar a obra em tempo real.
   - Lista das avaliações e comentários feitos por outros usuários/alunos.
   - Formulário para o próprio usuário enviar ou atualizar sua avaliação (nota de 1 a 5 estrelas e comentário opcional).
4. **Meus Favoritos:**
   - Aba ou tela dedicada listando apenas as obras favoritadas pelo usuário logado.
   - Possibilidade de remover dos favoritos diretamente por esta tela.
5. **Resiliência & UX:**
   - Estados bem definidos: **Carregando (Shimmer / Loading)**, **Vazio**, **Erro com botão de tentar novamente**.
   - Tratamento adequado de erros da API (401 Token Expirado, 404 Não Encontrado, 429 Muitas Requisições).

---

## 🔗 2. Acesso à API & Documentação Interativa (Swagger)

A API está em produção e disponibiliza uma interface interativa completa via Swagger UI:

- **URL Base:** `https://api-produtos-mobile.onrender.com/api/v1` *(também acessível diretamente na raiz)*
- **Swagger UI (Documentação Interativa):** `https://api-produtos-mobile.onrender.com/docs`
- **ReDoc (Documentação Alternativa):** `https://api-produtos-mobile.onrender.com/redoc`
- **Health Check:** `https://api-produtos-mobile.onrender.com/health`

> 💡 **Como testar pelo Swagger:**
> 1. Execute a rota `POST /auth/login` (ou crie um usuário em `POST /auth/register`).
> 2. Copie o valor retornado no campo `token`.
> 3. Clique no botão verde **Authorize** (no topo superior direito da página do Swagger).
> 4. Cole o token no campo de valor e clique em **Authorize**. Pronto! Todas as rotas autenticadas funcionarão diretamente pelo navegador.

---

## 🔑 3. Credenciais de Teste

Para agilizar o desenvolvimento, utilize a conta de testes compartilhada abaixo:

| E-mail | Senha | Perfil |
| :--- | :--- | :--- |
| `teste@app.com` | `123456` | Aluno Geral / Demonstração |
| `lucas@estudante.ifms.edu.br` | `123456` | Aluno 1 |
| `mariana@estudante.ifms.edu.br` | `123456` | Aluna 2 |
| `professor@ifms.edu.br` | `123456` | Docente |

---

## 📡 4. Especificação Técnica dos Endpoints

Todas as requisições autenticadas devem obrigatoriamente enviar o header HTTP:
```http
Authorization: Bearer <seu_token_jwt_aqui>
Content-Type: application/json
```

---

### 4.1. Verificação de Integridade (Health Check)
* **Rota:** `GET /health`
* **Autenticação:** Pública (Sem token).
* **Resposta de Sucesso (200 OK):**
```json
{
  "status": "ok"
}
```

---

### 4.2. Cadastro de Novo Aluno (Register)
* **Rota:** `POST /auth/register` (ou `POST /api/v1/auth/register`)
* **Autenticação:** Pública.
* **Corpo da Requisição (JSON):**
```json
{
  "name": "Maria Silva",
  "email": "maria@estudante.ifms.edu.br",
  "password": "senha_segura"
}
```
* **Resposta de Sucesso (201 Created):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 6,
    "name": "Maria Silva",
    "email": "maria@estudante.ifms.edu.br"
  }
}
```
* **Resposta de Erro (409 Conflict):**
```json
{
  "error": "E-mail já cadastrado no sistema"
}
```

---

### 4.3. Autenticação (Login)
* **Rota:** `POST /auth/login` (ou `POST /api/v1/auth/login`)
* **Autenticação:** Pública.
* **Corpo da Requisição (JSON):**
```json
{
  "email": "teste@app.com",
  "password": "123456"
}
```
* **Resposta de Sucesso (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "Aluno Teste (Geral)",
    "email": "teste@app.com"
  }
}
```
* **Resposta de Erro (401 Unauthorized):**
```json
{
  "error": "E-mail ou senha incorretos"
}
```

---

### 4.4. Perfil do Usuário & Auto-login
* **Rota:** `GET /auth/me` (ou `GET /api/v1/auth/me`)
* **Autenticação:** Obrigatória (`Bearer <token>`).
* **Objetivo:** Utilizada na inicialização do app (Splash Screen) para checar se o token salvo no `flutter_secure_storage` ainda é válido.
* **Resposta de Sucesso (200 OK):**
```json
{
  "id": 1,
  "name": "Aluno Teste (Geral)",
  "email": "teste@app.com"
}
```
* **Resposta se token expirado/inválido (401 Unauthorized):**
```json
{
  "error": "Token inválido ou expirado"
}
```

---

### 4.5. Listar Obras do Catálogo
* **Rota:** `GET /items` (ou `GET /api/v1/items`)
* **Autenticação:** Obrigatória (`Bearer <token>`).
* **Parâmetros de Consulta (Query Parameters):**
  * `page` *(inteiro, padrão: 1)*: Número da página atual.
  * `limit` *(inteiro, padrão: 10, máx: 50)*: Quantidade de itens por página.
  * `search` *(texto, opcional)*: Busca que contenha o texto no título (case-insensitive).
  * `category` *(texto, opcional)*: Filtro por categoria exata (`Ação`, `Drama`, `Animação`, etc.).
* **Exemplo de Chamada:** `GET /api/v1/items?page=1&limit=10&category=Ficção Científica&search=Matrix`
* **Resposta de Sucesso (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "title": "Matrix",
      "synopsis": "Um programador de computador descobre que a realidade que vive é uma simulação...",
      "category": "Ação",
      "release_year": 1999,
      "poster_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
      "created_at": "2026-11-25T01:00:00Z",
      "is_favorite": false,
      "average_rating": 4.8
    }
  ],
  "meta": {
    "current_page": 1,
    "last_page": 5,
    "total": 43,
    "limit": 10
  }
}
```

---

### 4.4. Detalhes de uma Obra & Avaliações
* **Rota:** `GET /items/{id}`
* **Autenticação:** Obrigatória (`Bearer <token>`).
* **Resposta de Sucesso (200 OK):**
```json
{
  "id": 1,
  "title": "Matrix",
  "synopsis": "Um programador de computador descobre que a realidade que vive é uma simulação...",
  "category": "Ação",
  "release_year": 1999,
  "poster_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
  "created_at": "2026-11-25T01:00:00Z",
  "is_favorite": true,
  "average_rating": 4.8,
  "reviews": [
    {
      "id": 15,
      "user_id": 3,
      "user_name": "Lucas Aluno",
      "rating": 5,
      "comment": "Um marco absoluto do cinema de ficção!",
      "created_at": "2026-11-25T01:15:00Z"
    }
  ]
}
```
* **Resposta de Erro (404 Not Found):**
```json
{
  "error": "Obra não encontrada"
}
```

---

### 4.5. Avaliar Obra (Criar ou Atualizar Nota)
* **Rota:** `POST /items/{id}/reviews`
* **Autenticação:** Obrigatória (`Bearer <token>`).
* **Comportamento:** É idempotente por aluno. Se o mesmo aluno avaliar a obra novamente, a nota anterior é atualizada automaticamente (*upsert*).
* **Corpo da Requisição (JSON):**
```json
{
  "rating": 5,
  "comment": "Filme espetacular, atuações incríveis!"
}
```
*Validações:* `rating` deve ser um número inteiro de 1 a 5. `comment` é opcional.
* **Resposta de Sucesso (201 Created):**
```json
{
  "id": 20,
  "user_id": 1,
  "user_name": "Aluno Teste (Geral)",
  "rating": 5,
  "comment": "Filme espetacular, atuações incríveis!",
  "created_at": "2026-11-25T01:20:00Z"
}
```

---

### 4.6. Listar Meus Favoritos
* **Rota:** `GET /me/favorites`
* **Autenticação:** Obrigatória (`Bearer <token>`).
* **Resposta de Sucesso (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Matrix",
    "synopsis": "Um programador de computador descobre...",
    "category": "Ação",
    "release_year": 1999,
    "poster_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "created_at": "2026-11-25T01:00:00Z",
    "is_favorite": true,
    "average_rating": 4.8
  }
]
```

---

### 4.7. Adicionar aos Favoritos
* **Rota:** `POST /me/favorites/{id}`
* **Autenticação:** Obrigatória (`Bearer <token>`).
* **Comportamento:** Idempotente (se clicar no botão duas vezes rápido, não gera erro 500).
* **Resposta de Sucesso (200 OK):**
```json
{
  "message": "Obra adicionada aos favoritos com sucesso",
  "item_id": 1,
  "is_favorite": true
}
```

---

### 4.8. Remover dos Favoritos
* **Rota:** `DELETE /me/favorites/{id}`
* **Autenticação:** Obrigatória (`Bearer <token>`).
* **Resposta de Sucesso (204 No Content):** Corpo vazio.

---

## ⚠️ 5. Cuidados Operacionais & Dicas de Avaliação da Vaga

1. **Cold Start do Render (Plano Gratuito):**
   - O servidor no Render hiberna após 15 minutos sem chamadas. O primeiro acesso pode demorar entre 20 a 40 segundos para "acordar".
   - *Dica para o App:* Configure um tempo de `timeout` razoável no seu cliente HTTP (ex: 30 a 45 segundos no Dio/Http) e exiba um indicador de carregamento claro.
2. **Rate Limiting (Proteção contra loops):**
   - A API possui um limite de **100 requisições por minuto por IP**.
   - Cuidado com `ScrollController` ou listeners no Flutter/React Native para não disparar requisições em cascata desnecessárias. Se exceder, receberá status `429 Too Many Requests`.
3. **Imagens Reais (CDN TMDB):**
   - Todos os pôsteres são servidos diretamente pela CDN oficial do TMDB (`https://image.tmdb.org/t/p/w500/...`). Utilize componentes de cache de imagem no app (ex: `cached_network_image`) para garantir alta performance.

---

## 🛠️ 6. Guia para o Professor (Administração & Execução Local)

### 1. Criar as Tabelas no Supabase
Execute o conteúdo do arquivo [`schema.sql`](file:///home/furlan/Documentos/workspace/exemplo/schema.sql) no **SQL Editor** do painel do Supabase.

### 2. Configurar o arquivo `.env`
Crie um arquivo `.env` baseado no `.env.example`:
```env
SUPABASE_URL=https://atiuybalximxhqhzjxst.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sua_service_role_key
JWT_SECRET=sua_chave_secreta_jwt
PORT=10000
```

### 3. Rodar a Carga Inicial de Dados (`seed.py`)
```bash
python seed.py
```
Esse comando cadastra automaticamente as 45 obras completas e os usuários de teste no Supabase.

### 4. Rodar o Servidor Localmente
```bash
# Ativar o ambiente virtual
source .venv/bin/activate

# Iniciar o servidor com reload
uvicorn main:app --reload --port 10000
```

### 5. Deploy no Render
No painel do Render (ou via `render.yaml`), basta cadastrar as seguintes variáveis de ambiente em **Environment**:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `JWT_SECRET`
- `PYTHON_VERSION`: `3.11.0`

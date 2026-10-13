# 📱 Web Service Didático em FastAPI (Exemplo para Mobile)

Este repositório contém uma API REST simples em Python utilizando **FastAPI** com persistência de dados em arquivo **JSON**. Foi desenvolvida especialmente para que estudantes de **Desenvolvimento Mobile** possam realizar seus primeiros testes de comunicação HTTP/REST com clientes móveis (Android com Kotlin/Retrofit/Ktor, iOS com Swift/URLSession/Alamofire, Flutter com Dio/Http, ou React Native com Axios/Fetch).

---

## ⚡ 1. Executando Direto (Sem Instalar o Python)

Se você já possui o arquivo executável compilado (`servidor_produtos.exe` no Windows ou `servidor_produtos` no Linux):

1. Dê um **duplo clique** no executável ou execute-o pelo terminal:
   - **Windows:** `servidor_produtos.exe`
   - **Linux:** `./servidor_produtos`
2. O servidor iniciará imediatamente e criará automaticamente o arquivo `produtos.json` caso ele não exista na pasta.

---

## 🖥️ 2. Banner de Inicialização no Terminal

Ao iniciar o servidor, uma tela informativa é exibida no console com todos os links úteis e a detecção do seu IP local na rede Wi-Fi:

```text
======================================================================
  🚀 SERVIDOR DA API DE PRODUTOS INICIADO COM SUCESSO!
======================================================================
  📖 Documentação Swagger UI:  http://localhost:8000/docs
  📖 Documentação ReDoc:       http://localhost:8000/redoc
----------------------------------------------------------------------
  📲 Para Conectar seu App Mobile:
     • Emulador Android:        http://10.0.2.2:8000
     • Simulador iOS / Web:     http://localhost:8000
     • Aparelho Físico (Wi-Fi): http://192.168.1.15:8000
----------------------------------------------------------------------
  💾 Arquivo de Dados (JSON):  produtos.json
  💡 Pressione CTRL + C para encerrar o servidor a qualquer momento.
======================================================================
```

---

## 🛠️ 3. Como Gerar o Executável (.exe)

O projeto já inclui scripts de build prontos que utilizam o **PyInstaller** para empacotar a aplicação com todas as bibliotecas necessárias em um único arquivo independente.

### No Windows:
Basta dar um duplo clique no arquivo [`build.bat`](file:///home/furlan/Documentos/workspace/exemplo/build.bat) ou executar no Prompt de Comando / PowerShell:
```cmd
build.bat
```
O executável gerado estará na pasta `dist\servidor_produtos.exe`. Você pode enviar apenas esse `.exe` para os alunos!

### No Linux / macOS:
Execute o script [`build.sh`](file:///home/furlan/Documentos/workspace/exemplo/build.sh):
```bash
./build.sh
```
O binário gerado estará em `dist/servidor_produtos`.

---

## 🚀 4. Executando via Código Fonte Python

Caso prefira rodar ou editar o código-fonte:

1. **Abra a pasta do projeto no terminal:**
   ```bash
   cd exemplo
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o servidor:**
   ```bash
   python main.py
   ```
   *(ou `uvicorn main:app --reload --host 0.0.0.0 --port 8000`)*

---

## 📖 5. Documentação Automática Interativa (Swagger & ReDoc)

Com o servidor em execução, abra o navegador em:

- **Swagger UI (OpenAPI):** [http://localhost:8000/docs](http://localhost:8000/docs)
  - Permite testar as requisições (botão *Try it out*), enviar corpos JSON e ver as respostas em tempo real.
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **JSON OpenAPI Schema:** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 📲 6. Como Conectar a partir do Aplicativo Mobile

Ao programar o app mobile, **não use `localhost` na URL base** (exceto no simulador iOS), pois no celular `localhost` aponta para o próprio aparelho:

| Ambiente do App | URL Base recomendada | Observação |
| :--- | :--- | :--- |
| **Emulador Android (Android Studio)** | `http://10.0.2.2:8000` | O endereço `10.0.2.2` é o alias do Android Emulator para acessar o `localhost` do seu PC. |
| **Simulador iOS (Xcode)** | `http://localhost:8000` | Compartilha a mesma rede do computador. |
| **Dispositivo Físico (Android / iPhone)** | `http://<IP_DO_SEU_PC>:8000` | O celular e o computador devem estar na **mesma rede Wi-Fi**. O terminal exibe seu IP ao iniciar! |

> ⚠️ **Atenção (Android Cleartext Traffic):** Em versões recentes do Android, conexões `http://` locais precisam de `android:usesCleartextTraffic="true"` na tag `<application>` do arquivo `AndroidManifest.xml`.

---

## 📋 7. Endpoints da API

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Boas-vindas e resumo dos endpoints disponíveis |
| `GET, POST` | `/teste-formulario` | Rota didática para a turma de Web 1 testar envio de formulários HTML (GET ou POST) |
| `POST` | `/auth/cadastrar` | Cadastra um novo usuário com senha criptografada via BCrypt |
| `POST` | `/auth/login` | Login com envio de JSON (ideal para apps Mobile Flutter/React Native/Android/iOS) |
| `POST` | `/auth/token` | Login OAuth2 via formulário (compatível com o botão "Authorize" do Swagger UI) |
| `GET` | `/auth/me` | Rota protegida de exemplo: retorna os dados do usuário autenticado |
| `GET` | `/produtos` | Retorna a lista de produtos (aceita filtros: `?apenas_disponiveis=true` ou `?busca=termo`) |
| `GET` | `/produtos/{id}` | Retorna os detalhes de um produto específico |
| `POST` | `/produtos` | Cadastra um novo produto (cria ID sequencial automático) |
| `PUT` | `/produtos/{id}` | Atualiza campos de um produto existente |
| `DELETE` | `/produtos/{id}` | Remove um produto |

---

## 🧪 8. Teste de Formulários HTML (Turma de Web 1)

Os estudantes que estão aprendendo HTML básico podem testar o envio de formulários diretamente apontando o `action` para o servidor (seja rodando localmente ou no Render):

```html
<form action="https://seu-servidor.onrender.com/teste-formulario" method="POST">
    <label for="nome">Nome:</label>
    <input type="text" id="nome" name="nome" required>

    <label for="email">E-mail:</label>
    <input type="email" id="email" name="email" required>

    <button type="submit">Enviar Formulário</button>
</form>
```

- **Acesso direto no navegador (`GET /teste-formulario`):** Exibe um **laboratório interativo** com guia didático e código de exemplo pronto para copiar.
- **Ao submeter o formulário (`POST` ou `GET`):** O servidor gera uma página estilizada confirmando o recebimento dos dados, destacando quais atributos `name` foram recebidos e os valores digitados.
- **Suporte a Redirecionamento:** Se o aluno incluir `<input type="hidden" name="_redirect" value="https://exemplo.com">`, o servidor detecta a URL de destino e disponibiliza o redirecionamento.

---

## 📝 8. Exemplos de Payloads JSON

### Criando um Produto (`POST /produtos`)
**Corpo da Requisição (JSON):**
```json
{
  "nome": "Teclado Mecânico RGB",
  "preco": 349.90,
  "descricao": "Switches azuis, padrão ABNT2, cabo removível",
  "disponivel": true
}
```

**Resposta (`201 Created`):**
```json
{
  "id": 5,
  "nome": "Teclado Mecânico RGB",
  "preco": 349.90,
  "descricao": "Switches azuis, padrão ABNT2, cabo removível",
  "disponivel": true
}
```

---

### Atualizando um Produto (`PUT /produtos/{id}`)
**Corpo da Requisição (JSON):**
```json
{
  "preco": 299.90,
  "disponivel": false
}
```

---

### Resposta de Erro (`404 Not Found`)
```json
{
  "detail": "Produto com ID 999 não encontrado."
}
```

---

---

## 🔐 9. Sistema de Autenticação com JWT

A API inclui um sistema completo de controle de acesso baseado em **JSON Web Tokens (JWT)** e senhas criptografadas com **BCrypt**:

### 👤 Usuários Padrão para Testes Rápidos
Caso o arquivo `usuarios.json` não exista, ele será criado automaticamente com as contas:
- **Admin:** Usuário `admin` | Senha: `admin123`
- **Aluno:** Usuário `aluno` | Senha: `123456`

### 📝 Cadastro de Novos Usuários (`POST /auth/cadastrar`)
**Corpo da Requisição (JSON):**
```json
{
  "username": "meu_usuario",
  "senha": "minhasenhaforte",
  "nome": "Meu Nome Completo"
}
```
**Resposta (`201 Created`):**
```json
{
  "id": 3,
  "username": "meu_usuario",
  "nome": "Meu Nome Completo"
}
```

### 🔑 Login nos Aplicativos Mobile & Web (`POST /auth/login`)
Envie os dados como JSON:
```json
{
  "username": "aluno",
  "senha": "123456"
}
```
**Resposta (`200 OK`):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 🔒 Login no Swagger UI (`POST /auth/token`)
- No navegador ([http://localhost:8000/docs](http://localhost:8000/docs)), clique no botão verde **Authorize** (cadeado).
- Digite `aluno` e `123456`.
- Todas as rotas testadas no Swagger passarão a incluir o cabeçalho `Authorization: Bearer <token>` automaticamente!

### 🛡️ Como Proteger Rotas em Aula (Passo a Passo)
Nenhuma rota de produtos vem protegida por padrão para não quebrar testes iniciais. Para proteger qualquer rota existente durante a aula (ex: `POST /produtos`), basta adicionar a dependência `Depends(obter_usuario_atual)`:

```python
from fastapi import Depends
from auth import obter_usuario_atual
from models import Usuario

@app.post("/produtos", response_model=Produto, status_code=status.HTTP_201_CREATED)
def criar_produto(
    novo_produto: ProdutoCreate, 
    usuario_logado: Usuario = Depends(obter_usuario_atual)  # <-- BASTA ADICIONAR ESTA LINHA!
):
    print(f"Produto cadastrado por: {usuario_logado.username}")
    return db.criar_produto(novo_produto)
```

---

## 📁 10. Estrutura do Projeto

```
exemplo/
├── main.py             # Rotas da API, configurações de CORS, banner e entrypoint
├── auth.py             # Lógica JWT, hash bcrypt, dependência de autenticação e rotas /auth
├── database.py         # Leitura, escrita e persistência nos arquivos JSON (produtos e usuários)
├── models.py           # Modelos de validação Pydantic (produtos, usuários, login e tokens)
├── produtos.json       # Base de dados de produtos em formato JSON
├── usuarios.json       # Base de dados de usuários em formato JSON (senhas em hash bcrypt)
├── formulario.py       # Módulo para suporte a testes práticos de formulários Web 1
├── requirements.txt    # Dependências do projeto (FastAPI, PyJWT, bcrypt, python-multipart, etc.)
├── build.bat           # Script de geração do .exe para Windows
├── build.sh            # Script de geração de executável para Linux/macOS
├── dist/               # Pasta onde o executável final compilado é gerado
└── README.md           # Guia de uso e dicas para desenvolvimento mobile
```

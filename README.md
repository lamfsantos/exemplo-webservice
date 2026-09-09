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
| `GET` | `/produtos` | Retorna a lista de produtos (aceita filtros: `?apenas_disponiveis=true` ou `?busca=termo`) |
| `GET` | `/produtos/{id}` | Retorna os detalhes de um produto específico |
| `POST` | `/produtos` | Cadastra um novo produto (cria ID sequencial automático) |
| `PUT` | `/produtos/{id}` | Atualiza campos de um produto existente |
| `DELETE` | `/produtos/{id}` | Remove um produto |

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

## 📁 9. Estrutura do Projeto

```
exemplo/
├── main.py             # Rotas da API, configurações de CORS, banner e entrypoint
├── database.py         # Leitura, escrita e persistência no arquivo JSON (suporte a standalone/frozen)
├── models.py           # Modelos de validação Pydantic (schemas da API)
├── produtos.json       # Base de dados em formato JSON
├── requirements.txt    # Dependências do projeto (FastAPI, Uvicorn, Pydantic, PyInstaller)
├── build.bat           # Script de geração do .exe para Windows
├── build.sh            # Script de geração de executável para Linux/macOS
├── dist/               # Pasta onde o executável final compilado é gerado
└── README.md           # Guia de uso e dicas para desenvolvimento mobile
```

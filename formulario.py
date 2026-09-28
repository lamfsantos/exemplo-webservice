"""
Módulo para suporte a testes práticos de formulários HTML para turmas de Web 1.
Permite aos estudantes testarem o envio de dados via GET e POST sem precisarem
implementar lógica de backend.
"""

import html
import json
import urllib.parse
from datetime import datetime
from typing import Any, Dict, List, Tuple
from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

formulario_router = APIRouter(
    tags=["Web 1 - Formulários"],
)


async def extrair_dados_requisicao(request: Request) -> Tuple[Dict[str, Any], str, str]:
    """
    Extrai parâmetros de query (GET) ou formulário/JSON (POST).
    Retorna uma tupla: (dados, metodo, content_type)
    """
    metodo = request.method.upper()
    content_type = request.headers.get("content-type", "").lower()
    dados: Dict[str, Any] = {}

    if metodo == "GET":
        for key in request.query_params.keys():
            valores = request.query_params.getlist(key)
            dados[key] = valores[0] if len(valores) == 1 else valores
        return dados, metodo, "application/x-www-form-urlencoded (URL Query String)"

    # Se for POST / PUT / etc.
    if "application/json" in content_type:
        try:
            dados = await request.json()
        except Exception:
            dados = {"erro": "JSON inválido enviado no corpo da requisição."}
        return dados, metodo, content_type

    # Tenta ler multipart ou urlencoded usando request.form()
    form_lido = False
    try:
        form_data = await request.form()
        for key in form_data.keys():
            valores = form_data.getlist(key)
            parsed_vals = []
            for val in valores:
                if hasattr(val, "filename"):
                    parsed_vals.append(f"📁 [Arquivo: {val.filename} ({getattr(val, 'content_type', 'binário')})]")
                else:
                    parsed_vals.append(str(val))
            dados[key] = parsed_vals[0] if len(parsed_vals) == 1 else parsed_vals
        form_lido = True
    except Exception:
        form_lido = False

    # Fallback caso python-multipart não esteja instalado para x-www-form-urlencoded
    if not form_lido or (not dados and "application/x-www-form-urlencoded" in content_type):
        body = await request.body()
        if body:
            body_str = body.decode("utf-8", errors="replace")
            qs_dict = urllib.parse.parse_qs(body_str, keep_blank_values=True)
            for k, v in qs_dict.items():
                dados[k] = v[0] if len(v) == 1 else v

    return dados, metodo, content_type or "application/x-www-form-urlencoded"


def obter_estilos_css() -> str:
    return """
    :root {
        --primary: #4f46e5;
        --primary-hover: #4338ca;
        --primary-light: #e0e7ff;
        --bg-color: #f8fafc;
        --card-bg: #ffffff;
        --text-main: #0f172a;
        --text-muted: #64748b;
        --border-color: #e2e8f0;
        --success: #10b981;
        --success-bg: #ecfdf5;
        --warning: #f59e0b;
        --warning-bg: #fffbeb;
        --radius: 12px;
        --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.07), 0 2px 4px -2px rgb(0 0 0 / 0.07);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    }

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        background-color: var(--bg-color);
        color: var(--text-main);
        line-height: 1.6;
        padding: 24px 16px;
    }

    .container {
        max-width: 860px;
        margin: 0 auto;
    }

    .header-bar {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        border-radius: var(--radius);
        padding: 28px 24px;
        margin-bottom: 24px;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }

    .header-bar h1 {
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .header-bar p {
        font-size: 0.95rem;
        opacity: 0.9;
        max-width: 650px;
    }

    .badge-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(4px);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }

    .card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: var(--shadow);
    }

    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--text-main);
    }

    .status-banner {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px;
        border-radius: var(--radius);
        margin-bottom: 20px;
    }

    .status-banner.success {
        background-color: var(--success-bg);
        border: 1px solid #a7f3d0;
        color: #065f46;
    }

    .status-icon {
        font-size: 2rem;
        line-height: 1;
    }

    .status-text h2 {
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 2px;
    }

    .status-text p {
        font-size: 0.9rem;
        opacity: 0.85;
    }

    .method-badge {
        display: inline-flex;
        align-items: center;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 4px 10px;
        border-radius: 6px;
        letter-spacing: 0.05em;
    }

    .method-post {
        background-color: #dbeafe;
        color: #1e40af;
        border: 1px solid #bfdbfe;
    }

    .method-get {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }

    .didactic-box {
        background-color: #f8fafc;
        border-left: 4px solid var(--primary);
        padding: 14px 18px;
        border-radius: 0 var(--radius) var(--radius) 0;
        margin: 16px 0;
        font-size: 0.92rem;
        color: #334155;
    }

    .didactic-box strong {
        color: var(--primary);
    }

    .data-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 12px;
        font-size: 0.95rem;
    }

    .data-table th, .data-table td {
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid var(--border-color);
    }

    .data-table th {
        background-color: #f8fafc;
        color: var(--text-muted);
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .data-table tr:last-child td {
        border-bottom: none;
    }

    .data-table tr:hover td {
        background-color: #f8fafc;
    }

    .field-name {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-weight: 600;
        color: #db2777;
        background-color: #fdf2f8;
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid #fbcfe8;
        display: inline-block;
    }

    .field-value {
        font-weight: 500;
        word-break: break-word;
    }

    .empty-state {
        text-align: center;
        padding: 32px 16px;
        color: var(--text-muted);
    }

    .empty-state-icon {
        font-size: 2.5rem;
        margin-bottom: 12px;
    }

    .btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: var(--primary);
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        border: none;
        cursor: pointer;
        transition: background-color 0.15s ease;
    }

    .btn:hover {
        background-color: var(--primary-hover);
    }

    .btn-secondary {
        background-color: #e2e8f0;
        color: #334155;
    }

    .btn-secondary:hover {
        background-color: #cbd5e1;
    }

    .button-group {
        display: flex;
        gap: 12px;
        margin-top: 20px;
        flex-wrap: wrap;
    }

    /* Formulário interativo de teste */
    .form-group {
        margin-bottom: 16px;
    }

    .form-group label {
        display: block;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 6px;
        color: #334155;
    }

    .form-group input[type="text"],
    .form-group input[type="email"],
    .form-group select,
    .form-group textarea {
        width: 100%;
        padding: 10px 12px;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        font-size: 0.95rem;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
        background-color: #fff;
    }

    .form-group input:focus,
    .form-group select:focus,
    .form-group textarea:focus {
        outline: none;
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
    }

    .radio-checkbox-group {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        margin-top: 6px;
    }

    .radio-checkbox-label {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-weight: 400;
        cursor: pointer;
    }

    /* Código syntax */
    pre.code-block {
        background: #1e293b;
        color: #f8fafc;
        padding: 16px;
        border-radius: 8px;
        overflow-x: auto;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.88rem;
        position: relative;
    }

    details {
        margin-top: 16px;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 12px 16px;
        background: #fafafa;
    }

    details summary {
        font-weight: 600;
        cursor: pointer;
        color: var(--text-muted);
        outline: none;
    }

    .copy-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(255, 255, 255, 0.15);
        color: white;
        border: none;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        cursor: pointer;
    }
    .copy-btn:hover {
        background: rgba(255, 255, 255, 0.25);
    }

    footer {
        text-align: center;
        margin-top: 32px;
        font-size: 0.85rem;
        color: var(--text-muted);
    }
    """


def renderizar_pagina_resultado(
    request: Request,
    dados: Dict[str, Any],
    metodo: str,
    content_type: str,
    url_base: str
) -> str:
    """Renderiza a página amigável com a visualização dos dados recebidos."""
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    qtd_campos = len(dados)

    metodo_class = "method-post" if metodo == "POST" else "method-get"
    metodo_desc = (
        "Enviado no corpo da requisição (HTTP Body). Os dados não ficam expostos na URL."
        if metodo == "POST"
        else "Enviado através da URL (Query String). Observe os dados anexados na barra de endereços do seu navegador!"
    )

    linhas_tabela = ""
    if dados:
        for campo, valor in dados.items():
            campo_escaped = html.escape(str(campo))
            if isinstance(valor, list):
                # Se for lista (ex: múltiplos checkboxes marcados)
                itens = "".join(f"<li>{html.escape(str(v))}</li>" for v in valor)
                valor_formatado = f"<ul style='margin-left: 18px; margin-top: 4px;'>{itens}</ul>"
            else:
                valor_formatado = html.escape(str(valor))

            linhas_tabela += f"""
            <tr>
                <td><span class="field-name">{campo_escaped}</span></td>
                <td><div class="field-value">{valor_formatado}</div></td>
            </tr>
            """
    else:
        linhas_tabela = """
        <tr>
            <td colspan="2">
                <div class="empty-state">
                    <div class="empty-state-icon">⚠️</div>
                    <h3>Nenhum campo com atributo <code>name</code> foi recebido!</h3>
                    <p style="margin-top: 8px; font-size: 0.9rem;">
                        Em HTML, se uma tag <code>&lt;input&gt;</code>, <code>&lt;select&gt;</code> ou <code>&lt;textarea&gt;</code>
                        não tiver o atributo <code>name="exemplo"</code>, seu valor é <strong>descartado</strong> pelo navegador no envio.
                    </p>
                </div>
            </td>
        </tr>
        """

    json_bruto = html.escape(json.dumps(dados, indent=2, ensure_ascii=False))

    # Verifica se o usuário pediu redirecionamento
    aviso_redirect = ""
    if "_redirect" in dados and str(dados["_redirect"]).strip():
        url_red = html.escape(str(dados["_redirect"]).strip())
        aviso_redirect = f"""
        <div class="didactic-box" style="border-left-color: #10b981; background: #ecfdf5;">
            <strong>🔗 Parâmetro de Redirecionamento Detectado (_redirect):</strong><br>
            Você incluiu o campo <code>_redirect</code> apontando para <a href="{url_red}" target="_blank">{url_red}</a>.
            <div style="margin-top: 8px;">
                <a href="{url_red}" class="btn" style="padding: 6px 12px; font-size: 0.85rem;">Ir para página de destino →</a>
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulário Recebido com Sucesso! - Web 1</title>
    <style>{obter_estilos_css()}</style>
</head>
<body>
    <div class="container">
        <header class="header-bar">
            <span class="badge-tag">Desenvolvimento Web 1 • Laboratório de Formulários</span>
            <h1>🎉 Formulário Recebido com Sucesso!</h1>
            <p>Seus dados foram processados pelo servidor web. Veja abaixo como o backend enxergou as informações enviadas pelo seu HTML.</p>
        </header>

        <div class="status-banner success">
            <div class="status-icon">✅</div>
            <div class="status-text">
                <h2>Envio Concluído (Código HTTP 200 OK)</h2>
                <p>O navegador enviou com sucesso os dados utilizando o método <span class="method-badge {metodo_class}">{metodo}</span>.</p>
            </div>
        </div>

        {aviso_redirect}

        <div class="card">
            <div class="card-title">
                <span>📋 Dados Recebidos pelo Servidor</span>
                <span style="font-size: 0.85rem; font-weight: normal; color: var(--text-muted); margin-left: auto;">
                    {qtd_campos} campo(s) identificado(s)
                </span>
            </div>

            <div class="didactic-box">
                <strong>💡 Conceito Web 1:</strong> O método utilizado foi <strong>{metodo}</strong>. {metodo_desc}
                <br>
                Cada linha abaixo corresponde a um elemento no seu formulário que possuía o atributo <code>name="..."</code>.
            </div>

            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 35%;">Atributo name (Campo)</th>
                        <th>Valor Recebido (value)</th>
                    </tr>
                </thead>
                <tbody>
                    {linhas_tabela}
                </tbody>
            </table>

            <div class="button-group">
                <button onclick="window.history.back()" class="btn">
                    ← Voltar para o Formulário
                </button>
                <a href="{url_base}/teste-formulario" class="btn btn-secondary">
                    📖 Abrir Guia & Exemplos de HTML
                </a>
            </div>
        </div>

        <div class="card">
            <div class="card-title">
                <span>🔍 Detalhes Técnicos da Requisição</span>
            </div>
            <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 12px;">
                Informações de cabeçalho enviadas automaticamente pelo seu navegador (User-Agent, Tipo de Mídia, etc.):
            </p>
            <ul style="font-size: 0.88rem; list-style: none; line-height: 1.8;">
                <li><strong>Método HTTP:</strong> {metodo}</li>
                <li><strong>Content-Type:</strong> {html.escape(content_type)}</li>
                <li><strong>Data/Hora do Recebimento:</strong> {agora}</li>
                <li><strong>Navegador / Cliente:</strong> {html.escape(request.headers.get("user-agent", "Desconhecido"))}</li>
            </ul>

            <details>
                <summary>Ver representação em formato JSON bruto</summary>
                <div style="position: relative; margin-top: 10px;">
                    <pre class="code-block"><code>{json_bruto}</code></pre>
                </div>
            </details>
        </div>

        <footer>
            Servidor de Testes Web 1 • Exemplo WebService • Hospedado no Render
        </footer>
    </div>
</body>
</html>
"""


def renderizar_pagina_guia(request: Request, url_completa: str) -> str:
    """Renderiza a página interativa de instruções e playground para os alunos de Web 1."""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laboratório de Formulários HTML - Web 1</title>
    <style>{obter_estilos_css()}</style>
</head>
<body>
    <div class="container">
        <header class="header-bar">
            <span class="badge-tag">Turma de Desenvolvimento Web 1</span>
            <h1>🧪 Laboratório de Formulários HTML</h1>
            <p>Aprenda na prática como os dados saem do seu formulário HTML e chegam a um servidor web real na nuvem.</p>
        </header>

        <div class="card">
            <div class="card-title">
                <span>🚀 Como Usar no Seu Código HTML</span>
            </div>
            <p style="font-size: 0.95rem; margin-bottom: 16px;">
                Para conectar o seu formulário a este servidor, basta configurar a tag <code>&lt;form&gt;</code> com a URL de destino no atributo <code>action</code>:
            </p>

            <div style="position: relative;">
                <button class="copy-btn" onclick="copiarCodigo('codigo-exemplo')">Copiar HTML</button>
                <pre class="code-block" id="codigo-exemplo"><code>&lt;!-- Exemplo para você colar no seu arquivo HTML --&gt;
&lt;form action="{url_completa}" method="POST"&gt;
    &lt;label for="nome"&gt;Nome:&lt;/label&gt;
    &lt;input type="text" id="nome" name="nome" placeholder="Seu nome completo" required&gt;

    &lt;label for="email"&gt;E-mail:&lt;/label&gt;
    &lt;input type="email" id="email" name="email" placeholder="seu@email.com" required&gt;

    &lt;label for="curso"&gt;Curso:&lt;/label&gt;
    &lt;select id="curso" name="curso"&gt;
        &lt;option value="Web 1"&gt;Desenvolvimento Web 1&lt;/option&gt;
        &lt;option value="Mobile"&gt;Desenvolvimento Mobile&lt;/option&gt;
        &lt;option value="Banco de Dados"&gt;Banco de Dados&lt;/option&gt;
    &lt;/select&gt;

    &lt;label for="comentarios"&gt;Mensagem:&lt;/label&gt;
    &lt;textarea id="comentarios" name="comentarios" rows="3"&gt;&lt;/textarea&gt;

    &lt;button type="submit"&gt;Enviar Formulário&lt;/button&gt;
&lt;/form&gt;</code></pre>
            </div>

            <div class="didactic-box">
                <strong>📌 Regras de Ouro do HTML para Formulários:</strong>
                <ul style="margin-left: 20px; margin-top: 6px; line-height: 1.7;">
                    <li><strong>Atributo <code>action</code>:</strong> URL do servidor para onde o formulário é enviado (<code>{url_completa}</code>).</li>
                    <li><strong>Atributo <code>method</code>:</strong> Use <code>POST</code> (recomendado para formulários de cadastro) ou <code>GET</code> (adiciona os dados na URL).</li>
                    <li><strong>Atributo <code>name</code>:</strong> OBRIGATÓRIO em cada campo! Sem o <code>name</code>, o navegador simplesmente NÃO envia o valor para o servidor.</li>
                    <li><strong>Botão de Envio:</strong> Deve ser <code>&lt;button type="submit"&gt;</code> ou <code>&lt;input type="submit"&gt;</code>.</li>
                </ul>
            </div>
        </div>

        <div class="card">
            <div class="card-title">
                <span>⚡ Teste Agora Mesmo (Playground Interativo)</span>
            </div>
            <p style="font-size: 0.95rem; margin-bottom: 20px; color: var(--text-muted);">
                Preencha os campos abaixo e clique em Enviar para testar a comunicação imediata com o servidor:
            </p>

            <form action="{url_completa}" method="POST" id="form-teste">
                <div class="form-group">
                    <label>Método de Envio HTTP:</label>
                    <div class="radio-checkbox-group">
                        <label class="radio-checkbox-label">
                            <input type="radio" name="_metodo_escolhido" value="POST" checked onchange="document.getElementById('form-teste').method = 'POST'">
                            <strong>POST</strong> (dados via corpo da requisição)
                        </label>
                        <label class="radio-checkbox-label">
                            <input type="radio" name="_metodo_escolhido" value="GET" onchange="document.getElementById('form-teste').method = 'GET'">
                            <strong>GET</strong> (dados anexados na barra de URL)
                        </label>
                    </div>
                </div>

                <div class="form-group">
                    <label for="campo-nome">Nome do Aluno(a):</label>
                    <input type="text" id="campo-nome" name="nome" placeholder="Ex: Maria Eduarda" required>
                </div>

                <div class="form-group">
                    <label for="campo-email">E-mail Institucional ou Pessoal:</label>
                    <input type="email" id="campo-email" name="email" placeholder="aluno@instituto.edu.br" required>
                </div>

                <div class="form-group">
                    <label for="campo-turma">Turma / Matéria:</label>
                    <select id="campo-turma" name="turma">
                        <option value="Web 1 - Matutino">Web 1 - Matutino</option>
                        <option value="Web 1 - Vespertino">Web 1 - Vespertino</option>
                        <option value="Web 1 - Noturno">Web 1 - Noturno</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Quais tecnologias você já praticou?</label>
                    <div class="radio-checkbox-group">
                        <label class="radio-checkbox-label">
                            <input type="checkbox" name="tecnologias" value="HTML5" checked> HTML5
                        </label>
                        <label class="radio-checkbox-label">
                            <input type="checkbox" name="tecnologias" value="CSS3" checked> CSS3
                        </label>
                        <label class="radio-checkbox-label">
                            <input type="checkbox" name="tecnologias" value="JavaScript"> JavaScript
                        </label>
                    </div>
                </div>

                <div class="form-group">
                    <label for="campo-mensagem">Dúvida ou Comentário sobre a aula:</label>
                    <textarea id="campo-mensagem" name="mensagem" rows="3" placeholder="Escreva algo para ver como o texto viaja até o backend..."></textarea>
                </div>

                <button type="submit" class="btn" style="width: 100%; justify-content: center; padding: 12px;">
                    🚀 Enviar Dados para o Servidor
                </button>
            </form>
        </div>

        <div class="card">
            <div class="card-title">
                <span>🔀 Dica Avançada: Como Fazer Redirecionamento Automático?</span>
            </div>
            <p style="font-size: 0.92rem; color: #334155; line-height: 1.6;">
                Se você quiser que o formulário redirecione para outra página após o envio, basta adicionar um campo oculto (<code>&lt;input type="hidden"&gt;</code>) com o nome <code>_redirect</code>:
            </p>
            <div style="position: relative; margin-top: 10px;">
                <pre class="code-block"><code>&lt;input type="hidden" name="_redirect" value="https://sua-pagina-de-obrigado.html"&gt;</code></pre>
            </div>
        </div>

        <footer>
            Servidor de Testes Web 1 • Exemplo WebService • Hospedado no Render
        </footer>
    </div>

    <script>
    function copiarCodigo(id) {{
        const elemento = document.getElementById(id);
        if (!elemento) return;
        const texto = elemento.innerText;
        navigator.clipboard.writeText(texto).then(() => {{
            alert('Código HTML copiado com sucesso! Agora é só colar no seu editor.');
        }}).catch(() => {{
            prompt('Copie o código abaixo:', texto);
        }});
    }}
    </script>
</body>
</html>
"""


@formulario_router.api_route(
    "/teste-formulario",
    methods=["GET", "POST"],
    summary="Receber e exibir dados de formulários HTML (Turma de Web 1)",
    description=(
        "Endpoint didático para estudantes de Web 1 testarem envios de formulários HTML (GET ou POST). "
        "Apresenta uma página de confirmação visual com todos os campos recebidos, sem exigir backend dos alunos."
    ),
    response_class=HTMLResponse
)
@formulario_router.api_route(
    "/formulario",
    methods=["GET", "POST"],
    include_in_schema=False
)
async def processar_teste_formulario(request: Request):
    dados, metodo, content_type = await extrair_dados_requisicao(request)
    
    # URL base para links
    base_url = str(request.base_url).rstrip("/")
    url_completa = f"{base_url}/teste-formulario"

    # Se a requisição pedir JSON explicitamente (via header Accept ou parâmetro ?formato=json)
    if "application/json" in request.headers.get("accept", "") or request.query_params.get("formato") == "json":
        return JSONResponse({
            "sucesso": True,
            "metodo": metodo,
            "total_campos": len(dados),
            "dados": dados,
            "mensagem": "Formulário recebido com sucesso pelo servidor!"
        })

    # Se for um GET sem nenhum parâmetro de formulário na URL, exibe o Guia / Playground
    if metodo == "GET" and not request.query_params:
        return HTMLResponse(
            content=renderizar_pagina_guia(request, url_completa),
            status_code=200
        )

    # Se o usuário especificou redirecionamento com parâmetro de URL redirect_now=true e passou _redirect
    if "_redirect" in dados and request.query_params.get("redirect_now") == "true":
        url_destino = str(dados["_redirect"]).strip()
        if url_destino.startswith("http://") or url_destino.startswith("https://") or url_destino.startswith("/"):
            return RedirectResponse(url=url_destino, status_code=303)

    # Exibe a página com o resultado dos dados recebidos
    html_resposta = renderizar_pagina_resultado(
        request=request,
        dados=dados,
        metodo=metodo,
        content_type=content_type,
        url_base=base_url
    )
    return HTMLResponse(content=html_resposta, status_code=200)

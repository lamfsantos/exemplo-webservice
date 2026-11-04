import os
import requests

def enviar_notificacao():
    url_padrao = os.environ.get("API_URL", "http://localhost:8000")
    print("="*50)
    print(" 🚀 DISPARO DE NOTIFICAÇÃO PUSH (SIMULADA)")
    print("="*50)
    print(f"URL Base atual: {url_padrao}")
    nova_url = input("Pressione ENTER para manter ou digite a nova URL (ex: https://sua-api.onrender.com): ").strip()
    base_url = nova_url if nova_url else url_padrao
    base_url = base_url.rstrip("/")
    login_url = f"{base_url}/auth/login"
    url = f"{base_url}/notificacoes/enviar"

    print("\n🔐 Autenticação Requerida:")
    user_default = os.environ.get("AUTH_USER", "admin")
    senha_default = os.environ.get("AUTH_PASSWORD", "admin123")
    usuario = input(f"Usuário [{user_default}]: ").strip() or user_default
    senha = input(f"Senha [{senha_default}]: ").strip() or senha_default

    try:
        resp_login = requests.post(login_url, json={"username": usuario, "senha": senha})
        if resp_login.status_code != 200:
            print("\n❌ Falha na autenticação!")
            print(f"Status: {resp_login.status_code} - {resp_login.text}")
            return
        token = resp_login.json().get("access_token")
        print("✅ Autenticado com sucesso!")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO DE CONEXÃO!")
        print("O servidor FastAPI parece estar desligado. Certifique-se de iniciar o 'main.py' primeiro.")
        return

    titulo = input("\nDigite o Título da notificação: ")
    mensagem = input("Digite a Mensagem: ")
    
    payload = {
        "titulo": titulo,
        "mensagem": mensagem
    }
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            dados = response.json()
            print("\n✅ SUCESSO!")
            print(f"Detalhes: {dados['mensagem']}")
        else:
            print("\n❌ ERRO ao enviar notificação.")
            print(f"Status Code: {response.status_code}")
            print(f"Detalhes: {response.text}")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO DE CONEXÃO!")
        print("O servidor FastAPI parece estar desligado. Certifique-se de iniciar o 'main.py' primeiro.")

if __name__ == "__main__":
    enviar_notificacao()

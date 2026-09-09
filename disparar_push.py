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
    url = f"{base_url}/notificacoes/enviar"

    
    titulo = input("Digite o Título da notificação: ")
    mensagem = input("Digite a Mensagem: ")
    
    payload = {
        "titulo": titulo,
        "mensagem": mensagem
    }
    
    try:
        response = requests.post(url, json=payload)
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

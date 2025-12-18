import requests
import json

# URL do backend no Render
API_URL = "https://libelulavittage.onrender.com/api"

print("=" * 50)
print("POPULANDO BANCO DE DADOS COM PRODUTOS")
print("=" * 50)
print()

# 1. Configurar WhatsApp e margem de lucro
print("1. Configurando WhatsApp e margem de lucro...")
config_data = {
    "numero_whatsapp": "43996048712",
    "margem_lucro": 105
}

try:
    response = requests.post(f"{API_URL}/config/setup", json=config_data)
    if response.status_code == 200:
        print("   ✓ Configurações salvas com sucesso!")
    else:
        print(f"   ✗ Erro: {response.text}")
except Exception as e:
    print(f"   ✗ Erro: {e}")

print()

# 2. Executar scraper para criar produtos
print("2. Executando scraper (isso pode demorar alguns minutos)...")
print("   Aguarde...")

try:
    scraper_data = {"strategy": "sitemap"}
    response = requests.post(f"{API_URL}/scraper/executar", json=scraper_data)

    if response.status_code == 200:
        print("   ✓ Scraper iniciado!")
        print()

        # Acompanhar progresso
        import time
        while True:
            progress = requests.get(f"{API_URL}/scraper/progress")
            if progress.status_code == 200:
                data = progress.json()
                status = data.get('status')
                percentage = data.get('percentage', 0)
                message = data.get('message', '')

                print(f"\r   Progresso: {percentage}% - {message}", end='', flush=True)

                if status == 'completed':
                    print()
                    details = data.get('details', {})
                    print(f"\n   ✓ Concluído!")
                    print(f"   - Produtos novos: {details.get('produtos_novos', 0)}")
                    print(f"   - Produtos atualizados: {details.get('produtos_atualizados', 0)}")
                    print(f"   - Total: {details.get('total_encontrados', 0)}")
                    break
                elif status == 'error':
                    print(f"\n   ✗ Erro: {message}")
                    break

            time.sleep(2)
    else:
        print(f"   ✗ Erro ao iniciar scraper: {response.text}")
except Exception as e:
    print(f"   ✗ Erro: {e}")

print()
print("=" * 50)
print("PROCESSO CONCLUÍDO!")
print("=" * 50)
print()
print("Acesse: https://libelulavittage.vercel.app")
print()

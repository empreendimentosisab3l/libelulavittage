import requests

url = "https://calientelingerie.com.br/produto/2823474/17996842783"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Fetching {url}...")
response = requests.get(url, headers=headers)
with open('product_dump.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
print("Done.")

import requests

def inspect_sitemap_raw():
    url = 'https://calientelingerie.com.br/sitemap.xml'
    try:
        resp = requests.get(url, timeout=10)
        print(f"Status: {resp.status_code}")
        print("--- CONTENT START ---")
        print(resp.text[:1000]) # First 1000 chars
        print("--- CONTENT END ---")
        
        if '<lastmod>' in resp.text:
            print("FOUND: <lastmod> tag exists!")
        else:
            print("NOT FOUND: <lastmod> tag does not exist.")
            
    except Exception as e:
        print(e)

if __name__ == "__main__":
    inspect_sitemap_raw()

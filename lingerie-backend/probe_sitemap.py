import requests
import re
import xml.etree.ElementTree as ET

def extract_ids_from_sitemap():
    url = "https://calientelingerie.com.br/sitemap.xml"
    print(f"Fetching {url}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # The sitemap might be a sitemap index or a single sitemap
        # Let's inspect the content first
        print(f"Content start: {response.text[:200]}...")
        
        ids = set()
        
        # Simple regex extraction for now to test feasibility
        # URL pattern: https://calientelingerie.com.br/produto/{ID}/...
        
        # Regex to find product URLs and capture ID
        # Looking for /produto/(\d+)
        matches = re.findall(r'/produto/(\d+)', response.text)
        
        for match in matches:
            ids.add(match)
            
        print(f"Found {len(ids)} unique IDs.")
        print(f"Sample IDs: {list(ids)[:10]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_ids_from_sitemap()

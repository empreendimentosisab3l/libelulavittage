import requests
from bs4 import BeautifulSoup

url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    print(f"Fetching {url}...")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    print("Fetch successful.")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try to identify product containers
    print("\n--- Potential Product Containers (searching for 'product' or 'item') ---")
    potential_products = soup.find_all(lambda tag: tag.has_attr('class') and any('product' in c.lower() or 'item' in c.lower() for c in tag['class']))
    
    # List first 3 unique classes found that might be products
    seen_classes = set()
    count = 0
    for tag in potential_products:
        classes = tuple(tag['class'])
        if classes not in seen_classes:
            print(f"Tag: {tag.name}, Class: {classes}")
            # Print a bit of content to see if it looks like a product
            print(f"   Content snippet: {tag.get_text(strip=True)[:100]}...")
            seen_classes.add(classes)
            count += 1
            if count >= 5: break

    # Try to find prices
    print("\n--- Potential Prices (searching for 'price' or 'R$') ---")
    potential_prices = soup.find_all(string=lambda text: text and 'R$' in text)
    for i, price_text in enumerate(potential_prices[:5]):
        parent = price_text.parent
        print(f"Price found in <{parent.name} class='{parent.get('class', [])}'>: {price_text.strip()}")

    # Try to find images
    print("\n--- Potential Images ---")
    imgs = soup.find_all('img', limit=5)
    for img in imgs:
        print(f"Img src: {img.get('src', 'No src')}, Alt: {img.get('alt', 'No alt')}")

except Exception as e:
    print(f"Error: {e}")

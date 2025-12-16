def find_lines():
    target = "c:/Users/Lucas/Documents/loja-lingerie-completa/lingerie-backend/scripts_dump.txt"
    try:
        with open(target, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "ProdutoConteudoMixin =" in line or "ProdutoConteudoMixin =" in line:
                    print(f"Mixin Found at line {i+1}: {line.strip()}")
                if "carregarDadosCompletosAPI" in line:
                    print(f"Method Usage/Def at line {i+1}: {line.strip()}")
                if "acao:" in line and "produto" in line: # Potential API calls
                     pass # Too noisy
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_lines()

import sqlite3

def migrate_hash():
    db_path = "c:/Users/Lucas/Documents/loja-lingerie-completa/lingerie-backend/instance/lingerie_store.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(produtos)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'data_hash' not in columns:
            print("Adicionando coluna 'data_hash'...")
            cursor.execute("ALTER TABLE produtos ADD COLUMN data_hash TEXT")
            conn.commit()
            print("Coluna adicionada com sucesso.")
        else:
            print("Coluna 'data_hash' já existe.")
            
    except Exception as e:
        print(f"Erro na migração: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_hash()

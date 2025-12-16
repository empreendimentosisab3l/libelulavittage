import sqlite3

def migrate_db():
    db_path = 'c:/Users/Lucas/Documents/loja-lingerie-completa/lingerie-backend/instance/loja.db' # Assuming standard Flask structure, checking if exists
    
    # Check if instance folder exists, otherwise try logic from main.py
    import os
    if not os.path.exists(db_path):
        # Maybe it's in the root or src?
        # Let's check config, but standard is instance/loja.db usually if strictly following Flask
        # Or look at where the app initializes DB.
        # Given I can't check easily, I'll try the likely paths
        paths = [
            'c:/Users/Lucas/Documents/loja-lingerie-completa/lingerie-backend/instance/lingerie_store.db',
            'c:/Users/Lucas/Documents/loja-lingerie-completa/lingerie-backend/loja.db',
            'c:/Users/Lucas/Documents/loja-lingerie-completa/lingerie-backend/src/loja.db'
        ]
        
        found = False
        for p in paths:
            if os.path.exists(p):
                db_path = p
                found = True
                break
        
        if not found:
            print("Database file not found!")
            return

    print(f"Migrating {db_path}...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns exist
        cursor.execute("PRAGMA table_info(produtos)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'tamanhos' not in columns:
            print("Adding column 'tamanhos'...")
            cursor.execute("ALTER TABLE produtos ADD COLUMN tamanhos TEXT")
        else:
            print("Column 'tamanhos' already exists.")
            
        if 'cores' not in columns:
            print("Adding column 'cores'...")
            cursor.execute("ALTER TABLE produtos ADD COLUMN cores TEXT")
        else:
            print("Column 'cores' already exists.")
            
        conn.commit()
        conn.close()
        print("Migration successful.")
        
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate_db()

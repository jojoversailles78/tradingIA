with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Desactiver le scheduler automatique
old_startup = '''@app.on_event("startup")
async def startup():
    # Initialiser la base de donnees
    db_ok = _db.init_db()
    print("PostgreSQL:", "OK" if db_ok else "Fallback fichier local")
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=scheduler_thread, args=(loop,), daemon=True)
    t.start()
    print("6 agents demarres - refresh toutes les 15 minutes")'''

new_startup = '''@app.on_event("startup")
async def startup():
    # Initialiser la base de donnees
    db_ok = _db.init_db()
    print("PostgreSQL:", "OK" if db_ok else "Fallback fichier local")
    print("Agents prets - mode manuel uniquement")'''

c = c.replace(old_startup, new_startup)

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK - scheduler desactive')
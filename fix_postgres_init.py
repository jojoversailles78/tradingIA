with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_startup = '''@app.on_event("startup")
async def startup():
    print("Agents prets - scheduler desactive")'''

new_startup = '''@app.on_event("startup")
async def startup():
    from app import db as _db2
    db_ok = _db2.init_db()
    print("PostgreSQL:", "OK" if db_ok else "ERREUR - fallback fichier")
    print("Agents prets - scheduler desactive")'''

c = c.replace(old_startup, new_startup)

# Aussi corriger load_agents et save_agents
old_load = '''def load_agents():
    # Essayer PostgreSQL d abord
    db_state = _db.load_agents_db()'''

if old_load not in c:
    # Ajouter import db si absent
    if 'from app import db as _db' not in c:
        c = 'from app import db as _db\n' + c
    
    old_load2 = 'def load_agents():\n    if os.path.exists(AGENTS_FILE):'
    new_load2 = '''def load_agents():
    # Essayer PostgreSQL d abord
    try:
        db_state = _db.load_agents_db()
        if db_state:
            return db_state
    except Exception as e:
        print("DB load error:", e)
    # Fallback fichier local
    if os.path.exists(AGENTS_FILE):'''
    c = c.replace(old_load2, new_load2)

    old_save = 'def save_agents(state):\n    with open(AGENTS_FILE'
    new_save = '''def save_agents(state):
    # Sauvegarder dans PostgreSQL
    try:
        _db.save_agents_db(state)
    except Exception as e:
        print("DB save error:", e)
    # Backup fichier local
    try:
        with open(AGENTS_FILE'''
    
    # Trouver la fin de save_agents
    idx = c.find('def save_agents(state):\n    with open(AGENTS_FILE')
    if idx > 0:
        end_idx = c.find('\n\ndef ', idx)
        old_save_full = c[idx:end_idx]
        new_save_full = '''def save_agents(state):
    try:
        _db.save_agents_db(state)
    except Exception as e:
        print("DB save error:", e)
    try:
        with open(AGENTS_FILE, "w") as f:
            json.dump(state, f, indent=2, default=str)
    except:
        pass'''
        c = c.replace(old_save_full, new_save_full)

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK - PostgreSQL reinitialise')
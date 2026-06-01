# Lire main.py
with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Remplacer les routes HTML par une version qui lit les fichiers
import os

# Nouvelle approche : lire le fichier au moment de la requete
new_routes = '''
import os as _os

def _get_html_path(filename):
    # Chercher le fichier HTML dans plusieurs endroits possibles
    paths = [
        _os.path.join(_os.path.dirname(__file__), '..', '..', 'html', filename),
        _os.path.join(_os.path.dirname(__file__), '..', 'html', filename),
        _os.path.join('/app', 'html', filename),
        _os.path.join(_os.getcwd(), 'html', filename),
        filename,
    ]
    for p in paths:
        if _os.path.exists(p):
            return p
    return None

@app.get("/")
async def root():
    path = _get_html_path('index.html')
    if path:
        with open(path, encoding='utf-8') as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>TradingIA</h1><p><a href='/docs'>API Docs</a> | <a href='/agent'>Agent</a></p>")

@app.get("/agent")
async def agent_page():
    path = _get_html_path('agent.html')
    if path:
        with open(path, encoding='utf-8') as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>Agent IA</h1><p><a href='/'>Dashboard</a></p>")
'''

# Supprimer les anciennes routes
import re
c = re.sub(r'@app\.get\("/"\)\nasync def root\(\):[\s\S]*?(?=\n@app|\Z)', '', c)
c = re.sub(r'@app\.get\("/agent"\)\nasync def agent_page\(\):[\s\S]*?(?=\n@app|\Z)', '', c)

# Ajouter HTMLResponse dans les imports si pas present
if 'HTMLResponse' not in c:
    c = c.replace('from fastapi.responses import FileResponse', 'from fastapi.responses import FileResponse, HTMLResponse')

# Ajouter les nouvelles routes a la fin
c = c.rstrip() + '\n' + new_routes

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)

print('OK - routes HTML corrigees')
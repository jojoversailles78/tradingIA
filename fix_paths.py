import os

# Lire les fichiers HTML
with open('html/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

with open('html/agent.html', 'r', encoding='utf-8') as f:
    agent_html = f.read()

# Lire main.py
with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Remplacer les FileResponse par HTMLResponse
c = c.replace(
    "from fastapi.responses import FileResponse",
    "from fastapi.responses import FileResponse, HTMLResponse"
)

# Remplacer les routes qui servent les fichiers HTML
old_root = '''@app.get("/")
async def root():
    return FileResponse("html/index.html")'''

new_root = '''@app.get("/")
async def root():
    html = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "html", "index.html"), encoding="utf-8").read() if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "html", "index.html")) else "<h1>TradingIA API</h1><p><a href='/docs'>API Docs</a></p>"
    return HTMLResponse(html)'''

old_agent = '''@app.get("/agent")
async def agent_page():
    return FileResponse("html/agent.html")'''

new_agent = '''@app.get("/agent")
async def agent_page():
    html = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "html", "agent.html"), encoding="utf-8").read() if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "html", "agent.html")) else "<h1>Agent</h1>"
    return HTMLResponse(html)'''

c = c.replace(old_root, new_root)
c = c.replace(old_agent, new_agent)

# Ajouter import os si pas present
if 'import os' not in c:
    c = 'import os\n' + c

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)

print('OK - main.py mis a jour')
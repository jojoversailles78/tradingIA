# Remettre main.py a une version simple sans HTML embarque
with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# Remplacer les grosses routes HTML par des versions legeres
new_root = '''@app.get("/")
async def root():
    return HTMLResponse("<html><head><meta http-equiv='refresh' content='0;url=/static/index.html'></head></html>")

@app.get("/agent")
async def agent_page():
    return HTMLResponse("<html><head><meta http-equiv='refresh' content='0;url=/static/agent.html'></head></html>")

'''

c = re.sub(r'@app\.get\("/"\)\nasync def root\(\):[\s\S]*?(?=\n@app\.get|\Z)', new_root, c, flags=re.DOTALL)
c = re.sub(r'@app\.get\("/agent"\)\nasync def agent_page\(\):[\s\S]*?(?=\n@app\.get|\Z)', '', c, flags=re.DOTALL)

# Ajouter StaticFiles
if 'StaticFiles' not in c:
    c = c.replace(
        'from fastapi.responses import FileResponse, HTMLResponse',
        'from fastapi.responses import FileResponse, HTMLResponse\nfrom fastapi.staticfiles import StaticFiles'
    )

# Ajouter le montage des fichiers statiques apres la creation de app
if 'mount' not in c:
    c = c.replace(
        'app.add_middleware(',
        'import os as _os\nif _os.path.exists("html"):\n    app.mount("/static", StaticFiles(directory="html"), name="static")\n\napp.add_middleware('
    )

if 'HTMLResponse' not in c:
    c = c.replace('from fastapi.responses import FileResponse', 'from fastapi.responses import FileResponse, HTMLResponse')

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)

print('OK - main.py:', len(c), 'caracteres')
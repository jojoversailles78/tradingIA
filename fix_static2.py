with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

import re, json

# Lire les HTML
with open('html/index.html', 'r', encoding='utf-8') as f:
    index = f.read()
with open('html/agent.html', 'r', encoding='utf-8') as f:
    agent = f.read()

# Créer les routes simples
new_root = '@app.get("/")\nasync def root():\n    return HTMLResponse(' + repr(index) + ')\n'
new_agent = '@app.get("/agent")\nasync def agent_page():\n    return HTMLResponse(' + repr(agent) + ')\n'

# Remplacer
c = re.sub(r'@app\.get\("/"\)\nasync def root\(\):[\s\S]*?(?=\n@app\.get|\Z)', new_root + '\n', c)
c = re.sub(r'@app\.get\("/agent"\)\nasync def agent_page\(\):[\s\S]*?(?=\n@app\.get|\Z)', new_agent + '\n', c)

if 'HTMLResponse' not in c:
    c = c.replace('from fastapi.responses import FileResponse', 'from fastapi.responses import FileResponse, HTMLResponse')

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)

size = len(c)
print(f'OK - main.py: {size} caracteres')
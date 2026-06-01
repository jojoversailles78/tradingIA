with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# Ajouter import serve
if 'from app.serve' not in c and 'import serve' not in c:
    c = 'from app import serve as _serve\n' + c

# Route debug
debug = '''
@app.get("/debug")
async def debug():
    import os
    cwd = os.getcwd()
    exists = {}
    for p in ['html/index.html', '../html/index.html', '/app/html/index.html', 'app/html/index.html']:
        exists[p] = os.path.exists(p)
    files = []
    for root, dirs, filenames in os.walk('.'):
        if len(files) > 30:
            break
        for fname in filenames[:5]:
            files.append(os.path.join(root, fname))
    return {"cwd": cwd, "exists": exists, "files": files}

'''

# Route root
new_root = '''@app.get("/")
async def root():
    html = _serve.get_index_html()
    if html:
        return HTMLResponse(html)
    return HTMLResponse("<h1>TradingIA API</h1><p><a href='/docs'>Docs</a></p>")

@app.get("/agent")
async def agent_page():
    html = _serve.get_agent_html()
    if html:
        return HTMLResponse(html)
    return HTMLResponse("<h1>Agent</h1>")

'''

# Supprimer anciennes routes
c = re.sub(r'@app\.get\("/"\)\nasync def root\(\):[\s\S]*?(?=\n@app\.|\Z)', '', c)
c = re.sub(r'@app\.get\("/agent"\)\nasync def agent_page\(\):[\s\S]*?(?=\n@app\.|\Z)', '', c)
c = re.sub(r'@app\.get\("/debug"\)\nasync def debug\(\):[\s\S]*?(?=\n@app\.|\Z)', '', c)
c = re.sub(r'def _get_html_path[\s\S]*?(?=\n@app\.|\Z)', '', c)

# Ajouter HTMLResponse si absent
if 'HTMLResponse' not in c:
    c = c.replace('from fastapi.responses import FileResponse', 'from fastapi.responses import FileResponse, HTMLResponse')

# Ajouter les nouvelles routes a la fin
c = c.rstrip() + '\n\n' + debug + new_root

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)

print('OK - main.py:', len(c), 'caracteres')
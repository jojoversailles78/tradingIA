# Lire les fichiers HTML
with open('html/index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

with open('html/agent.html', 'r', encoding='utf-8') as f:
    agent_content = f.read()

# Lire main.py
with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Remplacer les imports
if 'HTMLResponse' not in c:
    c = c.replace(
        'from fastapi.responses import FileResponse',
        'from fastapi.responses import FileResponse, HTMLResponse'
    )

# Remplacer la route root
import re

# Nouvelle route root avec HTML inline
new_root = '''@app.get("/")
async def root():
    return HTMLResponse("""''' + index_content.replace('"""', '\\"\\"\\"') + '''""")'''

new_agent = '''@app.get("/agent")
async def agent_page():
    return HTMLResponse("""''' + agent_content.replace('"""', '\\"\\"\\"') + '''""")'''

# Remplacer les anciennes routes
c = re.sub(r'@app\.get\("/"\)\nasync def root\(\):.*?return.*?(?=\n@|\Z)', new_root + '\n', c, flags=re.DOTALL)
c = re.sub(r'@app\.get\("/agent"\)\nasync def agent_page\(\):.*?return.*?(?=\n@|\Z)', new_agent + '\n', c, flags=re.DOTALL)

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)

print('OK - HTML integre directement dans main.py')
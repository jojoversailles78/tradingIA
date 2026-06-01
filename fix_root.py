with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# Remplacer la route root par une redirection
new_root = '''@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard")
async def dashboard():
    return HTMLResponse(open("html/index.html", encoding="utf-8").read() if __import__("os").path.exists("html/index.html") else "<h1>TradingIA</h1>")

'''

c = re.sub(r'@app\.get\("/"\)\nasync def root\(\):.*?(?=\n@app\.|\Z)', new_root, c, flags=re.DOTALL)

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK')
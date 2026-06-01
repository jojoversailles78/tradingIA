with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

debug_route = '''
@app.get("/debug")
async def debug():
    import os
    cwd = os.getcwd()
    files = []
    for root, dirs, filenames in os.walk('.'):
        for fname in filenames:
            files.append(os.path.join(root, fname))
    return {"cwd": cwd, "files": files[:50]}
'''

# Ajouter avant la route root
c = c.replace('@app.get("/")', debug_route + '\n@app.get("/")', 1)

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK')
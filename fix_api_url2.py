files = [
    'backend/html/index.html',
    'html/index.html',
]

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace("const API = 'http://localhost:8000'", "const API = 'https://tradingia2-production.up.railway.app'")
        c = c.replace('const API = "http://localhost:8000"', 'const API = "https://tradingia2-production.up.railway.app"')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print('OK -', path)
    except Exception as e:
        print('Erreur -', path, e)
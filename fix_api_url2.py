files = ['backend/html/index.html', 'html/index.html', 'backend/html/agent.html', 'html/agent.html']

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace("https://tradingia-production.up.railway.app", "https://tradingia2-production.up.railway.app")
        c = c.replace("http://localhost:8000", "https://tradingia2-production.up.railway.app")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print('OK -', path)
    except Exception as e:
        print('Erreur -', path, ':', e)
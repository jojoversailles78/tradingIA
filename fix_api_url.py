with open('backend/html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("const API = 'http://localhost:8000'", "const API = 'https://tradingia-production.up.railway.app'")
c = c.replace('const API = "http://localhost:8000"', 'const API = "https://tradingia-production.up.railway.app"')

with open('backend/html/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK index.html')

with open('backend/html/agent.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("const API = 'http://localhost:8000'", "const API = 'https://tradingia-production.up.railway.app'")
c = c.replace('const API = "http://localhost:8000"', 'const API = "https://tradingia-production.up.railway.app"')

with open('backend/html/agent.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK agent.html')
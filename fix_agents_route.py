with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

new_route = '''
@app.get("/agents")
async def agents_page():
    html = _serve.get_agents_html()
    if html:
        return HTMLResponse(html)
    return HTMLResponse("<h1>Agents</h1><p><a href=\'/docs\'>API</a></p>")

'''

c = c.replace('@app.get("/debug")', new_route + '@app.get("/debug")')

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK')
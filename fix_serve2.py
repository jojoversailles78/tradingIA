with open('backend/app/serve.py', 'r', encoding='utf-8') as f:
    c = f.read()

new_func = '''
def get_agents_html():
    import os
    paths = [
        os.path.join(os.path.dirname(__file__), '..', 'html', 'agents.html'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'html', 'agents.html'),
        '/app/html/agents.html',
        'html/agents.html',
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                return f.read()
    return None
'''

c += new_func

with open('backend/app/serve.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK - get_agents_html ajoute')
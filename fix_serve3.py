# Lire le fichier agents.html
with open('backend/html/agents.html', 'r', encoding='utf-8') as f:
    agents_html = f.read()

with open('backend/html/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

with open('backend/html/agent.html', 'r', encoding='utf-8') as f:
    agent_html = f.read()

# Ecrire serve.py avec les HTML en dur
serve_content = '''import os

INDEX_HTML = {index}

AGENT_HTML = {agent}

AGENTS_HTML = {agents}

def get_index_html():
    return INDEX_HTML

def get_agent_html():
    return AGENT_HTML

def get_agents_html():
    return AGENTS_HTML
'''.format(
    index=repr(index_html),
    agent=repr(agent_html),
    agents=repr(agents_html)
)

with open('backend/app/serve.py', 'w', encoding='utf-8') as f:
    f.write(serve_content)

print('OK - serve.py avec HTML integre:', len(serve_content), 'chars')
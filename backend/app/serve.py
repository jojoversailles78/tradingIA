import os

def get_index_html():
    paths = [
        os.path.join(os.path.dirname(__file__), '..', 'html', 'index.html'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'html', 'index.html'),
        '/app/html/index.html',
        'html/index.html',
        '../html/index.html',
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                return f.read()
    return None

def get_agent_html():
    paths = [
        os.path.join(os.path.dirname(__file__), '..', 'html', 'agent.html'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'html', 'agent.html'),
        '/app/html/agent.html',
        'html/agent.html',
        '../html/agent.html',
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                return f.read()
    return None
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

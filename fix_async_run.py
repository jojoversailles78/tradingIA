with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Ajouter un endpoint qui lance en background
new_endpoint = '''
@app.post("/api/agents/{agent_id}/run_async")
async def run_agent_async(agent_id: str, background_tasks: BackgroundTasks):
    from fastapi import BackgroundTasks
    state = load_agents()
    if agent_id not in state:
        return {"error": "Agent inconnu"}
    async def do_run():
        try:
            actions = await run_agent(agent_id, state[agent_id], ALL_TICKERS)
            save_agents(state)
        except Exception as e:
            print("Background run error:", e)
    background_tasks.add_task(do_run)
    return {"status": "started", "agent_id": agent_id}

'''

c = c.replace('@app.post("/api/agents/run_all")', new_endpoint + '@app.post("/api/agents/run_all")')

# Ajouter BackgroundTasks dans les imports
if 'BackgroundTasks' not in c:
    c = c.replace('from fastapi import FastAPI', 'from fastapi import FastAPI, BackgroundTasks')

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK - endpoint async ajoute')
print('BackgroundTasks:', 'BackgroundTasks' in c)
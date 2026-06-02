with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Corriger run_single_agent pour sauvegarder seulement cet agent
old_run = '''@app.post("/api/agents/{agent_id}/run")
async def run_single_agent(agent_id: str):
    state = load_agents()
    if agent_id not in state:
        return {"error": "Agent inconnu"}
    actions = await run_agent(agent_id, state[agent_id], ALL_TICKERS)
    save_agents(state)
    pos_val = sum(p["qty"] * p["buy_price"] for p in state[agent_id]["positions"].values())
    return {"agent_id": agent_id, "actions": actions, "portfolio_value": state[agent_id]["capital"] + pos_val}'''

new_run = '''@app.post("/api/agents/{agent_id}/run")
async def run_single_agent(agent_id: str):
    state = load_agents()
    if agent_id not in state:
        return {"error": "Agent inconnu"}
    actions = await run_agent(agent_id, state[agent_id], ALL_TICKERS)
    # Sauvegarder SEULEMENT cet agent pour ne pas ecraser les autres
    try:
        _db.save_single_agent_db(agent_id, state[agent_id])
    except Exception as e:
        print("Save single error:", e)
    try:
        full_state = load_agents()
        full_state[agent_id] = state[agent_id]
        with open(AGENTS_FILE, "w") as f:
            json.dump(full_state, f, indent=2, default=str)
    except:
        pass
    pos_val = sum(p["qty"] * p["buy_price"] for p in state[agent_id]["positions"].values())
    return {"agent_id": agent_id, "actions": actions, "portfolio_value": state[agent_id]["capital"] + pos_val}'''

c = c.replace(old_run, new_run)

# Corriger aussi run_all pour sauvegarder agent par agent
old_run_all = '''    for agent_id in state:
        try:
            actions = await run_agent(agent_id, state[agent_id], ALL_TICKERS)
            print("Agent {} - {} actions".format(agent_id, len(actions)))
            save_agents(state)
            await asyncio.sleep(60)
        except Exception as e:
            print("Erreur agent {}: {}".format(agent_id, e))
            await asyncio.sleep(30)'''

new_run_all = '''    for agent_id in state:
        try:
            actions = await run_agent(agent_id, state[agent_id], ALL_TICKERS)
            print("Agent {} - {} actions".format(agent_id, len(actions)))
            # Sauvegarder seulement cet agent
            _db.save_single_agent_db(agent_id, state[agent_id])
            await asyncio.sleep(60)
        except Exception as e:
            print("Erreur agent {}: {}".format(agent_id, e))
            await asyncio.sleep(30)'''

c = c.replace(old_run_all, new_run_all)

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK - save single agent corrige')
print('save_single_agent_db in run:', 'save_single_agent_db' in c)
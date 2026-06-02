with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_scheduler = '''async def run_all_agents():
    state = load_agents()
    print("Auto-analyse tous agents - {}".format(datetime.utcnow().isoformat()))
    for agent_id in state:
        try:
            actions = await run_agent(agent_id, state[agent_id], ALL_TICKERS)
            print("Agent {} - {} actions".format(agent_id, len(actions)))
        except Exception as e:
            print("Erreur agent {}: {}".format(agent_id, e))
    save_agents(state)'''

new_scheduler = '''async def run_all_agents():
    state = load_agents()
    print("Auto-analyse tous agents - {}".format(datetime.utcnow().isoformat()))
    # Tourner un agent a la fois avec pause entre chaque
    for agent_id in state:
        try:
            actions = await run_agent(agent_id, state[agent_id], ALL_TICKERS)
            print("Agent {} - {} actions".format(agent_id, len(actions)))
            save_agents(state)
            # Pause 60 secondes entre chaque agent pour eviter surcharge memoire
            await asyncio.sleep(60)
        except Exception as e:
            print("Erreur agent {}: {}".format(agent_id, e))
            await asyncio.sleep(30)'''

c = c.replace(old_scheduler, new_scheduler)

# Aussi reduire le nombre de tickers par agent
c = c.replace('if analyzed >= 15:', 'if analyzed >= 10:')

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK - scheduler optimise')
print('asyncio.sleep:', 'asyncio.sleep(60)' in c)
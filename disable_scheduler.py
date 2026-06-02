with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Trouver et commenter le demarrage du thread scheduler
import re

# Remplacer le thread scheduler par rien
c = re.sub(
    r'loop = asyncio\.get_event_loop\(\)\s*\n\s*t = threading\.Thread\(target=scheduler_thread.*?\n\s*t\.start\(\)\s*\n\s*print\("6 agents.*?"\)',
    'print("Agents prets - scheduler desactive")',
    c,
    flags=re.DOTALL
)

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)

# Verifier
with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c2 = f.read()
    
print('scheduler_thread in startup:', 't.start()' in c2)
print('OK')
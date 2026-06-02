with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# S'assurer que l'import _db est en haut du fichier
if 'from app import db as _db' not in c:
    c = 'from app import db as _db\n' + c
else:
    # Deplacer l'import en haut
    c = c.replace('from app import db as _db\n', '')
    c = 'from app import db as _db\n' + c

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK')
print('_db import position:', c.find('from app import db as _db'))
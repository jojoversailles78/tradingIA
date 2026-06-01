with open('backend/html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Supprimer le doublon portefeuille et ajouter onglet agents
old_tabs = "['analyse','scanner','portfolio','politics']"
new_tabs = "['analyse','scanner','portfolio','politics','agents']"
c = c.replace(old_tabs, new_tabs)

# Ajouter onglet agents dans la barre
old_tab_bar = '<div class="tab" onclick="showTab(\'politics\')">&#x1F3DB; Congres &amp; IPO</div>'
new_tab_bar = '<div class="tab" onclick="showTab(\'politics\')">&#x1F3DB; Congres &amp; IPO</div>\n  <div class="tab" onclick="window.location.href=\'/agents\'">&#x1F916; 6 Agents IA</div>'
c = c.replace(old_tab_bar, new_tab_bar)

# Supprimer le doublon portefeuille si present
import re
# Compter combien de fois tab-portfolio apparait
count = c.count('id="tab-portfolio"')
if count > 1:
    # Garder seulement le premier
    idx = c.find('id="tab-portfolio"')
    idx2 = c.find('id="tab-portfolio"', idx+1)
    if idx2 > 0:
        # Trouver la fin du second bloc
        end = c.find('<!-- ONGLET', idx2)
        if end > 0:
            c = c[:idx2-50] + c[end:]
            print('Doublon supprime')

with open('backend/html/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
with open('html/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK - tabs mis a jour')
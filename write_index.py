# Lire le fichier actuel
with open('C:/tradingIA/html/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Ajouter onglet Congres dans la barre
old_tab = '<div class="tab" onclick="showTab(\'portfolio\')">&#x1F4BC; Mon Portefeuille</div>'
new_tab = '<div class="tab" onclick="showTab(\'portfolio\')">&#x1F4BC; Mon Portefeuille</div>\n  <div class="tab" onclick="showTab(\'politics\')">&#x1F3DB; Congres &amp; IPO</div>'

if 'politics' not in content:
    content = content.replace(old_tab, new_tab)
    print("Onglet ajoute")
else:
    print("Onglet deja present")

# 2. Mettre a jour showTab
old_show = "['analyse','scanner','portfolio']"
new_show = "['analyse','scanner','portfolio','politics']"
content = content.replace(old_show, new_show)

# 3. Ajouter le contenu de l'onglet avant le portefeuille
politics_html = """
<!-- ONGLET POLITIQUE ET IPO -->
<div class="tab-content" id="tab-politics">
  <div class="card">
    <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">
      <div class="stitle" style="margin:0">Donnees politiques et marches prives</div>
      <button class="btn-primary" onclick="loadCongressTrades()">Trades Congres US</button>
      <button class="btn-primary" onclick="loadIPOs()" style="background:#7c3aed">IPO a venir</button>
    </div>
    <div id="politics-status" style="margin-top:10px;font-size:13px;color:#555"></div>
  </div>
  <div id="congress-opportunities" style="display:none" class="card">
    <div class="stitle" style="color:#4ade80">Opportunites - Tickers achetes par le Congres avec Score IA eleve</div>
    <div id="congress-opp-list"></div>
  </div>
  <div id="congress-trades-wrap" style="display:none" class="card">
    <div class="stitle">Derniers trades declares - Membres du Congres US</div>
    <div id="congress-trades-list"></div>
  </div>
  <div id="ipo-wrap" style="display:none" class="card">
    <div class="stitle">IPO et Entreprises Pre-IPO Surveillees</div>
    <div id="ipo-list"></div>
  </div>
</div>
"""

old_portfolio = "<!-- ONGLET PORTEFEUILLE -->"
if "tab-politics" not in content:
    content = content.replace(old_portfolio, politics_html + "\n" + old_portfolio)
    print("Contenu onglet ajoute")
else:
    print("Contenu deja present")

# 4. Ajouter les fonctions JavaScript avant loadTicker('AAPL')
js_functions = """
async function loadCongressTrades() {
  document.getElementById('politics-status').textContent = 'Chargement des trades du Congres... (30-60 sec)';
  document.getElementById('congress-trades-wrap').style.display = 'none';
  document.getElementById('congress-opportunities').style.display = 'none';
  try {
    const [tradesR, oppR] = await Promise.all([
      fetch(API + '/api/congress/trades?days=30'),
      fetch(API + '/api/congress/opportunities')
    ]);
    const tradesD = await tradesR.json();
    const oppD = await oppR.json();
    const trades = tradesD.trades || [];
    const opps = oppD.opportunities || [];
    document.getElementById('politics-status').textContent = trades.length + ' trades charges - ' + opps.length + ' opportunites detectees';
    if(opps.length > 0) {
      document.getElementById('congress-opp-list').innerHTML = opps.map(function(o) {
        return '<div class="row" style="cursor:pointer" onclick="showTab(\\'analyse\\');loadTicker(\\'' + o.ticker + '\\')">' +
          '<div style="flex:1"><span style="font-weight:600;color:#1D9E75">' + o.ticker + '</span>' +
          '<span style="font-size:12px;color:#888;margin-left:8px">' + o.name + '</span>' +
          '<span style="font-size:11px;color:#555;margin-left:8px">' + o.congress_buys + ' achat(s) - ' + (o.buyers||[]).slice(0,2).join(', ') + '</span></div>' +
          '<div style="display:flex;gap:12px;align-items:center">' +
          '<span style="font-size:12px;color:#555">Dernier: ' + o.last_trade_date + '</span>' +
          '<span style="font-weight:600;color:' + sc(o.score) + '">' + o.score + '/10</span>' +
          recBadge(o.recommendation) + '</div></div>';
      }).join('');
      document.getElementById('congress-opportunities').style.display = 'block';
    }
    document.getElementById('congress-trades-list').innerHTML = '<div style="display:grid;grid-template-columns:150px 80px 1fr 120px 150px 100px;gap:10px;padding:8px 14px;font-size:11px;color:#555;border-bottom:1px solid #222"><span>Elu</span><span>Ticker</span><span>Description</span><span>Type</span><span>Montant</span><span>Date</span></div>' +
    trades.slice(0,50).map(function(t) {
      var tc = t.type && t.type.toLowerCase().includes('purchase') ? '#4ade80' : '#f87171';
      return '<div style="display:grid;grid-template-columns:150px 80px 1fr 120px 150px 100px;gap:10px;padding:8px 14px;border-bottom:1px solid #1a1a2e;font-size:12px;align-items:center">' +
        '<span style="color:#aaa;font-size:11px">' + t.representative + '</span>' +
        '<span style="font-weight:600;color:#1D9E75;cursor:pointer" onclick="showTab(\\'analyse\\');loadTicker(\\'' + t.ticker + '\\')">' + t.ticker + '</span>' +
        '<span style="color:#666;font-size:11px">' + t.asset_description + '</span>' +
        '<span style="color:' + tc + ';font-weight:500">' + t.type + '</span>' +
        '<span style="color:#888">' + t.amount + '</span>' +
        '<span style="color:#555">' + t.date + '</span></div>';
    }).join('');
    document.getElementById('congress-trades-wrap').style.display = 'block';
  } catch(e) {
    document.getElementById('politics-status').textContent = 'Erreur : ' + e.message;
  }
}

async function loadIPOs() {
  document.getElementById('politics-status').textContent = 'Chargement des IPO...';
  document.getElementById('ipo-wrap').style.display = 'none';
  try {
    const r = await fetch(API + '/api/ipo/upcoming');
    const d = await r.json();
    const ipos = d.ipos || [];
    document.getElementById('politics-status').textContent = ipos.length + ' IPO/pre-IPO chargees';
    var statusColors = {'Confirme':'#4ade80','En attente':'#facc15','Rumeur':'#888'};
    document.getElementById('ipo-list').innerHTML = ipos.map(function(ipo) {
      return '<div style="background:#0d0d15;border-radius:8px;padding:14px;border:1px solid #1e1e2e;margin-bottom:10px">' +
        '<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">' +
        '<div><div style="font-size:16px;font-weight:600;color:#fff">' + ipo.company + '</div>' +
        '<div style="font-size:12px;color:#555;margin-top:3px">Ticker prevu : <span style="color:#1D9E75;font-weight:600">' + ipo.ticker + '</span> - ' + ipo.exchange + '</div></div>' +
        '<div style="text-align:right"><div style="font-size:13px;color:#fff;font-weight:500">' + ipo.price_range + '</div>' +
        '<div style="font-size:11px;color:#555">' + ipo.currency + '</div></div></div>' +
        '<div style="display:flex;gap:12px;margin-top:10px;flex-wrap:wrap">' +
        '<span style="background:#1a1a2e;color:#888;padding:3px 10px;border-radius:20px;font-size:11px">Date: ' + ipo.date + '</span>' +
        '<span style="background:#1a1a2e;color:#888;padding:3px 10px;border-radius:20px;font-size:11px">Actions: ' + ipo.shares + '</span>' +
        '<span style="background:#1a1a2e;color:' + (statusColors[ipo.status]||'#888') + ';padding:3px 10px;border-radius:20px;font-size:11px;font-weight:500">' + (ipo.status||'N/A') + '</span>' +
        '</div></div>';
    }).join('');
    document.getElementById('ipo-wrap').style.display = 'block';
  } catch(e) {
    document.getElementById('politics-status').textContent = 'Erreur : ' + e.message;
  }
}

"""

if 'loadCongressTrades' not in content:
    content = content.replace("loadTicker('AAPL');", js_functions + "\nloadTicker('AAPL');")
    print("Fonctions JS ajoutees")
else:
    print("Fonctions deja presentes")

# Sauvegarder
with open('C:/tradingIA/html/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK - index.html mis a jour avec succes')
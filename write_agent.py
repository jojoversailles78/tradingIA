html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>TradingIA Agent</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;background:#0a0a0f;color:#e0e0e0;min-height:100vh}
.top{background:#111118;padding:12px 20px;display:flex;align-items:center;gap:16px;border-bottom:1px solid #222;flex-wrap:wrap}
.top b{font-size:18px;color:#fff}
.nav-link{color:#555;font-size:13px;text-decoration:none;padding:6px 12px;border-radius:8px;border:1px solid #333}
.nav-link:hover{color:#1D9E75;border-color:#1D9E75}
.content{padding:20px;max-width:1200px;margin:0 auto;display:flex;flex-direction:column;gap:16px}
.card{background:#111118;border-radius:12px;padding:20px;border:1px solid #1e1e2e}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
.stitle{font-size:11px;font-weight:600;color:#555;margin-bottom:14px;text-transform:uppercase;letter-spacing:0.08em}
.metric{background:#0d0d15;border-radius:8px;padding:16px;border:1px solid #1e1e2e}
.metric-val{font-size:28px;font-weight:600;margin-bottom:4px}
.metric-lbl{font-size:11px;color:#555}
.btn{padding:10px 20px;border-radius:8px;border:none;cursor:pointer;font-size:14px;font-weight:500}
.btn-green{background:#1D9E75;color:#fff}
.btn-red{background:#3a1a1a;color:#f87171;border:1px solid #f87171}
.btn-gray{background:#1a1a24;color:#aaa;border:1px solid #333}
.action-row{display:grid;grid-template-columns:110px 80px 1fr 100px 120px 130px;gap:10px;align-items:center;padding:10px 14px;border-bottom:1px solid #1a1a2e;font-size:13px}
.action-header{display:grid;grid-template-columns:110px 80px 1fr 100px 120px 130px;gap:10px;padding:8px 14px;font-size:11px;color:#555;text-transform:uppercase;border-bottom:1px solid #222}
.pos-row{display:grid;grid-template-columns:90px 1fr 100px 80px 100px 80px;gap:10px;align-items:center;padding:10px 14px;border-bottom:1px solid #1a1a2e;font-size:13px}
.pos-header{display:grid;grid-template-columns:90px 1fr 100px 80px 100px 80px;gap:10px;padding:8px 14px;font-size:11px;color:#555;text-transform:uppercase;border-bottom:1px solid #222}
.badge{padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600}
.badge-buy{background:#0d2a1a;color:#4ade80}
.badge-sell{background:#2a0d0d;color:#f87171}
.badge-partial{background:#2a2200;color:#facc15}
.progress-bar{height:8px;background:#1a1a2e;border-radius:4px;margin-top:10px;overflow:hidden}
.progress-fill{height:8px;border-radius:4px;transition:width 1s;background:#1D9E75}
.pulse{animation:pulse 1.5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
input[type=text]{background:#1a1a24;border:1px solid #333;border-radius:8px;color:#fff;padding:8px 12px;font-size:13px;width:100%}
</style>
</head>
<body>
<div class="top">
  <b>TradingIA - Agent Autonome</b>
  <a href="/" class="nav-link">Retour Dashboard</a>
  <span id="agent-status" style="margin-left:auto;font-size:12px;color:#555">En attente</span>
</div>
<div class="content">
  <div class="grid4" id="metrics">
    <div class="metric"><div class="metric-val" id="m-capital">20 000</div><div class="metric-lbl">Capital disponible (EUR)</div></div>
    <div class="metric"><div class="metric-val" id="m-portfolio">--</div><div class="metric-lbl">Valeur portefeuille (EUR)</div></div>
    <div class="metric"><div class="metric-val" id="m-pnl">--</div><div class="metric-lbl">P&L total</div></div>
    <div class="metric"><div class="metric-val" id="m-winrate">--</div><div class="metric-lbl">Taux de reussite</div></div>
  </div>
  <div class="card">
    <div class="stitle">Controles de l Agent</div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end">
      <div style="flex:1;min-width:300px">
        <div style="font-size:12px;color:#555;margin-bottom:6px">Actions a surveiller</div>
        <input type="text" id="tickers-input" value="AAPL,MSFT,NVDA,TSLA,AMZN,META,GOOGL,SPY,SU.PA,MC.PA,TTE.PA,BNP.PA,AIR.PA,RMS.PA">
      </div>
      <button class="btn btn-green" onclick="runAgent()">Lancer analyse</button>
      <button class="btn btn-gray" onclick="loadState()">Rafraichir</button>
      <button class="btn btn-red" onclick="resetAgent()">Reinitialiser</button>
    </div>
    <div id="status-bar" style="margin-top:12px;font-size:13px;color:#555">Appuie sur Lancer analyse pour demarrer.</div>
    <div id="progress-wrap" style="display:none"><div class="progress-bar"><div class="progress-fill pulse" id="progress-fill" style="width:0%"></div></div></div>
  </div>
  <div class="card">
    <div class="stitle">Regles de Decision IA</div>
    <div class="grid3">
      <div style="background:#0d2a1a;border-radius:8px;padding:14px;border:1px solid #1a3a2a">
        <div style="color:#4ade80;font-weight:600;margin-bottom:8px">CONDITIONS ACHAT</div>
        <div style="font-size:12px;color:#aaa;line-height:1.8">Score IA >= 7.2/10<br>Recommandation ACHETER<br>RSI entre 30 et 70<br>MACD haussier<br>ADX > 20<br>Analystes >= 50% achat</div>
      </div>
      <div style="background:#2a2200;border-radius:8px;padding:14px;border:1px solid #3a3200">
        <div style="color:#facc15;font-weight:600;margin-bottom:8px">CAPITALISATION</div>
        <div style="font-size:12px;color:#aaa;line-height:1.8">+15% plus-value<br>Tendance encore forte<br>MACD toujours positif<br>Vente 50% seulement<br>Conservation 50% restants<br>Recyclage du capital</div>
      </div>
      <div style="background:#2a0d0d;border-radius:8px;padding:14px;border:1px solid #3a1a1a">
        <div style="color:#f87171;font-weight:600;margin-bottom:8px">CONDITIONS VENTE</div>
        <div style="font-size:12px;color:#aaa;line-height:1.8">+5% avec score en baisse<br>+10% avec RSI > 70<br>+15% si tendance affaiblie<br>Stop loss a -8%<br>Signal VENDRE de l IA<br>Max 8 positions</div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="stitle">Positions Ouvertes</div>
    <div id="positions-wrap"><div style="color:#555;text-align:center;padding:20px">Aucune position ouverte</div></div>
  </div>
  <div class="card">
    <div class="stitle">Journal des Decisions IA</div>
    <div id="history-wrap"><div style="color:#555;text-align:center;padding:20px">Aucune action effectuee</div></div>
  </div>
</div>
<script>
const API = "http://localhost:8000";
function n2(v,s){s=s||"";return v!=null?Number(v).toFixed(2)+s:"N/A";}
function n1(v,s){s=s||"";return v!=null?Number(v).toFixed(1)+s:"N/A";}
function fmt(v){return v!=null?Math.round(Number(v)).toLocaleString("fr-FR"):"--";}
function sc(s){return s>=7?"#4ade80":s>=5?"#facc15":"#f87171";}
function updateMetrics(state,pv){
  var initial=state.initial_capital;
  var pnl=pv-initial;
  var pnlPct=(pnl/initial)*100;
  var wr=state.total_trades>0?(state.winning_trades/state.total_trades*100):0;
  var pc=pnl>=0?"#4ade80":"#f87171";
  document.getElementById("m-capital").textContent=fmt(state.capital)+" EUR";
  document.getElementById("m-portfolio").textContent=fmt(pv)+" EUR";
  document.getElementById("m-pnl").innerHTML="<span style=\\"color:"+pc+"\\">"+( pnl>=0?"+":"")+fmt(pnl)+" EUR ("+( pnlPct>=0?"+":"")+pnlPct.toFixed(1)+"%)</span>";
  document.getElementById("m-winrate").innerHTML="<span style=\\"color:"+(wr>=50?"#4ade80":"#f87171")+"\\">"+wr.toFixed(0)+"%</span> <span style=\\"font-size:14px;color:#555\\">("+state.winning_trades+"/"+state.total_trades+")</span>";
}
function renderPositions(state){
  var positions=Object.values(state.positions||{});
  if(!positions.length){document.getElementById("positions-wrap").innerHTML="<div style=\\"color:#555;text-align:center;padding:20px\\">Aucune position ouverte</div>";return;}
  var rows=positions.map(function(p){
    var invested=p.qty*p.buy_price;
    return "<div class=\\"pos-row\\"><span style=\\"font-weight:600;color:#1D9E75\\">"+p.ticker+"</span><span style=\\"font-size:12px;color:#888\\">"+p.name+"</span><span style=\\"color:#fff\\">$"+n2(p.buy_price)+"</span><span style=\\"color:#888\\">"+p.qty.toFixed(4)+"</span><span style=\\"color:#fff\\">"+fmt(invested)+" EUR</span><span style=\\"color:"+sc(p.score_at_buy)+";font-weight:600\\">"+p.score_at_buy+"/10</span></div>";
  }).join("");
  document.getElementById("positions-wrap").innerHTML="<div class=\\"pos-header\\"><span>Ticker</span><span>Nom</span><span>Px achat</span><span>Qte</span><span>Investi</span><span>Score</span></div>"+rows;
}
function renderHistory(state){
  var history=(state.history||[]).slice(0,30);
  if(!history.length){document.getElementById("history-wrap").innerHTML="<div style=\\"color:#555;text-align:center;padding:20px\\">Aucune action effectuee</div>";return;}
  var rows=history.map(function(a){
    var bc="badge-err";
    if(a.type==="ACHAT") bc="badge-buy";
    else if(a.type==="VENTE") bc="badge-sell";
    else if(a.type==="VENTE PARTIELLE") bc="badge-partial";
    var pnlHtml=a.pnl_abs!=null?"<span style=\\"color:"+(a.pnl_abs>=0?"#4ade80":"#f87171")+";font-weight:600\\">"+(a.pnl_abs>=0?"+":"")+fmt(a.pnl_abs)+" EUR ("+(a.pnl_pct>=0?"+":"")+n1(a.pnl_pct)+"%)</span>":a.cost!=null?"<span style=\\"color:#888\\">-"+fmt(a.cost)+" EUR</span>":"--";
    var ts=a.timestamp?a.timestamp.slice(0,16).replace("T"," "):"";
    return "<div class=\\"action-row\\"><span class=\\"badge "+bc+"\\">"+a.type+"</span><span style=\\"font-weight:600;color:#1D9E75\\">"+a.ticker+"</span><span style=\\"font-size:12px;color:#666\\">"+( a.reason||"")+"</span><span style=\\"color:#fff\\">$"+n2(a.price)+"</span>"+pnlHtml+"<span style=\\"font-size:11px;color:#444\\">"+ts+"</span></div>";
  }).join("");
  document.getElementById("history-wrap").innerHTML="<div class=\\"action-header\\"><span>Action</span><span>Ticker</span><span>Raison IA</span><span>Prix</span><span>P&L</span><span>Date</span></div>"+rows;
}
async function loadState(){
  try{
    var r=await fetch(API+"/api/agent/state");
    var state=await r.json();
    var pv=state.capital+Object.values(state.positions||{}).reduce(function(s,p){return s+p.qty*p.buy_price;},0);
    updateMetrics(state,pv);
    renderPositions(state);
    renderHistory(state);
    if(state.last_run) document.getElementById("agent-status").textContent="Derniere analyse : "+state.last_run.slice(0,16).replace("T"," ");
  }catch(e){document.getElementById("status-bar").textContent="Impossible de contacter le backend";}
}
async function runAgent(){
  var tickers=document.getElementById("tickers-input").value.trim();
  if(!tickers) return;
  document.getElementById("status-bar").textContent="Agent en cours d analyse... (2-5 minutes)";
  document.getElementById("progress-wrap").style.display="block";
  document.getElementById("agent-status").innerHTML="<span class=\\"pulse\\" style=\\"color:#1D9E75\\">Analyse en cours</span>";
  var progress=0;
  var iv=setInterval(function(){progress=Math.min(progress+2,90);document.getElementById("progress-fill").style.width=progress+"%";},3000);
  try{
    var r=await fetch(API+"/api/agent/run?tickers="+encodeURIComponent(tickers),{method:"POST"});
    if(!r.ok) throw new Error("Erreur serveur");
    var data=await r.json();
    clearInterval(iv);
    document.getElementById("progress-fill").style.width="100%";
    var actions=data.actions||[];
    var buys=actions.filter(function(a){return a.type==="ACHAT";}).length;
    var sells=actions.filter(function(a){return a.type==="VENTE"||a.type==="VENTE PARTIELLE";}).length;
    document.getElementById("status-bar").textContent="Analyse terminee - "+buys+" achat(s) - "+sells+" vente(s)";
    document.getElementById("agent-status").textContent="Derniere analyse : "+new Date().toLocaleString("fr-FR");
    updateMetrics(data.state,data.portfolio_value);
    renderPositions(data.state);
    renderHistory(data.state);
    setTimeout(function(){document.getElementById("progress-wrap").style.display="none";document.getElementById("progress-fill").style.width="0%";},2000);
  }catch(e){
    clearInterval(iv);
    document.getElementById("status-bar").textContent="Erreur : "+e.message;
    document.getElementById("progress-wrap").style.display="none";
  }
}
async function resetAgent(){
  if(!confirm("Reinitialiser l agent a 20000 EUR ? Toutes les positions seront effacees.")) return;
  try{
    var r=await fetch(API+"/api/agent/reset?capital=20000",{method:"POST"});
    var state=await r.json();
    updateMetrics(state,20000);
    renderPositions(state);
    renderHistory(state);
    document.getElementById("status-bar").textContent="Agent reinitialise a 20 000 EUR";
  }catch(e){alert("Erreur : "+e.message);}
}
loadState();
</script>
</body>
</html>'''

with open('C:/tradingIA/html/agent.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('OK - agent.html ecrit avec succes')
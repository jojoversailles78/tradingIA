import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from datetime import datetime
import json, os, asyncio, threading, time

app = FastAPI(title="TradingIA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CAC40 = ["AC.PA","ACA.PA","AI.PA","AIR.PA","ALO.PA","MT.AS","ATO.PA","CS.PA","BNP.PA","EN.PA","CAP.PA","CA.PA","AXA.PA","CNH.MI","DSY.PA","EDEN.PA","EL.PA","ERF.PA","EDF.PA","FTI.PA","GTT.PA","GLE.PA","HO.PA","KER.PA","LR.PA","OR.PA","LHN.SW","MC.PA","ML.PA","ORA.PA","RI.PA","PUB.PA","RNO.PA","RMS.PA","SAF.PA","SAN.PA","SGO.PA","SU.PA","STM.PA","TEP.PA","TTE.PA","UG.PA","VIE.PA","DG.PA","WLN.PA"]

NASDAQ100 = ["AAPL","ABNB","ADBE","ADI","ADP","ADSK","AEP","AMAT","AMD","AMGN","AMZN","ANSS","ARM","ASML","AVGO","AZN","BIIB","BKNG","BKR","CDNS","CEG","CHTR","CMCSA","COST","CPRT","CRWD","CSCO","CTSH","DASH","DDOG","DLTR","DXCM","EA","EXC","FANG","FAST","FTNT","GEHC","GFS","GILD","GOOG","GOOGL","HON","IDXX","ILMN","INTC","INTU","ISRG","KDP","KHC","KLAC","LRCX","LULU","MAR","MCHP","MDB","MDLZ","MELI","META","MNST","MRNA","MRVL","MSFT","MU","NFLX","NVDA","NXPI","ODFL","ON","ORLY","PANW","PAYX","PCAR","PDD","PEP","PYPL","QCOM","REGN","ROP","ROST","SBUX","SIRI","SMCI","SNPS","SPLK","TEAM","TMUS","TSLA","TTD","TTWO","TXN","VRSK","VRTX","WDAY","WBD","WLTW","XEL","ZS"]

SP500 = ["A","AAL","AAP","AAPL","ABBV","ABC","ABMD","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEE","AEP","AES","AFL","AIG","AIZ","AJG","AKAM","ALB","ALGN","ALK","ALL","ALLE","AMAT","AMCR","AMD","AME","AMGN","AMP","AMT","AMZN","ANET","ANSS","AON","AOS","APA","APD","APH","APTV","ARE","ATO","AVB","AVGO","AVY","AWK","AXP","AZO","BA","BAC","BAX","BBWI","BBY","BDX","BEN","BF.B","BIO","BK","BKNG","BKR","BLK","BMY","BR","BRK.B","BSX","BWA","BXP","C","CAG","CAH","CARR","CAT","CB","CBOE","CBRE","CCI","CCL","CDNS","CDW","CE","CEG","CF","CFG","CHD","CHRW","CHTR","CI","CINF","CL","CLX","CMA","CMCSA","CME","CMG","CMI","CMS","CNC","CNP","COF","COO","COP","COST","CPB","CPRT","CRL","CRM","CSCO","CSX","CTAS","CTLT","CTRA","CTSH","CTVA","CVS","CVX","CZR","D","DAL","DD","DE","DFS","DG","DGX","DHI","DHR","DIS","DISH","DLR","DLTR","DOV","DOW","DPZ","DRE","DRI","DTE","DUK","DVA","DVN","DXC","DXCM","EA","EBAY","ECL","ED","EFX","EIX","EL","EMN","EMR","ENPH","EOG","EPAM","EQIX","EQR","EQT","ES","ESS","ETN","ETR","EVRG","EW","EXC","EXPD","EXPE","EXR","F","FANG","FAST","FCX","FDS","FDX","FE","FFIV","FIS","FISV","FITB","FLT","FMC","FOX","FOXA","FRC","FRT","FTNT","FTV","GD","GE","GILD","GIS","GL","GLW","GM","GNRC","GOOGL","GPC","GPN","GS","GWW","HAL","HAS","HBAN","HCA","HD","HES","HIG","HII","HLT","HOLX","HON","HPE","HPQ","HRL","HSIC","HST","HSY","HUM","HWM","IBM","ICE","IDXX","IEX","IFF","ILMN","INCY","INTC","INTU","INVH","IP","IPG","IQV","IR","IRM","ISRG","IT","ITW","IVZ","J","JBHT","JCI","JKHY","JNJ","JNPR","JPM","K","KEY","KEYS","KHC","KIM","KLAC","KMB","KMI","KMX","KO","KR","L","LDOS","LEN","LH","LHX","LIN","LKQ","LLY","LMT","LNC","LNT","LOW","LRCX","LUV","LVS","LW","LYB","LYV","MA","MAA","MAR","MAS","MCD","MCHP","MCK","MCO","MDLZ","MDT","MET","META","MGM","MHK","MKC","MKTX","MLM","MMC","MMM","MNST","MO","MOH","MOS","MPC","MPWR","MRK","MRNA","MRO","MS","MSCI","MSFT","MSI","MTB","MTCH","MTD","MU","NCLH","NDAQ","NEE","NEM","NFLX","NI","NKE","NOC","NOW","NRG","NSC","NTAP","NTRS","NUE","NVDA","NVR","NWL","NWS","NWSA","NXPI","O","ODFL","OGN","OKE","OMC","ORCL","ORLY","OTIS","OXY","PARA","PAYC","PAYX","PCAR","PCG","PEAK","PEG","PEP","PFE","PFG","PG","PGR","PH","PHM","PKG","PKI","PLD","PM","PNC","PNR","PNW","POOL","PPG","PPL","PRU","PSA","PSX","PTC","PWR","PXD","PYPL","QCOM","QRVO","RCL","RE","REG","REGN","RF","RHI","RJF","RL","RMD","ROK","ROL","ROP","ROST","RSG","RTX","SBAC","SBUX","SEDG","SEE","SHW","SIVB","SJM","SLB","SNA","SNPS","SO","SPG","SPGI","SRE","STE","STT","STX","STZ","SWK","SWKS","SYF","SYK","SYY","T","TAP","TDG","TDY","TECH","TEL","TER","TFC","TFX","TGT","TJX","TMO","TMUS","TPR","TRMB","TROW","TRV","TSCO","TSLA","TSN","TT","TTWO","TXN","TXT","TYL","UAL","UDR","UHS","ULTA","UNH","UNP","UPS","URI","USB","V","VFC","VICI","VLO","VMC","VNO","VRSK","VRSN","VRTX","VTR","VTRS","VZ","WAB","WAT","WBA","WBD","WDC","WEC","WELL","WFC","WHR","WM","WMB","WMT","WRB","WRK","WST","WTW","WY","WYNN","XEL","XOM","XRAY","XYL","YUM","ZBH","ZBRA","ZION","ZTS"]

ALL_TICKERS = list(set(CAC40 + NASDAQ100 + SP500))
AGENT_FILE = "agent_state.json"

def load_agent():
    if os.path.exists(AGENT_FILE):
        with open(AGENT_FILE, "r") as f:
            return json.load(f)
    return {"capital": 20000.0, "initial_capital": 20000.0, "positions": {}, "history": [], "created_at": datetime.utcnow().isoformat(), "last_run": None, "total_trades": 0, "winning_trades": 0, "daily_trades": 0, "last_trade_date": None, "auto_runs": 0}

def save_agent(state):
    with open(AGENT_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)

async def run_agent_logic(tickers, min_score=7.2, min_daily_trades=3):
    from app.api.routes import analyze_ticker
    import random
    state = load_agent()
    state["last_run"] = datetime.utcnow().isoformat()
    state["auto_runs"] = state.get("auto_runs", 0) + 1
    today = datetime.utcnow().strftime("%Y-%m-%d")
    if state.get("last_trade_date") != today:
        state["daily_trades"] = 0
        state["last_trade_date"] = today
    actions = []
    MIN_PROFIT_PCT = 5.0
    MAX_POSITION_PCT = 0.15
    MAX_POSITIONS = 10

    for ticker, pos in list(state["positions"].items()):
        try:
            data = await analyze_ticker(ticker)
            current_price = data["price"]["current"]
            score = data["scoring"]["global_score"]
            rec = data["scoring"]["recommendation"]
            rsi = data["technical"]["rsi"] or 50
            macd = data["technical"]["macd"]["value"] or 0
            adx = data["technical"]["adx"]["value"] or 0
            buy_price = pos["buy_price"]
            qty = pos["qty"]
            pnl_pct = (current_price - buy_price) / buy_price * 100
            should_sell = False
            sell_reason = ""
            if pnl_pct >= MIN_PROFIT_PCT and score < 6.5:
                should_sell = True
                sell_reason = "Plus-value +{:.1f}% avec score en baisse ({}/10)".format(pnl_pct, score)
            elif pnl_pct >= 10 and rsi > 70:
                should_sell = True
                sell_reason = "Prise de profit +{:.1f}% - RSI surachat ({:.1f})".format(pnl_pct, rsi)
            elif pnl_pct >= 15:
                if score >= 7.0 and macd > 0 and adx > 25:
                    qty_sell = int(qty * 0.5)
                    if qty_sell > 0:
                        profit = (current_price - buy_price) * qty_sell
                        state["capital"] += current_price * qty_sell
                        state["positions"][ticker]["qty"] -= qty_sell
                        state["total_trades"] += 1
                        state["winning_trades"] += 1
                        state["daily_trades"] += 1
                        action = {"type": "VENTE PARTIELLE", "ticker": ticker, "name": data["name"], "qty": qty_sell, "price": current_price, "buy_price": buy_price, "pnl_pct": pnl_pct, "pnl_abs": profit, "score": score, "reason": "Capitalisation +{:.1f}% - tendance forte conservee".format(pnl_pct), "timestamp": datetime.utcnow().isoformat(), "auto": True}
                        actions.append(action)
                        state["history"].insert(0, action)
                        continue
                else:
                    should_sell = True
                    sell_reason = "Prise de profit +{:.1f}% - tendance affaiblie".format(pnl_pct)
            elif pnl_pct <= -8:
                should_sell = True
                sell_reason = "Stop loss declenche ({:.1f}%)".format(pnl_pct)
            elif rec == "sell" and pnl_pct > 0:
                should_sell = True
                sell_reason = "Signal VENTE IA avec plus-value +{:.1f}%".format(pnl_pct)
            if should_sell:
                state["capital"] += current_price * qty
                profit = (current_price - buy_price) * qty
                if profit > 0: state["winning_trades"] += 1
                state["total_trades"] += 1
                state["daily_trades"] += 1
                action = {"type": "VENTE", "ticker": ticker, "name": data["name"], "qty": qty, "price": current_price, "buy_price": buy_price, "pnl_pct": pnl_pct, "pnl_abs": profit, "score": score, "reason": sell_reason, "timestamp": datetime.utcnow().isoformat(), "auto": True}
                actions.append(action)
                state["history"].insert(0, action)
                del state["positions"][ticker]
        except:
            pass

    tickers_shuffled = list(tickers)
    random.shuffle(tickers_shuffled)
    opportunities = []
    analyzed = 0
    for ticker in tickers_shuffled:
        if ticker in state["positions"]:
            continue
        if analyzed >= 40:
            break
        try:
            data = await analyze_ticker(ticker)
            score = data["scoring"]["global_score"]
            rec = data["scoring"]["recommendation"]
            rsi = data["technical"]["rsi"] or 50
            macd = data["technical"]["macd"]["value"] or 0
            macd_hist = data["technical"]["macd"]["histogram"] or 0
            adx = data["technical"]["adx"]["value"] or 0
            golden_cross = data["technical"]["moving_averages"]["golden_cross"]
            price_above_sma50 = data["technical"]["moving_averages"]["price_above_sma50"]
            buy_pct = data["analysts"]["buy_pct"] or 0
            effective_min = min_score if state["daily_trades"] >= min_daily_trades else 6.8
            if score >= effective_min and rec in ["buy","hold"] and rsi < 72 and macd > 0 and adx > 18 and buy_pct >= 45:
                confidence = score
                if golden_cross: confidence += 0.3
                if price_above_sma50: confidence += 0.2
                if buy_pct > 65: confidence += 0.3
                if macd_hist > 0: confidence += 0.2
                opportunities.append({"ticker": ticker, "data": data, "score": score, "confidence": confidence, "rsi": rsi, "macd": macd, "adx": adx, "buy_pct": buy_pct})
            analyzed += 1
        except:
            analyzed += 1

    opportunities.sort(key=lambda x: x["confidence"], reverse=True)
    needed = max(min_daily_trades - state["daily_trades"], 0)
    max_buys = max(5, needed)

    for opp in opportunities[:max_buys]:
        if len(state["positions"]) >= MAX_POSITIONS:
            break
        ticker = opp["ticker"]
        data = opp["data"]
        current_price = data["price"]["current"]
        if not current_price or current_price <= 0:
            continue
        score_factor = (opp["score"] - 6.5) / (10 - 6.5)
        position_pct = 0.06 + score_factor * (MAX_POSITION_PCT - 0.06)
        invest_amount = state["capital"] * position_pct
        invest_amount = min(invest_amount, state["capital"] * 0.18)
        if invest_amount < 50 or invest_amount > state["capital"]:
            continue
        qty = invest_amount / current_price
        cost = qty * current_price
        if cost > state["capital"]:
            continue
        state["capital"] -= cost
        state["positions"][ticker] = {"ticker": ticker, "name": data["name"], "buy_price": current_price, "qty": qty, "cost": cost, "score_at_buy": opp["score"], "bought_at": datetime.utcnow().isoformat()}
        state["total_trades"] += 1
        state["daily_trades"] += 1
        action = {"type": "ACHAT", "ticker": ticker, "name": data["name"], "qty": qty, "price": current_price, "cost": cost, "score": opp["score"], "rsi": opp["rsi"], "macd": opp["macd"], "adx": opp["adx"], "buy_pct": opp["buy_pct"], "reason": "Score {}/10 - MACD haussier - RSI {:.1f} - {}% analystes achat".format(opp["score"], opp["rsi"], opp["buy_pct"]), "timestamp": datetime.utcnow().isoformat(), "auto": True}
        actions.append(action)
        state["history"].insert(0, action)

    state["history"] = state["history"][:200]
    save_agent(state)
    total_pos_val = sum(p["qty"] * p["buy_price"] for p in state["positions"].values())
    return {"actions": actions, "state": state, "portfolio_value": state["capital"] + total_pos_val, "actions_count": len(actions), "daily_trades": state["daily_trades"]}

def scheduler_thread(loop):
    while True:
        now = datetime.utcnow()
        hour = now.hour
        weekday = now.weekday()
        if weekday < 5 and 7 <= hour <= 16:
            print("Auto-analyse planifiee lancee a {}".format(now.isoformat()))
            future = asyncio.run_coroutine_threadsafe(
                run_agent_logic(ALL_TICKERS, min_score=7.2, min_daily_trades=3),
                loop
            )
            try:
                result = future.result(timeout=600)
                print("Auto-analyse terminee - {} actions - {} trades aujourd hui".format(result["actions_count"], result["daily_trades"]))
            except Exception as e:
                print("Erreur auto-analyse: {}".format(e))
        time.sleep(3600)

@app.on_event("startup")
async def startup():
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=scheduler_thread, args=(loop,), daemon=True)
    t.start()
    print("Agent planificateur demarre - analyse automatique toutes les heures 9h-18h")

@app.get("/health")
async def health():
    state = load_agent()
    return {"status": "ok", "auto_runs": state.get("auto_runs", 0), "daily_trades": state.get("daily_trades", 0), "last_run": state.get("last_run")}

@app.get("/api/analyze/{ticker:path}")
async def analyze(ticker: str):
    import importlib
    import app.api.routes
    importlib.reload(app.api.routes)
    from app.api.routes import analyze_ticker
    return await analyze_ticker(ticker)

@app.get("/api/history/{ticker:path}")
async def history(ticker: str, period: str = "2y", interval: str = "1d"):
    import yfinance as yf, math
    t = yf.Ticker(ticker)
    hist = t.history(period=period, interval=interval)
    if hist.empty:
        return {"data": []}
    def clean(v):
        if v is None: return None
        try:
            if isinstance(v, float) and (math.isnan(v) or math.isinf(v)): return None
        except: pass
        return v
    return {"ticker": ticker, "data": [{"date": str(idx)[:10], "open": clean(round(float(row["Open"]),2)), "high": clean(round(float(row["High"]),2)), "low": clean(round(float(row["Low"]),2)), "close": clean(round(float(row["Close"]),2)), "volume": int(row["Volume"])} for idx, row in hist.iterrows()]}

@app.get("/api/search")
async def search(q: str):
    import yfinance as yf
    try:
        s = yf.Search(q, max_results=8)
        return {"results": [{"ticker": r.get("symbol",""), "name": r.get("longname") or r.get("shortname",""), "type": r.get("quoteType",""), "exchange": r.get("exchange","")} for r in (s.quotes or [])]}
    except:
        return {"results": []}

@app.get("/api/scanner/{market}")
async def scanner(market: str):
    from app.api.routes import analyze_ticker
    if market == "cac40": tickers = CAC40
    elif market == "nasdaq": tickers = NASDAQ100
    elif market == "sp500": tickers = SP500_TOP
    else: return {"error": "Marche inconnu"}
    results = []
    for ticker in tickers:
        try:
            data = await analyze_ticker(ticker)
            results.append({"ticker": ticker, "name": data["name"], "price": data["price"]["current"], "change_24h": data["price"]["change_24h"], "score": data["scoring"]["global_score"], "recommendation": data["scoring"]["recommendation"], "rsi": data["technical"]["rsi"], "macd": data["technical"]["macd"]["value"], "adx": data["technical"]["adx"]["value"], "pe": data["fundamental"]["pe_ratio"], "revenue_growth": data["fundamental"]["revenue_growth"], "buy_pct": data["analysts"]["buy_pct"], "beta": data["risk"]["beta"]})
        except Exception as e:
            results.append({"ticker": ticker, "name": ticker, "error": str(e), "score": 0})
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return {"market": market, "total": len(results), "results": results}

@app.get("/api/agent/state")
async def agent_state():
    return load_agent()

@app.post("/api/agent/reset")
async def agent_reset(capital: float = 20000.0):
    state = {"capital": capital, "initial_capital": capital, "positions": {}, "history": [], "created_at": datetime.utcnow().isoformat(), "last_run": None, "total_trades": 0, "winning_trades": 0, "daily_trades": 0, "last_trade_date": None, "auto_runs": 0}
    save_agent(state)
    return state

@app.post("/api/agent/run")
async def agent_run(tickers: str = "AAPL,MSFT,NVDA,TSLA,AMZN,META,GOOGL,SPY,SU.PA,MC.PA,TTE.PA,BNP.PA"):
    ticker_list = [t.strip() for t in tickers.split(",")]
    return await run_agent_logic(ticker_list)

@app.post("/api/agent/run_full")
async def agent_run_full():
    return await run_agent_logic(ALL_TICKERS, min_score=7.2, min_daily_trades=3)
@app.get("/api/congress/trades")
async def congress_trades(days: int = 30):
    from app.api.congress import get_congress_trades
    trades = await get_congress_trades(days_back=days)
    return {"trades": trades, "total": len(trades)}

@app.get("/api/congress/opportunities")
async def congress_opportunities():
    from app.api.congress import get_congress_trades, analyze_congress_opportunities
    trades = await get_congress_trades(days_back=60)
    opportunities = await analyze_congress_opportunities(trades)
    return {"opportunities": opportunities, "total": len(opportunities)}

@app.get("/api/ipo/upcoming")
async def upcoming_ipos():
    from app.api.congress import get_upcoming_ipos
    ipos = await get_upcoming_ipos()
    return {"ipos": ipos, "total": len(ipos)}

@app.get("/")
async def root():
    return HTMLResponse("""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>TradingIA</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;background:#0a0a0f;color:#e0e0e0;min-height:100vh}
.top{background:#111118;padding:12px 20px;display:flex;align-items:center;gap:16px;border-bottom:1px solid #222;flex-wrap:wrap}
.top b{font-size:18px;color:#fff;white-space:nowrap}
.search-wrap{position:relative;flex:1;max-width:420px}
.search-wrap input{width:100%;padding:8px 14px;border:1px solid #333;border-radius:8px;font-size:14px;background:#1a1a24;color:#fff}
.search-wrap input::placeholder{color:#555}
#suggestions{position:absolute;top:38px;left:0;right:0;background:#1a1a24;border:1px solid #333;border-radius:8px;z-index:100;display:none;max-height:260px;overflow-y:auto}
.suggestion{padding:10px 14px;cursor:pointer;border-bottom:1px solid #222;display:flex;justify-content:space-between;align-items:center}
.suggestion:hover{background:#222}
.sug-ticker{font-weight:600;color:#1D9E75;font-size:13px}
.sug-name{font-size:12px;color:#888;margin-top:2px}
.sug-type{font-size:11px;color:#444;background:#111;padding:2px 6px;border-radius:4px}
.tabs{display:flex;gap:0;border-bottom:1px solid #222;background:#111118;padding:0 20px}
.tab{padding:12px 20px;font-size:13px;cursor:pointer;border-bottom:2px solid transparent;color:#555;transition:all 0.15s}
.tab:hover{color:#aaa}
.tab.active{color:#1D9E75;border-bottom-color:#1D9E75;font-weight:500}
.tab-content{display:none;padding:20px;max-width:1400px;margin:0 auto}
.tab-content.active{display:block}
button{padding:6px 14px;border-radius:20px;border:1px solid #333;background:#1a1a24;color:#aaa;cursor:pointer;font-size:13px;transition:all 0.15s;white-space:nowrap}
button:hover{border-color:#1D9E75;color:#1D9E75}
button.active{background:#1D9E75;color:#fff;border-color:#1D9E75}
.btn-primary{background:#1D9E75;color:#fff;border-color:#1D9E75;padding:8px 20px;border-radius:8px;font-size:14px}
.btn-primary:hover{background:#179060}
.card{background:#111118;border-radius:12px;padding:20px;border:1px solid #1e1e2e;margin-bottom:16px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #1a1a2e;font-size:13px}
.row:last-child{border-bottom:none}
.label{color:#666}
.stitle{font-size:11px;font-weight:600;color:#555;margin-bottom:14px;text-transform:uppercase;letter-spacing:0.08em}
.score-big{font-size:64px;font-weight:500;line-height:1}
.rec-box{padding:16px 20px;border-radius:10px;font-size:18px;font-weight:600;margin-bottom:14px}
.analyst-box{background:#0d0d15;border-radius:8px;padding:12px;text-align:center;border:1px solid #1e1e2e}
.bar-bg{height:5px;background:#1a1a2e;border-radius:3px;margin-top:3px}
.bar-fill{height:5px;border-radius:3px}
.ind-score{font-size:11px;padding:2px 8px;border-radius:12px;font-weight:500}
.bull{background:#1a3a2a;color:#4ade80}
.bear{background:#3a1a1a;color:#f87171}
.neut{background:#1e1e2e;color:#888}
.scanner-row{display:grid;grid-template-columns:120px 1fr 100px 80px 80px 100px 80px;gap:12px;align-items:center;padding:10px 14px;border-bottom:1px solid #1a1a2e;font-size:13px;cursor:pointer;transition:background 0.1s}
.scanner-row:hover{background:#1a1a24}
.scanner-header{display:grid;grid-template-columns:120px 1fr 100px 80px 80px 100px 80px;gap:12px;padding:8px 14px;font-size:11px;color:#555;text-transform:uppercase;letter-spacing:0.06em;border-bottom:1px solid #222}
.rec-badge{padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;text-align:center}
.news-item{padding:12px 0;border-bottom:1px solid #1a1a2e}
.news-item:last-child{border-bottom:none}
.news-title a{color:#e0e0e0;text-decoration:none;font-size:13px;line-height:1.4}
.news-title a:hover{color:#1D9E75}
.news-meta{font-size:11px;color:#555;margin-top:3px}
.pattern-item{background:#0d0d15;border-radius:8px;padding:14px;border:1px solid #1e1e2e;margin-bottom:10px}
input[type=text],input[type=number]{background:#1a1a24;border:1px solid #333;border-radius:8px;color:#fff;padding:8px 12px;font-size:13px;width:100%}
.portfolio-row{display:grid;grid-template-columns:100px 1fr 100px 100px 100px 120px 80px;gap:10px;align-items:center;padding:10px 14px;border-bottom:1px solid #1a1a2e;font-size:13px}
.portfolio-header{display:grid;grid-template-columns:100px 1fr 100px 100px 100px 120px 80px;gap:10px;padding:8px 14px;font-size:11px;color:#555;text-transform:uppercase;border-bottom:1px solid #222}
</style>
</head>
<body>

<div class="top">
  <b>📈 TradingIA</b>
	<a href="/agent" style="padding:6px 14px;border-radius:8px;border:1px solid #1D9E75;color:#1D9E75;font-size:13px;text-decoration:none">🤖 Agent IA</a>
  <div class="search-wrap">
    <input id="searchInput" placeholder="Rechercher : Apple, Schneider, BTC..." oninput="onSearch(this.value)" onkeydown="onSearchKey(event)">
    <div id="suggestions"></div>
  </div>
  <div id="watchlist" style="display:flex;gap:8px;flex-wrap:wrap"></div>
</div>

<div class="tabs">
  <div class="tab active" onclick="showTab('analyse')">🔍 Analyse</div>
  <div class="tab" onclick="showTab('scanner')">📡 Scanner Marché</div>
  <div class="tab" onclick="showTab('portfolio')">💼 Mon Portefeuille</div>
<div class="tab" onclick="showTab('portfolio')">💼 Mon Portefeuille</div>
<div class="tab" onclick="showTab('politics')">🏛️ Congrès & IPO</div>
</div>

<!-- ONGLET ANALYSE -->
<div class="tab-content active" id="tab-analyse">
  <div id="loading">Sélectionne un ticker pour démarrer l'analyse...</div>
  <div id="error" style="display:none;color:#f87171;text-align:center;padding:60px"></div>
  <div id="result" style="display:none"></div>
</div>

<!-- ONGLET SCANNER -->
<div class="tab-content" id="tab-scanner">
  <div class="card">
    <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <div class="stitle" style="margin:0">Choisir le marché à analyser :</div>
      <button id="btn-cac40" onclick="runScanner('cac40')" class="btn-primary">🇫🇷 CAC 40</button>
      <button id="btn-nasdaq" onclick="runScanner('nasdaq')">🇺🇸 NASDAQ 100</button>
      <button id="btn-sp500" onclick="runScanner('sp500')">🇺🇸 S&P 500 Top</button>
    </div>
    <div id="scanner-status" style="margin-top:12px;font-size:13px;color:#555"></div>
  </div>
  <div id="scanner-results"></div>
</div>
<!-- ONGLET POLITIQUE & IPO -->
<div class="tab-content" id="tab-politics">
  <div class="card">
    <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">
      <div class="stitle" style="margin:0">Données politiques & marchés privés</div>
      <button class="btn-primary" onclick="loadCongressTrades()">🏛️ Charger trades Congrès US</button>
      <button class="btn-primary" onclick="loadIPOs()" style="background:#7c3aed">🚀 IPO à venir</button>
    </div>
    <div id="politics-status" style="margin-top:10px;font-size:13px;color:#555"></div>
  </div>
  <div id="congress-opportunities" style="display:none" class="card">
    <div class="stitle" style="color:#4ade80">🎯 Opportunités détectées — Tickers achetés par le Congrès + Score IA élevé</div>
    <div id="congress-opp-list"></div>
  </div>
  <div id="congress-trades-wrap" style="display:none" class="card">
    <div class="stitle">📋 Derniers trades déclarés — Membres du Congrès US</div>
    <div style="display:grid;grid-template-columns:150px 80px 1fr 120px 150px 100px;gap:10px;padding:8px 14px;font-size:11px;color:#555;text-transform:uppercase;border-bottom:1px solid #222">
      <span>Élu</span><span>Ticker</span><span>Description</span><span>Type</span><span>Montant</span><span>Date</span>
    </div>
    <div id="congress-trades-list"></div>
  </div>
  <div id="ipo-wrap" style="display:none" class="card">
    <div class="stitle">🚀 IPO & Entreprises Pré-IPO Surveillées</div>
    <div style="font-size:12px;color:#555;margin-bottom:14px">Entreprises en attente d'introduction en bourse — données indicatives</div>
    <div id="ipo-list"></div>
  </div>
</div>

<!-- ONGLET PORTEFEUILLE -->
<div class="tab-content" id="tab-portfolio">
  <div class="card">
    <div class="stitle">Ajouter une action</div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:10px;align-items:end">
      <div>
        <div style="font-size:12px;color:#555;margin-bottom:6px">Ticker</div>
        <input type="text" id="pf-ticker" placeholder="AAPL, SU.PA...">
      </div>
      <div>
        <div style="font-size:12px;color:#555;margin-bottom:6px">Prix d'achat ($)</div>
        <input type="number" id="pf-price" placeholder="150.00" step="0.01">
      </div>
      <div>
        <div style="font-size:12px;color:#555;margin-bottom:6px">Quantité</div>
        <input type="number" id="pf-qty" placeholder="10" step="1">
      </div>
      <button class="btn-primary" onclick="addToPortfolio()">+ Ajouter</button>
    </div>
  </div>
  <div id="portfolio-summary" style="display:none" class="card">
    <div style="display:flex;gap:20px;flex-wrap:wrap">
      <div><div class="stitle">Valeur totale</div><div style="font-size:28px;font-weight:600;color:#fff" id="pf-total">$0</div></div>
      <div><div class="stitle">Investi</div><div style="font-size:28px;font-weight:600;color:#888" id="pf-invested">$0</div></div>
      <div><div class="stitle">P&L</div><div style="font-size:28px;font-weight:600" id="pf-pnl">$0</div></div>
      <div><div class="stitle">Performance</div><div style="font-size:28px;font-weight:600" id="pf-perf">0%</div></div>
    </div>
  </div>
  <div id="portfolio-list"></div>
</div>

<script>
const API = 'http://localhost:8000';
const WL = ['AAPL','TSLA','NVDA','SPY','MSFT','SU.PA','BTC-USD'];
let charts={}, searchTimer=null, scannerData=[], portfolio=JSON.parse(localStorage.getItem('portfolio')||'[]');

// Tabs
async function loadCongressTrades() {
  document.getElementById('politics-status').textContent = '⏳ Chargement des trades du Congrès... (peut prendre 30-60 sec)';
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
    document.getElementById('politics-status').textContent = '✅ ' + trades.length + ' trades chargés · ' + opps.length + ' opportunités détectées';

    if(opps.length > 0) {
      document.getElementById('congress-opp-list').innerHTML = opps.map(o => `
        <div class="row" style="cursor:pointer" onclick="showTab('analyse');loadTicker('${o.ticker}')">
          <div style="flex:1">
            <span style="font-weight:600;color:#1D9E75">${o.ticker}</span>
            <span style="font-size:12px;color:#888;margin-left:8px">${o.name}</span>
            <span style="font-size:11px;color:#555;margin-left:8px">${o.congress_buys} achat(s) · ${(o.buyers||[]).slice(0,2).join(', ')}</span>
          </div>
          <div style="display:flex;gap:12px;align-items:center">
            <span style="font-size:12px;color:#555">Dernier: ${o.last_trade_date}</span>
            <span style="font-weight:600;color:${sc(o.score)}">${o.score}/10</span>
            ${recBadge(o.recommendation)}
          </div>
        </div>`).join('');
      document.getElementById('congress-opportunities').style.display = 'block';
    }

    document.getElementById('congress-trades-list').innerHTML = trades.slice(0, 50).map(t => {
      const typeColor = t.type && t.type.toLowerCase().includes('purchase') ? '#4ade80' : '#f87171';
      return `<div style="display:grid;grid-template-columns:150px 80px 1fr 120px 150px 100px;gap:10px;padding:8px 14px;border-bottom:1px solid #1a1a2e;font-size:12px;align-items:center">
        <span style="color:#aaa;font-size:11px">${t.representative}</span>
        <span style="font-weight:600;color:#1D9E75;cursor:pointer" onclick="showTab('analyse');loadTicker('${t.ticker}')">${t.ticker}</span>
        <span style="color:#666;font-size:11px">${t.asset_description}</span>
        <span style="color:${typeColor};font-weight:500">${t.type}</span>
        <span style="color:#888">${t.amount}</span>
        <span style="color:#555">${t.date}</span>
      </div>`;
    }).join('');
    document.getElementById('congress-trades-wrap').style.display = 'block';
  } catch(e) {
    document.getElementById('politics-status').textContent = '❌ Erreur : ' + e.message;
  }
}

async function loadIPOs() {
  document.getElementById('politics-status').textContent = '⏳ Chargement des IPO...';
  document.getElementById('ipo-wrap').style.display = 'none';
  try {
    const r = await fetch(API + '/api/ipo/upcoming');
    const d = await r.json();
    const ipos = d.ipos || [];
    document.getElementById('politics-status').textContent = '✅ ' + ipos.length + ' IPO/pré-IPO chargées';
    const statusColors = {'Confirme':'#4ade80','En attente':'#facc15','Rumeur':'#888'};
    document.getElementById('ipo-list').innerHTML = ipos.map(ipo => `
      <div style="background:#0d0d15;border-radius:8px;padding:14px;border:1px solid #1e1e2e;margin-bottom:10px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
          <div>
            <div style="font-size:16px;font-weight:600;color:#fff">${ipo.company}</div>
            <div style="font-size:12px;color:#555;margin-top:3px">Ticker prévu : <span style="color:#1D9E75;font-weight:600">${ipo.ticker}</span> · ${ipo.exchange}</div>
          </div>
          <div style="text-align:right">
            <div style="font-size:13px;color:#fff;font-weight:500">${ipo.price_range}</div>
            <div style="font-size:11px;color:#555">${ipo.currency}</div>
          </div>
        </div>
        <div style="display:flex;gap:12px;margin-top:10px;flex-wrap:wrap">
          <span style="background:#1a1a2e;color:#888;padding:3px 10px;border-radius:20px;font-size:11px">📅 ${ipo.date}</span>
          <span style="background:#1a1a2e;color:#888;padding:3px 10px;border-radius:20px;font-size:11px">📊 ${ipo.shares} actions</span>
          <span style="background:#1a1a2e;color:${statusColors[ipo.status]||'#888'};padding:3px 10px;border-radius:20px;font-size:11px;font-weight:500">${ipo.status || 'N/A'}</span>
        </div>
      </div>`).join('');
    document.getElementById('ipo-wrap').style.display = 'block';
  } catch(e) {
    document.getElementById('politics-status').textContent = '❌ Erreur : ' + e.message;
  }
}
function showTab(name) {
  document.querySelectorAll('.tab').forEach((t,i)=>t.classList.toggle('active',['analyse','scanner','portfolio','politics'][i]===name));
  document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  if(name==='portfolio') renderPortfolio();
}

// Watchlist
const wlDiv=document.getElementById('watchlist');
WL.forEach(t=>{const btn=document.createElement('button');btn.textContent=t;btn.id='btn-'+t;btn.onclick=()=>{showTab('analyse');loadTicker(t);};wlDiv.appendChild(btn);});

// Recherche
async function onSearch(val) {
  clearTimeout(searchTimer);
  if(val.length<2){document.getElementById('suggestions').style.display='none';return;}
  searchTimer=setTimeout(async()=>{
    try{const r=await fetch(API+'/api/search?q='+encodeURIComponent(val));const d=await r.json();showSuggestions(d.results||[]);}catch(e){}
  },300);
}
function showSuggestions(results) {
  const el=document.getElementById('suggestions');
  if(!results.length){el.style.display='none';return;}
  el.innerHTML=results.map(r=>`<div class="suggestion" onclick="showTab('analyse');loadTicker('${r.ticker}');document.getElementById('searchInput').value='';document.getElementById('suggestions').style.display='none'"><div><div style="display:flex;align-items:center;gap:8px"><span class="sug-ticker">${r.ticker}</span><span class="sug-type">${r.type}</span></div><div class="sug-name">${r.name}</div></div><span style="font-size:11px;color:#444">${r.exchange}</span></div>`).join('');
  el.style.display='block';
}
function onSearchKey(e) {
  if(e.key==='Enter'){const v=e.target.value.trim().toUpperCase();if(v){showTab('analyse');loadTicker(v);e.target.value='';document.getElementById('suggestions').style.display='none';}}
  if(e.key==='Escape') document.getElementById('suggestions').style.display='none';
}
document.addEventListener('click',e=>{if(!e.target.closest('.search-wrap')) document.getElementById('suggestions').style.display='none';});

// Helpers
function sc(s){return s>=7?'#4ade80':s>=5?'#facc15':'#f87171';}
function n2(v,s=''){return v!=null?Number(v).toFixed(2)+s:'N/A';}
function n1(v,s=''){return v!=null?Number(v).toFixed(1)+s:'N/A';}
function n0(v,s=''){return v!=null?Number(v).toFixed(0)+s:'N/A';}
function recBadge(rec){const m={buy:['ACHETER','#4ade80','#0d2a1a'],hold:['CONSERVER','#facc15','#2a2200'],sell:['VENDRE','#f87171','#2a0d0d'],wait:['ATTENDRE','#888','#1a1a2e']};const[l,c,b]=m[rec]||m.wait;return `<span class="rec-badge" style="background:${b};color:${c}">${l}</span>`;}

// ══════════════════════════════════════════════
// ONGLET ANALYSE
// ══════════════════════════════════════════════
async function loadTicker(ticker) {
  WL.forEach(t=>{const b=document.getElementById('btn-'+t);if(b) b.className=t===ticker?'active':'';});
  document.getElementById('loading').style.display='block';
  document.getElementById('loading').textContent='⏳ Analyse de '+ticker+' en cours... (30-60 sec)';
  document.getElementById('error').style.display='none';
  document.getElementById('result').style.display='none';
  Object.values(charts).forEach(c=>c.destroy()); charts={};
  try{
    const [dataR,histR]=await Promise.all([fetch(API+'/api/analyze/'+encodeURIComponent(ticker)),fetch(API+'/api/history/'+encodeURIComponent(ticker)+'?period=2y&interval=1d')]);
    if(!dataR.ok) throw new Error('Ticker introuvable : '+ticker);
    const d=await dataR.json(), histD=histR.ok?await histR.json():null;
    showResult(d,histD);
  }catch(e){document.getElementById('loading').style.display='none';document.getElementById('error').style.display='block';document.getElementById('error').textContent='❌ '+e.message;}
}

function indScore(name,val,d){
  let score=5,label='Neutre',cls='neut';
  if(val===null||val===undefined) return{score,label,cls};
  if(name==='RSI'){if(val<25){score=8;label='Survente forte';cls='bull';}else if(val<35){score=7;label='Survente';cls='bull';}else if(val>=40&&val<=60){score=6;label='Neutre';cls='neut';}else if(val>60&&val<=70){score=7;label='Haussier';cls='bull';}else{score=3;label='Surachat';cls='bear';}}
  else if(name==='MACD'){const h=d.technical?.macd?.histogram||0;if(val>0&&h>0){score=8;label='Haussier fort';cls='bull';}else if(val>0){score=6;label='Haussier';cls='bull';}else if(val<0&&h<0){score=2;label='Baissier fort';cls='bear';}else{score=4;label='Baissier';cls='bear';}}
  else if(name==='ADX'){if(val>40){score=9;label='Tendance forte';cls='bull';}else if(val>25){score=6;label='Modérée';cls='neut';}else{score=3;label='Faible';cls='bear';}}
  else if(name==='Stoch'){if(val<20){score=8;label='Survente';cls='bull';}else if(val>80){score=2;label='Surachat';cls='bear';}else{score=5;label='Neutre';cls='neut';}}
  else if(name==='Boll'){const p=d.price?.current||0,u=d.technical?.bollinger?.upper||0,l=d.technical?.bollinger?.lower||0;if(p>u){score=2;label='Hors bande haute';cls='bear';}else if(p<l){score=8;label='Hors bande basse';cls='bull';}else{score=5;label='Dans les bandes';cls='neut';}}
  else if(name==='GC'){if(val){score=8;label='Golden Cross';cls='bull';}else{score=2;label='Death Cross';cls='bear';}}
  else if(name==='Ichi'){if(val){score=7;label='Au-dessus nuage';cls='bull';}else{score=3;label='Sous le nuage';cls='bear';}}
  else if(name==='SMA'){const ma=d.technical?.moving_averages||{};const ab=[ma.price_above_sma20,ma.price_above_sma50,ma.price_above_sma200].filter(Boolean).length;if(ab===3){score=9;label='Au-dessus 3 MA';cls='bull';}else if(ab===2){score=7;label='Au-dessus 2 MA';cls='bull';}else if(ab===1){score=4;label='Sous 2 MA';cls='bear';}else{score=2;label='Sous 3 MA';cls='bear';}}
  return{score,label,cls};
}

function detectPatterns(histData){
  if(!histData?.data||histData.data.length<120) return[];
  const prices=histData.data.map(d=>d.close).filter(Boolean);
  const n=prices.length,ws=60,recent=prices.slice(-ws);
  function norm(arr){const mn=Math.min(...arr),mx=Math.max(...arr);return arr.map(v=>(v-mn)/(mx-mn||1));}
  function sim(a,b){let dot=0,na=0,nb=0;for(let i=0;i<a.length;i++){dot+=a[i]*b[i];na+=a[i]**2;nb+=b[i]**2;}return dot/(Math.sqrt(na)*Math.sqrt(nb)||1);}
  const rNorm=norm(recent),matches=[];
  for(let i=0;i<n-ws*2;i++){const w=prices.slice(i,i+ws),s=sim(rNorm,norm(w));if(s>0.85){const fut=prices.slice(i+ws,i+ws+30);if(fut.length>=20){const fr=(fut[fut.length-1]-fut[0])/fut[0]*100;matches.push({s,fr,startIdx:i,date:histData.data[i]?.date,wp:w,fp:fut});}}}
  matches.sort((a,b)=>b.s-a.s);
  const filtered=[];
  for(const m of matches){const tooClose=filtered.some(f=>Math.abs(f.startIdx-m.startIdx)<30);if(!tooClose)filtered.push(m);if(filtered.length>=3)break;}
  return filtered.map((m,i)=>({idx:i,sim:Math.round(m.s*100),fr:m.fr,bullish:m.fr>0,date:m.date?m.date.slice(0,7):'Historique',wp:m.wp,fp:m.fp,rp:recent}));
}

function buildCharts(histData){
  const data=histData?.data?.slice(-180)||[];
  if(!data.length) return;
  const labels=data.map(d=>d.date.slice(5));
  const closes=data.map(d=>d.close);
  const period=20;const bbU=[],bbL=[],sma20=[];
  for(let i=0;i<closes.length;i++){if(i<period-1){bbU.push(null);bbL.push(null);sma20.push(null);}else{const sl=closes.slice(i-period+1,i+1),mn=sl.reduce((a,b)=>a+b,0)/period,st=Math.sqrt(sl.map(x=>(x-mn)**2).reduce((a,b)=>a+b,0)/period);sma20.push(mn);bbU.push(mn+2*st);bbL.push(mn-2*st);}}
  charts['main']=new Chart(document.getElementById('mainChart'),{type:'line',data:{labels,datasets:[{label:'Prix',data:closes,borderColor:'#4ade80',borderWidth:2,pointRadius:0,tension:0.2,fill:false},{label:'SMA20',data:sma20,borderColor:'#facc15',borderWidth:1,pointRadius:0,borderDash:[4,2],fill:false},{label:'BB Haut',data:bbU,borderColor:'#444',borderWidth:1,pointRadius:0,fill:false},{label:'BB Bas',data:bbL,borderColor:'#444',borderWidth:1,pointRadius:0,fill:'-1',backgroundColor:'rgba(255,255,255,0.02)'}]},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{labels:{color:'#555',font:{size:10}}}},scales:{x:{grid:{color:'#1a1a2e'},ticks:{color:'#555',maxTicksLimit:8,font:{size:10}}},y:{grid:{color:'#1a1a2e'},ticks:{color:'#555',font:{size:10},callback:v=>'$'+v.toLocaleString()}}}}});
  const rsiData=[];for(let i=0;i<closes.length;i++){if(i<14){rsiData.push(null);continue;}const ch=closes.slice(i-14+1,i+1).map((v,j,a)=>j===0?0:v-a[j-1]),g=ch.filter(v=>v>0).reduce((a,b)=>a+b,0)/14,l=Math.abs(ch.filter(v=>v<0).reduce((a,b)=>a+b,0))/14;rsiData.push(l===0?100:Math.round(100-100/(1+g/l)));}
  charts['rsi']=new Chart(document.getElementById('rsiChart'),{type:'line',data:{labels,datasets:[{label:'RSI',data:rsiData,borderColor:'#a78bfa',borderWidth:1.5,pointRadius:0,fill:false},{label:'70',data:Array(labels.length).fill(70),borderColor:'#f87171',borderWidth:1,borderDash:[4,2],pointRadius:0,fill:false},{label:'30',data:Array(labels.length).fill(30),borderColor:'#4ade80',borderWidth:1,borderDash:[4,2],pointRadius:0,fill:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#555',font:{size:10}}}},scales:{x:{display:false},y:{grid:{color:'#1a1a2e'},ticks:{color:'#555',font:{size:10}},min:0,max:100}}}});
  function ema(arr,p){let k=2/(p+1),r=[arr[0]];for(let i=1;i<arr.length;i++)r.push(arr[i]*k+r[i-1]*(1-k));return r;}
  const e12=ema(closes,12),e26=ema(closes,26),ml=closes.map((_,i)=>e12[i]-e26[i]),sig=ema(ml,9),hist=ml.map((v,i)=>v-sig[i]);
  charts['macd']=new Chart(document.getElementById('macdChart'),{type:'bar',data:{labels,datasets:[{label:'Hist',data:hist,backgroundColor:hist.map(v=>v>=0?'rgba(74,222,128,0.5)':'rgba(248,113,113,0.5)'),order:2},{type:'line',label:'MACD',data:ml,borderColor:'#4ade80',borderWidth:1.5,pointRadius:0,fill:false,order:1},{type:'line',label:'Signal',data:sig,borderColor:'#f87171',borderWidth:1.5,pointRadius:0,fill:false,order:1}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#555',font:{size:10}}}},scales:{x:{display:false},y:{grid:{color:'#1a1a2e'},ticks:{color:'#555',font:{size:10}}}}}});
}

function showResult(d,histData){
  document.getElementById('loading').style.display='none';
  const rec=d.scoring?.recommendation;
  const recMap={buy:['🟢 ACHETER','#4ade80','#0d2a1a'],hold:['🟡 CONSERVER','#facc15','#2a2200'],sell:['🔴 VENDRE','#f87171','#2a0d0d'],wait:['⚪ ATTENDRE','#888','#1a1a2e']};
  const [recLabel,recColor,recBg]=recMap[rec]||recMap.wait;
  const score=d.scoring?.global_score;
  const patterns=detectPatterns(histData);
  const divPS=d.fundamental?.dividend_per_share, divY=d.fundamental?.dividend_yield;

  const inds=[
    {name:'RSI (14)',key:'RSI',val:d.technical?.rsi,display:n1(d.technical?.rsi)},
    {name:'MACD',key:'MACD',val:d.technical?.macd?.value,display:n2(d.technical?.macd?.value)},
    {name:'ADX',key:'ADX',val:d.technical?.adx?.value,display:n1(d.technical?.adx?.value)},
    {name:'Stoch K',key:'Stoch',val:d.technical?.stochastic?.k,display:n1(d.technical?.stochastic?.k)},
    {name:'Bollinger',key:'Boll',val:d.technical?.bollinger?.upper,display:'H:'+n0(d.technical?.bollinger?.upper)},
    {name:'SMA Trend',key:'SMA',val:d.technical?.moving_averages?.sma_50,display:'SMA50:'+n0(d.technical?.moving_averages?.sma_50)},
    {name:'Golden Cross',key:'GC',val:d.technical?.moving_averages?.golden_cross,display:d.technical?.moving_averages?.golden_cross?'Oui':'Non'},
    {name:'Ichimoku',key:'Ichi',val:d.technical?.ichimoku?.price_above_cloud,display:d.technical?.ichimoku?.price_above_cloud?'Au-dessus':'Sous'},
  ].map(ind=>({...ind,...indScore(ind.key,ind.val,d)}));

  let patternHTML='<div style="color:#555;font-size:13px;text-align:center;padding:20px">Pas assez de données historiques (2 ans minimum)</div>';
  if(patterns.length>0){
    const avg=patterns.reduce((s,p)=>s+p.fr,0)/patterns.length;
    const bc=patterns.filter(p=>p.bullish).length;
    const sc2=avg>=0?'#4ade80':'#f87171',bg2=avg>=0?'#0d2a1a':'#2a0d0d';
    patternHTML=`<div style="background:${bg2};border:1px solid ${sc2}33;border-radius:10px;padding:16px;margin-bottom:14px">
      <div style="font-size:14px;font-weight:600;color:${sc2};margin-bottom:6px">${bc>=2?'📈 Scénario majoritairement haussier':'📉 Scénario majoritairement baissier'}</div>
      <div style="font-size:13px;color:#aaa">${patterns.length} période(s) similaire(s) · Rendement moyen +30j : <span style="color:${sc2};font-weight:600">${avg>=0?'+':''}${avg.toFixed(1)}%</span></div>
      <div style="font-size:11px;color:#444;margin-top:8px">⚠️ Analyse historique uniquement</div>
    </div>
    ${patterns.map(p=>{const pc=p.bullish?'#4ade80':'#f87171';return`<div class="pattern-item">
      <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:6px">Période similaire — ${p.date}</div>
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-size:12px;color:#555">Similarité : <span style="color:${pc};font-weight:600">${p.sim}%</span></span>
        <span style="font-size:12px;color:#555">Perf +30j : <span style="color:${pc};font-weight:600">${p.fr>=0?'+':''}${p.fr.toFixed(1)}%</span></span>
      </div>
      <div style="height:4px;background:#1a1a2e;border-radius:3px"><div style="height:4px;width:${p.sim}%;background:${pc};border-radius:3px"></div></div>
      <div style="position:relative;height:70px;margin-top:10px"><canvas id="pc-${p.idx}"></canvas></div>
    </div>`;}).join('')}`;
  }

  const newsHTML=(d.news||[]).filter(n=>n.title).length>0
    ?(d.news||[]).filter(n=>n.title).map(n=>`<div class="news-item"><div class="news-title"><a href="${n.link}" target="_blank">${n.title}</a></div><div class="news-meta">${n.publisher}${n.date?' · '+n.date:''}</div></div>`).join('')
    :'<div style="color:#555;font-size:13px;padding:10px 0">Aucune actualité disponible</div>';

  document.getElementById('result').innerHTML=`
    <div class="card" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px">
      <div>
        <div style="font-size:24px;font-weight:600;color:#fff">${d.name}</div>
        <div style="color:#555;margin-top:4px;font-size:13px">${d.ticker} · ${d.sector}</div>
        <div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">
          <span style="background:${(d.price?.change_24h||0)>=0?'#0d2a1a':'#2a0d0d'};color:${(d.price?.change_24h||0)>=0?'#4ade80':'#f87171'};padding:3px 10px;border-radius:20px;font-size:12px">${(d.price?.change_24h||0)>=0?'+':''}${n2(d.price?.change_24h)}% 24h</span>
          <span style="background:#1a1a2e;color:#888;padding:3px 10px;border-radius:20px;font-size:12px">Vol. ${(d.price?.volume||0).toLocaleString()}</span>
          <span style="background:#1a1a2e;color:#888;padding:3px 10px;border-radius:20px;font-size:12px">Cap. ${d.price?.market_cap?(d.price.market_cap/1e12).toFixed(2)+'T':'N/A'}</span>
          ${divPS?`<span style="background:#1a3a2a;color:#4ade80;padding:3px 10px;border-radius:20px;font-size:12px">Div. ${n2(divPS)}$/action${divY?' ('+( divY*100).toFixed(2)+'%)':''}</span>`:''}
        </div>
      </div>
      <div style="text-align:right">
        <div style="font-size:40px;font-weight:500;color:#fff">$${n2(d.price?.current)}</div>
        <button onclick="addTickerToPortfolio('${d.ticker}')" style="margin-top:8px;font-size:12px">+ Ajouter au portefeuille</button>
      </div>
    </div>
    <div class="grid2">
      <div class="card">
        <div class="stitle">Score IA Global</div>
        <div class="score-big" style="color:${sc(score)}">${score}<span style="font-size:24px;color:#333">/10</span></div>
        <div style="margin-top:16px;display:flex;flex-direction:column;gap:8px">
          ${Object.entries(d.scoring?.breakdown||{}).map(([k,v])=>`<div><div style="display:flex;justify-content:space-between;font-size:12px;color:#555;margin-bottom:3px"><span>${k} (${v.weight})</span><span style="color:${sc(v.score)}">${v.score}/10</span></div><div class="bar-bg"><div class="bar-fill" style="width:${v.score*10}%;background:${sc(v.score)}"></div></div></div>`).join('')}
        </div>
      </div>
      <div class="card">
        <div class="stitle">Recommandation IA</div>
        <div class="rec-box" style="background:${recBg};color:${recColor}">${recLabel}</div>
        <div style="font-size:13px;color:#555;margin-bottom:14px">${d.scoring?.recommendation_reason}</div>
        <div style="font-size:12px;font-weight:600;color:#4ade80;margin-bottom:6px">Points forts</div>
        ${(d.scoring?.forces||[]).map(f=>`<div style="font-size:12px;color:#555;margin-bottom:3px">+ ${f}</div>`).join('')}
        <div style="font-size:12px;font-weight:600;color:#f87171;margin-top:10px;margin-bottom:6px">Risques</div>
        ${(d.scoring?.risks||[]).map(r=>`<div style="font-size:12px;color:#555;margin-bottom:3px">- ${r}</div>`).join('')}
      </div>
    </div>
    <div class="card">
      <div class="stitle">📊 Prix + Bollinger + SMA20</div>
      <div style="position:relative;height:260px"><canvas id="mainChart"></canvas></div>
      <div style="margin-top:14px"><div class="stitle">RSI (14)</div><div style="position:relative;height:90px"><canvas id="rsiChart"></canvas></div></div>
      <div style="margin-top:14px"><div class="stitle">MACD</div><div style="position:relative;height:90px"><canvas id="macdChart"></canvas></div></div>
    </div>
    <div class="card">
      <div class="stitle">Indicateurs Techniques — Notes IA</div>
      <div class="grid4">${inds.map(ind=>`<div style="background:#0d0d15;border-radius:8px;padding:12px;border:1px solid #1e1e2e"><div style="font-size:11px;color:#555;margin-bottom:4px">${ind.name}</div><div style="font-size:15px;font-weight:600;color:#fff;margin-bottom:6px">${ind.display}</div><div style="display:flex;justify-content:space-between;align-items:center"><span class="ind-score ${ind.cls}">${ind.label}</span><span style="font-size:13px;font-weight:600;color:${sc(ind.score)}">${ind.score}/10</span></div><div class="bar-bg" style="margin-top:6px"><div class="bar-fill" style="width:${ind.score*10}%;background:${sc(ind.score)}"></div></div></div>`).join('')}</div>
    </div>
    <div class="grid2">
      <div class="card">
        <div class="stitle">Analyse Fondamentale</div>
        ${[['PER (TTM)',n1(d.fundamental?.pe_ratio)],['PER Forward',n1(d.fundamental?.forward_pe)],['EPS',n2(d.fundamental?.eps,'$')],['Dividende/action',divPS?n2(divPS,'$'):'Aucun'],['Rendement dividende',divY?(divY*100).toFixed(2)+'%':'Aucun'],['Croissance CA',d.fundamental?.revenue_growth!=null?(d.fundamental.revenue_growth*100).toFixed(1)+'%':'N/A'],['Marges nettes',d.fundamental?.profit_margins!=null?(d.fundamental.profit_margins*100).toFixed(1)+'%':'N/A'],['Dette/Capitaux',n2(d.fundamental?.debt_to_equity)],['ROE',d.fundamental?.return_on_equity!=null?(d.fundamental.return_on_equity*100).toFixed(1)+'%':'N/A'],['Free Cash Flow',d.fundamental?.free_cash_flow?(d.fundamental.free_cash_flow/1e9).toFixed(1)+'B$':'N/A']].map(([k,v])=>`<div class="row"><span class="label">${k}</span><span style="font-weight:500;color:#fff">${v}</span></div>`).join('')}
      </div>
      <div>
        <div class="card" style="margin-bottom:16px">
          <div class="stitle">Consensus Analystes</div>
          <div class="grid3" style="margin-bottom:14px">
            <div class="analyst-box"><div style="font-size:26px;font-weight:600;color:#4ade80">${d.analysts?.buy_pct}%</div><div style="font-size:11px;color:#555">Acheter</div></div>
            <div class="analyst-box"><div style="font-size:26px;font-weight:600;color:#facc15">${d.analysts?.hold_pct}%</div><div style="font-size:11px;color:#555">Conserver</div></div>
            <div class="analyst-box"><div style="font-size:26px;font-weight:600;color:#f87171">${d.analysts?.sell_pct}%</div><div style="font-size:11px;color:#555">Vendre</div></div>
          </div>
          ${[['Objectif moyen','$'+n0(d.analysts?.target_mean)],['Objectif haut','$'+n0(d.analysts?.target_high)],['Objectif bas','$'+n0(d.analysts?.target_low)]].map(([k,v])=>`<div class="row"><span class="label">${k}</span><span style="font-weight:500;color:#fff">${v}</span></div>`).join('')}
        </div>
        <div class="card">
          <div class="stitle">Risque & Volatilité</div>
          ${[['Beta',n2(d.risk?.beta)],['Volatilité ann.',n1(d.risk?.std_dev_annual,'%')],['Max Drawdown',n1(d.risk?.max_drawdown,'%')],['Ratio Sharpe',n2(d.risk?.sharpe_ratio)],['VaR 95%',n2(d.risk?.var_95,'%')]].map(([k,v])=>`<div class="row"><span class="label">${k}</span><span style="font-weight:500;color:#fff">${v}</span></div>`).join('')}
        </div>
      </div>
    </div>
    <div class="card">
      <div class="stitle">🤖 Agent IA — Patterns Historiques</div>
      ${patternHTML}
    </div>
    <div class="card">
      <div class="stitle">📰 Actualités</div>
      ${newsHTML}
    </div>
    <div style="text-align:center;color:#333;font-size:11px;padding:10px">Données Yahoo Finance · ⚠️ Pas de conseil financier</div>`;

  document.getElementById('result').style.display='block';
  setTimeout(()=>{
    buildCharts(histData);
    patterns.forEach(p=>{
      const ctx=document.getElementById('pc-'+p.idx);if(!ctx) return;
      function norm(arr){const mn=Math.min(...arr),mx=Math.max(...arr);return arr.map(v=>(v-mn)/(mx-mn||1));}
      charts['p'+p.idx]=new Chart(ctx,{type:'line',data:{labels:[...p.wp.map((_,j)=>j),...p.fp.map((_,j)=>p.wp.length+j)],datasets:[{label:'Passé',data:[...norm(p.wp),...Array(p.fp.length).fill(null)],borderColor:'#555',borderWidth:1.5,pointRadius:0,fill:false},{label:'Suite',data:[...Array(p.wp.length).fill(null),...norm(p.fp)],borderColor:p.bullish?'#4ade80':'#f87171',borderWidth:1.5,pointRadius:0,fill:false,borderDash:[4,2]}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{display:false},y:{display:false}}}});
    });
  },100);
}

// ══════════════════════════════════════════════
// ONGLET SCANNER
// ══════════════════════════════════════════════
let scannerRunning=false;
async function runScanner(market) {
  if(scannerRunning) return;
  scannerRunning=true;
  ['cac40','nasdaq','sp500'].forEach(m=>{const b=document.getElementById('btn-'+m);if(b) b.className=m===market?'btn-primary active':'';});
  document.getElementById('scanner-status').textContent='⏳ Analyse en cours... Cela peut prendre plusieurs minutes.';
  document.getElementById('scanner-results').innerHTML='<div style="color:#555;text-align:center;padding:40px">Analyse de toutes les actions en cours...<br><span style="font-size:12px">Yahoo Finance est interrogé action par action</span></div>';
  try {
    const r=await fetch(API+'/api/scanner/'+market);
    if(!r.ok) throw new Error('Erreur scanner');
    const data=await r.json();
    scannerData=data.results||[];
    renderScanner(scannerData);
    document.getElementById('scanner-status').textContent=`✅ ${scannerData.length} actions analysées`;
  } catch(e) {
    document.getElementById('scanner-status').textContent='❌ Erreur : '+e.message;
  }
  scannerRunning=false;
}

function renderScanner(results) {
  const valid=results.filter(r=>!r.error);
  const top5buy=valid.filter(r=>r.recommendation==='buy').slice(0,5);
  const top5sell=valid.filter(r=>r.recommendation==='sell').slice(0,5);

  const tableRows=results.map(r=>{
    if(r.error) return `<div class="scanner-row" style="opacity:0.3"><span style="font-weight:600;color:#aaa">${r.ticker}</span><span style="color:#555">${r.name}</span><span style="color:#555">Erreur</span><span></span><span></span><span></span><span></span></div>`;
    const chColor=(r.change_24h||0)>=0?'#4ade80':'#f87171';
    return `<div class="scanner-row" onclick="showTab('analyse');loadTicker('${r.ticker}')">
      <span style="font-weight:600;color:#1D9E75">${r.ticker}</span>
      <span style="color:#aaa;font-size:12px">${r.name}</span>
      <span style="color:#fff">$${n2(r.price)}</span>
      <span style="color:${chColor}">${(r.change_24h||0)>=0?'+':''}${n1(r.change_24h)}%</span>
      <span style="color:${sc(r.score)};font-weight:600">${r.score}/10</span>
      ${recBadge(r.recommendation)}
      <span style="color:#555;font-size:11px">RSI ${n1(r.rsi)}</span>
    </div>`;
  }).join('');

  document.getElementById('scanner-results').innerHTML=`
    <div class="grid2" style="margin-bottom:16px">
      <div class="card" style="border-color:#1a3a2a">
        <div class="stitle" style="color:#4ade80">🟢 Top 5 Opportunités Achat</div>
        ${top5buy.length?top5buy.map(r=>`<div class="row" style="cursor:pointer" onclick="showTab('analyse');loadTicker('${r.ticker}')">
          <div><span style="font-weight:600;color:#1D9E75">${r.ticker}</span> <span style="font-size:12px;color:#555">${r.name}</span></div>
          <div style="text-align:right"><span style="color:#4ade80;font-weight:600">${r.score}/10</span> <span style="font-size:11px;color:#555">RSI:${n1(r.rsi)}</span></div>
        </div>`).join(''):'<div style="color:#555;font-size:13px">Aucune opportunité achat détectée</div>'}
      </div>
      <div class="card" style="border-color:#3a1a1a">
        <div class="stitle" style="color:#f87171">🔴 Top 5 Signaux Vente</div>
        ${top5sell.length?top5sell.map(r=>`<div class="row" style="cursor:pointer" onclick="showTab('analyse');loadTicker('${r.ticker}')">
          <div><span style="font-weight:600;color:#f87171">${r.ticker}</span> <span style="font-size:12px;color:#555">${r.name}</span></div>
          <div style="text-align:right"><span style="color:#f87171;font-weight:600">${r.score}/10</span> <span style="font-size:11px;color:#555">RSI:${n1(r.rsi)}</span></div>
        </div>`).join(''):'<div style="color:#555;font-size:13px">Aucun signal vente détecté</div>'}
      </div>
    </div>
    <div class="card">
      <div class="stitle">Toutes les actions — classées par score IA</div>
      <div class="scanner-header"><span>Ticker</span><span>Nom</span><span>Prix</span><span>24h</span><span>Score IA</span><span>Signal</span><span>RSI</span></div>
      ${tableRows}
    </div>`;
}

// ══════════════════════════════════════════════
// ONGLET PORTEFEUILLE
// ══════════════════════════════════════════════
function savePortfolio(){localStorage.setItem('portfolio',JSON.stringify(portfolio));}

function addToPortfolio(){
  const ticker=document.getElementById('pf-ticker').value.trim().toUpperCase();
  const price=parseFloat(document.getElementById('pf-price').value);
  const qty=parseFloat(document.getElementById('pf-qty').value);
  if(!ticker||!price||!qty){alert('Remplis tous les champs');return;}
  portfolio.push({ticker,buyPrice:price,qty,addedAt:new Date().toLocaleDateString('fr-FR')});
  savePortfolio();
  document.getElementById('pf-ticker').value='';
  document.getElementById('pf-price').value='';
  document.getElementById('pf-qty').value='';
  renderPortfolio();
}

function addTickerToPortfolio(ticker){
  showTab('portfolio');
  document.getElementById('pf-ticker').value=ticker;
  document.getElementById('pf-ticker').focus();
}

function removeFromPortfolio(idx){portfolio.splice(idx,1);savePortfolio();renderPortfolio();}

async function renderPortfolio(){
  const listEl=document.getElementById('portfolio-list');
  if(!portfolio.length){listEl.innerHTML='<div class="card" style="text-align:center;color:#555;padding:40px">Aucune action dans le portefeuille.<br>Ajoute une action ci-dessus ou depuis la page d\'analyse.</div>';document.getElementById('portfolio-summary').style.display='none';return;}
  listEl.innerHTML='<div class="card" style="color:#555;text-align:center;padding:20px">Chargement des prix actuels...</div>';
  let totalVal=0,totalInvested=0;
  const rows=await Promise.all(portfolio.map(async(p,i)=>{
    try{
      const r=await fetch(API+'/api/analyze/'+encodeURIComponent(p.ticker));
      const d=await r.json();
      const currentPrice=d.price?.current||0;
      const score=d.scoring?.global_score;
      const rec=d.scoring?.recommendation;
      const val=currentPrice*p.qty;
      const invested=p.buyPrice*p.qty;
      const pnl=val-invested;
      const pnlPct=(pnl/invested)*100;
      totalVal+=val; totalInvested+=invested;
      const pColor=pnl>=0?'#4ade80':'#f87171';
      return `<div class="portfolio-row">
        <span style="font-weight:600;color:#1D9E75;cursor:pointer" onclick="showTab('analyse');loadTicker('${p.ticker}')">${p.ticker}</span>
        <span style="font-size:12px;color:#888">${d.name}</span>
        <span style="color:#fff">$${n2(currentPrice)}</span>
        <span style="color:#888">${p.qty} × $${n2(p.buyPrice)}</span>
        <span style="color:#fff;font-weight:500">$${val.toFixed(0)}</span>
        <span style="color:${pColor};font-weight:600">${pnl>=0?'+':''}$${pnl.toFixed(0)} (${pnlPct>=0?'+':''}${pnlPct.toFixed(1)}%)</span>
        <div style="display:flex;align-items:center;gap:8px">
          <span style="color:${sc(score)};font-weight:600;font-size:13px">${score}/10</span>
          <button onclick="removeFromPortfolio(${i})" style="padding:3px 8px;font-size:11px;color:#f87171;border-color:#3a1a1a">✕</button>
        </div>
      </div>`;
    }catch(e){return `<div class="portfolio-row"><span style="color:#f87171">${p.ticker}</span><span style="color:#555">Erreur</span><span></span><span></span><span></span><span></span><button onclick="removeFromPortfolio(${i})" style="padding:3px 8px;font-size:11px;color:#f87171">✕</button></div>`;}
  }));
  const pnlTotal=totalVal-totalInvested, pnlPctTotal=(pnlTotal/totalInvested)*100;
  const pColor=pnlTotal>=0?'#4ade80':'#f87171';
  document.getElementById('pf-total').textContent='$'+totalVal.toFixed(0);
  document.getElementById('pf-invested').textContent='$'+totalInvested.toFixed(0);
  document.getElementById('pf-pnl').textContent=(pnlTotal>=0?'+':'')+' $'+pnlTotal.toFixed(0);
  document.getElementById('pf-pnl').style.color=pColor;
  document.getElementById('pf-perf').textContent=(pnlPctTotal>=0?'+':'')+pnlPctTotal.toFixed(1)+'%';
  document.getElementById('pf-perf').style.color=pColor;
  document.getElementById('portfolio-summary').style.display='block';
  listEl.innerHTML=`<div class="card"><div class="stitle">Mes Actions</div><div class="portfolio-header"><span>Ticker</span><span>Nom</span><span>Prix actuel</span><span>Position</span><span>Valeur</span><span>P&L</span><span>Score IA</span></div>${rows.join('')}</div>`;
}

loadTicker('AAPL');
</script>
</body>
</html>""")

@app.get("/agent")
async def agent_page():
    return HTMLResponse("""<!DOCTYPE html>
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
  document.getElementById("m-pnl").innerHTML="<span style=\"color:"+pc+"\">"+( pnl>=0?"+":"")+fmt(pnl)+" EUR ("+( pnlPct>=0?"+":"")+pnlPct.toFixed(1)+"%)</span>";
  document.getElementById("m-winrate").innerHTML="<span style=\"color:"+(wr>=50?"#4ade80":"#f87171")+"\">"+wr.toFixed(0)+"%</span> <span style=\"font-size:14px;color:#555\">("+state.winning_trades+"/"+state.total_trades+")</span>";
}
function renderPositions(state){
  var positions=Object.values(state.positions||{});
  if(!positions.length){document.getElementById("positions-wrap").innerHTML="<div style=\"color:#555;text-align:center;padding:20px\">Aucune position ouverte</div>";return;}
  var rows=positions.map(function(p){
    var invested=p.qty*p.buy_price;
function currency(ticker) {
    if(!ticker) return "$";
    var t = ticker.toUpperCase();
    if(t.endsWith(".PA") || t.endsWith(".BR") || t.endsWith(".AS") || t.endsWith(".DE") || t.endsWith(".MI")) return "€";
    if(t.endsWith(".L")) return "£";
    if(t.endsWith(".SW") || t.endsWith(".ZU")) return "CHF";
    if(t.includes("BTC") || t.includes("ETH")) return "$";
    return "$";
}
    return "<div class=\"pos-row\"><span style=\"font-weight:600;color:#1D9E75\">"+p.ticker+"</span><span style=\"font-size:12px;color:#888\">"+p.name+"</span><span style=\"color:#fff\">$"+n2(p.buy_price)+"</span><span style=\"color:#888\">"+p.qty.toFixed(4)+"</span><span style=\"color:#fff\">"+fmt(invested)+" EUR</span><span style=\"color:"+sc(p.score_at_buy)+";font-weight:600\">"+p.score_at_buy+"/10</span></div>";
  }).join("");
  document.getElementById("positions-wrap").innerHTML="<div class=\"pos-header\"><span>Ticker</span><span>Nom</span><span>Px achat</span><span>Qte</span><span>Investi</span><span>Score</span></div>"+rows;
}
function renderHistory(state){
  var history=(state.history||[]).slice(0,30);
  if(!history.length){document.getElementById("history-wrap").innerHTML="<div style=\"color:#555;text-align:center;padding:20px\">Aucune action effectuee</div>";return;}
  var rows=history.map(function(a){
    var bc="badge-err";
    if(a.type==="ACHAT") bc="badge-buy";
    else if(a.type==="VENTE") bc="badge-sell";
    else if(a.type==="VENTE PARTIELLE") bc="badge-partial";
    var pnlHtml=a.pnl_abs!=null?"<span style=\"color:"+(a.pnl_abs>=0?"#4ade80":"#f87171")+";font-weight:600\">"+(a.pnl_abs>=0?"+":"")+fmt(a.pnl_abs)+" EUR ("+(a.pnl_pct>=0?"+":"")+n1(a.pnl_pct)+"%)</span>":a.cost!=null?"<span style=\"color:#888\">-"+fmt(a.cost)+" EUR</span>":"--";
    var ts=a.timestamp?a.timestamp.slice(0,16).replace("T"," "):"";
    return "<div class=\"action-row\"><span class=\"badge "+bc+"\">"+a.type+"</span><span style=\"font-weight:600;color:#1D9E75\">"+a.ticker+"</span><span style=\"font-size:12px;color:#666\">"+( a.reason||"")+"</span><span style=\"color:#fff\">$"+n2(a.price)+"</span>"+pnlHtml+"<span style=\"font-size:11px;color:#444\">"+ts+"</span></div>";
  }).join("");
  document.getElementById("history-wrap").innerHTML="<div class=\"action-header\"><span>Action</span><span>Ticker</span><span>Raison IA</span><span>Prix</span><span>P&L</span><span>Date</span></div>"+rows;
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
  document.getElementById("agent-status").innerHTML="<span class=\"pulse\" style=\"color:#1D9E75\">Analyse en cours</span>";
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
</html>""")

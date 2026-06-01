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

import os as _os

def _get_html_path(filename):
    # Chercher le fichier HTML dans plusieurs endroits possibles
    paths = [
        _os.path.join(_os.path.dirname(__file__), '..', '..', 'html', filename),
        _os.path.join(_os.path.dirname(__file__), '..', 'html', filename),
        _os.path.join('/app', 'html', filename),
        _os.path.join(_os.getcwd(), 'html', filename),
        filename,
    ]
    for p in paths:
        if _os.path.exists(p):
            return p
    return None

import os as _os

def _get_html_path(filename):
    # Chercher le fichier HTML dans plusieurs endroits possibles
    paths = [
        _os.path.join(_os.path.dirname(__file__), '..', '..', 'html', filename),
        _os.path.join(_os.path.dirname(__file__), '..', 'html', filename),
        _os.path.join('/app', 'html', filename),
        _os.path.join(_os.getcwd(), 'html', filename),
        filename,
    ]
    for p in paths:
        if _os.path.exists(p):
            return p
    return None

import os as _os

def _get_html_path(filename):
    # Chercher le fichier HTML dans plusieurs endroits possibles
    paths = [
        _os.path.join(_os.path.dirname(__file__), '..', '..', 'html', filename),
        _os.path.join(_os.path.dirname(__file__), '..', 'html', filename),
        _os.path.join('/app', 'html', filename),
        _os.path.join(_os.getcwd(), 'html', filename),
        filename,
    ]
    for p in paths:
        if _os.path.exists(p):
            return p
    return None

@app.get("/")
async def root():
    path = _get_html_path('index.html')
    if path:
        with open(path, encoding='utf-8') as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>TradingIA</h1><p><a href='/docs'>API Docs</a> | <a href='/agent'>Agent</a></p>")

@app.get("/agent")
async def agent_page():
    path = _get_html_path('agent.html')
    if path:
        with open(path, encoding='utf-8') as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>Agent IA</h1><p><a href='/'>Dashboard</a></p>")

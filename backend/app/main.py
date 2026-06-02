from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from datetime import datetime
import json, os, asyncio, threading, time, random
from app import serve as _serve

app = FastAPI(title="TradingIA API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CAC40 = ["MC.PA","TTE.PA","SAN.PA","AIR.PA","SU.PA","BNP.PA","RI.PA","OR.PA","RMS.PA","SAF.PA","DSY.PA","ACA.PA","SGO.PA","ORA.PA","GLE.PA","EN.PA","KER.PA","CAP.PA","EL.PA","PUB.PA","HO.PA","RNO.PA","ATO.PA","ALO.PA","ML.PA","ADP.PA","AF.PA"]
NASDAQ100 = ["AAPL","MSFT","NVDA","AMZN","META","GOOGL","TSLA","AVGO","COST","NFLX","AMD","ADBE","QCOM","AMAT","MU","LRCX","MRVL","PANW","SNPS","CDNS","INTU","CRWD","FTNT","ADI","TXN","NXPI","WDAY","DDOG","PYPL","GILD","REGN","VRTX"]
SP500_TOP = ["JPM","V","MA","UNH","JNJ","PG","HD","MRK","ABBV","PEP","KO","WMT","BAC","CVX","XOM","LLY","TMO","ABT","ACN","NEE","DHR","ORCL","CRM","CSCO","IBM","HON","UPS","CAT","GE","MMM","DE","BA","LMT","RTX"]
CHINA_TECH = ["BABA","BIDU","JD","PDD","NIO","XPEV","LI","TCOM","NTES","BILI"]
ALL_TICKERS = list(set(CAC40 + NASDAQ100 + SP500_TOP + CHINA_TECH))

AGENTS = {
    "global":      {"name": "Agent Global",      "emoji": "🧠", "capital": 20000.0, "strategy": "global"},
    "technique":   {"name": "Agent Technique",   "emoji": "📊", "capital": 20000.0, "strategy": "technique"},
    "fondamental": {"name": "Agent Fondamental", "emoji": "💰", "capital": 20000.0, "strategy": "fondamental"},
    "analystes":   {"name": "Agent Analystes",   "emoji": "👥", "capital": 20000.0, "strategy": "analystes"},
    "actualites":  {"name": "Agent Actualites",  "emoji": "📰", "capital": 20000.0, "strategy": "actualites"},
    "patterns":    {"name": "Agent Patterns",    "emoji": "🔮", "capital": 20000.0, "strategy": "patterns"},
}

AGENTS_FILE = "agents_state.json"

def load_agents():
    if os.path.exists(AGENTS_FILE):
        with open(AGENTS_FILE, "r") as f:
            return json.load(f)
    state = {}
    for key, cfg in AGENTS.items():
        state[key] = {
            "id": key,
            "name": cfg["name"],
            "emoji": cfg["emoji"],
            "strategy": cfg["strategy"],
            "capital": cfg["capital"],
            "initial_capital": cfg["capital"],
            "positions": {},
            "history": [],
            "total_trades": 0,
            "winning_trades": 0,
            "daily_trades": 0,
            "daily_buys": 0,
            "daily_sells": 0,
            "last_trade_date": None,
            "last_run": None,
            "auto_runs": 0,
        }
    return state

def save_agents(state):
    with open(AGENTS_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)

def compute_strategy_score(strategy, data):
    tech = data.get("technical", {})
    fund = data.get("fundamental", {})
    analysts = data.get("analysts", {})
    news = data.get("news", [])
    scoring = data.get("scoring", {})
    breakdown = scoring.get("breakdown", {})

    if strategy == "global":
        return scoring.get("global_score", 0), scoring.get("recommendation", "wait")

    elif strategy == "technique":
        score = breakdown.get("technique", {}).get("score", 0)
        rsi = tech.get("rsi", 50) or 50
        macd = (tech.get("macd") or {}).get("value", 0) or 0
        macd_hist = (tech.get("macd") or {}).get("histogram", 0) or 0
        adx = (tech.get("adx") or {}).get("value", 0) or 0
        golden = tech.get("moving_averages", {}).get("golden_cross", False)
        ichi = tech.get("ichimoku", {}).get("price_above_cloud", False)
        buy = score >= 7.0 and macd > 0 and macd_hist > 0 and adx > 20 and 30 < rsi < 70
        sell_sig = score < 4 or rsi > 75 or (macd < 0 and macd_hist < 0)
        rec = "buy" if buy else ("sell" if sell_sig else "wait")
        return score, rec

    elif strategy == "fondamental":
        score = breakdown.get("fondamental", {}).get("score", 0)
        rev_growth = fund.get("revenue_growth", 0) or 0
        margins = fund.get("profit_margins", 0) or 0
        pe = fund.get("pe_ratio", 30) or 30
        roe = fund.get("return_on_equity", 0) or 0
        buy = score >= 6.5 and rev_growth > 0.05 and margins > 0.10 and pe < 50
        sell_sig = score < 4 or rev_growth < -0.05 or margins < 0
        rec = "buy" if buy else ("sell" if sell_sig else "wait")
        return score, rec

    elif strategy == "analystes":
        score = breakdown.get("analystes", {}).get("score", 0)
        buy_pct = analysts.get("buy_pct", 0) or 0
        sell_pct = analysts.get("sell_pct", 0) or 0
        buy = score >= 6.0 and buy_pct >= 60
        sell_sig = sell_pct > 40 or buy_pct < 30
        rec = "buy" if buy else ("sell" if sell_sig else "wait")
        return score, rec

    elif strategy == "actualites":
        score = breakdown.get("actualites", {}).get("score", 0)
        news_scores = [n.get("sentiment_score", 5) for n in news if n.get("sentiment_score")]
        avg_news = sum(news_scores) / len(news_scores) if news_scores else 5
        positive = sum(1 for n in news if n.get("sentiment") == "positif")
        negative = sum(1 for n in news if n.get("sentiment") == "negatif")
        buy = avg_news >= 7.0 and positive > negative
        sell_sig = avg_news <= 3.0 or negative > positive * 2
        rec = "buy" if buy else ("sell" if sell_sig else "wait")
        return avg_news, rec

    elif strategy == "patterns":
        # Utiliser le score technique comme proxy pour les patterns
        score = breakdown.get("technique", {}).get("score", 0)
        rsi = tech.get("rsi", 50) or 50
        macd = (tech.get("macd") or {}).get("value", 0) or 0
        stoch = (tech.get("stochastic") or {}).get("k", 50) or 50
        # Pattern survente + momentum
        buy = rsi < 35 and macd > 0 and stoch < 30
        # Pattern surachat
        sell_sig = rsi > 72 and stoch > 80
        # Pattern neutre fort
        if not buy and not sell_sig and score >= 6.5 and 40 < rsi < 65:
            buy = True
        rec = "buy" if buy else ("sell" if sell_sig else "wait")
        return score, rec

    return 0, "wait"

async def run_agent(agent_id, agent_state, tickers, min_profit_pct=3.0, stop_loss_pct=8.0, min_daily=3):
    from app.api.routes import analyze_ticker
    import importlib, app.api.routes
    importlib.reload(app.api.routes)
    from app.api.routes import analyze_ticker

    today = datetime.utcnow().strftime("%Y-%m-%d")
    if agent_state.get("last_trade_date") != today:
        agent_state["daily_trades"] = 0
        agent_state["daily_buys"] = 0
        agent_state["daily_sells"] = 0
        agent_state["last_trade_date"] = today

    agent_state["last_run"] = datetime.utcnow().isoformat()
    agent_state["auto_runs"] = agent_state.get("auto_runs", 0) + 1
    strategy = agent_state["strategy"]
    actions = []

    # 1. VERIFIER POSITIONS EXISTANTES
    for ticker, pos in list(agent_state["positions"].items()):
        try:
            data = await analyze_ticker(ticker)
            current_price = data["price"]["current"]
            if not current_price:
                continue
            buy_price = pos["buy_price"]
            qty = pos["qty"]
            pnl_pct = (current_price - buy_price) / buy_price * 100

            should_sell = False
            sell_reason = ""

            # Stop loss
            if pnl_pct <= -stop_loss_pct:
                should_sell = True
                sell_reason = "STOP LOSS {:.1f}%".format(pnl_pct)

            # Take profit minimum 3%
            elif pnl_pct >= min_profit_pct:
                score, rec = compute_strategy_score(strategy, data)
                if rec in ["sell", "wait"] or score < 6.0:
                    should_sell = True
                    sell_reason = "TAKE PROFIT +{:.1f}%".format(pnl_pct)
                elif pnl_pct >= 8:
                    # Vente partielle 50%
                    qty_sell = qty * 0.5
                    profit = (current_price - buy_price) * qty_sell
                    agent_state["capital"] += current_price * qty_sell
                    agent_state["positions"][ticker]["qty"] -= qty_sell
                    agent_state["total_trades"] += 1
                    agent_state["winning_trades"] += 1
                    agent_state["daily_trades"] += 1
                    agent_state["daily_sells"] += 1
                    action = {"type": "VENTE PARTIELLE", "ticker": ticker, "name": data["name"], "qty": qty_sell, "price": current_price, "buy_price": buy_price, "pnl_pct": pnl_pct, "pnl_abs": profit, "strategy": strategy, "reason": "Capitalisation +{:.1f}%".format(pnl_pct), "timestamp": datetime.utcnow().isoformat()}
                    actions.append(action)
                    agent_state["history"].insert(0, action)
                    continue

            # Force vente si min daily sells pas atteint en fin de journee
            hour = datetime.utcnow().hour
            if hour >= 15 and agent_state["daily_sells"] < min_daily and pnl_pct > 0:
                should_sell = True
                sell_reason = "Objectif ventes journalieres +{:.1f}%".format(pnl_pct)

            if should_sell:
                revenue = current_price * qty
                profit = (current_price - buy_price) * qty
                agent_state["capital"] += revenue
                if profit > 0:
                    agent_state["winning_trades"] += 1
                agent_state["total_trades"] += 1
                agent_state["daily_trades"] += 1
                agent_state["daily_sells"] += 1
                action = {"type": "VENTE", "ticker": ticker, "name": data["name"], "qty": qty, "price": current_price, "buy_price": buy_price, "pnl_pct": pnl_pct, "pnl_abs": profit, "strategy": strategy, "reason": sell_reason, "timestamp": datetime.utcnow().isoformat()}
                actions.append(action)
                agent_state["history"].insert(0, action)
                del agent_state["positions"][ticker]
        except:
            pass

    # 2. CHERCHER OPPORTUNITES
    tickers_shuffled = list(tickers)
    random.shuffle(tickers_shuffled)
    opportunities = []
    analyzed = 0

    for ticker in tickers_shuffled:
        if ticker in agent_state["positions"]:
            continue
        if analyzed >= 30:
            break
        try:
            data = await analyze_ticker(ticker)
            score, rec = compute_strategy_score(strategy, data)
            rsi = (data.get("technical") or {}).get("rsi", 50) or 50

            # Seuil selon strategy
            thresholds = {"global": 7.0, "technique": 7.0, "fondamental": 6.5, "analystes": 6.0, "actualites": 6.5, "patterns": 6.0}
            min_score = thresholds.get(strategy, 6.5)

            # Baisser seuil si pas assez de trades
            if agent_state["daily_buys"] < min_daily:
                min_score -= 0.5

            if score >= min_score and rec == "buy" and rsi < 72:
                opportunities.append({"ticker": ticker, "data": data, "score": score, "rsi": rsi})
            analyzed += 1
        except:
            analyzed += 1

    opportunities.sort(key=lambda x: x["score"], reverse=True)

    # 3. ACHETER
    max_positions = 10
    needed = max(min_daily - agent_state["daily_buys"], 0)
    max_buys = max(5, needed)

    for opp in opportunities[:max_buys]:
        if len(agent_state["positions"]) >= max_positions:
            break
        ticker = opp["ticker"]
        data = opp["data"]
        current_price = data["price"]["current"]
        if not current_price or current_price <= 0:
            continue

        invest_amount = agent_state["capital"] * 0.12
        invest_amount = min(invest_amount, agent_state["capital"] * 0.20)
        if invest_amount < 50 or invest_amount > agent_state["capital"]:
            continue

        qty = invest_amount / current_price
        cost = qty * current_price
        if cost > agent_state["capital"]:
            continue

        agent_state["capital"] -= cost
        agent_state["positions"][ticker] = {
            "ticker": ticker, "name": data["name"],
            "buy_price": current_price, "qty": qty, "cost": cost,
            "score_at_buy": opp["score"], "bought_at": datetime.utcnow().isoformat()
        }
        agent_state["total_trades"] += 1
        agent_state["daily_trades"] += 1
        agent_state["daily_buys"] += 1

        action = {"type": "ACHAT", "ticker": ticker, "name": data["name"], "qty": qty, "price": current_price, "cost": cost, "score": opp["score"], "strategy": strategy, "reason": "Score {:.1f} - RSI {:.1f} - Strategie {}".format(opp["score"], opp["rsi"], strategy), "timestamp": datetime.utcnow().isoformat()}
        actions.append(action)
        agent_state["history"].insert(0, action)

    agent_state["history"] = agent_state["history"][:200]
    return actions

async def run_all_agents():
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
            await asyncio.sleep(30)

def scheduler_thread(loop):
    while True:
        now = datetime.utcnow()
        hour = now.hour
        weekday = now.weekday()
        if weekday < 5 and 7 <= hour <= 17:
            future = asyncio.run_coroutine_threadsafe(run_all_agents(), loop)
            try:
                future.result(timeout=1200)
            except Exception as e:
                print("Erreur scheduler: {}".format(e))
        time.sleep(900)  # 15 minutes

@app.on_event("startup")
async def startup():
    print("Agents prets - scheduler desactive")

@app.get("/health")
async def health():
    state = load_agents()
    total_cap = sum(a["capital"] for a in state.values())
    total_pos = sum(len(a["positions"]) for a in state.values())
    return {"status": "ok", "agents": len(state), "total_capital": total_cap, "total_positions": total_pos}

@app.get("/api/analyze/{ticker:path}")
async def analyze(ticker: str):
    import importlib, app.api.routes
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
    import importlib, app.api.routes
    importlib.reload(app.api.routes)
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

@app.get("/api/agents/state")
async def agents_state():
    return load_agents()

@app.get("/api/agents/{agent_id}/state")
async def agent_state_single(agent_id: str):
    state = load_agents()
    if agent_id not in state:
        return {"error": "Agent inconnu"}
    return state[agent_id]

@app.post("/api/agents/{agent_id}/reset")
async def agent_reset(agent_id: str, capital: float = 20000.0):
    state = load_agents()
    if agent_id not in state:
        return {"error": "Agent inconnu"}
    cfg = AGENTS[agent_id]
    state[agent_id] = {"id": agent_id, "name": cfg["name"], "emoji": cfg["emoji"], "strategy": cfg["strategy"], "capital": capital, "initial_capital": capital, "positions": {}, "history": [], "total_trades": 0, "winning_trades": 0, "daily_trades": 0, "daily_buys": 0, "daily_sells": 0, "last_trade_date": None, "last_run": None, "auto_runs": 0}
    save_agents(state)
    return state[agent_id]

@app.post("/api/agents/reset_all")
async def reset_all_agents(capital: float = 20000.0):
    state = {}
    for key, cfg in AGENTS.items():
        state[key] = {"id": key, "name": cfg["name"], "emoji": cfg["emoji"], "strategy": cfg["strategy"], "capital": capital, "initial_capital": capital, "positions": {}, "history": [], "total_trades": 0, "winning_trades": 0, "daily_trades": 0, "daily_buys": 0, "daily_sells": 0, "last_trade_date": None, "last_run": None, "auto_runs": 0}
    save_agents(state)
    return {"status": "ok", "agents": list(state.keys())}

@app.post("/api/agents/{agent_id}/run")
async def run_single_agent(agent_id: str):
    state = load_agents()
    if agent_id not in state:
        return {"error": "Agent inconnu"}
    actions = await run_agent(agent_id, state[agent_id], ALL_TICKERS)
    save_agents(state)
    pos_val = sum(p["qty"] * p["buy_price"] for p in state[agent_id]["positions"].values())
    return {"agent_id": agent_id, "actions": actions, "portfolio_value": state[agent_id]["capital"] + pos_val}

@app.post("/api/agents/run_all")
async def run_all():
    await run_all_agents()
    return {"status": "ok"}

@app.get("/api/agents/pnl_realtime")
async def pnl_realtime():
    import yfinance as yf, math
    state = load_agents()
    result = {}
    for agent_id, agent in state.items():
        positions_live = {}
        total_pos_value = 0
        total_cost = 0
        for ticker, pos in agent["positions"].items():
            try:
                t = yf.Ticker(ticker)
                info = t.info
                current_price = info.get("currentPrice") or info.get("regularMarketPrice") or pos["buy_price"]
                if isinstance(current_price, float) and (math.isnan(current_price) or math.isinf(current_price)):
                    current_price = pos["buy_price"]
                qty = pos["qty"]
                buy_price = pos["buy_price"]
                value = current_price * qty
                cost = buy_price * qty
                pnl = value - cost
                pnl_pct = (pnl / cost * 100) if cost > 0 else 0
                total_pos_value += value
                total_cost += cost
                positions_live[ticker] = {
                    "name": pos["name"],
                    "qty": qty,
                    "buy_price": buy_price,
                    "current_price": round(current_price, 2),
                    "value": round(value, 2),
                    "cost": round(cost, 2),
                    "pnl": round(pnl, 2),
                    "pnl_pct": round(pnl_pct, 2),
                    "bought_at": pos.get("bought_at", "")
                }
            except:
                positions_live[ticker] = {**pos, "current_price": pos["buy_price"], "pnl": 0, "pnl_pct": 0, "value": pos["qty"] * pos["buy_price"]}
                total_pos_value += pos["qty"] * pos["buy_price"]
                total_cost += pos["qty"] * pos["buy_price"]

        portfolio_value = agent["capital"] + total_pos_value
        total_pnl = portfolio_value - agent["initial_capital"]
        total_pnl_pct = (total_pnl / agent["initial_capital"] * 100) if agent["initial_capital"] > 0 else 0
        winrate = (agent["winning_trades"] / agent["total_trades"] * 100) if agent["total_trades"] > 0 else 0

        result[agent_id] = {
            "id": agent_id,
            "name": agent["name"],
            "emoji": agent["emoji"],
            "strategy": agent["strategy"],
            "capital": round(agent["capital"], 2),
            "initial_capital": agent["initial_capital"],
            "portfolio_value": round(portfolio_value, 2),
            "total_pnl": round(total_pnl, 2),
            "total_pnl_pct": round(total_pnl_pct, 2),
            "positions_value": round(total_pos_value, 2),
            "positions": positions_live,
            "positions_count": len(positions_live),
            "total_trades": agent["total_trades"],
            "winning_trades": agent["winning_trades"],
            "winrate": round(winrate, 1),
            "daily_buys": agent.get("daily_buys", 0),
            "daily_sells": agent.get("daily_sells", 0),
            "last_run": agent.get("last_run"),
            "history": agent["history"][:20],
        }
    return result

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


@app.get("/agents")
async def agents_page():
    html = _serve.get_agents_html()
    if html:
        return HTMLResponse(html)
    return HTMLResponse("<h1>Agents</h1><p><a href='/docs'>API</a></p>")

@app.get("/debug")
async def debug():
    import os
    cwd = os.getcwd()
    files = []
    for root, dirs, filenames in os.walk("."):
        for fname in filenames[:3]:
            files.append(os.path.join(root, fname))
        if len(files) > 20:
            break
    return {"cwd": cwd, "files": files}

@app.get("/")
async def root():
    html = _serve.get_index_html()
    if html:
        return HTMLResponse(html)
    return HTMLResponse("<h1>TradingIA</h1><p><a href='/docs'>API Docs</a></p>")

@app.get("/agent")
async def agent_page():
    html = _serve.get_agent_html()
    if html:
        return HTMLResponse(html)
    return HTMLResponse("<h1>Agents IA</h1>")

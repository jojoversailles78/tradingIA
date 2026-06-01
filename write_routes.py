content = '''import yfinance as yf
import pandas_ta as ta
import numpy as np
import math
from datetime import datetime

def clean(v):
    if v is None: return None
    try:
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)): return None
    except: pass
    return v

def score_news_sentiment(news_list):
    if not news_list:
        return 5.0, []

    POSITIVE_WORDS = [
        "hausse","monte","croissance","benefice","profit","record","depasse","surpasse",
        "ameliore","progression","achat","recommande","objectif","releve","forte","solide",
        "optimiste","accord","contrat","partenariat","acquisition","dividende","rachat",
        "acceleration","boom","rebond","rally","breakout","buy","upgrade","beat","strong",
        "growth","rise","surge","gain","positive","bullish","outperform","exceed","raise",
        "expand","revenue","beat","record","high","momentum","boost","rally","win"
    ]
    NEGATIVE_WORDS = [
        "baisse","recul","perte","chute","avertissement","deception","manque","reduit",
        "ralentissement","inquietude","risque","vente","degrade","abaisse","faible",
        "pessimiste","litige","amende","sanction","fraude","restructuration","licenciement",
        "faillite","dette","deficit","crise","sell","downgrade","miss","weak","decline",
        "fall","drop","loss","negative","bearish","underperform","cut","reduce","warn",
        "concern","risk","lawsuit","fine","restructure","layoff","bankrupt","debt"
    ]

    scored_news = []
    total_score = 0
    count = 0

    for item in news_list:
        title = (item.get("title") or "").lower()
        if not title:
            continue

        pos_count = sum(1 for w in POSITIVE_WORDS if w in title)
        neg_count = sum(1 for w in NEGATIVE_WORDS if w in title)

        if pos_count > neg_count:
            score = min(10, 6 + pos_count * 1.5)
            sentiment = "positif"
        elif neg_count > pos_count:
            score = max(1, 4 - neg_count * 1.5)
            sentiment = "negatif"
        else:
            score = 5.0
            sentiment = "neutre"

        score = round(score, 1)
        total_score += score
        count += 1
        scored_news.append({
            "title": item.get("title", ""),
            "publisher": item.get("publisher", ""),
            "link": item.get("link", ""),
            "date": item.get("date", ""),
            "sentiment_score": score,
            "sentiment": sentiment,
        })

    avg_score = round(total_score / count, 1) if count > 0 else 5.0
    return avg_score, scored_news

async def analyze_ticker(ticker: str):
    t = yf.Ticker(ticker)
    info = t.info
    hist = t.history(period="1y", interval="1d")
    if hist.empty:
        raise Exception(f"Ticker {ticker} introuvable")
    close = hist["Close"]
    high = hist["High"]
    low = hist["Low"]
    rsi = ta.rsi(close, length=14)
    rsi_val = clean(float(rsi.iloc[-1])) if rsi is not None else None
    macd_df = ta.macd(close)
    macd_val = clean(float(macd_df["MACD_12_26_9"].iloc[-1])) if macd_df is not None else None
    macd_sig = clean(float(macd_df["MACDs_12_26_9"].iloc[-1])) if macd_df is not None else None
    macd_hist = clean(float(macd_df["MACDh_12_26_9"].iloc[-1])) if macd_df is not None else None
    sma_20 = clean(float(ta.sma(close, 20).iloc[-1]))
    sma_50 = clean(float(ta.sma(close, 50).iloc[-1]))
    sma_200 = clean(float(ta.sma(close, 200).iloc[-1]))
    boll = ta.bbands(close, length=20)
    boll_upper = clean(float(boll.iloc[-1, 0])) if boll is not None else None
    boll_lower = clean(float(boll.iloc[-1, 2])) if boll is not None else None
    stoch = ta.stoch(high, low, close)
    stoch_k = clean(float(stoch["STOCHk_14_3_3"].iloc[-1])) if stoch is not None else None
    adx_df = ta.adx(high, low, close)
    adx_val = clean(float(adx_df["ADX_14"].iloc[-1])) if adx_df is not None else None
    returns = close.pct_change().dropna()
    std_dev = clean(float(returns.std() * np.sqrt(252) * 100))
    try:
        import pandas as pd
        spy = yf.Ticker("SPY").history(period="1y")["Close"]
        spy_ret = spy.pct_change().dropna()
        aligned = pd.concat([returns, spy_ret], axis=1).dropna()
        cov = np.cov(aligned.iloc[:,0], aligned.iloc[:,1])
        beta = clean(float(cov[0,1] / cov[1,1]))
    except:
        beta = 1.0
    cum = (1 + returns).cumprod()
    max_dd = clean(float(((cum - cum.cummax()) / cum.cummax()).min() * 100))
    excess = returns - 0.05/252
    sharpe = clean(float(excess.mean() / excess.std() * np.sqrt(252))) if excess.std() > 0 else 0
    golden_cross = bool(sma_50 and sma_200 and sma_50 > sma_200)
    price = clean(float(close.iloc[-1]))

    buy_pct = 50
    hold_pct = 30
    sell_pct = 20
    try:
        recs = t.recommendations_summary
        if recs is not None and not recs.empty:
            row = recs.iloc[0]
            b = int(row.get("strongBuy", 0)) + int(row.get("buy", 0))
            h = int(row.get("hold", 0))
            s = int(row.get("sell", 0)) + int(row.get("strongSell", 0))
            total = b + h + s or 1
            buy_pct = round(b / total * 100)
            hold_pct = round(h / total * 100)
            sell_pct = round(s / total * 100)
    except:
        try:
            recs = t.recommendations
            if recs is not None and not recs.empty:
                recent = recs.tail(20)
                b = h = s = 0
                for _, row in recent.iterrows():
                    g = str(row.get("To Grade", "")).lower()
                    if any(x in g for x in ["buy","outperform","overweight"]): b += 1
                    elif any(x in g for x in ["sell","underperform","underweight"]): s += 1
                    else: h += 1
                total = b + h + s or 1
                buy_pct = round(b/total*100)
                hold_pct = round(h/total*100)
                sell_pct = round(s/total*100)
        except:
            pass

    # Actualites avec scoring sentiment
    raw_news = []
    try:
        raw_news_data = t.news
        if raw_news_data:
            for item in raw_news_data[:8]:
                content2 = item.get("content", item)
                title = content2.get("title") or item.get("title", "")
                publisher = ""
                try:
                    publisher = content2.get("provider", {}).get("displayName") or content2.get("publisher") or item.get("publisher", "")
                except: pass
                link = ""
                try:
                    link = content2.get("canonicalUrl", {}).get("url") or content2.get("link") or item.get("link", "")
                except: pass
                pub_time = content2.get("pubDate") or content2.get("providerPublishTime") or item.get("providerPublishTime")
                date_str = ""
                if pub_time:
                    try:
                        if isinstance(pub_time, (int, float)):
                            date_str = datetime.fromtimestamp(pub_time).strftime("%d/%m/%Y %H:%M")
                        else:
                            date_str = str(pub_time)[:16]
                    except: pass
                if title:
                    raw_news.append({"title": title, "publisher": publisher, "link": link, "date": date_str})
    except:
        pass

    news_sentiment_score, scored_news = score_news_sentiment(raw_news)

    # Scores individuels
    tech_score = 5.0
    if rsi_val:
        if rsi_val < 30: tech_score += 1.5
        elif 40 <= rsi_val <= 65: tech_score += 0.5
        elif rsi_val > 70: tech_score -= 1.0
    if macd_val and macd_val > 0: tech_score += 1.0
    else: tech_score -= 0.5
    if golden_cross: tech_score += 0.5
    if adx_val and adx_val > 35: tech_score += 0.5
    tech_score = max(0, min(10, tech_score))

    rev_growth = clean(info.get("revenueGrowth"))
    fund_score = 5.0
    if rev_growth:
        if rev_growth > 0.20: fund_score += 2.0
        elif rev_growth > 0.05: fund_score += 0.5
        elif rev_growth < 0: fund_score -= 1.5
    pe = clean(info.get("trailingPE"))
    if pe:
        if pe < 15: fund_score += 1.0
        elif pe > 50: fund_score -= 1.5
    margins = clean(info.get("profitMargins"))
    if margins:
        if margins > 0.20: fund_score += 0.5
        elif margins < 0: fund_score -= 1.0
    fund_score = max(0, min(10, fund_score))

    sent_score = max(0, min(10, buy_pct / 10))
    risk_score = max(0, min(10, 10 - (std_dev or 20)/10))
    if sharpe and sharpe > 1.5: risk_score += 1.0
    elif sharpe and sharpe < 0: risk_score -= 1.5
    risk_score = max(0, min(10, risk_score))

    # Score global avec sentiment actualites 15%
    global_score = round(
        tech_score * 0.35 +
        fund_score * 0.25 +
        sent_score * 0.15 +
        news_sentiment_score * 0.15 +
        risk_score * 0.10,
        1
    )

    if global_score >= 7.5: rec = "buy"
    elif global_score >= 6.0: rec = "hold"
    elif global_score >= 4.5: rec = "wait"
    else: rec = "sell"

    forces = []
    risks = []
    if tech_score >= 7: forces.append("Analyse technique favorable ({}/10)".format(round(tech_score,1)))
    if fund_score >= 7: forces.append("Fondamentaux solides ({}/10)".format(round(fund_score,1)))
    if buy_pct >= 65: forces.append("{}% des analystes recommandent l achat".format(buy_pct))
    if news_sentiment_score >= 7: forces.append("Actualites positives (score {}/10)".format(news_sentiment_score))
    if golden_cross: forces.append("Golden Cross actif")
    if tech_score < 4: risks.append("Signaux techniques negatifs ({}/10)".format(round(tech_score,1)))
    if news_sentiment_score <= 3: risks.append("Actualites negatives (score {}/10)".format(news_sentiment_score))
    if (std_dev or 0) > 35: risks.append("Forte volatilite ({:.1f}% ann.)".format(std_dev or 0))
    if max_dd and max_dd < -20: risks.append("Drawdown important ({:.1f}%)".format(max_dd))
    if sell_pct > 30: risks.append("{}% des analystes recommandent la vente".format(sell_pct))

    return {
        "ticker": ticker.upper(),
        "name": info.get("longName", ticker),
        "sector": info.get("sector") or info.get("quoteType", "N/A"),
        "currency": info.get("currency", "USD"),
        "price": {
            "current": clean(info.get("currentPrice") or info.get("regularMarketPrice") or price),
            "change_24h": clean(info.get("regularMarketChangePercent")),
            "volume": info.get("regularMarketVolume"),
            "market_cap": info.get("marketCap"),
        },
        "technical": {
            "rsi": rsi_val,
            "macd": {"value": macd_val, "signal": macd_sig, "histogram": macd_hist},
            "moving_averages": {"sma_20": sma_20, "sma_50": sma_50, "sma_200": sma_200, "golden_cross": golden_cross, "price_above_sma20": bool(price and sma_20 and price > sma_20), "price_above_sma50": bool(price and sma_50 and price > sma_50), "price_above_sma200": bool(price and sma_200 and price > sma_200)},
            "bollinger": {"upper": boll_upper, "lower": boll_lower},
            "stochastic": {"k": stoch_k},
            "adx": {"value": adx_val},
            "ichimoku": {"price_above_cloud": bool(price and sma_50 and price > sma_50)},
        },
        "fundamental": {
            "pe_ratio": clean(info.get("trailingPE")),
            "forward_pe": clean(info.get("forwardPE")),
            "eps": clean(info.get("trailingEps")),
            "revenue_growth": clean(info.get("revenueGrowth")),
            "profit_margins": clean(info.get("profitMargins")),
            "dividend_yield": clean(info.get("dividendYield")),
            "dividend_per_share": clean(info.get("dividendRate")),
            "debt_to_equity": clean(info.get("debtToEquity")),
            "return_on_equity": clean(info.get("returnOnEquity")),
            "free_cash_flow": info.get("freeCashflow"),
        },
        "analysts": {
            "buy_pct": buy_pct,
            "hold_pct": hold_pct,
            "sell_pct": sell_pct,
            "target_mean": clean(info.get("targetMeanPrice")),
            "target_high": clean(info.get("targetHighPrice")),
            "target_low": clean(info.get("targetLowPrice")),
        },
        "risk": {
            "beta": clean(beta),
            "std_dev_annual": clean(std_dev),
            "max_drawdown": clean(max_dd),
            "sharpe_ratio": clean(sharpe),
            "var_95": clean(float(np.percentile(returns, 5) * 100)),
        },
        "scoring": {
            "global_score": global_score,
            "breakdown": {
                "technique": {"score": round(tech_score,1), "weight": "35%"},
                "fondamental": {"score": round(fund_score,1), "weight": "25%"},
                "analystes": {"score": round(sent_score,1), "weight": "15%"},
                "actualites": {"score": news_sentiment_score, "weight": "15%"},
                "risque": {"score": round(risk_score,1), "weight": "10%"},
            },
            "recommendation": rec,
            "recommendation_reason": "Analyse IA multi-sources : technique + fondamental + analystes + actualites",
            "forces": forces[:5],
            "risks": risks[:5],
        },
        "news": scored_news,
        "analyzed_at": datetime.utcnow().isoformat(),
    }
'''

with open('C:/tradingIA/backend/app/api/routes.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK - routes.py avec scoring sentiment actualites ecrit avec succes')
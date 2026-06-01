"use client";
import { useState, useEffect } from 'react';
const API = 'http://localhost:8000';
const WL = [{t:'AAPL'},{t:'TSLA'},{t:'NVDA'},{t:'SPY'},{t:'MSFT'}];
export default function Home() {
  const [ticker, setTicker] = useState('AAPL');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  useEffect(() => { load(ticker); }, [ticker]);
  async function load(t) {
    setLoading(true); setError(null); setData(null);
    try { const r = await fetch(API+'/api/analyze/'+encodeURIComponent(t)); if(!r.ok) throw new Error('Erreur'); setData(await r.json()); } catch(e){ setError(e.message); }
    setLoading(false);
  }
  return (
    <div style={{fontFamily:'system-ui',background:'#f5f5f5',minHeight:'100vh'}}>
      <div style={{background:'#fff',padding:'12px 20px',display:'flex',gap:16,alignItems:'center',borderBottom:'1px solid #eee'}}>
        <b>TradingIA</b>
        <input value={search} onChange={e=>setSearch(e.target.value.toUpperCase())} onKeyDown={e=>{if(e.key==='Enter'&&search){setTicker(search);setSearch('');}}} placeholder='Ticker puis Entree' style={{flex:1,maxWidth:400,padding:'8px 12px',border:'1px solid #ddd',borderRadius:8}} />
        {WL.map(w=><button key={w.t} onClick={()=>setTicker(w.t)} style={{padding:'6px 12px',borderRadius:20,border:'1px solid #ddd',background:ticker===w.t?'#1D9E75':'#fff',color:ticker===w.t?'#fff':'#333',cursor:'pointer'}}>{w.t}</button>)}
      </div>
      <div style={{padding:20}}>
        {loading && <div style={{textAlign:'center',padding:80,fontSize:18}}>Analyse de {ticker} en cours... (30-60 sec)</div>}
        {error && <div style={{textAlign:'center',padding:80,color:'red'}}>{error}</div>}
        {data && !loading && <div style={{display:'flex',flexDirection:'column',gap:16}}>
          <div style={{background:'#fff',borderRadius:12,padding:20,display:'flex',justifyContent:'space-between'}}>
            <div><div style={{fontSize:24,fontWeight:600}}>{data.name}</div><div style={{color:'#888'}}>{data.ticker} - {data.sector}</div></div>
            <div style={{textAlign:'right'}}><div style={{fontSize:36,fontWeight:600}}>\</div><div style={{color:'#888'}}>Prix actuel</div></div>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16}}>
            <div style={{background:'#fff',borderRadius:12,padding:20}}>
              <div style={{fontSize:12,fontWeight:600,color:'#888',marginBottom:12}}>SCORE IA</div>
              <div style={{fontSize:64,fontWeight:600,color:data.scoring?.global_score>=7?'#1D9E75':data.scoring?.global_score>=5?'#BA7517':'#E24B4A'}}>{data.scoring?.global_score}<span style={{fontSize:24,color:'#aaa'}}>/10</span></div>
            </div>
            <div style={{background:'#fff',borderRadius:12,padding:20}}>
              <div style={{fontSize:12,fontWeight:600,color:'#888',marginBottom:12}}>RECOMMANDATION</div>
              <div style={{padding:'16px 20px',borderRadius:10,fontSize:20,fontWeight:600,background:data.scoring?.recommendation==='buy'?'#EAF3DE':data.scoring?.recommendation==='sell'?'#FCEBEB':'#FAEEDA',color:data.scoring?.recommendation==='buy'?'#27500A':data.scoring?.recommendation==='sell'?'#791F1F':'#633806'}}>{data.scoring?.recommendation==='buy'?'ACHETER':data.scoring?.recommendation==='sell'?'VENDRE':data.scoring?.recommendation==='hold'?'CONSERVER':'ATTENDRE'}</div>
              <div style={{marginTop:12,fontSize:13,color:'#666'}}>{data.scoring?.recommendation_reason}</div>
            </div>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16}}>
            <div style={{background:'#fff',borderRadius:12,padding:20}}>
              <div style={{fontSize:12,fontWeight:600,color:'#888',marginBottom:12}}>TECHNIQUE</div>
              {[['RSI',data.technical?.rsi?.toFixed(1)],['MACD',data.technical?.macd?.value?.toFixed(2)],['SMA20',data.technical?.moving_averages?.sma_20?.toFixed(2)],['SMA50',data.technical?.moving_averages?.sma_50?.toFixed(2)],['ADX',data.technical?.adx?.value?.toFixed(1)],['Golden Cross',data.technical?.moving_averages?.golden_cross?'Oui':'Non']].map(([k,v])=><div key={k} style={{display:'flex',justifyContent:'space-between',padding:'7px 0',borderBottom:'1px solid #f5f5f5',fontSize:13}}><span style={{color:'#666'}}>{k}</span><span style={{fontWeight:500}}>{v??'N/A'}</span></div>)}
            </div>
            <div style={{background:'#fff',borderRadius:12,padding:20}}>
              <div style={{fontSize:12,fontWeight:600,color:'#888',marginBottom:12}}>FONDAMENTAL</div>
              {[['PER',data.fundamental?.pe_ratio?.toFixed(1)],['EPS',data.fundamental?.eps?.toFixed(2)],['Croissance CA',data.fundamental?.revenue_growth!=null?(data.fundamental.revenue_growth*100).toFixed(1)+'%':'N/A'],['Marges',data.fundamental?.profit_margins!=null?(data.fundamental.profit_margins*100).toFixed(1)+'%':'N/A'],['Dividende',data.fundamental?.dividend_yield?(data.fundamental.dividend_yield*100).toFixed(2)+'%':'Aucun'],['ROE',data.fundamental?.return_on_equity!=null?(data.fundamental.return_on_equity*100).toFixed(1)+'%':'N/A']].map(([k,v])=><div key={k} style={{display:'flex',justifyContent:'space-between',padding:'7px 0',borderBottom:'1px solid #f5f5f5',fontSize:13}}><span style={{color:'#666'}}>{k}</span><span style={{fontWeight:500}}>{v??'N/A'}</span></div>)}
            </div>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16}}>
            <div style={{background:'#fff',borderRadius:12,padding:20}}>
              <div style={{fontSize:12,fontWeight:600,color:'#888',marginBottom:12}}>ANALYSTES</div>
              <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:10,marginBottom:12}}>
                {[['Acheter',data.analysts?.buy_pct,'#1D9E75'],['Conserver',data.analysts?.hold_pct,'#BA7517'],['Vendre',data.analysts?.sell_pct,'#E24B4A']].map(([l,v,c])=><div key={l} style={{background:'#f9f9f9',borderRadius:8,padding:12,textAlign:'center'}}><div style={{fontSize:28,fontWeight:600,color:c}}>{v}%</div><div style={{fontSize:11,color:'#888'}}>{l}</div></div>)}
              </div>
              {[['Cible moy.',data.analysts?.target_mean?.toFixed(0)],['Cible haute',data.analysts?.target_high?.toFixed(0)],['Cible basse',data.analysts?.target_low?.toFixed(0)]].map(([k,v])=><div key={k} style={{display:'flex',justifyContent:'space-between',padding:'7px 0',borderBottom:'1px solid #f5f5f5',fontSize:13}}><span style={{color:'#666'}}>{k}</span><span style={{fontWeight:500}}>{v??'N/A'}</span></div>)}
            </div>
            <div style={{background:'#fff',borderRadius:12,padding:20}}>
              <div style={{fontSize:12,fontWeight:600,color:'#888',marginBottom:12}}>RISQUE</div>
              {[['Beta',data.risk?.beta?.toFixed(2)],['Volatilite',data.risk?.std_dev_annual?.toFixed(1)+'%'],['Max Drawdown',data.risk?.max_drawdown?.toFixed(1)+'%'],['Sharpe',data.risk?.sharpe_ratio?.toFixed(2)]].map(([k,v])=><div key={k} style={{display:'flex',justifyContent:'space-between',padding:'7px 0',borderBottom:'1px solid #f5f5f5',fontSize:13}}><span style={{color:'#666'}}>{k}</span><span style={{fontWeight:500}}>{v??'N/A'}</span></div>)}
            </div>
          </div>
        </div>}
      </div>
    </div>
  );
}

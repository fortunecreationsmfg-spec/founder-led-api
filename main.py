"""
FastAPI Backend for Founder-Led Investment App
With caching to avoid Yahoo Finance rate limits
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import yfinance as yf
from datetime import datetime, timedelta
import time

app = FastAPI(title="Founder-Led Investment API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory cache
cache = {}
CACHE_DURATION = 3600  # 1 hour in seconds

FOUNDER_LED_COMPANIES = [
    {"ticker": "META", "name": "Meta Platforms", "founder": "Mark Zuckerberg", "sector": "Information Technology", "founded_year": 2004, "ipo_year": 2012, "network_effects_rank": 10, "founder_leadership_rank": 10, "cramer_recommendation": "sell", "cramer_date": "2022-10-25", "top_seven": True},
    {"ticker": "NVDA", "name": "Nvidia", "founder": "Jensen Huang", "sector": "Information Technology", "founded_year": 1993, "ipo_year": 1999, "network_effects_rank": 8, "founder_leadership_rank": 10, "cramer_recommendation": "sell", "cramer_date": "2023-01-15", "top_seven": True},
    {"ticker": "TSLA", "name": "Tesla", "founder": "Elon Musk", "sector": "Consumer Discretionary", "founded_year": 2003, "ipo_year": 2010, "network_effects_rank": 7, "founder_leadership_rank": 10, "cramer_recommendation": "sell", "cramer_date": "2023-04-20", "top_seven": False},
    {"ticker": "PLTR", "name": "Palantir", "founder": "Peter Thiel", "sector": "Information Technology", "founded_year": 2003, "ipo_year": 2020, "network_effects_rank": 7, "founder_leadership_rank": 10, "cramer_recommendation": "sell", "cramer_date": "2024-01-08", "top_seven": True},
    {"ticker": "NFLX", "name": "Netflix", "founder": "Reed Hastings", "sector": "Communication Services", "founded_year": 1997, "ipo_year": 2002, "network_effects_rank": 9, "founder_leadership_rank": 8, "cramer_recommendation": "buy", "cramer_date": "2022-06-10", "top_seven": True},
    {"ticker": "HOOD", "name": "Robinhood", "founder": "Vladimir Tenev", "sector": "Financials", "founded_year": 2013, "ipo_year": 2021, "network_effects_rank": 8, "founder_leadership_rank": 10, "cramer_recommendation": "sell", "cramer_date": "2021-08-15", "top_seven": True},
    {"ticker": "COIN", "name": "Coinbase", "founder": "Brian Armstrong", "sector": "Financials", "founded_year": 2012, "ipo_year": 2021, "network_effects_rank": 8, "founder_leadership_rank": 10, "cramer_recommendation": "buy", "cramer_date": "2022-05-20", "top_seven": True},
    {"ticker": "AVGO", "name": "Broadcom", "founder": "Henry Samueli", "sector": "Information Technology", "founded_year": 1991, "ipo_year": 2009, "network_effects_rank": 6, "founder_leadership_rank": 8, "cramer_recommendation": None, "cramer_date": None, "top_seven": True},
    {"ticker": "CRM", "name": "Salesforce", "founder": "Marc Benioff", "sector": "Information Technology", "founded_year": 1999, "ipo_year": 2004, "network_effects_rank": 9, "founder_leadership_rank": 9, "cramer_recommendation": None, "cramer_date": None, "top_seven": False},
    {"ticker": "SQ", "name": "Block", "founder": "Jack Dorsey", "sector": "Financials", "founded_year": 2009, "ipo_year": 2015, "network_effects_rank": 8, "founder_leadership_rank": 10, "cramer_recommendation": "buy", "cramer_date": "2022-11-30", "top_seven": False}
]

class StockData(BaseModel):
    ticker: str
    name: str
    founder: str
    sector: str
    founded_year: int
    ipo_year: int
    network_effects_rank: int
    founder_leadership_rank: int
    current_price: float
    market_cap: float
    pe_ratio: Optional[float]
    ytd_return: float
    avg_200_day: float
    volume: int
    cramer_recommendation: Optional[str]
    cramer_date: Optional[str]
    top_seven: bool
    last_updated: str

class MARecommendation(BaseModel):
    action: str
    reason: str
    percent_above_ma: float

def get_stock_live_data(ticker: str):
    """Fetch live stock data with caching and rate limiting"""
    # Check cache first
    if ticker in cache:
        cached_data, cached_time = cache[ticker]
        if time.time() - cached_time < CACHE_DURATION:
            print(f"Using cached data for {ticker}")
            return cached_data
    
    try:
        # Add delay to avoid rate limiting
        time.sleep(0.5)
        
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        
        if hist.empty:
            return None
        
        current_price = hist['Close'].iloc[-1]
        avg_200_day = hist['Close'].rolling(window=200).mean().iloc[-1]
        
        # Calculate YTD return
        year_start = datetime(datetime.now().year, 1, 1)
        ytd_hist = stock.history(start=year_start)
        if not ytd_hist.empty:
            ytd_return = ((ytd_hist['Close'].iloc[-1] - ytd_hist['Close'].iloc[0]) / ytd_hist['Close'].iloc[0]) * 100
        else:
            ytd_return = 0.0
        
        # Try to get info, but handle if it fails
        try:
            info = stock.info
            market_cap = round(info.get('marketCap', 0) / 1e9, 2)
            pe_ratio = round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else None
            volume = info.get('volume', 0)
        except:
            market_cap = 0
            pe_ratio = None
            volume = 0
        
        data = {
            "current_price": round(current_price, 2),
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "ytd_return": round(ytd_return, 2),
            "avg_200_day": round(avg_200_day, 2),
            "volume": volume
        }
        
        # Cache the data
        cache[ticker] = (data, time.time())
        
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

def calculate_ma_recommendation(current_price: float, avg_200_day: float) -> MARecommendation:
    """Calculate buy/sell recommendation"""
    percent_above = ((current_price - avg_200_day) / avg_200_day) * 100
    
    if percent_above > 15:
        return MARecommendation(action="SELL", reason="Well above 200-day MA", percent_above_ma=round(percent_above, 2))
    elif percent_above < -5:
        return MARecommendation(action="BUY", reason="Below 200-day MA", percent_above_ma=round(percent_above, 2))
    else:
        return MARecommendation(action="HOLD", reason="Near 200-day MA", percent_above_ma=round(percent_above, 2))

@app.get("/")
async def root():
    return {
        "message": "Founder-Led Investment API",
        "version": "1.0.0",
        "endpoints": {
            "companies": "/api/companies",
            "company": "/api/companies/{ticker}",
            "top_seven": "/api/top-seven",
            "inverse_cramer": "/api/inverse-cramer",
            "health": "/api/health"
        }
    }

@app.get("/api/companies", response_model=List[StockData])
async def get_all_companies():
    """Get all companies with cached data"""
    results = []
    
    for company in FOUNDER_LED_COMPANIES:
        live_data = get_stock_live_data(company['ticker'])
        
        if live_data:
            results.append(StockData(
                ticker=company['ticker'],
                name=company['name'],
                founder=company['founder'],
                sector=company['sector'],
                founded_year=company['founded_year'],
                ipo_year=company['ipo_year'],
                network_effects_rank=company['network_effects_rank'],
                founder_leadership_rank=company['founder_leadership_rank'],
                current_price=live_data['current_price'],
                market_cap=live_data['market_cap'],
                pe_ratio=live_data['pe_ratio'],
                ytd_return=live_data['ytd_return'],
                avg_200_day=live_data['avg_200_day'],
                volume=live_data['volume'],
                cramer_recommendation=company['cramer_recommendation'],
                cramer_date=company['cramer_date'],
                top_seven=company['top_seven'],
                last_updated=datetime.now().isoformat()
            ))
    
    return results

@app.get("/api/companies/{ticker}", response_model=StockData)
async def get_company(ticker: str):
    """Get specific company data"""
    ticker = ticker.upper()
    company = next((c for c in FOUNDER_LED_COMPANIES if c['ticker'] == ticker), None)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    live_data = get_stock_live_data(ticker)
    if not live_data:
        raise HTTPException(status_code=500, detail="Unable to fetch stock data")
    
    return StockData(
        ticker=company['ticker'],
        name=company['name'],
        founder=company['founder'],
        sector=company['sector'],
        founded_year=company['founded_year'],
        ipo_year=company['ipo_year'],
        network_effects_rank=company['network_effects_rank'],
        founder_leadership_rank=company['founder_leadership_rank'],
        current_price=live_data['current_price'],
        market_cap=live_data['market_cap'],
        pe_ratio=live_data['pe_ratio'],
        ytd_return=live_data['ytd_return'],
        avg_200_day=live_data['avg_200_day'],
        volume=live_data['volume'],
        cramer_recommendation=company['cramer_recommendation'],
        cramer_date=company['cramer_date'],
        top_seven=company['top_seven'],
        last_updated=datetime.now().isoformat()
    )

@app.get("/api/top-seven")
async def get_top_seven():
    """Get top 7 performers"""
    top_seven = [c for c in FOUNDER_LED_COMPANIES if c['top_seven']]
    results = []
    
    for company in top_seven:
        live_data = get_stock_live_data(company['ticker'])
        if live_data:
            rec = calculate_ma_recommendation(live_data['current_price'], live_data['avg_200_day'])
            results.append({
                "ticker": company['ticker'],
                "name": company['name'],
                "founder": company['founder'],
                "current_price": live_data['current_price'],
                "avg_200_day": live_data['avg_200_day'],
                "ytd_return": live_data['ytd_return'],
                "recommendation": rec.dict(),
                "network_effects_rank": company['network_effects_rank'],
                "founder_leadership_rank": company['founder_leadership_rank']
            })
    
    results.sort(key=lambda x: x['ytd_return'], reverse=True)
    return results

@app.get("/api/inverse-cramer")
async def get_inverse_cramer():
    """Get Inverse Cramer plays"""
    buy_signals = []
    avoid_signals = []
    
    for company in FOUNDER_LED_COMPANIES:
        live_data = get_stock_live_data(company['ticker'])
        if not live_data:
            continue
            
        signal_data = {
            "ticker": company['ticker'],
            "name": company['name'],
            "founder": company['founder'],
            "cramer_date": company['cramer_date'],
            "current_price": live_data['current_price'],
            "ytd_return": live_data['ytd_return'],
            "network_effects_rank": company['network_effects_rank']
        }
        
        if company['cramer_recommendation'] == 'sell':
            buy_signals.append(signal_data)
        elif company['cramer_recommendation'] == 'buy':
            avoid_signals.append(signal_data)
    
    return {"buy_signals": buy_signals, "avoid_signals": avoid_signals}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "cache_size": len(cache)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

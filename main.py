"""
FastAPI backend for AIstrolog - Turkish Horoscope Application
Provides endpoints for zodiac sign data, rankings, and daily summaries
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import glob

app = FastAPI(
    title="AIstrolog API",
    description="Turkish Horoscope API with AI-powered summaries and rankings",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory
DATA_DIR = Path(__file__).parent / "data"

# Zodiac sign mappings (Turkish to English slug)
ZODIAC_SIGNS = {
    "Koç": "koc",
    "Boğa": "boga",
    "İkizler": "ikizler",
    "Yengeç": "yengec",
    "Aslan": "aslan",
    "Başak": "basak",
    "Terazi": "terazi",
    "Akrep": "akrep",
    "Yay": "yay",
    "Oğlak": "oglak",
    "Kova": "kova",
    "Balık": "balik",
}

# Reverse mapping
SLUG_TO_TURKISH = {v: k for k, v in ZODIAC_SIGNS.items()}

# Category mappings
CATEGORY_MAPPING = {
    "general": "genel",
    "love": "aşk",
    "money": "para",
    "health": "sağlık"
}


def get_latest_file(pattern: str) -> Optional[Path]:
    """Get the most recent file matching the pattern"""
    files = list(DATA_DIR.glob(pattern))
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)


def load_json_file(file_path: Path) -> Dict:
    """Load and parse JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")


def get_file_for_date(date_str: str, file_type: str = "summarized") -> Optional[Path]:
    """Get data file for specific date (format: DD-MM-YYYY or YYYY-MM-DD)"""
    # Convert DD-MM-YYYY to YYYY-MM-DD for file matching
    parts = date_str.split('-')
    if len(parts) == 3:
        if len(parts[0]) == 4:  # Already YYYY-MM-DD
            file_date = date_str
        else:  # DD-MM-YYYY format
            file_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
    else:
        return None
    
    # Try to find the file
    pattern = f"{file_type}_processed_daily_raw_{file_date}.json"
    file_path = DATA_DIR / pattern
    
    if file_path.exists():
        return file_path
    
    return None


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "AIstrolog API",
        "version": "1.0.0",
        "endpoints": {
            "burclar": "/api/burclar",
            "gunluk": "/api/gunluk/{sign}/{date}",
            "rankings": "/api/rankings/{date}",
            "available_dates": "/api/available-dates"
        }
    }


@app.get("/api/burclar")
async def get_zodiac_signs():
    """Get list of all zodiac signs"""
    signs = []
    for turkish_name, slug in ZODIAC_SIGNS.items():
        signs.append({
            "name": turkish_name,
            "slug": slug,
            "symbol": get_zodiac_symbol(slug)
        })
    return {"signs": signs}


@app.get("/api/gunluk/{sign}/{date}")
async def get_daily_horoscope(sign: str, date: str):
    """
    Get daily horoscope for a specific sign and date
    
    Parameters:
    - sign: zodiac sign slug (e.g., 'koc', 'boga')
    - date: date in DD-MM-YYYY format
    """
    # Validate sign
    turkish_name = SLUG_TO_TURKISH.get(sign)
    if not turkish_name:
        raise HTTPException(status_code=404, detail="Zodiac sign not found")
    
    # Get data file for date
    data_file = get_file_for_date(date, "summarized")
    
    if not data_file:
        # Try to get the latest available data
        data_file = get_latest_file("summarized_processed_daily_raw_*.json")
        if not data_file:
            raise HTTPException(status_code=404, detail="No horoscope data available")
    
    # Load data
    data = load_json_file(data_file)
    
    # Get sign data
    sign_data = data.get(turkish_name)
    if not sign_data:
        raise HTTPException(status_code=404, detail="Sign data not found")
    
    return {
        "sign": turkish_name,
        "slug": sign,
        "date": date,
        "horoscope": {
            "general": sign_data.get("genel", ""),
            "love": sign_data.get("aşk", ""),
            "money": sign_data.get("para", ""),
            "health": sign_data.get("sağlık", "")
        }
    }


@app.get("/api/rankings/{date}")
async def get_rankings(date: str, period: str = "daily"):
    """
    Get zodiac sign rankings for a specific date from rankings_history.json
    
    Parameters:
    - date: date in DD-MM-YYYY format (e.g., "23-11-2025")
    - period: "daily", "weekly", or "monthly" (query parameter)
    """
    # Load rankings history file
    history_file = DATA_DIR / "rankings_history.json"
    
    if not history_file.exists():
        raise HTTPException(status_code=404, detail="Rankings history not found")
    
    history_data = load_json_file(history_file)
    
    # Convert DD-MM-YYYY to YYYY-MM-DD for matching
    parts = date.split('-')
    if len(parts) == 3:
        if len(parts[0]) == 4:  # Already YYYY-MM-DD
            search_date = date
        else:  # DD-MM-YYYY format
            search_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
    else:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY")
    
    # Get dates to process based on period
    if period == "weekly":
        # Get last 7 days of data (or as many as available)
        target_date = datetime.strptime(search_date, "%Y-%m-%d")
        dates_to_process = []
        
        for i in range(7):
            check_date = target_date - timedelta(days=i)
            date_str = check_date.strftime("%Y-%m-%d")
            if date_str in history_data:
                dates_to_process.append(date_str)
        
        # If we don't have any data, use whatever we have
        if not dates_to_process and history_data:
            dates_to_process = list(history_data.keys())[:7]
            
    elif period == "monthly":
        # Get last 30 days of data (or as many as available)
        target_date = datetime.strptime(search_date, "%Y-%m-%d")
        dates_to_process = []
        
        for i in range(30):
            check_date = target_date - timedelta(days=i)
            date_str = check_date.strftime("%Y-%m-%d")
            if date_str in history_data:
                dates_to_process.append(date_str)
        
        # If we don't have any data, use whatever we have
        if not dates_to_process and history_data:
            dates_to_process = list(history_data.keys())[:30]
            
    else:  # daily
        dates_to_process = [search_date] if search_date in history_data else []
        
        # If requested date not found, use latest
        if not dates_to_process and history_data:
            latest_date = next(iter(history_data))
            dates_to_process = [latest_date]
            search_date = latest_date
    
    if not dates_to_process:
        raise HTTPException(status_code=404, detail="No ranking data available")
    
    # Calculate rankings based on period
    if period in ["weekly", "monthly"]:
        # Average scores across multiple days
        sign_scores = {
            "general": {},
            "love": {},
            "money": {},
            "health": {}
        }
        
        ranking_map = {
            "genel_ranking": "general",
            "aşk_ranking": "love",
            "para_ranking": "money",
            "sağlık_ranking": "health"
        }
        
        # Collect all scores
        for date_str in dates_to_process:
            date_rankings = history_data[date_str]
            
            for file_key, api_key in ranking_map.items():
                if file_key in date_rankings:
                    for item in date_rankings[file_key]:
                        burc = item['burc']
                        score = item['score']
                        
                        if burc not in sign_scores[api_key]:
                            sign_scores[api_key][burc] = []
                        sign_scores[api_key][burc].append(score)
        
        # Calculate averages and create rankings
        rankings = {
            "general": [],
            "love": [],
            "money": [],
            "health": []
        }
        
        for api_key in ["general", "love", "money", "health"]:
            for burc, scores in sign_scores[api_key].items():
                avg_score = sum(scores) / len(scores) if scores else 0
                slug = ZODIAC_SIGNS.get(burc, '')
                rankings[api_key].append({
                    "sign": burc,
                    "slug": slug,
                    "score": round(avg_score, 1)
                })
            
            # Sort by score descending
            rankings[api_key].sort(key=lambda x: x['score'], reverse=True)
    
    else:
        # Single day ranking
        date_rankings = history_data[dates_to_process[0]]
        
        rankings = {
            "general": [],
            "love": [],
            "money": [],
            "health": []
        }
        
        ranking_map = {
            "genel_ranking": "general",
            "aşk_ranking": "love",
            "para_ranking": "money",
            "sağlık_ranking": "health"
        }
        
        for file_key, api_key in ranking_map.items():
            if file_key in date_rankings:
                for item in date_rankings[file_key]:
                    slug = ZODIAC_SIGNS.get(item['burc'], '')
                    rankings[api_key].append({
                        "sign": item['burc'],
                        "slug": slug,
                        "score": item['score']
                    })
    
    # Convert date back to DD-MM-YYYY for response
    date_parts = search_date.split('-')
    display_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
    
    return {
        "date": display_date,
        "period": period,
        "days_analyzed": len(dates_to_process),
        "rankings": rankings
    }


@app.get("/api/available-dates")
async def get_available_dates():
    """Get list of available dates for horoscope data"""
    summarized_files = list(DATA_DIR.glob("summarized_processed_daily_raw_*.json"))
    
    # Also get dates from rankings_history.json
    rankings_dates = []
    history_file = DATA_DIR / "rankings_history.json"
    if history_file.exists():
        try:
            history_data = load_json_file(history_file)
            for date_key in history_data.keys():
                # Convert YYYY-MM-DD to DD-MM-YYYY
                parts = date_key.split('-')
                if len(parts) == 3:
                    dd_mm_yyyy = f"{parts[2]}-{parts[1]}-{parts[0]}"
                    rankings_dates.append(dd_mm_yyyy)
        except:
            pass
    
    dates = {
        "summarized": [],
        "rankings": rankings_dates
    }
    
    for file in summarized_files:
        # Extract date from filename: summarized_processed_daily_raw_YYYY-MM-DD.json
        date_part = file.stem.replace("summarized_processed_daily_raw_", "")
        # Convert YYYY-MM-DD to DD-MM-YYYY
        parts = date_part.split('-')
        if len(parts) == 3:
            dd_mm_yyyy = f"{parts[2]}-{parts[1]}-{parts[0]}"
            dates["summarized"].append(dd_mm_yyyy)
    
    # Sort dates (most recent first)
    dates["summarized"].sort(reverse=True)
    dates["rankings"].sort(reverse=True)
    
    return dates


def get_zodiac_symbol(slug: str) -> str:
    """Get zodiac symbol for slug"""
    symbols = {
        "koc": "♈",
        "boga": "♉",
        "ikizler": "♊",
        "yengec": "♋",
        "aslan": "♌",
        "basak": "♍",
        "terazi": "♎",
        "akrep": "♏",
        "yay": "♐",
        "oglak": "♑",
        "kova": "♒",
        "balik": "♓"
    }
    return symbols.get(slug, "")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

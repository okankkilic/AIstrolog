# AIstrolog API Documentation

FastAPI backend for Turkish Horoscope Application with AI-powered summaries and rankings.

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install fastapi uvicorn

# Or using requirements.txt
pip install -r requirements.txt
```

### Running the Server

```bash
# Development mode
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Root
- **GET** `/`
  - Returns API information and available endpoints
  - Response: 
    ```json
    {
      "name": "AIstrolog API",
      "version": "1.0.0",
      "endpoints": {
        "burclar": "/api/burclar",
        "gunluk": "/api/gunluk/{sign}/{date}",
        "rankings": "/api/rankings/{date}",
        "available_dates": "/api/available-dates"
      }
    }
    ```

### Get Zodiac Signs
- **GET** `/api/burclar`
  - Returns list of all 12 zodiac signs
  - Response:
    ```json
    {
      "signs": [
        {
          "name": "Koç",
          "slug": "koc",
          "symbol": "♈"
        },
        ...
      ]
    }
    ```

### Get Daily Horoscope
- **GET** `/api/gunluk/{sign}/{date}`
  - Parameters:
    - `sign`: Zodiac sign slug (e.g., `koc`, `boga`, `ikizler`)
    - `date`: Date in DD-MM-YYYY format (e.g., `23-11-2025`)
  - Response:
    ```json
    {
      "sign": "Koç",
      "slug": "koc",
      "date": "23-11-2025",
      "horoscope": {
        "general": "Bugün yıldızlar sizin için...",
        "love": "Aşk hayatınızda...",
        "money": "Maddi konularda...",
        "health": "Sağlık açısından..."
      }
    }
    ```

### Get Rankings
- **GET** `/api/rankings/{date}`
  - Parameters:
    - `date`: Date in DD-MM-YYYY format
    - `period` (optional): Query parameter - `daily`, `weekly`, or `monthly` (default: `daily`)
  - Examples:
    - `/api/rankings/23-11-2025` - Daily rankings
    - `/api/rankings/23-11-2025?period=weekly` - Average of last 7 days
    - `/api/rankings/23-11-2025?period=monthly` - Average of last 30 days
  - Response:
    ```json
    {
      "date": "23-11-2025",
      "period": "weekly",
      "days_analyzed": 7,
      "rankings": {
        "general": [
          { "sign": "Aslan", "slug": "aslan", "score": 95 },
          { "sign": "Koç", "slug": "koc", "score": 88 },
          ...
        ],
        "love": [...],
        "money": [...],
        "health": [...]
      }
    }
    ```

### Get Available Dates
- **GET** `/api/available-dates`
  - Returns list of dates with available data
  - Response:
    ```json
    {
      "summarized": ["23-11-2025", "22-11-2025", ...],
      "scored": ["23-11-2025", "22-11-2025", ...]
    }
    ```

## 🎯 Zodiac Sign Slugs

| Turkish Name | Slug     | Symbol |
|-------------|----------|--------|
| Koç         | koc      | ♈      |
| Boğa        | boga     | ♉      |
| İkizler     | ikizler  | ♊      |
| Yengeç      | yengec   | ♋      |
| Aslan       | aslan    | ♌      |
| Başak       | basak    | ♍      |
| Terazi      | terazi   | ♎      |
| Akrep       | akrep    | ♏      |
| Yay         | yay      | ♐      |
| Oğlak       | oglak    | ♑      |
| Kova        | kova     | ♒      |
| Balık       | balik    | ♓      |

## 📁 Data Files

The API reads data from the `data/` directory:

- **Summarized Data**: `summarized_processed_daily_raw_YYYY-MM-DD.json`
  - Contains AI-summarized horoscope text for each sign and category
  
- **Scored Data**: `scored_processed_daily_raw_YYYY-MM-DD.json`
  - Contains sentiment scores and rankings for each sign

## 🔧 Configuration

### CORS Settings

The API allows cross-origin requests from:
- `http://localhost:3000` (Next.js frontend)

To add more origins, modify the `CORSMiddleware` settings in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🛠️ Development

### Project Structure

```
AIstrolog/
├── main.py                 # FastAPI application
├── data/                   # Data directory
│   ├── summarized_*.json   # AI summaries
│   └── scored_*.json       # Sentiment scores
├── scraper.py             # Data collection
├── categorizer.py         # Text categorization
├── summarizer.py          # AI summarization
└── scorer.py              # Sentiment analysis
```

### Running the Full Pipeline

```bash
# 1. Scrape data
python scraper.py

# 2. Categorize sentences
python categorize_horoscopes.py

# 3. Generate summaries
python summarizer.py

# 4. Calculate scores
python scorer.py

# 5. Start API server
python main.py
```

## 📊 API Status

- **Version**: 1.0.0
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Port**: 8000
- **Host**: 0.0.0.0

## 🔒 Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful request
- `404 Not Found`: Resource not found (invalid sign or date)
- `500 Internal Server Error`: Server error (data loading issues)

Error response format:
```json
{
  "detail": "Error message"
}
```

## 📝 Example Usage

### Using cURL

```bash
# Get all zodiac signs
curl http://localhost:8000/api/burclar

# Get daily horoscope for Koç on 23-11-2025
curl http://localhost:8000/api/gunluk/koc/23-11-2025

# Get rankings for 23-11-2025
curl http://localhost:8000/api/rankings/23-11-2025
```

### Using JavaScript/Fetch

```javascript
// Get daily horoscope
const response = await fetch('http://localhost:8000/api/gunluk/koc/23-11-2025');
const data = await response.json();
console.log(data.horoscope.general);

// Get rankings
const rankings = await fetch('http://localhost:8000/api/rankings/23-11-2025');
const rankData = await rankings.json();
console.log(rankData.rankings.general);
```

## 🎨 Frontend Integration

The API is designed to work with the Next.js frontend located in the `frontend/` directory.

Frontend URL: `http://localhost:3000`

## 📄 License

MIT License

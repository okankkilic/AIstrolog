"""
Tam Pipeline: Scraping ve Kategorizasyon

Burç yorumlarını çekip otomatik olarak kategorize eder.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_scraper():
    """Burç yorumlarını çek"""
    print("Burç yorumları çekiliyor...")
    result = subprocess.run([sys.executable, "scraper.py"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Scraping tamamlandı!")
        return True
    else:
        print(f"Scraping hatası: {result.stderr}")
        return False


def run_categorizer(input_file):
    """Çekilen verileri kategorize et"""
    print("\nKategorizasyon başlıyor...")
    result = subprocess.run(
        [sys.executable, "categorize_horoscopes.py", input_file],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("Kategorizasyon tamamlandı!")
        print(result.stdout)
        return True
    else:
        print(f"Kategorizasyon hatası: {result.stderr}")
        return False


def main():
    print("=" * 60)
    print("Burç Yorumu Pipeline")
    print("=" * 60)
    
    if not run_scraper():
        print("\nPipeline başarısız: Scraping hatası")
        return
    
    today = datetime.now().strftime('%Y-%m-%d')
    input_file = f"data/daily_raw_{today}.json"
    
    if not Path(input_file).exists():
        print(f"\nDosya bulunamadı: {input_file}")
        return
    
    if not run_categorizer(input_file):
        print("\nPipeline başarısız: Kategorizasyon hatası")
        return
    
    print("\n" + "=" * 60)
    print("Pipeline başarıyla tamamlandı!")
    print("=" * 60)
    print(f"\nİşlenmiş dosya: data/processed_daily_raw_{today}.json")


if __name__ == "__main__":
    main()

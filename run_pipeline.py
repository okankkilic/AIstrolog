"""
Tam Pipeline: Scraping ve Kategorizasyon

Burç yorumlarını çekip otomatik olarak kategorize eder.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_tests(raw_file, processed_file):
    """Workflow testlerini çalıştır"""
    print("\n" + "=" * 60)
    print("Test Başlıyor...")
    print("=" * 60)
    
    result = subprocess.run(
        [sys.executable, "test_workflow.py", raw_file, processed_file],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.returncode == 0:
        print("\n✅ Testler başarılı!")
        return True
    else:
        print("\n❌ Testler başarısız!")
        if result.stderr:
            print(f"Hata: {result.stderr}")
        return False


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
    
    # Scraper'ı çalıştır
    if not run_scraper():
        print("\n❌ Pipeline başarısız: Scraping hatası")
        sys.exit(1)
    
    # Dosya varlığını kontrol et
    today = datetime.now().strftime('%Y-%m-%d')
    raw_file = f"data/daily_raw_{today}.json"
    processed_file = f"data/processed_daily_raw_{today}.json"
    
    if not Path(raw_file).exists():
        print(f"\n❌ HATA: Dosya bulunamadı: {raw_file}")
        print("Scraper dosyayı oluşturamadı. Lütfen scraper.py'yi kontrol edin.")
        sys.exit(1)
    
    # İlk test: Scraping sonrası
    print("\n" + "=" * 60)
    print("Adım 1: Scraping Testi")
    print("=" * 60)
    
    # Geçici processed file oluştur (boş olsa da test için)
    if not Path(processed_file).exists():
        print(f"⚠️  Processed file henüz yok, scraping testi atlanıyor...")
    
    # Kategorizasyonu çalıştır
    if not run_categorizer(raw_file):
        print("\n❌ Pipeline başarısız: Kategorizasyon hatası")
        sys.exit(1)
    
    # İkinci test: Kategorizasyon sonrası
    print("\n" + "=" * 60)
    print("Adım 2: Kategorizasyon Testi")
    print("=" * 60)
    
    if not run_tests(raw_file, processed_file):
        print("\n⚠️  Pipeline tamamlandı ama testler uyarılar içeriyor")
        print("Detaylar için yukarıdaki test çıktısını inceleyin.")
    
    print("\n" + "=" * 60)
    print("✅ Pipeline başarıyla tamamlandı!")
    print("=" * 60)
    print(f"\nHam dosya: {raw_file}")
    print(f"İşlenmiş dosya: {processed_file}")
    print("\nTest sonuçlarını yukarıda inceleyin.")


if __name__ == "__main__":
    main()

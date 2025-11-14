# AIstrolog

Günlük burç yorumlarını toplayan ve kategorize eden otomasyon sistemi.

## Özellikler

- 11 farklı kaynaktan burç yorumu toplama
- Yorumları otomatik olarak aşk, para ve sağlık kategorilerine ayırma
- Orijinal metinleri koruyarak kopyalama
- Tek komutla tam pipeline çalıştırma
- GitHub Actions ile otomatik günlük veri çekme (her gün 05:00)

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

### Basit kullanım

```bash
# Sadece veri çek
python scraper.py

# Sadece kategorize et
python categorize_horoscopes.py

# İkisini birden yap
python run_pipeline.py
```

### Gelişmiş kullanım

```bash
# Belirli bir dosyayı kategorize et
python categorize_horoscopes.py data/daily_raw_2025-11-14.json

# Çıktı dosyası belirt
python categorize_horoscopes.py input.json output.json

# Sonuçları doğrula
python verify_categorization.py ham_dosya.json islenmiş_dosya.json kaynak burç
```

## Kategorizasyon Nasıl Çalışır?

Script, "genel" anahtarındaki metni cümlelere ayırır ve her cümleyi analiz eder:

**Aşk kategorisi:** aşk, sevgi, partner, flört, ilişki, kalp, duygular, evlilik vb.

**Para kategorisi:** para, maddi, harcama, birikim, yatırım, kazanç, finans, maaş vb.

**Sağlık kategorisi:** sağlık, enerji, stres, egzersiz, spor, beslenme, uyku vb.

Önemli: Orijinal "genel" metin hiç değişmez. İlgili cümleler sadece uygun kategorilere kopyalanır.

## Veri Formatı

Ham veri:
```json
{
  "onedio": {
    "Koç": {
      "genel": "Bugün harika bir gün. Aşkta şanslısın. Para konusunda dikkatli ol.",
      "aşk": null,
      "para": null,
      "sağlık": null
    }
  }
}
```

İşlenmiş veri:
```json
{
  "onedio": {
    "Koç": {
      "genel": "Bugün harika bir gün. Aşkta şanslısın. Para konusunda dikkatli ol.",
      "aşk": "Aşkta şanslısın.",
      "para": "Para konusunda dikkatli ol.",
      "sağlık": null
    }
  }
}
```

## Desteklenen Kaynaklar

Milliyet, Hürriyet, NTV, Habertürk, Elle, Onedio, Mynet, TwitBurc, Vogue, GünlükBurç, MyBurç

## Proje Yapısı

```
AIstrolog/
├── .github/
│   └── workflows/
│       ├── daily_scrape.yml      # Günlük otomatik scraping
│       └── test.yml              # Push'larda test
├── scraper.py                    # Burç verilerini çeker
├── categorize_horoscopes.py      # Kategorize eder
├── run_pipeline.py               # İkisini birden çalıştırır
├── verify_categorization.py      # Sonuçları doğrular
├── requirements.txt
└── data/
    ├── daily_raw_*.json          # Ham veri
    └── processed_*.json          # İşlenmiş veri
```

## CI/CD

Proje GitHub Actions kullanarak otomatik çalışır:

**Günlük Scraping:** Her gün saat 05:00'de otomatik olarak burç verileri çekilir ve kategorize edilir.

**Test Pipeline:** Her push'ta kod kalitesi kontrol edilir ve import testleri çalıştırılır.

Manuel tetikleme için GitHub Actions sekmesinden "Daily Horoscope Scraping" workflow'unu çalıştırabilirsiniz.

## Gereksinimler

Python 3.7+, requests, beautifulsoup4, pandas

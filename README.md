# AIstrolog

Günlük burç yorumlarını toplayan, kategorize eden ve özetleyen otomasyon sistemi.

## Özellikler

- 10 farklı kaynaktan burç yorumu toplama
- Yorumları otomatik olarak aşk, para ve sağlık kategorilerine ayırma
- Birden fazla kaynaktaki yorumları akıllıca özetleme
- Orijinal metinleri koruyarak kopyalama
- Tek komutla tam pipeline çalıştırma
- GitHub Actions ile otomatik günlük çalıştırma

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

# Özetle (kategorize edilmiş veri gerekli)
python summarizer.py

# Full pipeline (scrape + kategorize + özetle + test)
python run_full_pipeline.py

# Hızlı pipeline (scrape + kategorize + test)
python run_pipeline.py
```

### Test ve Doğrulama

```bash
# Workflow'u test et (önerilen!)
python test_workflow.py data/daily_raw_2025-11-15.json data/processed_daily_raw_2025-11-15.json

# Detaylı inceleme
python verify_categorization.py data/daily_raw_2025-11-15.json data/processed_daily_raw_2025-11-15.json

# Belirli bir kaynak/burcu incele
python verify_categorization.py data/daily_raw_2025-11-15.json data/processed_daily_raw_2025-11-15.json milliyet Koç
```

**⚠️ Önemli:** Her scraping sonrası mutlaka test çalıştırın! Test, sahte/duplike veri kullanımını otomatik tespit eder.

### Gelişmiş kullanım

```bash
# Belirli bir dosyayı kategorize et
python categorize_horoscopes.py data/daily_raw_2025-11-14.json

# Belirli bir dosyayı özetle
python summarizer.py data/processed_daily_raw_2025-11-14.json

# Çıktı dosyası belirt
python categorize_horoscopes.py input.json output.json
python summarizer.py input.json output.json
```

## Özetleme Nasıl Çalışır?

Özetleme sistemi, farklı kaynaklardan gelen aynı burç/kategori yorumlarını birleştirerek en bilgilendirici özeti oluşturur:

1. **Cümle bazlı analiz:** Her kaynaktan gelen metinler cümlelere ayrılır
2. **Benzerlik tespiti:** Tekrar eden veya çok benzer cümleler çıkarılır
3. **Bilgi birleştirme:** Farklı kaynaklardan gelen benzersiz bilgiler birleştirilir
4. **Akıcı özet:** En bilgilendirici cümleler doğal bir özet oluşturur

**Sonuç:** 10 farklı kaynaktan gelen yorumlar, tekrar olmadan birleştirilmiş tek bir özette toplanır.

Detaylı bilgi için: [SUMMARIZATION_GUIDE.md](SUMMARIZATION_GUIDE.md)

## Test Sistemi

Workflow'un doğru çalıştığını garanti altına almak için kapsamlı test sistemi:

### Otomatik Kontroller

✅ **Duplike İçerik:** Aynı metin birden fazla burç için kullanılmış mı?
✅ **Generic/Test İçerik:** Sahte placeholder veriler var mı?
✅ **Boş İçerik:** Hangi kaynaklar veri çekememiş?
✅ **Kategorizasyon Kalitesi:** İçerikler doğru kategorize ediliyor mu?
✅ **Veri Güncelliği:** Bugüne ait veri mi?
✅ **Kategori Benzersizliği:** Her kategori farklı içerik mi?

### Test Sonuçları

- ✅ **TEST BAŞARILI:** Workflow düzgün çalışıyor
- ⚠️ **KISMEN BAŞARILI:** Bazı uyarılar var, kontrol edin
- ❌ **TEST BAŞARISIZ:** Kritik sorunlar var, düzeltilmeli

Detaylı test kılavuzu için: [TEST_GUIDE.md](TEST_GUIDE.md)

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

Özetlenmiş veri:
```json
{
  "Koç": {
    "genel": "Bugün harika bir gün. Enerji dolu hissedeceksin...",
    "aşk": "Aşkta şanslısın. İlişkilerinizde pozitif gelişmeler var...",
    "para": "Para konusunda dikkatli ol. Harcamalarınızı kontrol edin...",
    "sağlık": "Sağlığınız yerinde. Düzenli beslenmeye önem verin..."
  }
}
```

## Desteklenen Kaynaklar

Milliyet, Hürriyet, Habertürk, Elle, Onedio, Mynet, TwitBurc, Vogue, GünlükBurç, MyBurç

## Proje Yapısı

```
AIstrolog/
├── scraper.py                    # Burç verilerini çeker
├── categorize_horoscopes.py      # Kategorize eder
├── summarizer.py                 # Özetler
├── run_pipeline.py               # Scrape + kategorize + test
├── run_full_pipeline.py          # Scrape + kategorize + özetle + test
├── test_workflow.py              # Otomatik test sistemi
├── verify_categorization.py      # Detaylı inceleme aracı
├── TEST_GUIDE.md                 # Test kılavuzu
├── SUMMARIZATION_GUIDE.md        # Özetleme kılavuzu
├── requirements.txt
├── .github/workflows/
│   └── daily-scrape.yml          # Otomatik günlük çalıştırma
└── data/
    ├── daily_raw_*.json          # Ham veri
    ├── processed_*.json          # İşlenmiş veri
    └── summarized_*.json         # Özetlenmiş veri
```

## Otomatik Çalıştırma

Proje, GitHub Actions ile her gün otomatik çalışır:

- **Zamanlama:** Her gün saat 03:00 (Türkiye saati)
- **İşlemler:** Scraping → Kategorize → Özetleme → Commit & Push
- **Workflow dosyası:** `.github/workflows/daily-scrape.yml`

Manuel çalıştırma için GitHub repository'de "Actions" sekmesinden "Daily Horoscope Scraping" workflow'unu seçip "Run workflow" butonuna tıklayın.

## Güvenilirlik ve Kalite

### Sahte Veri Önleme

❌ **Default/fallback data kullanılmaz** - Eğer bir site veri çekemezse, boş bırakılır
❌ **Generic içerik tespit edilir** - Test sistemi placeholder metinleri otomatik bulur
✅ **Her scraping sonrası test** - `run_pipeline.py` otomatik test çalıştırır

### Sorun Giderme

Eğer testler başarısız olursa:

1. **Duplike içerik uyarısı:** Scraper burçları doğru ayıramıyor, ilgili fonksiyonu kontrol edin
2. **Generic içerik uyarısı:** Site yapısı değişmiş olabilir, scraper'ı güncelle
3. **Boş içerik uyarısı:** Site erişilebilir mi? HTML yapısı değişti mi?

Detaylı sorun giderme için: [TEST_GUIDE.md](TEST_GUIDE.md)

## Gereksinimler

Python 3.7+, requests, beautifulsoup4, pandas
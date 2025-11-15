# Test Kilavuzu

## Hizli Baslangic

### Tam Pipeline (Onerilir)

```bash
python run_pipeline.py
```

Bu komut otomatik olarak scraping yapar, kategorize eder ve test eder.

### Manuel Test

```bash
python test_workflow.py data/daily_raw_2025-11-15.json data/processed_daily_raw_2025-11-15.json
```

## Test Ne Kontrol Eder?

1. **Duplike icerik** - Ayni metin birden fazla burcta kullaniliyor mu?
2. **Generic icerik** - Sahte/test verileri var mi?
3. **Bos icerik** - Hangi kaynaklar veri cekemedi?
4. **Kategorizasyon** - Icerikler dogru kategorize ediliyor mu?
5. **Guncellik** - Veri bugune ait mi?

## Test Sonuclari

- `[OK] TEST BASARILI` - Her sey yolunda
- `[!] KISMEN BASARILI` - Uyarilar var, kontrol et
- `[X] TEST BASARISIZ` - Kritik hatalar var, duzeltilmeli

## Sorun Giderme

### Duplike icerik uyarisi
- Scraper burc ayrimini yanlis yapiyor
- Ilgili scraper fonksiyonunu kontrol et

### Generic icerik uyarisi
- Site yapisi degismis olabilir
- Scraper'i guncelle

### Bos icerik uyarisi
- Site erisilebilir mi?
- HTML yapisi degisti mi?
- `scraper.log` dosyasina bak

### Kategorizasyon dusuk
- Ham veriyi kontrol et
- Anahtar kelime listelerini guncelle

## Loglar

```bash
Get-Content scraper.log -Tail 50
```

## Detayli Inceleme

Belirli bir burc/kaynak icin:

```bash
python verify_categorization.py data/daily_raw_2025-11-15.json data/processed_daily_raw_2025-11-15.json milliyet Koc
```

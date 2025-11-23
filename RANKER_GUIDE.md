# Ranker - Burç Sıralama Sistemi

## Genel Bakış

`ranker.py` modülü, skorlanmış burç verilerinden ranking oluşturur ve `rankings_history.json` dosyasına ekler. Scorer'dan sonra pipeline'da çalışır.

## Kullanım

### Temel Kullanım

```bash
# Belirli bir scored dosya için
python ranker.py data/scored_processed_daily_raw_2025-11-23.json

# Bugünün dosyasını otomatik bul ve çalıştır
python ranker.py

# En son scored dosyayı kullan (bugünün dosyası yoksa)
python ranker.py
```

### Pipeline İçinde Kullanım

Ranker, tam pipeline'da scorer'dan sonra otomatik çalışır:

```bash
python run_full_pipeline.py
```

Pipeline adımları:
1. **Scraper** → Ham veri toplama
2. **Categorizer** → Kategorilere ayırma
3. **Summarizer** → Özetleme
4. **Scorer** → Skorlama
5. **Ranker** → Ranking oluşturma ⭐ (YENİ)

## Giriş ve Çıkış

### Giriş Formatı

Ranker, `scored_processed_daily_raw_YYYY-MM-DD.json` dosyalarını okur:

```json
{
  "metadata": {
    "date": "2025-11-23",
    "total_burcs": 12,
    "scored_at": "2025-11-23T22:01:41.616661"
  },
  "scores": {
    "Koç": {
      "genel": {...},
      "aşk": {...},
      "para": {...},
      "sağlık": {...},
      "toplam": 76.2
    }
  },
  "rankings": {
    "genel_ranking": [...],
    "aşk_ranking": [...],
    "para_ranking": [...],
    "sağlık_ranking": [...]
  }
}
```

### Çıkış Formatı

`rankings_history.json` dosyasına tarih bazlı ranking ekler:

```json
{
  "2025-11-23": {
    "genel_ranking": [
      {
        "burc": "Yengeç",
        "score": 98.2
      },
      {
        "burc": "Terazi",
        "score": 96.5
      }
    ],
    "aşk_ranking": [...],
    "para_ranking": [...],
    "sağlık_ranking": [...]
  },
  "2025-11-22": {...},
  "2025-11-21": {...}
}
```

## Özellikler

### 1. Tarih Bazlı Ranking
- Her tarih için ayrı ranking oluşturur
- Tarihleri kronolojik sırada tutar (en yeni en üstte)
- Mevcut tarih varsa günceller

### 2. Kategori Sıralamaları
Her tarih için 4 kategori:
- **genel_ranking** - Tüm kategorilerin ortalaması
- **aşk_ranking** - Aşk skorları
- **para_ranking** - Para/kariyer skorları
- **sağlık_ranking** - Sağlık skorları

### 3. Veri Birleştirme
- Mevcut history'yi okur
- Yeni ranking'i ekler
- Tarih bazlı sıralı tutar

### 4. Özet Rapor
Her çalıştırmada ilk 3'ü gösterir:

```
================================================================================
📅 2025-11-23 TARİHİ İÇİN RANKING
================================================================================

🏆 GENEL SIRALAMASI (İlk 3):
--------------------------------------------------------------------------------
🥇 Yengeç       → 98.2/100
🥈 Terazi       → 96.5/100
🥉 İkizler      → 95.6/100
```

## Fonksiyonlar

### `load_scored_data(filepath)`
Scored JSON dosyasını yükler.

### `load_rankings_history(filepath)`
Mevcut rankings history'yi yükler (yoksa boş dict döner).

### `save_rankings_history(data, filepath)`
Rankings history'yi kaydeder (tarihleri sıralı tutar).

### `create_ranking_for_date(scored_data)`
Scored veriden belirli bir tarih için ranking oluşturur.

### `update_rankings_history(scored_filepath, history_filepath)`
Scored dosyadan ranking oluşturur ve history'e ekler.

### `print_ranking_summary(ranking_data, date)`
Ranking özetini ekrana yazdırır.

## Loglama

Ranker, `ranker.log` dosyasına detaylı log yazar:

```
2025-11-24 02:13:40,756 - INFO - Scored veri yükleniyor: ...
2025-11-24 02:13:40,756 - INFO - Scored veri yüklendi: 2025-11-23
2025-11-24 02:13:40,756 - INFO - Tarih için ranking oluşturuluyor: 2025-11-23
2025-11-24 02:13:40,757 - INFO - Rankings history yüklendi: 3 tarih
2025-11-24 02:13:40,758 - INFO - Rankings history kaydedildi: ...
2025-11-24 02:13:40,760 - INFO - ✅ 2025-11-23 tarihi için ranking eklendi
```

## Hata Yönetimi

### Dosya Bulunamadı
```bash
❌ Scored dosya bulunamadı!
Kullanım: python ranker.py [scored_file.json]
```

### Tarih Zaten Mevcut
```bash
⚠️  2025-11-23 tarihi zaten mevcut, güncelleniyor...
```

## Örnek Kullanım Senaryoları

### Senaryo 1: Günlük Otomatik Çalıştırma
```bash
# Cron job veya Task Scheduler ile
python run_full_pipeline.py
# Tüm adımları çalıştırır, ranker son adım
```

### Senaryo 2: Manuel Ranking Güncelleme
```bash
# Eski bir scored dosya için ranking oluştur
python ranker.py data/scored_processed_daily_raw_2025-11-15.json
```

### Senaryo 3: History Kontrolü
```python
import json

with open('data/rankings_history.json', 'r', encoding='utf-8') as f:
    history = json.load(f)

# Tarihleri listele
print(list(history.keys()))

# Belirli bir tarih
print(history['2025-11-23']['genel_ranking'][0])
```

## Veri Akışı

```
scored_processed_daily_raw_2025-11-23.json
    ↓
ranker.py
    ↓
rankings_history.json (güncellenir)
```

## API Entegrasyonu

Rankings history, API tarafından kullanılır:

```python
# main.py içinde
@app.get("/api/rankings/{date}")
async def get_rankings(date: str):
    with open('data/rankings_history.json') as f:
        history = json.load(f)
    return history.get(date, {})
```

## Performans

- **Dosya Boyutu**: ~30-50 KB (tarih başına)
- **İşlem Süresi**: < 1 saniye
- **Bellek Kullanımı**: Minimal

## Önemli Notlar

1. **Tarih Formatı**: YYYY-MM-DD (ISO 8601)
2. **Encoding**: UTF-8 (Türkçe karakter desteği)
3. **Sıralama**: En yeni tarih en üstte
4. **Güncelleme**: Aynı tarih tekrar çalıştırılırsa güncellenir

## Sorun Giderme

### Problem: Rankings history boş
**Çözüm**: İlk çalıştırmada otomatik oluşturulur.

### Problem: Tarih sıralaması yanlış
**Çözüm**: Ranker otomatik sıralar, manual düzenleme gereksiz.

### Problem: Eksik kategori
**Çözüm**: Scorer'ın tüm kategorileri ürettiğinden emin olun.

## İlgili Dosyalar

- `scorer.py` - Ranking için input üreten modül
- `run_full_pipeline.py` - Pipeline orchestrator
- `data/rankings_history.json` - Output dosyası
- `ranker.log` - Log dosyası

## Geliştirme Notları

### Gelecek İyileştirmeler
- [ ] Haftalık/aylık trendler
- [ ] Burç karşılaştırma grafikleri
- [ ] Export to CSV/Excel
- [ ] API direkt entegrasyon

---

**Son Güncelleme**: 2025-11-24
**Versiyon**: 1.0.0

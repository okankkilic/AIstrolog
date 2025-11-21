# Burc Puanlama Sistemi (Scorer)

## Genel Bakis

Scorer sistemi, kategorileştirilmiş burç yorumlarını analiz ederek her burç için 0-100 arası skorlar verir ve günün en şanslı/şanssız burçlarını belirler.

## Ozellikler

### 1. Sentiment Analizi
- **200+ pozitif/negatif kelime** ile metin analizi
- **Ağırlıklı skorlama**: Kelime önemine göre farklı puanlar
- **Kategori bazlı boost**: Aşk, para, sağlık kategorilerine özel keyword bonusları

### 2. Akıllı Validasyon
- **Duplikasyon tespiti**: %95+ benzer metinleri filtreler
- **Keyword kontrolü**: Her kategorinin uygun içeriğe sahip olduğunu doğrular
- **Çoklu kaynak birleştirme**: 10 farklı siteden gelen verileri merge eder

### 3. Kapsamlı Skorlama
Her burç için:
- Genel skor (0-100)
- Ask skoru (0-100)
- Para skoru (0-100)
- Saglik skoru (0-100)
- Agirlikli toplam skor

### 4. Sıralama Sistemleri
- **Genel sıralama**: Tüm burçlar toplam skora göre
- **Kategori sıralamaları**: Aşk, para, sağlık bazında
- **Liderler**: Günün şampiyonları

## Kullanim

### Temel Kullanım
```bash
# Bugünkü veriyi otomatik bul
python scorer.py

# Belirli bir dosyayı skorla
python scorer.py data/processed_daily_raw_2025-11-19.json
```

### Çıktılar

#### 1. Terminal Çıktısı
```
================================================================================
🏆 GÜNÜN BURCLAR SIRALAMASI
================================================================================

⭐ GÜNÜN LİDERLERİ:
--------------------------------------------------------------------------------
🥇 EN ŞANSLI BURÇ:   Akrep        → 89.0/100
❤️  EN AŞIK BURÇ:     Koç          → 100.0/100
💰 EN ZENGİN BURÇ:   Yengeç       → 100.0/100
🏃 EN SAĞLIKLI BURÇ: Balık        → 76.2/100
⚠️  EN ŞANSSIZ BURÇ:  Başak        → 46.1/100

📊 GENEL SIRALAMA:
--------------------------------------------------------------------------------
🥇 Akrep        →  89.0/100 ⭐⭐⭐⭐
🥈 Terazi       →  87.0/100 ⭐⭐⭐⭐
🥉 Yengeç       →  86.5/100 ⭐⭐⭐⭐
...
```

#### 2. JSON Dosyası
`data/scored_processed_daily_raw_YYYY-MM-DD.json`:

```json
{
  "metadata": {
    "date": "2025-11-19",
    "total_burcs": 12,
    "scored_at": "2025-11-19T12:30:00"
  },
  "scores": {
    "Koç": {
      "genel": {
        "score": 73.8,
        "sentiment": "positive",
        "source_count": 8,
        "details": {
          "positive_count": 18,
          "negative_count": 14,
          "positive_score": 33.5,
          "negative_score": 24.0,
          "category_boost": 0,
          "net_score": 9.5
        }
      },
      "aşk": {...},
      "para": {...},
      "sağlık": {...},
      "toplam": 70.3,
      "issues": []
    },
    ...
  },
  "rankings": {
    "genel_ranking": [...],
    "aşk_ranking": [...],
    "para_ranking": [...],
    "sağlık_ranking": [...],
    "leaders": {...}
  }
}
```

#### 3. Log Dosyası
`scorer.log`: Tüm işlemlerin detaylı kayıtları

## Skorlama Mantigi

### Sentiment Skoru Hesaplama

```
Base Score = 50 (nötr)

Pozitif Katkı:
  - Çok güçlü: +3 puan (harika, mükemmel, muhteşem)
  - Güçlü: +2.5 puan (başarılı, şanslı, kazanç)
  - Orta: +2 puan (mutlu, iyi, güzel)
  - Hafif: +1.5 puan (uygun, yararlı)
  - Hafif-orta: +1 puan (yeni, umutlu)

Negatif Katkı:
  - Çok güçlü: -3 puan (felaket, korkunç, berbat)
  - Güçlü: -2.5 puan (kayıp, zarar, tehlike)
  - Orta: -2 puan (zor, sorun, stres)
  - Hafif: -1.5 puan (dikkat, temkinli)
  - Hafif-orta: -1 puan (gecikme, engel)

Kategori Boost:
  - Her uygun keyword: +5 puan
  - Her olumsuz keyword: -5 puan

Final Score = 50 + (Net Score × 2.5)
Limit: 0-100 arası
```

### Toplam Skor (Ağırlıklı Ortalama)

```
Toplam = (Genel × 0.30) + (Aşk × 0.25) + (Para × 0.25) + (Sağlık × 0.20)
```

## Validasyon Kurallari

### 1. Duplikasyon Kontrolü
```python
# %95+ benzerlik varsa → duplikasyon
if similarity >= 0.95:
    # Daha spesifik kategoriye at
    # Genel kategoriye ait olanı sil
```

### 2. Keyword Validasyonu
Her kategori için minimum keyword gereksinimi:

**Aşk:**
- Gerekli: aşk, sevgi, partner, ilişki, romantik, flört, vb.
- Yasaklı: -

**Para:**
- Gerekli: para, finans, iş, kariyer, kazanç, yatırım, vb.
- Yasaklı: aşk, sevgi, romantik (yanlış kategorileme önleme)

**Sağlık:**
- Gerekli: sağlık, enerji, vücut, fiziksel, mental, vb.
- Yasaklı: -

**Genel:**
- Her şey kabul edilir

### 3. Veri Birleştirme
Farklı sitelerden gelen veriler:
```python
# Her burç için tüm sitelerin verileri birleştirilir
merged_data["Koç"]["aşk"] = [
    "Site1: Aşk hayatınız...",
    "Site2: Romantik anlar...",
    "Site3: İlişkiniz güçleniyor...",
    ...
]
```

## Yildiz Sistemi

```
90-100 puan: ⭐⭐⭐⭐⭐ (Mükemmel)
75-89 puan:  ⭐⭐⭐⭐   (Çok İyi)
60-74 puan:  ⭐⭐⭐     (İyi)
45-59 puan:  ⭐⭐       (Orta)
0-44 puan:   ⭐         (Zayıf)
```

## Ornek Sonuclar

### Pozitif Metin Örneği
```
Metin: "Aşk hayatınız harika olacak! Partnerinizle romantik anlar yaşayacak,
        mutlu ve sevgi dolu bir gün geçireceksiniz."

Analiz:
  - Pozitif kelimeler: harika(3), romantik(2.5), mutlu(2), sevgi(2)
  - Kategori boost: +10 (aşk kategorisi için)
  - Net skor: 9.5 + 10 = 19.5
  - Final skor: 50 + (19.5 × 2.5) = 98.75/100
```

### Negatif Metin Örneği
```
Metin: "Dikkat! Bugün zorlu bir gün. Stresli ve gergin hissedebilir,
        sorunlarla karşılaşabilirsiniz."

Analiz:
  - Negatif kelimeler: dikkat(-1.5), zorlu(-2), stresli(-2.5), gergin(-2.5), sorun(-2.5)
  - Net skor: -11
  - Final skor: 50 + (-11 × 2.5) = 22.5/100
```

## Sorun Giderme

### "Burç verisi bulunamadı" hatası
- Processed dosyada eksik veri var
- `categorize_horoscopes.py` ile tekrar kategorileme yapın

### "Kategori keyword bulunamadı" uyarısı
- Metin o kategoriye uygun değil
- Normal bir validasyon, hata değil
- Skor `None` olarak işaretlenir

### Tüm skorlar 100
- Pozitif kelime bombardımanı var
- Normaldir, gerçekten iyi bir gün!

### Tüm skorlar düşük
- Çok fazla negatif kelime kullanılmış
- Yorum metinleri uyarı/dikkat içeriyor

## Konfigurasyon

### Sentiment Kelimelerini Özelleştirme
`scorer.py` içinde:
```python
POSITIVE_WORDS = {
    'yeni_kelime': 2.5,  # Ağırlık
    ...
}

NEGATIVE_WORDS = {
    'kötü_kelime': -2.5,  # Ağırlık
    ...
}
```

### Ağırlıkları Değiştirme
```python
# Toplam skor hesabında
weights = {
    'genel': 0.3,   # %30
    'aşk': 0.25,    # %25
    'para': 0.25,   # %25
    'sağlık': 0.20  # %20
}
```

## Pipeline Entegrasyonu

```bash
# Tam pipeline
python scraper.py                    # 1. Veri toplama
python categorize_horoscopes.py      # 2. Kategorileme
python scorer.py                      # 3. Skorlama
python summarizer.py                  # 4. Özetleme
```

## Notlar

- Birden fazla kaynak = daha guvenilir skor
- Duplikasyon tespiti = daha dogru sonuclar
- Keyword validasyonu = yanlis kategorileme onleme
- Agirlikli skorlama = dengeli degerlendirme
- Detayli loglama = seffaf islem

## Sonuc

Scorer sistemi, burc yorumlarini objektif bir sekilde puanlayarak kullanicilara:
- Gunun en sansli burclarini gosterir
- Kategori bazli (ask, para, saglik) liderlik tablosu sunar
- Tum burclar icin detayli analiz saglar
- Guvenilir, validasyonlu ve olculebilir sonuclar uretir

Artik sadece burc yorumu degil, VERIYE DAYALI burc analizi!

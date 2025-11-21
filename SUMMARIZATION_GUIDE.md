# Ozetleme Sistemi Kilavuzu

## Genel Bakis

AIstrolog ozetleme sistemi, 10 farkli kaynaktan toplanan burc yorumlarini birlestirerek her burc icin tek, tutarli ve bilgilendirici ozetler olusturur.

### Kaynak Guncelleme Saatleri

Bazi kaynaklar gecikmeli guncelleme yapar:
- **Hurriyet**: Sabah 09:00 civarinda
- **Vogue**: Sabah 08:30 civarinda

Bu nedenle otomasyon sistemi gunluk iki kez calisir (03:00 ve 09:00) ve en guncel verileri toplar.

## Ozetleme Sureci

### 1. Veri Toplama

Sistem, kategorize edilmiş verilerden (`processed_*.json`) her burç ve kategori için tüm kaynaklardan gelen metinleri toplar.

**Örnek Girdi:**
```json
{
  "milliyet": {
    "Koç": {
      "aşk": "Bugün aşk hayatınızda heyecan dolu anlar yaşayacaksınız."
    }
  },
  "hurriyet": {
    "Koç": {
      "aşk": "İlişkilerinizde pozitif gelişmeler sizi bekliyor."
    }
  },
  "onedio": {
    "Koç": {
      "aşk": "Bugün aşk hayatınızda güzel anlar yaşayacaksınız."
    }
  }
}
```

### 2. Metin Temizleme

- Fazla boşluklar kaldırılır
- Kaynak isimleri ve önek bilgileri temizlenir
- Noktalama işaretleri normalize edilir

**Temizleme Öncesi:**
```
"Aygül Aydın burç yorumları; Bugün harika bir gün."
```

**Temizleme Sonrası:**
```
"Bugün harika bir gün."
```

### 3. Cümlelere Ayırma

Her metin, nokta (.), ünlem (!) ve soru (?) işaretlerine göre cümlelere ayrılır.

**Örnek:**
```
"Bugün şanslısınız. Aşkta mutlu olacaksınız. İlişkiler güçlenecek."
```
↓
```
["Bugün şanslısınız", "Aşkta mutlu olacaksınız", "İlişkiler güçlenecek"]
```

### 4. Benzerlik Tespiti ve Tekrar Temizleme

Sistem, kelime örtüşmesine (Jaccard benzerliği) dayalı olarak benzer cümleleri tespit eder ve kaldırır.

**Benzerlik Algoritması:**
```python
similarity = (ortak_kelimeler) / (toplam_benzersiz_kelimeler)
```

**Eşik Değeri:** 0.7 (70% benzerlik üstü tekrar sayılır)

**Örnek:**

Cümle 1: "Bugün aşk hayatınızda heyecan dolu anlar yaşayacaksınız."
Cümle 2: "Bugün aşk hayatınızda güzel anlar yaşayacaksınız."

→ Benzerlik: ~0.85 → Tekrar olarak işaretlenir, biri çıkarılır

### 5. Cümle Skorlama

Her cümle, kategori ile alakasına göre skorlanır:

**Skorlama Kriteri:**

**Kategori Uygunluğu:** İlgili anahtar kelimeleri içeriyor mu?
- Aşk: aşk, sevgi, partner, flört, ilişki, kalp, duygusal, evlilik, romantik
- Para: para, maddi, harcama, birikim, yatırım, kazanç, finans, maaş, gelir
- Sağlık: sağlık, enerji, stres, egzersiz, spor, beslenme, uyku, yorgun, dinlen

**Örnek:**

```
Cümle: "Aşk hayatınızda bugün güzel gelişmeler olacak."
Kategori: aşk
Anahtar kelime: "aşk" → +1 puan
Final Skor: 1.0
```

### 6. En İyi Cümleleri Seçme

Skorlara göre sıralama yapılır ve en bilgilendirici cümleler seçilir:

- **Genel kategori:** En fazla 4 cümle
- **Aşk, para, sağlık:** En fazla 3 cümle

### 7. Özet Oluşturma

Seçilen cümleler birleştirilerek akıcı bir özet oluşturulur:

**Son İşlemler:**
- İlk cümledeki bağlantı sözcükleri kaldırılır (Ayrıca, Ancak, Fakat, vb.)
- Her cümlenin ilk harfi büyük yapılır
- Nokta işareti kontrolü yapılır ve gerekirse eklenir

**Örnek Çıktı:**
```json
{
  "Koç": {
    "aşk": "Aşk hayatınızda heyecan dolu anlar yaşayacaksınız. İlişkilerinizde pozitif gelişmeler sizi bekliyor. Partnerinizle güzel vakit geçireceksiniz."
  }
}
```

## Kullanım

### Komut Satırı

```bash
# Basit kullanım (varsayılan dosya)
python summarizer.py

# Belirli bir dosyayı özetle
python summarizer.py data/processed_daily_raw_2025-11-17.json

# Çıktı dosyası belirt
python summarizer.py input.json output.json
```

### Python'dan Kullanım

```python
from summarizer import TurkishHoroscopeSummarizer

# Summarizer oluştur
summarizer = TurkishHoroscopeSummarizer(similarity_threshold=0.7)

# Veriyi yükle
data = summarizer.load_data("data/processed_daily_raw_2025-11-17.json")

# Tüm burçları özetle
summaries = summarizer.summarize_all(data, "data/summarized_output.json")

# Karşılaştırma yap
summarizer.compare_with_original(data, summaries, "Koç", "aşk")
```

## Parametreler

### `similarity_threshold` (Benzerlik Eşiği)

Cümlelerin ne kadar benzer olması durumunda tekrar sayılacağını belirler.

- **Varsayılan:** 0.7 (70% benzerlik)
- **Düşük değer (0.5):** Daha fazla cümle tekrar sayılır → Daha kısa özetler
- **Yüksek değer (0.9):** Sadece çok benzer cümleler tekrar sayılır → Daha uzun özetler

**Örnek:**
```python
# Daha agresif tekrar temizleme
summarizer = TurkishHoroscopeSummarizer(similarity_threshold=0.6)

# Daha az tekrar temizleme
summarizer = TurkishHoroscopeSummarizer(similarity_threshold=0.8)
```

## Istatistikler

Ozetleme sonunda her kategori icin istatistikler gosterilir:

```
====================================================================
Summarization Statistics
====================================================================
Genel     : 12/12 summarized (100.0%)
Aşk       : 12/12 summarized (100.0%)
Para      : 11/12 summarized (91.7%)
Sağlık    : 10/12 summarized (83.3%)
====================================================================
```

- **summarized:** Başarıyla özet oluşturulan burç sayısı
- **null:** Özet oluşturulamayan burç sayısı (kaynaklarda veri yok)

## Örnek Karşılaştırma

Sistem, orijinal kaynak metinleri ile oluşturulan özeti karşılaştırma imkanı sunar:

```
================================================================================
Comparison: Koc - ASK
================================================================================

ORIGINAL SOURCES:
--------------------------------------------------------------------------------

[milliyet]
Bugun ask hayatinizda heyecan dolu anlar yasayacaksiniz. Partnerinizle uyum icinde olacaksiniz.

[hurriyet]
Iliskilerinizde pozitif gelismeler sizi bekliyor. Duygusal anlamda kendinizi iyi hissedeceksiniz.

[onedio]
Bugun ask hayatinizda guzel anlar yasayacaksiniz. Sevdiginiz kisiyle yakinlasacaksiniz.

--------------------------------------------------------------------------------
GENERATED SUMMARY:
--------------------------------------------------------------------------------
Ask hayatinizda heyecan dolu anlar yasayacaksiniz. Iliskilerinizde pozitif gelismeler sizi bekliyor. Partnerinizle uyum icinde olacaksiniz.

================================================================================
```

## Pipeline Entegrasyonu

Özetleme sistemi, tam pipeline içinde otomatik çalışır:

### Manuel Pipeline

```bash
# 1. Veri çek
python scraper.py

# 2. Kategorize et
python categorize_horoscopes.py

# 3. Özetle
python summarizer.py
```

### Otomatik Pipeline

```bash
# Hepsi birden (scrape + kategorize + özetle + test)
python run_full_pipeline.py
```

### GitHub Actions

GitHub Actions workflow'u her gün otomatik olarak:

1. Verileri toplar (`scraper.py`)
2. Kategorize eder (`categorize_horoscopes.py`)
3. Özetler (`summarizer.py`)
4. Sonuçları GitHub'a push eder

**Workflow dosyası:** `.github/workflows/daily-scrape.yml`

## Sorun Giderme

### Problem: Özetler çok kısa

**Çözüm:** Benzerlik eşiğini artırın
```python
summarizer = TurkishHoroscopeSummarizer(similarity_threshold=0.8)
```

### Problem: Özetler çok uzun veya tekrarlı

**Çözüm:** Benzerlik eşiğini azaltın
```python
summarizer = TurkishHoroscopeSummarizer(similarity_threshold=0.6)
```

### Problem: Bazı kategorilerde özet oluşmuyor

**Neden:** Kaynak verilerde o kategori için yeterli metin yok

**Kontrol:**
```bash
python verify_categorization.py data/processed_daily_raw_2025-11-17.json
```

### Problem: Özetler anlamsız veya alakasız

**Neden:** Kaynak verilerde kalite sorunu olabilir

**Kontrol:**
```bash
# Test sistemiyle kaynak kalitesini kontrol edin
python test_workflow.py data/daily_raw_2025-11-17.json data/processed_daily_raw_2025-11-17.json
```

## Performans

Tipik bir özetleme işlemi:

- **12 burç × 4 kategori = 48 özet**
- **İşlem süresi:** ~1-2 saniye
- **Bellek kullanımı:** Minimal (<50 MB)

## Gelecek Geliştirmeler

Potansiyel iyileştirmeler:

1. **Transformer tabanlı özetleme:** BERT/GPT modelleri ile daha akıcı özetler
2. **Duygu analizi:** Pozitif/negatif ton kontrolü
3. **Özel kategori ağırlıkları:** Kullanıcı tercihlerine göre özelleştirme
4. **Çoklu dil desteği:** İngilizce veya diğer diller

## İlgili Dökümanlar

- [README.md](README.md) - Proje genel bakış
- [TEST_GUIDE.md](TEST_GUIDE.md) - Test sistemi kılavuzu
- [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) - Sistem mimarisi

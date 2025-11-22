# AIstrolog

Günlük burç yorumlarını toplayan, kategorize eden, puanlayan ve modern bir arayüzle sunan tam kapsamlı astroloji platformu.

## Özellikler

### Backend & Veri İşleme
- **Çoklu Kaynak:** 10 farklı kaynaktan (Milliyet, Hürriyet, Onedio vb.) burç yorumu toplama
- **Akıllı Kategorizasyon:** Yorumları otomatik olarak Aşk, Para ve Sağlık kategorilerine ayırma
- **Sentiment Analizi & Puanlama:** Burçları kategorilere göre puanlayıp (0-100) sıralama (En Şanslı, En Aşık vb.)
- **AI Özetleme:** Farklı kaynaklardan gelen yorumları tek bir tutarlı metin haline getirme
- **Otomatik Test:** Veri kalitesini ve bütünlüğünü koruyan kapsamlı test sistemi

### Frontend & Arayüz
- **Modern UI:** Next.js 16 ve Tailwind CSS ile geliştirilmiş şık tasarım
- **Günlük Sıralamalar:** Burçların o günkü şans durumuna göre sıralanması
- **Detaylı Görünüm:** Her burç için kategorize edilmiş ve özetlenmiş yorumlar
- **Mobil Uyumlu:** Her cihazda kusursuz deneyim

## Kurulum

### Backend Kurulumu

```bash
pip install -r requirements.txt
```

### Frontend Kurulumu

```bash
cd frontend
npm install
```

## Kullanım

### Backend Komutları

#### Temel Kullanım

```bash
# 🚀 TAM OTOMASYON (Önerilen)
# Veri çeker, kategorize eder, özetler ve test eder
python run_full_pipeline.py

# 📊 Puanlama ve Sıralama
# İşlenmiş verileri analiz eder ve puanlar
python scorer.py
```

#### Modüler Kullanım

```bash
# Sadece veri çek
python scraper.py

# Sadece kategorize et
python categorize_horoscopes.py

# Sadece özetle
python summarizer.py

# İkisini birden yap + test et (Eski yöntem)
python run_pipeline.py
```

### Frontend Çalıştırma

```bash
cd frontend
npm run dev
# Tarayıcıda http://localhost:3000 adresine gidin
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

**Önemli:** Her scraping sonrası mutlaka test çalıştırın! Test, sahte/duplike veri kullanımını otomatik tespit eder.

### Gelişmiş kullanım

```bash
# Belirli bir dosyayı kategorize et
python categorize_horoscopes.py data/daily_raw_2025-11-14.json

# Çıktı dosyası belirt
python categorize_horoscopes.py input.json output.json
```

## Proje Yapısı

```
AIstrolog/
├── frontend/                     # Next.js Web Uygulaması
│   ├── app/                      # Sayfalar ve Routing
│   ├── components/               # React Bileşenleri
│   └── public/                   # Görseller ve Varlıklar
├── data/                         # Veri Klasörü
│   ├── daily_raw_*.json          # Ham veriler
│   ├── processed_*.json          # Kategorize edilmiş veriler
│   ├── summarized_*.json         # Özetlenmiş veriler
│   └── scored_*.json             # Puanlanmış veriler
├── scraper.py                    # Veri toplama motoru
├── categorize_horoscopes.py      # NLP tabanlı kategorizasyon
├── scorer.py                     # Sentiment analizi ve puanlama
├── summarizer.py                 # Yorum özetleme motoru
├── run_full_pipeline.py          # Ana orkestrasyon scripti
├── test_workflow.py              # Test otomasyonu
├── verify_categorization.py      # Detaylı inceleme aracı
├── TEST_GUIDE.md                 # Test kılavuzu
└── requirements.txt              # Python bağımlılıkları
```

## Backend Detayları

### Kategorizasyon Nasıl Çalışır?

Script, "genel" anahtarındaki metni cümlelere ayırır ve her cümleyi analiz eder:

**Aşk kategorisi:** aşk, sevgi, partner, flört, ilişki, kalp, duygular, evlilik vb.

**Para kategorisi:** para, maddi, harcama, birikim, yatırım, kazanç, finans, maaş vb.

**Sağlık kategorisi:** sağlık, enerji, stres, egzersiz, spor, beslenme, uyku vb.

Önemli: Orijinal "genel" metin hiç değişmez. İlgili cümleler sadece uygun kategorilere kopyalanır.

### Puanlama Sistemi (Scorer)

`scorer.py` scripti, burç yorumlarını analiz ederek 0-100 arası puanlar:
- **Pozitif Kelimeler:** harika (+3), şanslı (+2.5), güzel (+2)...
- **Negatif Kelimeler:** felaket (-3), riskli (-2.5), zor (-2)...
- **Kategori Bazlı:** Aşk, Para ve Sağlık için özel kelime setleri.

Sonuçta "Günün En Şanslısı", "En Aşık Burcu" gibi liderler belirlenir ve `scored_processed_daily_raw_YYYY-MM-DD.json` dosyasına kaydedilir.

### Test Sistemi

Workflow'un doğru çalıştığını garanti altına almak için kapsamlı test sistemi:

### Otomatik Kontroller

**Duplike İçerik:** Aynı metin birden fazla burç için kullanılmış mı?
**Generic/Test İçerik:** Sahte placeholder veriler var mı?
**Boş İçerik:** Hangi kaynaklar veri çekememiş?
**Kategorizasyon Kalitesi:** İçerikler doğru kategorize ediliyor mu?
**Veri Güncelliği:** Bugüne ait veri mi?
**Kategori Benzersizliği:** Her kategori farklı içerik mi?

### Test Sonuçları

**TEST BAŞARILI:** Workflow düzgün çalışıyor
**KISMEN BAŞARILI:** Bazı uyarılar var, kontrol edin
**TEST BAŞARISIZ:** Kritik sorunlar var, düzeltilmeli

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

Puanlanmış veri:
```json
{
  "scores": {
    "Koç": {
      "genel": { "score": 85.5, "sentiment": "positive" },
      "aşk": { "score": 92.0, "sentiment": "positive" },
      "toplam": 88.2
    }
  }
}
```

## Desteklenen Kaynaklar

Milliyet, Hürriyet, Habertürk, Elele, Onedio, Mynet, TwitBurc, Vogue, GünlükBurç, MyBurç

## Otomatik Güncelleme

GitHub Actions workflow'u günde iki kez otomatik çalışır:

- Sabah 03:00 (Türkiye saati): İlk veri toplama
- Sabah 09:00 (Türkiye saati): Güncellenmiş verilerle tekrar çalıştırma

Vogue sitesi verilerini sabah 08:30 civarında güncellediği için ikinci çalıştırma ile tam veri toplanması sağlanır.

## Güvenilirlik ve Kalite

### Sahte Veri Önleme

- Default/fallback data kullanılmaz - Eğer bir site veri çekemezse, boş bırakılır
- Generic içerik tespit edilir - Test sistemi placeholder metinleri otomatik bulur
- Her scraping sonrası test - `run_pipeline.py` otomatik test çalıştırır

### Veri Güncelleme Zamanlaması

Bazı kaynaklar (örn. Vogue) verilerini gün içinde geç saatlerde güncelleyebilir. Bu durumda otomatik workflow günde iki kez çalışarak eksik verilerin tamamlanmasını sağlar.

### Sorun Giderme

Eğer testler başarısız olursa:

1. **Duplike içerik uyarısı:** Scraper burçları doğru ayıramıyor, ilgili fonksiyonu kontrol edin
2. **Generic içerik uyarısı:** Site yapısı değişmiş olabilir, scraper'ı güncelle
3. **Boş içerik uyarısı:** Site erişilebilir mi? HTML yapısı değişti mi?

Detaylı sorun giderme için: [TEST_GUIDE.md](TEST_GUIDE.md)

## Gereksinimler

### Sistem
- Python 3.7+
- Node.js 18+

### Veri İşleme ve Backend (Python)
- **Veri Analizi & Manipülasyon:** pandas>=2.0.0
- **Web Scraping:** requests>=2.31.0, beautifulsoup4>=4.12.0, selenium>=4.0.0, lxml>=4.9.0

### Frontend (Node.js)
- **Framework:** Next.js 16.0.3, React 19.2.0
- **UI & Styling:** Tailwind CSS v4, Framer Motion, Lucide React

## Frontend Geliştirmeleri

Projenin kullanıcı arayüzü Next.js 16 ve Tailwind CSS kullanılarak geliştirilmiştir.

### Tasarım ve Tipografi

- **Fontlar:** Başlıklar için Khand (Regular), metinler için Lora fontları kullanıldı.
- **Renkler:** Arkaplan rengi göz yormayan kırık beyaz (#fdfbf7) olarak ayarlandı.
- **Hiyerarşi:** Başlık boyutları önem derecesine göre ölçeklendirildi.

### Sayfa Yapısı

- **Ana Sayfa:** Burç seçim ekranı, hover efektli kartlar ve günlük tarih bilgisi. Burç sembolleri PNG formatında güncellendi.
- **Sıralamalar:** SEO uyumlu URL yapısı (/siralama). Genel, Aşk, Para ve Sağlık kategorilerine göre filtreleme. Tek sütunlu (Sıra, Burç) sadeleştirilmiş tablo yapısı.
- **Burç Detay:** Dinamik yönlendirme (/burc-adi/tarih). Kategorilere ayrılmış (Genel, Aşk, Para, Sağlık) detaylı yorumlar. Başlıkta PNG burç görselleri.
- **Kaynaklar:** Kullanılan astroloji kaynaklarının listelendiği bilgilendirme sayfası. Kart tasarımı güncellendi, logolar PNG/JPG formatında eklendi.

### Teknik Detaylar

- Next.js 16 (App Router)
- Tailwind CSS v4
- Lucide React ikon seti
- Responsive (mobil uyumlu) tasarım
- SEO uyumlu URL yapısı
- Hydration hataları giderildi (SSR uyumlu random veri üretimi)
- Görsel optimizasyonu (PNG/JPG desteği, grayscale hover efektleri)

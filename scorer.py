"""
AIstrolog - Burç Puanlama Sistemi
Kategorileştirilmiş burç yorumlarını analiz eder ve skorlar.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher
from collections import defaultdict

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scorer.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Sabit burç listesi
BURCLAR = [
    "Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak",
    "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"
]

# ==================== SENTIMENT ANALİZİ KELİME LİSTELERİ ====================

# Pozitif kelimeler ve ağırlıkları
POSITIVE_WORDS = {
    # Çok güçlü pozitif (3 puan)
    'harika': 3, 'mükemmel': 3, 'muhteşem': 3, 'olağanüstü': 3, 'şahane': 3,
    'enfes': 3, 'parlak': 3, 'görkemli': 3, 'fevkalade': 3,
    
    # Güçlü pozitif (2.5 puan)
    'başarılı': 2.5, 'şanslı': 2.5, 'kazanç': 2.5, 'kazançlı': 2.5, 'verimli': 2.5,
    'üretken': 2.5, 'yaratıcı': 2.5, 'ilham verici': 2.5, 'coşkulu': 2.5,
    'heyecan verici': 2.5, 'tutku': 2.5, 'tutkulu': 2.5, 'romantik': 2.5,
    'aşk dolu': 2.5, 'sevgi dolu': 2.5, 'enerji dolu': 2.5, 'dinç': 2.5,
    
    # Orta pozitif (2 puan)
    'mutlu': 2, 'iyi': 2, 'güzel': 2, 'olumlu': 2, 'fırsat': 2, 'şans': 2,
    'gelişme': 2, 'ilerleme': 2, 'büyüme': 2, 'yükseliş': 2, 'kazanım': 2,
    'başarı': 2, 'zafer': 2, 'galibiyet': 2, 'değerli': 2, 'önemli': 2,
    'sağlıklı': 2, 'güçlü': 2, 'kuvvetli': 2, 'enerjik': 2, 'canlı': 2,
    'neşeli': 2, 'keyifli': 2, 'hoş': 2, 'rahat': 2, 'huzurlu': 2,
    
    # Hafif pozitif (1.5 puan)
    'uygun': 1.5, 'elverişli': 1.5, 'destekleyici': 1.5, 'yardımcı': 1.5,
    'yararlı': 1.5, 'faydalı': 1.5, 'avantajlı': 1.5, 'kazançlı': 1.5,
    'bereketli': 1.5, 'bol': 1.5, 'zengin': 1.5, 'varlıklı': 1.5,
    'istikrarlı': 1.5, 'dengeli': 1.5, 'uyumlu': 1.5, 'ahenkli': 1.5,
    
    # Hafif-orta pozitif (1 puan)
    'yeni': 1, 'değişim': 1, 'farklı': 1, 'özel': 1, 'anlamlı': 1,
    'dikkat çekici': 1, 'ilginç': 1, 'cezbedici': 1, 'çekici': 1,
    'umut': 1, 'umutlu': 1, 'iyimser': 1, 'pozitif': 1, 'açık': 1,
}

# Negatif kelimeler ve ağırlıkları
NEGATIVE_WORDS = {
    # Çok güçlü negatif (-3 puan)
    'felaket': -3, 'yıkım': -3, 'dehşet': -3, 'korkunç': -3, 'berbat': -3,
    'rezil': -3, 'feci': -3, 'trajik': -3, 'kötü': -3,
    
    # Güçlü negatif (-2.5 puan)
    'kayıp': -2.5, 'zarar': -2.5, 'zararlı': -2.5, 'tehlike': -2.5, 'tehlikeli': -2.5,
    'riskli': -2.5, 'sorun': -2.5, 'sorunlu': -2.5, 'problemli': -2.5,
    'hastalık': -2.5, 'hasta': -2.5, 'rahatsız': -2.5, 'huzursuz': -2.5,
    'gergin': -2.5, 'stresli': -2.5, 'kaygılı': -2.5, 'endişeli': -2.5,
    
    # Orta negatif (-2 puan)
    'zor': -2, 'zorlu': -2, 'güç': -2, 'çetin': -2, 'ağır': -2,
    'yoğun': -2, 'baskı': -2, 'baskılı': -2, 'sıkıntı': -2, 'sıkıntılı': -2,
    'mutsuz': -2, 'üzgün': -2, 'kederli': -2, 'hüzünlü': -2,
    'olumsuz': -2, 'kötümser': -2, 'karamsarlık': -2, 'umutsuz': -2,
    'belirsiz': -2, 'kararsız': -2, 'istikrarsız': -2, 'dengesiz': -2,
    
    # Hafif negatif (-1.5 puan)
    'dikkat': -1.5, 'dikkatli': -1.5, 'temkinli': -1.5, 'ihtiyatlı': -1.5,
    'tedbirli': -1.5, 'sakıncalı': -1.5, 'mahzurlu': -1.5,
    'zayıf': -1.5, 'güçsüz': -1.5, 'yorgun': -1.5, 'bitkin': -1.5,
    'düşük': -1.5, 'az': -1.5, 'eksik': -1.5, 'yetersiz': -1.5,
    
    # Hafif-orta negatif (-1 puan)
    'gecikme': -1, 'gecikmeli': -1, 'yavaş': -1, 'ağır': -1,
    'engel': -1, 'engelleyici': -1, 'zorlayıcı': -1, 'kısıtlayıcı': -1,
    'sınırlı': -1, 'dar': -1, 'kapalı': -1, 'karanlık': -1,
}

# Kategori bazlı özel kelimeler
CATEGORY_KEYWORDS = {
    'aşk': {
        'keywords': [
            'aşk', 'sevgi', 'sevgili', 'partner', 'eş', 'ilişki', 'romantik', 'romantizm',
            'flört', 'flörtöz', 'evlilik', 'evli', 'nişan', 'nişanlı', 'tutku', 'tutkulu',
            'duygusal', 'duygu', 'his', 'hissiyat', 'çift', 'birlikte', 'beraberlik',
            'yakınlık', 'yakınlaşma', 'sıcaklık', 'şefkat', 'şefkatli', 'özen', 'ilgi',
            'alaka', 'bağ', 'bağlılık', 'sadakat', 'vefa', 'güven', 'ihanet'
        ],
        'positive_boost': [
            'romantik', 'tutkulu', 'aşk dolu', 'sevgi dolu', 'uyumlu', 'bağ güçleniyor',
            'yakınlaşma', 'sıcak anlar', 'özel anlar', 'kalp kalbe', 'ruh eşi'
        ],
        'negative_words': [
            'ihanet', 'aldatma', 'ayrılık', 'kavga', 'tartışma', 'soğukluk', 'mesafe',
            'güvensizlik', 'kıskançlık', 'kırılma', 'hayal kırıklığı'
        ]
    },
    'para': {
        'keywords': [
            'para', 'finans', 'finansal', 'gelir', 'kazanç', 'kazanmak', 'yatırım', 
            'yatırımcı', 'ekonomi', 'ekonomik', 'bütçe', 'harcama', 'tasarruf', 'maddi',
            'mali', 'iş', 'işe', 'kariyer', 'kariyerde', 'maaş', 'ücret', 'prim', 'ikramiye',
            'proje', 'projeler', 'girişim', 'girişimci', 'başarı', 'şirket', 'firma',
            'ticaret', 'alışveriş', 'satış', 'satın alma', 'borç', 'kredi', 'servet',
            'varlık', 'zenginlik', 'refah', 'bolluk', 'bereket'
        ],
        'positive_boost': [
            'finansal fırsat', 'kazanç', 'gelir artışı', 'yatırım fırsatı', 'başarı',
            'terfi', 'zam', 'prim', 'kazançlı', 'bereketli', 'bol', 'zengin'
        ],
        'negative_words': [
            'kayıp', 'zarar', 'borç', 'kriz', 'iflas', 'düşüş', 'azalma', 'eksiklik',
            'yetersizlik', 'yoksulluk', 'sıkıntı', 'darboğaz'
        ]
    },
    'sağlık': {
        'keywords': [
            'sağlık', 'sağlıklı', 'enerji', 'enerjik', 'dinç', 'canlı', 'zinde',
            'hastalık', 'hasta', 'rahatsız', 'rahatsızlık', 'vücut', 'fiziksel', 'mental',
            'ruhsal', 'psikolojik', 'fitness', 'spor', 'egzersiz', 'hareket', 'aktivite',
            'dinlenme', 'istirahat', 'uyku', 'beslenme', 'diyet', 'vitamin', 'bağışıklık',
            'direniş', 'dayanıklılık', 'kondisyon', 'form', 'denge', 'huzur', 'sakinlik',
            'stres', 'gerginlik', 'yorgunluk', 'bitkinlik', 'tükenme'
        ],
        'positive_boost': [
            'enerji dolu', 'dinç', 'sağlıklı', 'zinde', 'formda', 'güçlü', 'dayanıklı',
            'bağışıklık güçlü', 'canlı', 'hayat dolu', 'dengeli'
        ],
        'negative_words': [
            'hastalık', 'rahatsızlık', 'yorgunluk', 'bitkinlik', 'tükenme', 'stres',
            'gerginlik', 'uykusuzluk', 'baş ağrısı', 'ağrı', 'sızı'
        ]
    },
    'genel': {
        'keywords': [],  # Genel her şeyi kabul eder
        'positive_boost': [],
        'negative_words': []
    }
}

# ==================== YARDIMCI FONKSİYONLAR ====================

def clean_text(text: str) -> str:
    """Metni temizler"""
    if not text:
        return ""
    return ' '.join(text.strip().split())


def text_similarity(text1: str, text2: str) -> float:
    """İki metin arasındaki benzerliği hesaplar (0-1 arası)"""
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def is_duplicate(text1: str, text2: str, threshold: float = 0.95) -> bool:
    """İki metnin duplikasyon olup olmadığını kontrol eder"""
    return text_similarity(text1, text2) >= threshold


def validate_category_keywords(text: str, category: str) -> bool:
    """
    Bir metnin belirtilen kategori için uygun keyword içerip içermediğini kontrol eder.
    """
    if category == 'genel':
        return True
    
    if category not in CATEGORY_KEYWORDS:
        return False
    
    text_lower = text.lower()
    keywords = CATEGORY_KEYWORDS[category]['keywords']
    
    # En az 1 keyword bulunmalı
    return any(kw in text_lower for kw in keywords)


# ==================== SENTIMENT ANALİZİ ====================

def calculate_sentiment_score(text: str, category: str = 'genel') -> Dict:
    """
    Metinden sentiment skoru hesaplar.
    
    Returns:
        {
            'score': 0-100 arası skor,
            'sentiment': 'positive', 'neutral', 'negative',
            'details': {
                'positive_count': int,
                'negative_count': int,
                'positive_score': float,
                'negative_score': float,
                'category_boost': float
            }
        }
    """
    if not text or text == 'null':
        return None
    
    text_lower = text.lower()
    
    # Pozitif ve negatif kelime sayıları
    positive_score = 0
    negative_score = 0
    positive_count = 0
    negative_count = 0
    
    # Pozitif kelimeleri say
    for word, weight in POSITIVE_WORDS.items():
        if word in text_lower:
            count = text_lower.count(word)
            positive_score += weight * count
            positive_count += count
    
    # Negatif kelimeleri say
    for word, weight in NEGATIVE_WORDS.items():
        if word in text_lower:
            count = text_lower.count(word)
            negative_score += abs(weight) * count  # Negatif değerleri pozitife çevir
            negative_count += count
    
    # Kategori bazlı boost
    category_boost = 0
    if category in CATEGORY_KEYWORDS:
        # Pozitif boost kelimeleri
        for boost_word in CATEGORY_KEYWORDS[category]['positive_boost']:
            if boost_word in text_lower:
                category_boost += 5  # Her boost kelimesi +5 puan
        
        # Negatif kelimeler (kategori spesifik)
        for neg_word in CATEGORY_KEYWORDS[category]['negative_words']:
            if neg_word in text_lower:
                category_boost -= 5  # Her negatif kelime -5 puan
    
    # Net skor hesapla
    net_score = positive_score - negative_score + category_boost
    
    # Normalizasyon: -20 ile +20 arası bir değer olabilir, bunu 0-100'e çevir
    # Base score: 50 (nötr)
    # Her pozitif puan +2.5, her negatif puan -2.5 etkisi
    final_score = 50 + (net_score * 2.5)
    
    # 0-100 aralığına sınırla
    final_score = max(0, min(100, final_score))
    
    # Sentiment durumu
    if final_score >= 70:
        sentiment = 'positive'
    elif final_score >= 40:
        sentiment = 'neutral'
    else:
        sentiment = 'negative'
    
    return {
        'score': round(final_score, 1),
        'sentiment': sentiment,
        'details': {
            'positive_count': positive_count,
            'negative_count': negative_count,
            'positive_score': round(positive_score, 2),
            'negative_score': round(negative_score, 2),
            'category_boost': round(category_boost, 2),
            'net_score': round(net_score, 2)
        }
    }


# ==================== BURC SKORLAMA ====================

def score_burc_category(texts: List[str], category: str, burc_name: str) -> Optional[Dict]:
    """
    Bir burç kategorisi için skorlama yapar.
    Birden fazla kaynaktan gelen metinleri birleştirir ve skorlar.
    """
    if not texts:
        return None
    
    # Liste değilse listeye çevir
    if not isinstance(texts, list):
        texts = [texts]
    
    # Boş metinleri filtrele
    texts = [t for t in texts if t and t != 'null']
    
    if not texts:
        return None
    
    # Tüm metinleri birleştir
    combined_text = ' '.join(texts)
    
    # Kategori keyword kontrolü (genel hariç)
    if category != 'genel':
        if not validate_category_keywords(combined_text, category):
            logger.warning(f"{burc_name} - '{category}' kategorisinde uygun keyword bulunamadı")
            return None
    
    # Sentiment analizi yap
    sentiment_result = calculate_sentiment_score(combined_text, category)
    
    if sentiment_result:
        return {
            'score': sentiment_result['score'],
            'sentiment': sentiment_result['sentiment'],
            'source_count': len(texts),
            'details': sentiment_result['details']
        }
    
    return None


def score_burc(burc_name: str, burc_data: Dict) -> Dict:
    """
    Bir burç için tüm kategorilerde skorlama yapar.
    Duplikasyon kontrolü yapar.
    """
    scores = {
        'genel': None,
        'aşk': None,
        'para': None,
        'sağlık': None,
        'toplam': None,
        'issues': []
    }
    
    # Her kategori için metinleri al
    category_texts = {}
    for cat in ['genel', 'aşk', 'para', 'sağlık']:
        texts = burc_data.get(cat, [])
        if texts and texts != 'null':
            if not isinstance(texts, list):
                texts = [texts]
            category_texts[cat] = ' '.join(texts)
        else:
            category_texts[cat] = None
    
    # Duplikasyon kontrolü
    categories = ['genel', 'aşk', 'para', 'sağlık']
    for i, cat1 in enumerate(categories):
        if not category_texts[cat1]:
            continue
        
        for cat2 in categories[i+1:]:
            if not category_texts[cat2]:
                continue
            
            similarity = text_similarity(category_texts[cat1], category_texts[cat2])
            
            if similarity >= 0.95:  # %95+ benzerlik = tam duplikasyon
                issue = f"'{cat1}' ve '{cat2}' kategorileri %{similarity*100:.0f} benzer (duplikasyon)"
                scores['issues'].append(issue)
                logger.warning(f"{burc_name}: {issue}")
                
                # Daha spesifik olanı tut (genel hariç)
                if cat1 == 'genel':
                    category_texts[cat1] = None
                elif cat2 == 'genel':
                    category_texts[cat2] = None
                else:
                    # İkisi de spesifik - keyword kontrolü yaparak karar ver
                    if not validate_category_keywords(category_texts[cat2], cat2):
                        category_texts[cat2] = None
                        scores['issues'].append(f"'{cat2}' kategorisi keyword eksikliği nedeniyle kaldırıldı")
    
    # Her kategori için skorlama yap
    for cat in ['genel', 'aşk', 'para', 'sağlık']:
        if category_texts[cat]:
            texts = burc_data.get(cat, [])
            if not isinstance(texts, list):
                texts = [texts]
            scores[cat] = score_burc_category(texts, cat, burc_name)
    
    # Toplam skor hesapla (ağırlıklı ortalama)
    valid_scores = {}
    weights = {'genel': 0.3, 'aşk': 0.25, 'para': 0.25, 'sağlık': 0.20}
    
    for cat, weight in weights.items():
        if scores[cat] and scores[cat]['score'] is not None:
            valid_scores[cat] = (scores[cat]['score'], weight)
    
    if valid_scores:
        total_weight = sum(w for _, w in valid_scores.values())
        weighted_sum = sum(score * weight for score, weight in valid_scores.values())
        scores['toplam'] = round(weighted_sum / total_weight, 1)
    else:
        scores['toplam'] = 0
    
    return scores


# ==================== GENEL SKORLAMA VE SIRALAMA ====================

def score_all_burcs(processed_data: Dict) -> Dict:
    """
    Tüm burçlar için skorlama yapar.
    processed_data formatı: {"site": {"Koç": {"genel": [...], "aşk": [...], ...}, ...}, ...}
    Veya: {"Koç": {"genel": [...], "aşk": [...], ...}, ...}
    """
    logger.info("Tüm burçlar için skorlama başlıyor...")
    
    # Veri formatını tespit et
    # Eğer ilk key bir site ismi ise (küçük harf), burç verilerini birleştir
    first_key = next(iter(processed_data.keys()))
    
    if first_key.lower() == first_key or first_key not in BURCLAR:
        # Site bazlı format: {"milliyet": {"Koç": {...}}, "hurriyet": {"Koç": {...}}}
        logger.info("Site bazlı format tespit edildi, burç verileri birleştiriliyor...")
        merged_data = {}
        
        for site_name, site_data in processed_data.items():
            for burc_name, burc_data in site_data.items():
                if burc_name not in merged_data:
                    merged_data[burc_name] = {
                        'genel': [],
                        'aşk': [],
                        'para': [],
                        'sağlık': []
                    }
                
                # Her kategoriyi birleştir
                for cat in ['genel', 'aşk', 'para', 'sağlık']:
                    content = burc_data.get(cat)
                    if content and content != 'null' and content is not None:
                        if isinstance(content, list):
                            merged_data[burc_name][cat].extend(content)
                        else:
                            merged_data[burc_name][cat].append(content)
        
        processed_data = merged_data
        logger.info(f"{len(processed_data)} burç verisi birleştirildi")
    
    all_scores = {}
    
    for burc in BURCLAR:
        if burc not in processed_data:
            logger.warning(f"{burc} verisi bulunamadı!")
            continue
        
        logger.info(f"{burc} skorlanıyor...")
        burc_score = score_burc(burc, processed_data[burc])
        all_scores[burc] = burc_score
        
        # Issue varsa logla
        if burc_score['issues']:
            for issue in burc_score['issues']:
                logger.warning(f"{burc}: {issue}")
    
    logger.info("Skorlama tamamlandı!")
    return all_scores


def rank_burcs(scores: Dict) -> Dict:
    """
    Burçları kategorilere göre sıralar ve liderleri belirler.
    """
    rankings = {
        'genel_ranking': [],
        'aşk_ranking': [],
        'para_ranking': [],
        'sağlık_ranking': [],
        'leaders': {
            'en_şanslı': None,
            'en_aşık': None,
            'en_zengin': None,
            'en_sağlıklı': None,
            'en_şanssız': None
        }
    }
    
    # Her kategori için sıralama
    categories = {
        'genel_ranking': 'toplam',
        'aşk_ranking': 'aşk',
        'para_ranking': 'para',
        'sağlık_ranking': 'sağlık'
    }
    
    for rank_key, cat in categories.items():
        valid_burcs = []
        
        for burc, score_data in scores.items():
            if cat == 'toplam':
                score_val = score_data.get('toplam', 0)
            else:
                cat_data = score_data.get(cat)
                score_val = cat_data['score'] if cat_data else 0
            
            if score_val and score_val > 0:
                valid_burcs.append({
                    'burc': burc,
                    'score': score_val,
                    'sentiment': score_data.get(cat, {}).get('sentiment', 'neutral') if cat != 'toplam' else None
                })
        
        # Skora göre sırala (yüksekten düşüğe)
        valid_burcs.sort(key=lambda x: x['score'], reverse=True)
        rankings[rank_key] = valid_burcs
    
    # Liderleri belirle
    if rankings['genel_ranking']:
        rankings['leaders']['en_şanslı'] = rankings['genel_ranking'][0]
        rankings['leaders']['en_şanssız'] = rankings['genel_ranking'][-1]
    
    if rankings['aşk_ranking']:
        rankings['leaders']['en_aşık'] = rankings['aşk_ranking'][0]
    
    if rankings['para_ranking']:
        rankings['leaders']['en_zengin'] = rankings['para_ranking'][0]
    
    if rankings['sağlık_ranking']:
        rankings['leaders']['en_sağlıklı'] = rankings['sağlık_ranking'][0]
    
    return rankings


# ==================== DOSYA İŞLEMLERİ ====================

def load_processed_data(filepath: str) -> Dict:
    """Processed JSON dosyasını yükler"""
    logger.info(f"Veri yükleniyor: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    logger.info(f"Veri yüklendi: {len(data)} burç")
    return data


def save_scored_data(scores: Dict, rankings: Dict, output_dir: str = "data"):
    """
    Skorlanmış verileri JSON dosyasına kaydeder.
    Format: scored_processed_daily_raw_YYYY-MM-DD.json
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"scored_processed_daily_raw_{today}.json"
    filepath = os.path.join(output_dir, filename)
    
    output_data = {
        'metadata': {
            'date': today,
            'total_burcs': len(scores),
            'scored_at': datetime.now().isoformat()
        },
        'scores': scores,
        'rankings': rankings
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Skorlar kaydedildi: {filepath}")
    return filepath


def print_rankings_summary(rankings: Dict):
    """Sıralama özetini ekrana yazdırır"""
    print("\n" + "=" * 80)
    print("🏆 GÜNÜN BURCLAR SIRALAMASI")
    print("=" * 80)
    
    # Liderler
    leaders = rankings['leaders']
    
    print("\n⭐ GÜNÜN LİDERLERİ:")
    print("-" * 80)
    
    if leaders['en_şanslı']:
        print(f"🥇 EN ŞANSLI BURÇ:   {leaders['en_şanslı']['burc']:12} → {leaders['en_şanslı']['score']:.1f}/100")
    
    if leaders['en_aşık']:
        print(f"❤️  EN AŞIK BURÇ:     {leaders['en_aşık']['burc']:12} → {leaders['en_aşık']['score']:.1f}/100")
    
    if leaders['en_zengin']:
        print(f"💰 EN ZENGİN BURÇ:   {leaders['en_zengin']['burc']:12} → {leaders['en_zengin']['score']:.1f}/100")
    
    if leaders['en_sağlıklı']:
        print(f"🏃 EN SAĞLIKLI BURÇ: {leaders['en_sağlıklı']['burc']:12} → {leaders['en_sağlıklı']['score']:.1f}/100")
    
    if leaders['en_şanssız']:
        print(f"⚠️  EN ŞANSSIZ BURÇ:  {leaders['en_şanssız']['burc']:12} → {leaders['en_şanssız']['score']:.1f}/100")
    
    # Genel sıralama (Tüm burçlar)
    print("\n📊 GENEL SIRALAMA:")
    print("-" * 80)
    
    medals = {0: '🥇', 1: '🥈', 2: '🥉'}
    for i, item in enumerate(rankings['genel_ranking']):
        medal = medals.get(i, f"{i+1:2d}.")
        
        # Yıldız sayısı (skor bazlı)
        score = item['score']
        if score >= 90:
            stars = '⭐⭐⭐⭐⭐'
        elif score >= 75:
            stars = '⭐⭐⭐⭐'
        elif score >= 60:
            stars = '⭐⭐⭐'
        elif score >= 45:
            stars = '⭐⭐'
        else:
            stars = '⭐'
        
        print(f"{medal} {item['burc']:12} → {item['score']:5.1f}/100 {stars}")
    
    # Kategori sıralamaları (Top 3)
    print("\n❤️  AŞK SIRALAMASI (Top 3):")
    print("-" * 80)
    for i, item in enumerate(rankings['aşk_ranking'][:3]):
        medal = medals.get(i, f"{i+1}.")
        print(f"{medal} {item['burc']:12} → {item['score']:5.1f}/100")
    
    print("\n💰 PARA SIRALAMASI (Top 3):")
    print("-" * 80)
    for i, item in enumerate(rankings['para_ranking'][:3]):
        medal = medals.get(i, f"{i+1}.")
        print(f"{medal} {item['burc']:12} → {item['score']:5.1f}/100")
    
    print("\n🏃 SAĞLIK SIRALAMASI (Top 3):")
    print("-" * 80)
    for i, item in enumerate(rankings['sağlık_ranking'][:3]):
        medal = medals.get(i, f"{i+1}.")
        print(f"{medal} {item['burc']:12} → {item['score']:5.1f}/100")
    
    print("\n" + "=" * 80)


# ==================== ANA FONKSİYON ====================

def main():
    """Ana fonksiyon"""
    import sys
    
    logger.info("AIstrolog Scorer başlatılıyor...")
    logger.info(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Dosya parametresi kontrol et
        if len(sys.argv) < 2:
            # Bugünün dosyasını otomatik bul
            today = datetime.now().strftime("%Y-%m-%d")
            input_file = f"data/processed_daily_raw_{today}.json"
            
            if not os.path.exists(input_file):
                # En son processed dosyayı bul
                import glob
                processed_files = glob.glob("data/processed_daily_raw_*.json")
                if processed_files:
                    input_file = sorted(processed_files)[-1]
                    logger.info(f"En son dosya kullanılıyor: {input_file}")
                else:
                    logger.error("Processed dosya bulunamadı!")
                    print("Kullanım: python scorer.py [processed_file.json]")
                    return
        else:
            input_file = sys.argv[1]
        
        # Veriyi yükle
        processed_data = load_processed_data(input_file)
        
        # Skorlama yap
        scores = score_all_burcs(processed_data)
        
        # Sıralama yap
        rankings = rank_burcs(scores)
        
        # Sonuçları kaydet
        output_file = save_scored_data(scores, rankings)
        
        # Özet göster
        print_rankings_summary(rankings)
        
        logger.info("=" * 80)
        logger.info("✅ Skorlama işlemi başarıyla tamamlandı!")
        logger.info(f"Çıktı dosyası: {output_file}")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"Hata oluştu: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

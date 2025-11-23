"""
AIstrolog - Burç Ranking Sistemi
Skorlanmış burç verilerinden ranking oluşturur ve rankings_history.json'a ekler.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ranker.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_scored_data(filepath: str) -> Dict:
    """Scored JSON dosyasını yükler"""
    logger.info(f"Scored veri yükleniyor: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    logger.info(f"Scored veri yüklendi: {data['metadata']['date']}")
    return data


def load_rankings_history(filepath: str = "data/rankings_history.json") -> Dict:
    """Rankings history dosyasını yükler, yoksa boş dict döner"""
    if os.path.exists(filepath):
        logger.info(f"Rankings history yükleniyor: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Rankings history yüklendi: {len(data)} tarih")
        return data
    else:
        logger.info("Rankings history dosyası bulunamadı, yeni oluşturulacak")
        return {}


def save_rankings_history(data: Dict, filepath: str = "data/rankings_history.json"):
    """Rankings history dosyasını kaydeder"""
    # Tarihleri sıralı tut (en yeni en üstte)
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Rankings history kaydedildi: {filepath}")


def create_ranking_for_date(scored_data: Dict) -> Dict:
    """
    Scored veriden belirli bir tarih için ranking oluşturur.
    
    Returns:
        {
            "genel_ranking": [...],
            "aşk_ranking": [...],
            "para_ranking": [...],
            "sağlık_ranking": [...]
        }
    """
    rankings = scored_data.get('rankings', {})
    
    # Ranking verilerini dönüştür
    result = {}
    
    for category in ['genel_ranking', 'aşk_ranking', 'para_ranking', 'sağlık_ranking']:
        if category in rankings:
            # Her burç için sadece burc ve score alanlarını al
            result[category] = [
                {
                    'burc': item['burc'],
                    'score': item['score']
                }
                for item in rankings[category]
            ]
    
    return result


def update_rankings_history(scored_filepath: str, history_filepath: str = "data/rankings_history.json"):
    """
    Scored dosyadan ranking oluşturur ve history'e ekler.
    """
    # Scored veriyi yükle
    scored_data = load_scored_data(scored_filepath)
    
    # Tarihi al
    date = scored_data['metadata']['date']
    logger.info(f"Tarih için ranking oluşturuluyor: {date}")
    
    # Ranking oluştur
    ranking_data = create_ranking_for_date(scored_data)
    
    # History'yi yükle
    history = load_rankings_history(history_filepath)
    
    # Yeni ranking'i ekle
    if date in history:
        logger.warning(f"{date} tarihi zaten mevcut, güncelleniyor...")
    
    history[date] = ranking_data
    
    # Kaydet
    save_rankings_history(history, history_filepath)
    
    logger.info(f"✅ {date} tarihi için ranking eklendi")
    print_ranking_summary(ranking_data, date)
    
    return history


def print_ranking_summary(ranking_data: Dict, date: str):
    """Ranking özetini ekrana yazdırır"""
    print("\n" + "=" * 80)
    print(f"📅 {date} TARİHİ İÇİN RANKING")
    print("=" * 80)
    
    # Her kategori için ilk 3'ü göster
    categories = {
        'genel_ranking': '🏆 GENEL',
        'aşk_ranking': '❤️  AŞK',
        'para_ranking': '💰 PARA',
        'sağlık_ranking': '🏃 SAĞLIK'
    }
    
    for cat_key, cat_name in categories.items():
        if cat_key in ranking_data:
            print(f"\n{cat_name} SIRALAMASI (İlk 3):")
            print("-" * 80)
            
            medals = ['🥇', '🥈', '🥉']
            for i, item in enumerate(ranking_data[cat_key][:3]):
                print(f"{medals[i]} {item['burc']:12} → {item['score']:.1f}/100")
    
    print("\n" + "=" * 80)


def main():
    """Ana fonksiyon"""
    import sys
    
    logger.info("AIstrolog Ranker başlatılıyor...")
    logger.info(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Dosya parametresi kontrol et
        if len(sys.argv) < 2:
            # Bugünün dosyasını otomatik bul
            today = datetime.now().strftime("%Y-%m-%d")
            input_file = f"data/scored_processed_daily_raw_{today}.json"
            
            if not os.path.exists(input_file):
                # En son scored dosyayı bul
                import glob
                scored_files = glob.glob("data/scored_processed_daily_raw_*.json")
                if scored_files:
                    input_file = sorted(scored_files)[-1]
                    logger.info(f"En son dosya kullanılıyor: {input_file}")
                else:
                    logger.error("Scored dosya bulunamadı!")
                    print("Kullanım: python ranker.py [scored_file.json]")
                    return
        else:
            input_file = sys.argv[1]
        
        # Rankings history'yi güncelle
        update_rankings_history(input_file)
        
        logger.info("=" * 80)
        logger.info("✅ Ranking işlemi başarıyla tamamlandı!")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"Hata oluştu: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

"""
AIstrolog - Profesyonel Web Scraping Sistemi
Çeşitli haber/burç sitelerinden günlük burç yorumlarını toplar.
"""

import requests
from bs4 import BeautifulSoup
import json
import logging
import os
import random
import re
import time
from datetime import datetime
from typing import Dict, Optional

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Sabit burç listesi
BURCLAR = [
    "Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak",
    "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"
]

# Burç URL slug'ları
BURC_SLUGS = {
    "Koç": "koc",
    "Boğa": "boga",
    "İkizler": "ikizler",
    "Yengeç": "yengec",
    "Aslan": "aslan",
    "Başak": "basak",
    "Terazi": "terazi",
    "Akrep": "akrep",
    "Yay": "yay",
    "Oğlak": "oglak",
    "Kova": "kova",
    "Balık": "balik"
}

# Burç isim normalizasyonu için mapping
BURC_NORMALIZATION = {
    "koc": "Koç", "koç": "Koç", "aries": "Koç",
    "boga": "Boğa", "boğa": "Boğa", "taurus": "Boğa",
    "ikizler": "İkizler", "gemini": "İkizler",
    "yengec": "Yengeç", "yengeç": "Yengeç", "cancer": "Yengeç",
    "aslan": "Aslan", "leo": "Aslan",
    "basak": "Başak", "başak": "Başak", "virgo": "Başak",
    "terazi": "Terazi", "libra": "Terazi",
    "akrep": "Akrep", "scorpio": "Akrep",
    "yay": "Yay", "sagittarius": "Yay",
    "oglak": "Oğlak", "oğlak": "Oğlak", "capricorn": "Oğlak",
    "kova": "Kova", "aquarius": "Kova",
    "balik": "Balık", "balık": "Balık", "pisces": "Balık"
}

# User agent listesi
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]


def clean_text(text: str) -> str:
    """Metni temizler: whitespace, satır sonu vb."""
    if not text:
        return ""
    return ' '.join(text.strip().split())


def normalize_burc_name(name: str) -> Optional[str]:
    """Burç ismini normalize eder"""
    if not name:
        return None
    
    # Özel durumlar için direkt mapping (Hurriyet'te büyük harf sorunları için)
    special_cases = {
        "İKİZLER": "İkizler",
        "IKIZLER": "İkizler",
        "TERAZİ": "Terazi",
        "TERAZI": "Terazi",
    }
    
    clean_name_upper = name.strip().upper()
    if clean_name_upper in special_cases:
        return special_cases[clean_name_upper]
    
    clean_name = name.strip().lower()
    normalized = BURC_NORMALIZATION.get(clean_name)
    if normalized:
        return normalized
    # Direkt eşleşme kontrolü
    for burc in BURCLAR:
        if burc.lower() == clean_name:
            return burc
    return None


def get_random_headers() -> Dict[str, str]:
    """Random user agent döner - Accept-Encoding REMOVED to avoid brotli issues"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        # NOTE: Accept-Encoding removed - requests will handle this automatically
        # and some sites (like elele.com.tr) return broken brotli when we set it
        'Connection': 'keep-alive',
    }


def random_sleep():
    """1-3 saniye arası random bekler"""
    time.sleep(random.uniform(1, 3))


def create_empty_burc_dict() -> Dict:
    """Boş burç dictionary'si oluşturur - SADECE sonuç initialize için kullanılır"""
    return {burc: {"genel": None, "aşk": None, "para": None, "sağlık": None} for burc in BURCLAR}


# SCRAPING FONKSİYONLARI - HER SİTE İÇİN AYRI

def scrape_milliyet() -> Optional[Dict]:
    """Milliyet.com.tr'den burç yorumlarını çeker"""
    logger.info("Milliyet scrape başladı...")
    results = create_empty_burc_dict()
    
    try:
        for burc_name, slug in BURC_SLUGS.items():
            try:
                url = f"https://www.milliyet.com.tr/pembenar/astroloji/{slug}-burcu-gunluk-yorum/"
                response = requests.get(url, headers=get_random_headers(), timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.content, 'lxml')
                
                # HTML yapısına göre içeriği çek
                content_div = soup.select_one('.horoscope-tabs__content__main-inner')
                
                if content_div:
                    # Tüm p etiketlerini al
                    paragraphs = content_div.find_all('p')
                    
                    yorum_dict = {"genel": None, "aşk": None, "para": None, "sağlık": None}
                    
                    # Tüm paragrafları birleştir - hepsini genel'e ekle (etiketleri temizleyerek)
                    all_texts = []
                    
                    # Kategori etiketleri (temizlemek için)
                    category_labels = ['iş:', 'aşk:', 'para:', 'kariyer:', 'sağlık:', 'ilişkiler:']
                    
                    for p in paragraphs:
                        text = clean_text(p.get_text())
                        if text and len(text) > 5:
                            # Kategori etiketlerini temizle
                            text_clean = text
                            for label in category_labels:
                                # Case-insensitive replace
                                if text_clean.lower().startswith(label):
                                    text_clean = text_clean[len(label):].strip()
                                    break
                                # Etiket cümle içinde de olabilir
                                text_clean = re.sub(rf'\b{label}\s*', '', text_clean, flags=re.IGNORECASE)
                            
                            all_texts.append(text_clean)
                        
                        text_lower = text.lower()
                        
                        # Ayrıca kategorilere göre de ayır
                        if text_lower.startswith('para:'):
                            yorum_dict["para"] = text.split(':', 1)[1].strip() if ':' in text else text
                        elif text_lower.startswith('sağlık:'):
                            yorum_dict["sağlık"] = text.split(':', 1)[1].strip() if ':' in text else text
                        elif 'aşk' in text_lower and ('ilişki' in text_lower or 'i̇lişki' in text_lower):
                            yorum_dict["aşk"] = text.split(':', 1)[1].strip() if ':' in text else text
                    
                    # Tüm metni genel'e ekle (etiketler temizlenmiş haliyle)
                    if all_texts:
                        yorum_dict["genel"] = ' '.join(all_texts)
                    
                    results[burc_name] = yorum_dict
                    logger.info(f"Milliyet - {burc_name} tamamlandı")
                
                random_sleep()
                
            except Exception as e:
                logger.error(f"Milliyet - {burc_name} error: {e}")
                continue
        
        logger.info("Milliyet scrape tamamlandı")
        return results
        
    except Exception as e:
        logger.error(f"Milliyet scraping error: {e}")
        return None


def scrape_hurriyet() -> Optional[Dict]:
    """Hurriyet.com.tr'den burç yorumlarını çeker - Ana sayfadaki widget'tan tüm burçları alır"""
    logger.info("Hurriyet scrape başladı...")
    results = create_empty_burc_dict()
    
    try:
        # Ana astroloji sayfasını çek - tüm burçlar burada
        url = "https://www.hurriyet.com.tr/mahmure/astroloji/"
        response = requests.get(url, headers=get_random_headers(), timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Zodiac widget içindeki tüm burç açıklamalarını al
        widget_descriptions = soup.select('.zodiac-widget-description-wrapper')
        
        if not widget_descriptions:
            logger.warning("Hurriyet - Zodiac widget bulunamadı")
            return results
        
        # Her bir burç açıklamasını işle
        for desc_wrapper in widget_descriptions:
            try:
                # Burç ismini al (link içinden)
                title_elem = desc_wrapper.select_one('.zodiac-widget-description-wrapper-title a')
                if not title_elem:
                    continue
                
                title_text = clean_text(title_elem.get_text())
                # "KOÇ BURCU" -> "Koç" gibi normalize et
                burc_name_raw = title_text.replace('BURCU', '').replace('BURÇ', '').strip()
                burc_name = normalize_burc_name(burc_name_raw)
                
                if not burc_name:
                    logger.warning(f"Hurriyet - Burç ismi normalize edilemedi: {burc_name_raw}")
                    continue
                
                # Burç yorumunu al
                text_elem = desc_wrapper.select_one('.zodiac-widget-description-wrapper-text .truncate')
                if text_elem:
                    yorum = clean_text(text_elem.get_text())
                    
                    if yorum and len(yorum) > 20:
                        results[burc_name]["genel"] = yorum
                        logger.info(f"Hurriyet - {burc_name} tamamlandı")
                
            except Exception as e:
                logger.error(f"Hurriyet - Burç işleme hatası: {e}")
                continue
        
        logger.info("Hurriyet scrape tamamlandı")
        return results
        
    except Exception as e:
        logger.error(f"Hurriyet scraping error: {e}")
        return None

def scrape_haberturk() -> Optional[Dict]:
    """Haberturk Hayat'tan burç yorumlarını çeker - gunun-yorumu sayfasından günlük link bulur"""
    logger.info("Haberturk scrape başladı...")
    results = create_empty_burc_dict()
    
    try:
        # Günün yorumu sayfasından günlük burç yorumları linkini bul
        main_url = "https://hthayat.haberturk.com/astroloji/gunun-yorumu"
        response = requests.get(main_url, headers=get_random_headers(), timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Günlük burç yorumu linkini ara - figcaption içinde title içeren bağlantıyı bul
        daily_link = None
        today = datetime.now()
        
        # figcaption içindeki bağlantıları ara
        figcaptions = soup.find_all('figcaption')
        for figcaption in figcaptions:
            # h2.title içinde "Günlük burç yorumları" içeren linki ara
            title_heading = figcaption.find('h2', class_='title')
            if title_heading and 'günlük burç yorumları' in title_heading.get_text().lower():
                # Parent <a> tag'ini bul
                parent_link = figcaption.find_parent('a', href=True)
                if parent_link:
                    href = parent_link['href']
                    daily_link = href if href.startswith('http') else f"https://hthayat.haberturk.com{href}"
                    break
        
        # Alternatif yöntem: link içinde 'gunluk-burc-yorumlari' içeren bağlantıyı ara
        if not daily_link:
            for link in soup.find_all('a', href=True):
                href = link['href']
                if 'gunluk-burc-yorumlari' in href.lower():
                    daily_link = href if href.startswith('http') else f"https://hthayat.haberturk.com{href}"
                    break
        
        if not daily_link:
            logger.warning("Haberturk - Günlük burç yorumları linki bulunamadı")
            return results
        
        logger.info(f"Haberturk - Günlük link bulundu: {daily_link}")
        
        # Günlük sayfayı çek
        response = requests.get(daily_link, headers=get_random_headers(), timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Sayfadaki tüm burç yorumlarını çek
        figcaptions = soup.find_all('figcaption')
        
        for fig in figcaptions:
            text = clean_text(fig.get_text())
            text_upper = text.upper()  # Türkçe büyük harfe çevir
            
            # Burç ismini bul - hem Türkçe hem İngilizce büyük harf versiyonları
            for burc_name in BURCLAR:
                burc_upper_tr = burc_name.upper()  # İKİZLER, TERAZİ (Türkçe)
                burc_upper_en = burc_name.replace('İ', 'I').replace('i', 'I').upper()  # IKIZLER, TERAZI (İngilizce)
                
                # Her iki versiyonu da kontrol et
                found = False
                search_term = None
                
                if burc_upper_tr in text_upper[:200]:  # 100'den 200'e çıkardık
                    found = True
                    search_term = burc_upper_tr
                elif burc_upper_en in text_upper[:200]:
                    found = True
                    search_term = burc_upper_en
                
                if found and search_term:
                    # Orijinal text'te arama yap (case-insensitive)
                    # İlk önce Türkçe versiyonu dene
                    if search_term in text_upper:
                        idx = text_upper.index(search_term)
                        burc_text = text[idx + len(search_term):].replace('GÜNLÜK BURÇ YORUMU', '').replace('Günlük Burç Yorumu', '').strip()
                        
                        if burc_text and len(burc_text) > 20:
                            results[burc_name]["genel"] = burc_text
                            logger.info(f"Haberturk - {burc_name} tamamlandı")
                    break
        
        random_sleep()
        logger.info("Haberturk scrape tamamlandı")
        return results
        
    except Exception as e:
        logger.error(f"Haberturk scraping error: {e}")
        return None


def scrape_elele() -> Optional[Dict]:
    """Elele.com.tr'den burç yorumlarını çeker"""
    logger.info("Elele scrape başladı...")
    results = create_empty_burc_dict()
    
    try:
        for burc_name, slug in BURC_SLUGS.items():
            try:
                url = f"https://www.elele.com.tr/astroloji/burclar/{slug}"
                response = requests.get(url, headers=get_random_headers(), timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.content, 'lxml')
                
                # .news-content div'i içindeki içeriği al
                content_div = soup.select_one('.news-content')
                
                if content_div:
                    # p etiketini al
                    p_tag = content_div.find('p')
                    
                    if p_tag:
                        # Metni al ve temizle
                        text = clean_text(p_tag.get_text())
                        
                        # "14 Kasım 2025 Günlük Burç Yorumu:" gibi prefix'leri kaldır
                        if text and ':' in text:
                            parts = text.split(':', 1)
                            if len(parts) > 1 and len(parts[1].strip()) > 20:
                                text = parts[1].strip()
                        
                        # En az 20 karakter olmalı
                        if text and len(text) > 20:
                            results[burc_name]["genel"] = text
                            logger.info(f"Elele - {burc_name} tamamlandı")
                
                random_sleep()
                
            except Exception as e:
                logger.error(f"Elele - {burc_name} error: {e}")
                continue
        
        logger.info("Elele scrape tamamlandı")
        return results
        
    except Exception as e:
        logger.error(f"Elele scraping error: {e}")
        return None


def scrape_onedio() -> Optional[Dict]:
    """Onedio.com'dan burç yorumlarını çeker - Her kategoride 12 figcaption var (her burç için bir tane)"""
    logger.info("Onedio scrape başladı...")
    results = create_empty_burc_dict()
    
    try:
        today = datetime.now()
        date_str = today.strftime("%d-%B-%Y").lower()  # 21-kasim-2025 formatı
        
        # Türkçe ay isimleri
        ay_map = {
            'january': 'ocak', 'february': 'subat', 'march': 'mart', 'april': 'nisan',
            'may': 'mayis', 'june': 'haziran', 'july': 'temmuz', 'august': 'agustos',
            'september': 'eylul', 'october': 'ekim', 'november': 'kasim', 'december': 'aralik'
        }
        
        for eng, tr in ay_map.items():
            date_str = date_str.replace(eng, tr)
        
        # Kategoriler: genel, aşk, para, sağlık
        categories = {
            'genel': f"https://onedio.com/astroloji/gunluk-burc-yorumuna-gore-{date_str}-gunun-nasil-gececek",
            'aşk': f'https://onedio.com/astroloji/gunluk-ask-burc-yorumuna-gore-{date_str}-gunun-nasil-gececek',
            'para': f'https://onedio.com/astroloji/gunluk-para-burc-yorumuna-gore-{date_str}-gunun-nasil-gececek',
            'sağlık': f'https://onedio.com/astroloji/gunluk-saglik-burc-yorumuna-gore-{date_str}-gunun-nasil-gececek'
        }
        
        # Her kategori için tüm burçları al
        for category_name, category_url in categories.items():
            try:
                response = requests.get(category_url, headers=get_random_headers(), timeout=10)
                response.encoding = 'utf-8'
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'lxml')
                    
                    # Tüm figcaption'ları al (her biri bir burç için)
                    figcaptions = soup.find_all('figcaption')
                    
                    for figcaption in figcaptions:
                        paragraphs = figcaption.find_all('p')
                        full_text = ' '.join([clean_text(p.get_text()) for p in paragraphs])
                        
                        # Hangi burç için olduğunu bul
                        for burc_name in BURCLAR:
                            if f'Sevgili {burc_name}' in full_text:
                                # "Sevgili Burç," kısmından sonrasını al
                                burc_yorum = full_text.split(f'Sevgili {burc_name}', 1)[1].strip()
                                # Virgül varsa kaldır
                                if burc_yorum.startswith(','):
                                    burc_yorum = burc_yorum[1:].strip()
                                
                                results[burc_name][category_name] = burc_yorum
                                break
                    
                    logger.info(f"Onedio - {category_name} kategorisi tamamlandı")
                
                random_sleep()
            
            except Exception as e:
                logger.error(f"Onedio - {category_name} kategori hatası: {e}")
                continue
        
        logger.info("Onedio scrape tamamlandı")
        return results
        
    except Exception as e:
        logger.error(f"Onedio scraping error: {e}")
        return None


def scrape_mynet() -> Optional[Dict]:
    """Mynet.com'dan burç yorumlarını çeker"""
    logger.info("Mynet scrape başladı...")
    results = create_empty_burc_dict()
    
    try:
        for burc_name, slug in BURC_SLUGS.items():
            try:
                url = f"https://www.mynet.com/kadin/burclar-astroloji/{slug}-burcu-gunluk-yorumu.html"
                response = requests.get(url, headers=get_random_headers(), timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.content, 'lxml')
                
                # #contextual div içindeki .detail-content-inner'ı bul
                content_div = soup.select_one('#contextual .detail-content-inner')
                
                if content_div:
                    # p etiketini al
                    p_tag = content_div.find('p')
                    
                    if p_tag:
                        text = clean_text(p_tag.get_text())
                        
                        if text and len(text) > 20:
                            results[burc_name]["genel"] = text
                            logger.info(f"Mynet - {burc_name} tamamlandı")
                
                random_sleep()
                
            except Exception as e:
                logger.error(f"Mynet - {burc_name} error: {e}")
                continue
        
        logger.info("Mynet scrape tamamlandı")
        return results
        
    except Exception as e:
        logger.error(f"Mynet scraping error: {e}")
        return None


def scrape_twitburc() -> Optional[Dict]:
    """Twitburc.com.tr'den burç yorumlarını çeker"""
    logger.info("Twitburc scrape başladı...")
    results = create_empty_burc_dict()
    
    try:
        for burc_name, slug in BURC_SLUGS.items():
            try:
                url = f"https://twitburc.com.tr/burclar/{slug}"
                response = requests.get(url, headers=get_random_headers(), timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Tüm tab-pane'leri bul
                # Sıralama: 1. Hakkında, 2. Dün, 3. Günlük, 4. Haftalık, 5. Aylık, 6. Yıllık
                tab_panes = soup.find_all('div', class_='tab-pane')
                
                target_pane = None
                if len(tab_panes) >= 3:
                    # 3. pane (index 2) Günlük yorumdur
                    target_pane = tab_panes[2]
                elif tab_panes:
                    # Eğer 3 tane yoksa, active olanı veya ilkini dene (fallback)
                    target_pane = soup.find('div', class_='tab-pane active') or tab_panes[0]
                
                if target_pane:
                    # "Günlük Yorumu" veya "Günün Ruh Hali" içeren bölümü bul
                    # Bazen h2 içinde olmayabilir, direkt p'leri alalım
                    
                    paragraphs = target_pane.find_all('p')
                    
                    # Başlıkları filtrele ve sadece yorum metnini al
                    text_parts = []
                    for p in paragraphs:
                        text = clean_text(p.get_text())
                        
                        # Burç özellikleri gibi uzun metinleri atla
                        if 'BURCU ÖZELLİKLERİ' in text or 'Grubun:' in text or 'Şanslı' in text:
                            continue
                        
                        # Başlıkları temizle
                        if text.startswith('Günün Ruh Hali:'):
                            text = text.replace('Günün Ruh Hali:', '').strip()
                        
                        if text and len(text) > 20:
                            text_parts.append(text)
                    
                    if text_parts:
                        full_text = ' '.join(text_parts)
                        results[burc_name]["genel"] = full_text
                        logger.info(f"Twitburc - {burc_name} tamamlandı")
                    else:
                        logger.warning(f"Twitburc - {burc_name} metin bulunamadı")
                else:
                    logger.warning(f"Twitburc - {burc_name} için tab-pane bulunamadı")
                
                random_sleep()
                
            except Exception as e:
                logger.error(f"Twitburc - {burc_name} error: {e}")
                continue
        
        logger.info("Twitburc scrape tamamlandı")
        return results
        
    except Exception as e:
        logger.error(f"Twitburc scraping error: {e}")
        return None


def scrape_vogue() -> Optional[Dict]:
    """Vogue.com.tr'den burç yorumlarını çeker - Günlük burç yorumları sayfasından"""
    logger.info("Vogue scrape başladı...")
    results = create_empty_burc_dict()
    
    try:
        # Bugünkü tarih için URL oluştur
        today = datetime.now()
        date_str = today.strftime("%d-%B-%Y").lower()  # 14-kasim-2025 formatı
        
        # Türkçe ay isimlerine çevir
        ay_map = {
            'january': 'ocak', 'february': 'subat', 'march': 'mart', 'april': 'nisan',
            'may': 'mayis', 'june': 'haziran', 'july': 'temmuz', 'august': 'agustos',
            'september': 'eylul', 'october': 'ekim', 'november': 'kasim', 'december': 'aralik'
        }
        
        for eng, tr in ay_map.items():
            date_str = date_str.replace(eng, tr)
        
        url = f"https://vogue.com.tr/astroloji/gunluk-burc-yorumlari-{date_str}"
        response = requests.get(url, headers=get_random_headers(), timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'lxml')
        
        # category-detail__content div'ini bul
        content_div = soup.select_one('.category-detail__content')
        
        if content_div:
            # Tüm h2 ve p etiketlerini sırayla al
            current_burc = None
            
            for element in content_div.find_all(['h2', 'p']):
                if element.name == 'h2':
                    # Burç ismini bul
                    h2_text = element.get_text(strip=True)
                    
                    # "ve yükselen" kısmını temizle
                    if ' ve yükselen' in h2_text:
                        burc_text = h2_text.split(' ve yükselen')[0].strip()
                    else:
                        burc_text = h2_text
                    
                    # Burç ismini normalize et
                    current_burc = normalize_burc_name(burc_text)
                
                elif element.name == 'p' and current_burc:
                    # Görsel içeren p etiketlerini atla
                    if element.find('img'):
                        continue
                    
                    text = clean_text(element.get_text())
                    
                    if text and len(text) > 20:
                        results[current_burc]["genel"] = text
                        logger.info(f"Vogue - {current_burc} tamamlandı")
                        current_burc = None  # Bir sonraki burca geç
        
        random_sleep()
        logger.info("Vogue scrape tamamlandı")
        return results
        
    except Exception as e:
        logger.error(f"Vogue scraping error: {e}")
        return None


def scrape_gunlukburc() -> Optional[Dict]:
    """Gunlukburc.net'den burç yorumlarını çeker"""
    logger.info("Gunlukburc scrape başladı...")
    results = create_empty_burc_dict()
    
    try:
        for burc_name, slug in BURC_SLUGS.items():
            try:
                url = f"https://www.gunlukburc.net/gunluk-burc-yorumlari/{slug}.html"
                response = requests.get(url, headers=get_random_headers(), timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.content, 'lxml')
                
                # div#agplay içindeki başlıkları ve paragrafları çek
                content_div = soup.select_one('#agplay')
                
                if content_div:
                    yorum_dict = {"genel": None, "aşk": None, "para": None, "sağlık": None}
                    current_category = None
                    
                    # H2 ve p etiketlerini sırayla işle
                    for element in content_div.find_all(['h2', 'p']):
                        if element.name == 'h2':
                            heading_text = clean_text(element.get_text()).lower()
                            
                            # Kategoriyi belirle
                            if 'genel durum' in heading_text:
                                current_category = "genel"
                            elif 'aşk' in heading_text or 'ilişki' in heading_text:  # AND yerine OR
                                current_category = "aşk"
                            elif 'iş' in heading_text or 'kariyer' in heading_text:  # AND yerine OR
                                current_category = "iş"
                            elif 'maddi durum' in heading_text or 'para' in heading_text:
                                current_category = "para"
                            else:
                                current_category = None
                        
                        elif element.name == 'p' and current_category:
                            text = clean_text(element.get_text())
                            text_lower = text.lower()
                            
                            # Tanıtım metinlerini filtrele
                            skip_phrases = [
                                'günlük yıldız falınız',
                                'yıldız falınızı okuyun',
                                'gününe özel',
                                'gezegenler ve yıldızların',
                                'burcu günlük yorumu'
                            ]
                            
                            # Eğer tanıtım metni içeriyorsa atla
                            if any(phrase in text_lower for phrase in skip_phrases):
                                continue
                            
                            # Burç ismi içeren başlık metinlerini atla (örn: "Koç Burcu 17 Kasım...")
                            if any(burc.lower() in text_lower for burc in BURCLAR) and len(text) < 150:
                                continue
                            
                            # Yeterli uzunlukta metinleri al
                            if text and len(text) > 50:
                                # İş ve para kategorilerini birleştir
                                if current_category == "iş":
                                    if yorum_dict["para"]:
                                        yorum_dict["para"] += " " + text
                                    else:
                                        yorum_dict["para"] = text
                                else:
                                    if yorum_dict[current_category]:
                                        yorum_dict[current_category] += " " + text
                                    else:
                                        yorum_dict[current_category] = text
                    
                    results[burc_name] = yorum_dict
                    logger.info(f"Gunlukburc - {burc_name} tamamlandı")
                
                random_sleep()
                
            except Exception as e:
                logger.error(f"Gunlukburc - {burc_name} error: {e}")
                continue
        
        logger.info("Gunlukburc scrape tamamlandı")
        return results
        
    except Exception as e:
        logger.error(f"Gunlukburc scraping error: {e}")
        return None


def scrape_myburc() -> Optional[Dict]:
    """Myburc.com'dan burç yorumlarını çeker"""
    logger.info("Myburc scrape başladı...")
    results = create_empty_burc_dict()
    
    try:
        for burc_name, slug in BURC_SLUGS.items():
            try:
                url = f"https://www.myburc.com/gunluk-burc-yorumu/{slug}-burcu.htm"
                response = requests.get(url, headers=get_random_headers(), timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.content, 'lxml')
                
                yorum_dict = {"genel": None, "aşk": None, "para": None, "sağlık": None}
                
                # Tab içeriklerini çek
                tab_content = soup.select_one('#myTabContent')
                
                if tab_content:
                    # Genel Durum - p.d-block.px-4 class'ına sahip paragrafı al
                    genel_p = soup.select_one('p.d-block.px-4')
                    if genel_p:
                        yorum_dict["genel"] = clean_text(genel_p.get_text())
                    else:
                        # Alternatif: İlk tab içindeki ilk p
                        genel_div = tab_content.select_one('#gununburcu')
                        if not genel_div:
                            genel_div = tab_content.find('div', class_='tab-pane')
                        
                        if genel_div:
                            paragraphs = genel_div.find_all('p')
                            if paragraphs:
                                yorum_dict["genel"] = clean_text(paragraphs[0].get_text())
                    
                    # Aşk falı
                    ask_div = tab_content.select_one('#gununaskfali')
                    if ask_div:
                        paragraphs = ask_div.find_all('p')
                        if paragraphs:
                            yorum_dict["aşk"] = clean_text(paragraphs[0].get_text())
                    
                    # İş & Kariyer falı
                    is_div = tab_content.select_one('#gununisfali')
                    if is_div:
                        paragraphs = is_div.find_all('p')
                        if paragraphs:
                            is_text = clean_text(paragraphs[0].get_text())
                            yorum_dict["para"] = is_text  # İş ve kariyeri para kategorisine ekle
                    
                    # Para falı - İki içeriği birleştir
                    para_div = tab_content.select_one('#gununparafali')
                    if para_div:
                        # Tüm p etiketlerini al ve birleştir
                        paragraphs = para_div.find_all('p')
                        para_texts = []
                        for p in paragraphs:
                            para_text = clean_text(p.get_text())
                            if para_text and len(para_text) > 20:
                                para_texts.append(para_text)
                        
                        if para_texts:
                            combined_para_text = ' '.join(para_texts)
                            # İş falı varsa üzerine ekle, yoksa sadece para falını yaz
                            if yorum_dict["para"]:
                                yorum_dict["para"] += " " + combined_para_text
                            else:
                                yorum_dict["para"] = combined_para_text
                    
                    results[burc_name] = yorum_dict
                    logger.info(f"Myburc - {burc_name} tamamlandı")
                
                random_sleep()
                
            except Exception as e:
                logger.error(f"Myburc - {burc_name} error: {e}")
                continue
        
        logger.info("Myburc scrape tamamlandı")
        return results
        
    except Exception as e:
        logger.error(f"Myburc scraping error: {e}")
        return None

# ANA FONKSİYONLAR

def collect_all_data() -> Dict:
    """Tüm sitelerden veri toplar"""
    logger.info("=" * 60)
    logger.info("Tüm sitelerde scraping başlatılıyor...")
    logger.info("=" * 60)
    
    all_results = {
        "milliyet": scrape_milliyet(),
        "hurriyet": scrape_hurriyet(),
        "haberturk": scrape_haberturk(),
        "elele": scrape_elele(),
        "onedio": scrape_onedio(),
        "mynet": scrape_mynet(),
        "twitburc": scrape_twitburc(),
        "vogue": scrape_vogue(),
        "gunlukburc": scrape_gunlukburc(),
        "myburc": scrape_myburc(),
    }
    
    # None olan siteleri kontrol et
    failed_sites = []
    for site_name, data in all_results.items():
        if data is None:
            logger.error(f"❌ {site_name} için veri alınamadı!")
            failed_sites.append(site_name)
    
    logger.info("=" * 60)
    logger.info("Tüm siteler tamamlandı!")
    logger.info("=" * 60)
    
    if failed_sites:
        logger.warning(f"⚠️  {len(failed_sites)} site başarısız oldu: {', '.join(failed_sites)}")
        logger.warning("Bu siteler için veri eksik olacak!")
    
    return all_results


def save_to_json(data: Dict, output_dir: str = "data"):
    """Verileri JSON dosyasına kaydeder"""
    # None olan siteleri filtrele
    filtered_data = {}
    failed_count = 0
    
    for site_name, site_data in data.items():
        if site_data is None:
            logger.warning(f"⚠️  {site_name} verisi None - dosyaya eklenmeyecek")
            failed_count += 1
        else:
            filtered_data[site_name] = site_data
    
    if not filtered_data:
        raise ValueError("❌ Hiçbir siteden veri alınamadı! Dosya oluşturulmayacak.")
    
    if failed_count > 0:
        logger.warning(f"⚠️  {failed_count} site verisi eksik")
    
    # Klasör yoksa oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"{output_dir} klasörü oluşturuldu")
    
    # Dosya adı: daily_raw_YYYY-MM-DD.json
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"daily_raw_{today}.json"
    filepath = os.path.join(output_dir, filename)
    
    # JSON'a kaydet
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Veriler {filepath} dosyasına kaydedildi")
    logger.info(f"✅ {len(filtered_data)} site verisi kaydedildi")
    
    return filepath


def main():
    """Ana fonksiyon: Tüm işlemleri yönetir"""
    start_time = time.time()
    
    logger.info("AIstrolog Scraper başlatılıyor...")
    logger.info(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Tüm siteleri scrape et
        all_data = collect_all_data()
        
        # JSON'a kaydet
        filepath = save_to_json(all_data)
        
        # İstatistikler
        elapsed = time.time() - start_time
        
        # Başarılı siteleri say (None olmayanlar)
        successful_sites = sum(1 for v in all_data.values() if v is not None)
        failed_sites = sum(1 for v in all_data.values() if v is None)
        
        logger.info("=" * 60)
        logger.info("ÖZET")
        logger.info("=" * 60)
        logger.info(f"Toplam site sayısı: {len(all_data)}")
        logger.info(f"✅ Başarılı siteler: {successful_sites}")
        
        if failed_sites > 0:
            logger.warning(f"❌ Başarısız siteler: {failed_sites}")
        
        logger.info(f"Toplam süre: {elapsed:.2f} saniye")
        logger.info(f"Çıktı dosyası: {filepath}")
        logger.info("=" * 60)
        
        if successful_sites > 0:
            logger.info("✅ Scraping işlemi tamamlandı!")
        else:
            logger.error("❌ Scraping tamamen başarısız oldu!")
            raise ValueError("Hiçbir siteden veri alınamadı!")
        
    except Exception as e:
        logger.error(f"Ana işlem sırasında hata: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

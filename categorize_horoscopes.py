"""
Burç Yorumu Kategorizasyon Sistemi

Ham burç yorumu JSON verisini işleyerek "genel" anahtarındaki metni analiz eder.
Aşk, para ve sağlık konularına dair cümleleri tespit edip ilgili kategorilere kopyalar.
"""

import json
import re
from datetime import datetime
from pathlib import Path


class HoroscopeCategorizer:
    """Burç yorumlarını kategorilere ayıran sınıf"""

    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002700-\U000027BF"
        "\U0001F900-\U0001F9FF"
        "\U00002600-\U000026FF"
        "\U00002B00-\U00002BFF"
        "]+",
        flags=re.UNICODE
    )

    def remove_emojis(self, text: str) -> str:
        return self.EMOJI_PATTERN.sub("", text)

    
    LOVE_KEYWORDS = {
        'aşk', 'sevgi', 'sevgili', 'partner', 'flört', 'ilişki', 'kalp',
        'duygular', 'itiraf', 'buluşma', 'evlilik', 'romantik', 'tutku',
        'şehvet', 'çift', 'eş', 'bekar', 'çekim', 'ayrılık', 'birlikte'
    }
    
    MONEY_KEYWORDS = {
        'para', 'maddi', 'harcama', 'birik', 'yatır', 'kazanç', 'kazan',
        'finans', 'finansal', 'maaş', 'bütçe', 'gelir', 'gider', 'borç',
        'ödeme', 'ekonomik', 'mali', 'hesap', 'kredi', 'kar', 'zarar',
        'ticaret', 'alım', 'satım', 'tasarruf', 'ücret', 'kariyer', 'iş',
        'proje', 'görev', 'fırsat', 'terfi', 'yatırım'
    }
    
    HEALTH_KEYWORDS = {
        'sağlık', 'sağlık', 'hastalık', 'egzersiz', 'spor', 'beslen', 'uyku',
        'stres', 'enerji', 'yorgunluk', 'fiziksel', 'ruhsal', 'zihin', 'rahatla',
        'dinlen', 'yorgun', 'sağlam', 'dinç', 'aktivite', 'hareket', 'gevşe',
        'meditasyon', 'nefes', 'beden', 'vücut', 'form', 'kondisyon', 'hastalık',
        'ağrı', 'acı', 'doktor', 'boyun', 'omuz', 'bel', 'mide', 'kas', 'eklem', 'diz',
        'zihinsel'
    }
    
    
    def __init__(self, input_file: str, output_file: str = None):
        from TurkishStemmer import TurkishStemmer
        self.stemmer = TurkishStemmer()

        # Keywordleri köke çeviriyoruz (bir kez)
        self.LOVE_STEMS = {self.stemmer.stem(x) for x in self.LOVE_KEYWORDS}
        self.MONEY_STEMS = {self.stemmer.stem(x) for x in self.MONEY_KEYWORDS}
        self.HEALTH_STEMS = {self.stemmer.stem(x) for x in self.HEALTH_KEYWORDS}

        # PHRASES (sadece tek kelimeyle yakalanamayanlar)
        self.LOVE_PHRASES = [
            "duygusal bağ",
            "duygusal bağlanma",
            "duygusal yakınlık",
            "duygusal destek",
            "duygusal bir konuşma",
            "duygusal bir buluşma",
            "ilişki adımı",
            "ilişkide adım"
        ]
        self.MONEY_PHRASES = [
            "ek gelir",
            "ek kazanç",
            "gelir artışı",
            "iş fırsatı",
            "kariyer fırsatı",
            "iş kurmak"
        ]
        self.HEALTH_PHRASES = [
            "dikkat et",
            "soğuk algınlığı",
            "baş ağrısı",
            "ruh sağlığı",
            "zihinsel yorgunluk",
            "zihinsel olarak",
            "psikolojik olarak",
            "fiziksel yorgunluk"
        ]


        self.input_file = Path(input_file)
        
        if output_file:
            self.output_file = Path(output_file)
        else:
            self.output_file = self.input_file.parent / f"processed_{self.input_file.name}"
    
    def split_into_sentences(self, text: str) -> list:
        """Metni cümlelere ayırır"""
        if not text or text == "null" or text is None:
            return []
        
        sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s+'
        sentences = re.split(sentence_pattern, text)
        
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()

            sentence = self.remove_emojis(sentence)

            if sentence and len(sentence) > 10:
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def stem_sentence(self, sentence: str) -> set:
        """Cümledeki tüm kelimeleri köklerine indirger ve set döner."""
        words = re.findall(r'\b\w+\b', sentence.lower())
        return {self.stemmer.stem(w) for w in words}
    
    def categorize_sentence(self, sentence: str) -> dict:
        """Bir cümleyi PHRASE ve kök tabanlı olarak kategorize eder."""

        sentence_lower = sentence.lower()
    
        # Önce PHRASE kontrolü (öncelikli)
        for phrase in self.LOVE_PHRASES:
            if phrase in sentence_lower:
                return {'love': True, 'money': False, 'health': False}

        for phrase in self.MONEY_PHRASES:
            if phrase in sentence_lower:
                return {'love': False, 'money': True, 'health': False}

        for phrase in self.HEALTH_PHRASES:
            if phrase in sentence_lower:
                return {'love': False, 'money': False, 'health': True}

        # Kök tabanlı kontrol
        sent_stems = self.stem_sentence(sentence)
        
        return {
            'love': len(self.LOVE_STEMS & sent_stems) > 0,
            'money': len(self.MONEY_STEMS & sent_stems) > 0,
            'health': len(self.HEALTH_STEMS & sent_stems) > 0
        }
    
    def process_horoscope(self, horoscope_data: dict) -> dict:
        """Bir burç verisini işler ve kategorize eder"""
        result = horoscope_data.copy()
        
        genel_text = horoscope_data.get('genel', '')
        
        if not genel_text or genel_text == 'null' or genel_text is None:
            return result
        
        sentences = self.split_into_sentences(genel_text)
        
        love_sentences = []
        money_sentences = []
        health_sentences = []
        
        for sentence in sentences:
            categories = self.categorize_sentence(sentence)
            
            if categories['love']:
                love_sentences.append(sentence)
            
            if categories['money']:
                money_sentences.append(sentence)
            
            if categories['health']:
                health_sentences.append(sentence)
        
        if love_sentences:
            result['aşk'] = ' '.join(love_sentences)
        
        if money_sentences:
            result['para'] = ' '.join(money_sentences)
        
        if health_sentences:
            result['sağlık'] = ' '.join(health_sentences)
        
        return result
    
    def process_file(self) -> dict:
        """JSON dosyasını yükler, tüm burçları işler ve sonucu kaydeder"""
        print(f"Dosya okunuyor: {self.input_file}")
        
        # Dosya varlığını kontrol et
        if not self.input_file.exists():
            raise FileNotFoundError(
                f"Gerekli dosya bulunamadı: {self.input_file}\n"
                f"Lütfen önce scraper.py çalıştırılarak veri çekildiğinden emin olun."
            )
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        stats = {
            'total_sources': 0,
            'total_signs': 0,
            'categorized': {'love': 0, 'money': 0, 'health': 0}
        }
        
        for source_name, source_data in data.items():
            stats['total_sources'] += 1
            print(f"\nİşleniyor: {source_name}")
            
            for sign_name, sign_data in source_data.items():
                stats['total_signs'] += 1
                
                processed_data = self.process_horoscope(sign_data)
                
                if processed_data.get('aşk') and processed_data['aşk'] != 'null':
                    stats['categorized']['love'] += 1
                if processed_data.get('para') and processed_data['para'] != 'null':
                    stats['categorized']['money'] += 1
                if processed_data.get('sağlık') and processed_data['sağlık'] != 'null':
                    stats['categorized']['health'] += 1
                
                data[source_name][sign_name] = processed_data
        
        print(f"\nSonuç kaydediliyor: {self.output_file}")
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("\n" + "="*50)
        print("İşleme İstatistikleri")
        print("="*50)
        print(f"Toplam Kaynak: {stats['total_sources']}")
        print(f"Toplam Burç: {stats['total_signs']}")
        print(f"\nKategorize Edilen:")
        print(f"  Aşk: {stats['categorized']['love']}")
        print(f"  Para: {stats['categorized']['money']}")
        print(f"  Sağlık: {stats['categorized']['health']}")
        print("="*50)
        
        return data


def main():
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        today = datetime.now().strftime('%Y-%m-%d')
        input_file = f"data/daily_raw_{today}.json"
    
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    categorizer = HoroscopeCategorizer(input_file, output_file)
    categorizer.process_file()
    
    print(f"\nİşlem tamamlandı!")
    print(f"Çıktı dosyası: {categorizer.output_file}")


if __name__ == "__main__":
    main()

"""
Workflow Test Sistemi

Scraping ve kategorizasyon sürecinin doğru çalışıp çalışmadığını test eder.
Default/sahte veri kullanımını tespit eder.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys


class WorkflowValidator:
    """Pipeline'ın doğru çalışıp çalışmadığını test eder"""
    
    def __init__(self, raw_file: str, processed_file: str):
        self.raw_file = Path(raw_file)
        self.processed_file = Path(processed_file)
        self.errors = []
        self.warnings = []
        self.stats = defaultdict(int)
        
    def load_data(self):
        """Dosyaları yükle"""
        if not self.raw_file.exists():
            self.errors.append(f"Ham dosya bulunamadı: {self.raw_file}")
            return False
        
        if not self.processed_file.exists():
            self.errors.append(f"İşlenmiş dosya bulunamadı: {self.processed_file}")
            return False
        
        try:
            with open(self.raw_file, 'r', encoding='utf-8') as f:
                self.raw_data = json.load(f)
            
            with open(self.processed_file, 'r', encoding='utf-8') as f:
                self.processed_data = json.load(f)
            
            return True
        except Exception as e:
            self.errors.append(f"Dosya yükleme hatası: {e}")
            return False
    
    def test_duplicate_content(self):
        """Aynı içeriğin birden fazla burçta/kaynakta kullanıldığını tespit et"""
        print("\n[1] Test: Duplike Icerik Kontrolu")
        print("-" * 80)
        
        content_map = defaultdict(list)
        
        for source_name, source_data in self.raw_data.items():
            for sign_name, sign_data in source_data.items():
                genel = sign_data.get('genel', '')
                if genel and genel.strip():
                    content_map[genel].append(f"{source_name}/{sign_name}")
        
        duplicates_found = False
        for content, locations in content_map.items():
            if len(locations) > 1:
                duplicates_found = True
                self.warnings.append(
                    f"Duplike içerik tespit edildi ({len(locations)} yerde): {content[:60]}..."
                )
                print(f"[X] Duplike: '{content[:60]}...'")
                print(f"   Kullanildigi yerler: {', '.join(locations[:5])}")
                if len(locations) > 5:
                    print(f"   ... ve {len(locations) - 5} yer daha")
        
        if not duplicates_found:
            print("[OK] Duplike icerik bulunamadi - her burc icin farkli veri var")
            self.stats['no_duplicates'] = True
        else:
            print(f"\n[!] {len([v for v in content_map.values() if len(v) > 1])} farkli duplike icerik bulundu")
            self.stats['duplicates'] = len([v for v in content_map.values() if len(v) > 1])
    
    def test_generic_content(self):
        """Generic/test içerik tespit et"""
        print("\n[2] Test: Generic/Test Icerik Kontrolu")
        print("-" * 80)
        
        # Şüpheli patternler
        generic_patterns = [
            "sakin ve üretken bir gün",
            "iç sesinizi dinleyin",
            "önemli gelişmeler yaşayabilirsiniz",
            "dikkatli olun, planlı hareket",
            "kendinize zaman ayırın",
            "test data",
            "örnek veri",
            "lorem ipsum"
        ]
        
        generic_found = False
        for source_name, source_data in self.raw_data.items():
            source_generics = 0
            for sign_name, sign_data in source_data.items():
                genel = (sign_data.get('genel') or '').lower()
                ask = (sign_data.get('aşk') or '').lower()
                para = (sign_data.get('para') or '').lower()
                saglik = (sign_data.get('sağlık') or '').lower()
                
                all_content = f"{genel} {ask} {para} {saglik}"
                
                for pattern in generic_patterns:
                    if pattern in all_content:
                        generic_found = True
                        source_generics += 1
                        self.warnings.append(
                            f"Generic pattern tespit edildi: '{pattern}' - {source_name}/{sign_name}"
                        )
                        break
            
            if source_generics > 0:
                print(f"[X] {source_name}: {source_generics} burcta generic icerik bulundu")
        
        if not generic_found:
            print("[OK] Generic/test icerik bulunamadi")
            self.stats['no_generic'] = True
        else:
            print(f"\n[!] Generic icerik bulundu - gercek veri cekilmemis olabilir")
    
    def test_empty_content(self):
        """Boş içerikleri tespit et"""
        print("\n[3] Test: Bos Icerik Kontrolu")
        print("-" * 80)
        
        empty_count = 0
        for source_name, source_data in self.raw_data.items():
            source_empty = 0
            for sign_name, sign_data in source_data.items():
                genel = sign_data.get('genel')
                if not genel or genel == 'null' or len(genel.strip()) < 20:
                    source_empty += 1
                    empty_count += 1
            
            if source_empty > 0:
                print(f"[!] {source_name}: {source_empty}/12 burcta bos/cok kisa icerik")
                self.warnings.append(f"{source_name} için {source_empty} burçta içerik eksik")
        
        if empty_count == 0:
            print("[OK] Tum burclar icin icerik mevcut")
            self.stats['no_empty'] = True
        else:
            total = len(self.raw_data) * 12
            print(f"\n[!] Toplam {empty_count}/{total} burcta bos icerik var")
    
    def test_categorization_quality(self):
        """Kategorizasyon kalitesini test et"""
        print("\n[4] Test: Kategorizasyon Kalitesi")
        print("-" * 80)
        
        total_signs = 0
        categorized = {'aşk': 0, 'para': 0, 'sağlık': 0}
        
        for source_name, source_data in self.processed_data.items():
            for sign_name, sign_data in source_data.items():
                total_signs += 1
                
                if sign_data.get('aşk') and sign_data['aşk'] != 'null':
                    categorized['aşk'] += 1
                if sign_data.get('para') and sign_data['para'] != 'null':
                    categorized['para'] += 1
                if sign_data.get('sağlık') and sign_data['sağlık'] != 'null':
                    categorized['sağlık'] += 1
        
        print(f"Toplam burç: {total_signs}")
        print(f"Aşk kategorisi: {categorized['aşk']}/{total_signs} ({categorized['aşk']/total_signs*100:.1f}%)")
        print(f"Para kategorisi: {categorized['para']}/{total_signs} ({categorized['para']/total_signs*100:.1f}%)")
        print(f"Sağlık kategorisi: {categorized['sağlık']}/{total_signs} ({categorized['sağlık']/total_signs*100:.1f}%)")
        
        # Eğer kategorize oranı çok düşükse uyar
        avg_rate = sum(categorized.values()) / (3 * total_signs) * 100
        
        if avg_rate < 30:
            print(f"\n[X] Kategorizasyon orani cok dusuk ({avg_rate:.1f}%)")
            self.errors.append("Kategorizasyon başarısız - çoğu içerik kategorize edilemedi")
        elif avg_rate < 60:
            print(f"\n[!] Kategorizasyon orani dusuk ({avg_rate:.1f}%)")
            self.warnings.append("Kategorizasyon iyileştirilebilir")
        else:
            print(f"\n[OK] Kategorizasyon orani yeterli ({avg_rate:.1f}%)")
            self.stats['good_categorization'] = True
        
        self.stats['categorization_rate'] = avg_rate
    
    def test_data_freshness(self):
        """Verinin güncel olup olmadığını test et"""
        print("\n[5] Test: Veri Guncelligi")
        print("-" * 80)
        
        # Dosya adından tarihi çıkar
        try:
            filename = self.raw_file.name
            if 'daily_raw_' in filename:
                date_str = filename.replace('daily_raw_', '').replace('.json', '')
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                today = datetime.now()
                
                days_old = (today - file_date).days
                
                if days_old == 0:
                    print(f"[OK] Veri bugune ait ({file_date.strftime('%Y-%m-%d')})")
                    self.stats['fresh_data'] = True
                elif days_old == 1:
                    print(f"[!] Veri dun ({file_date.strftime('%Y-%m-%d')})")
                else:
                    print(f"[!] Veri {days_old} gun once ({file_date.strftime('%Y-%m-%d')})")
                    self.warnings.append(f"Veri {days_old} gün eski")
            else:
                print("[i] Dosya adindan tarih belirlenemiyor")
        except Exception as e:
            print(f"[i] Tarih kontrolu yapilamadi: {e}")
    
    def test_category_content_similarity(self):
        """Kategori içeriklerinin birbirinden farklı olup olmadığını test et"""
        print("\n[6] Test: Kategori Icerik Benzersizligi")
        print("-" * 80)
        
        identical_categories = 0
        
        for source_name, source_data in self.processed_data.items():
            for sign_name, sign_data in source_data.items():
                ask = sign_data.get('aşk', '')
                para = sign_data.get('para', '')
                saglik = sign_data.get('sağlık', '')
                
                # Eğer tüm kategoriler aynı metinse sorun var
                if ask and para and saglik:
                    if ask == para == saglik:
                        identical_categories += 1
                        self.warnings.append(
                            f"{source_name}/{sign_name} için tüm kategoriler aynı"
                        )
        
        if identical_categories == 0:
            print("[OK] Tum kategoriler birbirinden farkli icerik iceriyor")
            self.stats['unique_categories'] = True
        else:
            print(f"[X] {identical_categories} burcta tum kategoriler ayni icerik")
    
    def run_all_tests(self):
        """Tüm testleri çalıştır"""
        print("=" * 80)
        print("WORKFLOW TEST BASLIYOR")
        print("=" * 80)
        print(f"Ham dosya: {self.raw_file}")
        print(f"Islenmiş dosya: {self.processed_file}")
        
        if not self.load_data():
            print("\n[X] Dosyalar yuklenmedi!")
            return False
        
        # Testleri çalıştır
        self.test_duplicate_content()
        self.test_generic_content()
        self.test_empty_content()
        self.test_categorization_quality()
        self.test_data_freshness()
        self.test_category_content_similarity()
        
        # Sonuçları göster
        print("\n" + "=" * 80)
        print("TEST SONUCLARI")
        print("=" * 80)
        
        if self.errors:
            print(f"\n[X] Hatalar ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print(f"\n[!] Uyarilar ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # İlk 10 uyarı
                print(f"  - {warning}")
            if len(self.warnings) > 10:
                print(f"  ... ve {len(self.warnings) - 10} uyari daha")
        
        # Genel durum
        print("\n" + "=" * 80)
        passed_tests = sum(1 for v in self.stats.values() if v is True)
        
        if self.errors:
            print("[X] TEST BASARISIZ - Kritik hatalar var!")
            return False
        elif len(self.warnings) > 10:
            print("[!] TEST KISMEN BASARILI - Cok sayida uyari var")
            return False
        else:
            print("[OK] TEST BASARILI - Workflow duzgun calisiyor!")
            return True


def main():
    if len(sys.argv) < 3:
        print("Kullanım: python test_workflow.py <raw_file> <processed_file>")
        print("\nÖrnek:")
        print("  python test_workflow.py data/daily_raw_2025-11-15.json data/processed_daily_raw_2025-11-15.json")
        return
    
    raw_file = sys.argv[1]
    processed_file = sys.argv[2]
    
    validator = WorkflowValidator(raw_file, processed_file)
    success = validator.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

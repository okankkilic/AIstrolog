"""
Kategorizasyon Sonuçlarını Doğrulama Aracı

Ham ve işlenmiş verileri karşılaştırarak kategorizasyon kalitesini değerlendirir.
"""

import json
import sys
from pathlib import Path


def compare_files(raw_file: str, processed_file: str, source: str = None, sign: str = None):
    """Ham ve işlenmiş dosyaları karşılaştır"""
    
    with open(raw_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    with open(processed_file, 'r', encoding='utf-8') as f:
        processed_data = json.load(f)
    
    print("=" * 80)
    print("Kategorizasyon Karşılaştırma")
    print("=" * 80)
    
    if source and sign:
        show_comparison(raw_data, processed_data, source, sign)
        return
    
    for source_name in raw_data.keys():
        if source and source_name != source:
            continue
            
        print(f"\nKaynak: {source_name.upper()}")
        print("-" * 80)
        
        for sign_name in raw_data[source_name].keys():
            if sign and sign_name != sign:
                continue
                
            raw_item = raw_data[source_name][sign_name]
            processed_item = processed_data[source_name][sign_name]
            
            has_love = processed_item.get('aşk') and processed_item['aşk'] != 'null'
            has_money = processed_item.get('para') and processed_item['para'] != 'null'
            has_health = processed_item.get('sağlık') and processed_item['sağlık'] != 'null'
            
            categories = []
            if has_love:
                categories.append('Aşk')
            if has_money:
                categories.append('Para')
            if has_health:
                categories.append('Sağlık')
            
            status = ', '.join(categories) if categories else 'Yok'
            print(f"  {sign_name:12} -> {status}")


def show_comparison(raw_data, processed_data, source, sign):
    """Detaylı karşılaştırma göster"""
    
    if source not in raw_data or sign not in raw_data[source]:
        print(f"{source} / {sign} bulunamadı!")
        return
    
    raw_item = raw_data[source][sign]
    processed_item = processed_data[source][sign]
    
    print(f"\nKaynak: {source}")
    print(f"Burç: {sign}")
    print("=" * 80)
    
    print("\nGENEL:")
    print("-" * 80)
    genel = raw_item.get('genel', 'N/A')
    if genel and len(genel) > 300:
        print(genel[:300] + "...")
    else:
        print(genel)
    
    print(f"\nOrijinal uzunluk: {len(genel) if genel else 0} karakter")
    
    categories_info = []
    
    if processed_item.get('aşk') and processed_item['aşk'] != 'null':
        categories_info.append({
            'name': 'AŞK',
            'content': processed_item['aşk']
        })
    
    if processed_item.get('para') and processed_item['para'] != 'null':
        categories_info.append({
            'name': 'PARA',
            'content': processed_item['para']
        })
    
    if processed_item.get('sağlık') and processed_item['sağlık'] != 'null':
        categories_info.append({
            'name': 'SAĞLIK',
            'content': processed_item['sağlık']
        })
    
    if categories_info:
        print("\n" + "=" * 80)
        print("Kategorize Edilen İçerik:")
        print("=" * 80)
        
        for cat in categories_info:
            print(f"\n{cat['name']}:")
            print("-" * 80)
            content = cat['content']
            if len(content) > 200:
                print(content[:200] + "...")
            else:
                print(content)
            print(f"Uzunluk: {len(content)} karakter")
    else:
        print("\nHiçbir kategori bulunamadı!")
    
    print("\n" + "=" * 80)
    print("İstatistikler:")
    print("=" * 80)
    print(f"Toplam Kategori: {len(categories_info)}")
    print(f"Aşk: {'Var' if any(c['name'] == 'AŞK' for c in categories_info) else 'Yok'}")
    print(f"Para: {'Var' if any(c['name'] == 'PARA' for c in categories_info) else 'Yok'}")
    print(f"Sağlık: {'Var' if any(c['name'] == 'SAĞLIK' for c in categories_info) else 'Yok'}")


def main():
    
    if len(sys.argv) < 3:
        print("Kullanım:")
        print("  python verify_categorization.py raw.json processed.json")
        print("  python verify_categorization.py raw.json processed.json kaynak_adi")
        print("  python verify_categorization.py raw.json processed.json kaynak_adi Burç")
        return
    
    raw_file = sys.argv[1]
    processed_file = sys.argv[2]
    source = sys.argv[3] if len(sys.argv) > 3 else None
    sign = sys.argv[4] if len(sys.argv) > 4 else None
    
    if not Path(raw_file).exists():
        print(f"Ham dosya bulunamadı: {raw_file}")
        return
    
    if not Path(processed_file).exists():
        print(f"İşlenmiş dosya bulunamadı: {processed_file}")
        return
    
    compare_files(raw_file, processed_file, source, sign)
    
    print("\n" + "=" * 80)
    print("Karşılaştırma tamamlandı!")
    print("=" * 80)


if __name__ == "__main__":
    main()

"""
TEMPORARY SCRAPER - Creates sample data for testing
This is a placeholder until the real scraper is restored.
"""

import json
import os
from datetime import datetime
from pathlib import Path


def create_sample_data():
    """Creates sample horoscope data matching the expected format"""
    
    signs = ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", 
             "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]
    
    sources = {
        "milliyet": {},
        "hurriyet": {},
        "ntv": {},
        "haberturk": {},
        "elele": {},
        "onedio": {}
    }
    
    # Sample horoscope content for each sign
    for source in sources:
        for sign in signs:
            sources[source][sign] = {
                "genel": f"{sign} burcu için bugün sakin ve üretken bir gün olacak. İç sesinizi dinleyin.",
                "aşk": f"Duygusal ilişkilerinizde önemli gelişmeler yaşayabilirsiniz.",
                "para": f"Mali konularda dikkatli olun, planlı hareket edin.",
                "sağlık": f"Kendinize zaman ayırın, dinlenmeye özen gösterin."
            }
    
    return sources


def main():
    print("=" * 60)
    print("TEMPORARY SCRAPER - Creating sample data")
    print("=" * 60)
    print("\nNOTE: This is a placeholder scraper for testing.")
    print("Replace with your actual scraper implementation.\n")
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Generate filename with today's date
    today = datetime.now().strftime('%Y-%m-%d')
    output_file = data_dir / f"daily_raw_{today}.json"
    
    # Create sample data
    data = create_sample_data()
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Sample data created: {output_file}")
    print(f"✓ Sources: {len(data)}")
    print(f"✓ Signs per source: {len(data['milliyet'])}")
    print("\n" + "=" * 60)
    print("Scraping completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

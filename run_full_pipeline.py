"""
Complete Pipeline: Scrape → Categorize → Summarize → Score → Rank
==================================================================

This script runs the complete horoscope data pipeline:
1. Scrapes data from 11 sources
2. Categorizes into love, money, health
3. Summarizes predictions from all sources
4. Scores predictions with sentiment analysis
5. Creates rankings and updates history
6. Tests the workflow
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, check=True, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(e.output)
        return False

def main():
    """Run complete pipeline."""
    print("🌟 Complete Horoscope Data Pipeline")
    print("="*60)
    print("Steps: Scrape → Categorize → Summarize → Score → Rank → Test")
    print("="*60)
    
    # Get today's date for filenames
    today = datetime.now().strftime('%Y-%m-%d')
    
    raw_file = f"data/daily_raw_{today}.json"
    processed_file = f"data/processed_daily_raw_{today}.json"
    summary_file = f"data/summarized_processed_daily_raw_{today}.json"
    scored_file = f"data/scored_processed_daily_raw_{today}.json"
    
    # Step 1: Scrape
    if not run_command("python scraper.py", "STEP 1: Scraping horoscope data"):
        print("\n❌ Scraping failed!")
        return 1
    
    # Check if raw file exists
    if not os.path.exists(raw_file):
        print(f"\n❌ Expected file not found: {raw_file}")
        return 1
    
    # Step 2: Categorize
    if not run_command(f"python categorize_horoscopes.py {raw_file}", "STEP 2: Categorizing predictions"):
        print("\n❌ Categorization failed!")
        return 1
    
    # Check if processed file exists
    if not os.path.exists(processed_file):
        print(f"\n❌ Expected file not found: {processed_file}")
        return 1
    
    # Step 3: Summarize
    if not run_command(f"python summarizer.py {processed_file} {summary_file}", "STEP 3: Summarizing predictions"):
        print("\n❌ Summarization failed!")
        return 1
    
    # Check if summary file exists
    if not os.path.exists(summary_file):
        print(f"\n❌ Expected file not found: {summary_file}")
        return 1
    
    # Step 4: Score
    if not run_command(f"python scorer.py {processed_file}", "STEP 4: Scoring predictions"):
        print("\n❌ Scoring failed!")
        return 1
    
    # Check if scored file exists
    if not os.path.exists(scored_file):
        print(f"\n❌ Expected file not found: {scored_file}")
        return 1
    
    # Step 5: Rank
    if not run_command(f"python ranker.py {scored_file}", "STEP 5: Creating rankings"):
        print("\n❌ Ranking failed!")
        return 1
    
    # Step 6: Test (optional)
    print(f"\n{'='*60}")
    print("✅ STEP 4: Testing workflow (optional)")
    print('='*60)
    
    run_test = input("Run workflow tests? (y/n): ").lower().strip() == 'y'
    
    if run_test:
        run_command(f"python test_workflow.py {raw_file} {processed_file}", "Running tests")
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 PIPELINE COMPLETE!")
    print("="*60)
    print(f"\n📁 Generated files:")
    print(f"   Raw data:        {raw_file}")
    print(f"   Categorized:     {processed_file}")
    print(f"   Summarized:      {summary_file}")
    print(f"   Scored:          {scored_file}")
    print(f"   Rankings:        data/rankings_history.json")
    
    # Show file sizes
    if os.path.exists(raw_file):
        size = os.path.getsize(raw_file) / 1024
        print(f"\n📊 File sizes:")
        print(f"   Raw:         {size:.1f} KB")
    
    if os.path.exists(processed_file):
        size = os.path.getsize(processed_file) / 1024
        print(f"   Categorized: {size:.1f} KB")
    
    if os.path.exists(summary_file):
        size = os.path.getsize(summary_file) / 1024
        print(f"   Summarized:  {size:.1f} KB")
    
    if os.path.exists(scored_file):
        size = os.path.getsize(scored_file) / 1024
        print(f"   Scored:      {size:.1f} KB")
    
    print("\n✨ All done! Your horoscope data is ready to use.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

"""
Turkish Horoscope Summarization System
======================================

This module provides ML-based text summarization for Turkish horoscope predictions.
It combines multiple predictions from different sources into coherent summaries.

Approaches:
1. Extractive Summarization (traditional)
2. Abstractive Summarization (transformer-based)
3. Hybrid approach (recommended)
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TurkishHoroscopeSummarizer:
    """
    Summarizes Turkish horoscope predictions from multiple sources.
    
    Features:
    - Handles null/empty values gracefully
    - Removes duplicate or highly similar content
    - Generates coherent summaries per category
    - Turkish language-aware processing
    """
    
    # Turkish stopwords and common horoscope phrases
    TURKISH_STOPWORDS = {
        've', 'bir', 'bu', 'için', 'ile', 'daha', 'çok', 'gibi', 'ya', 'da',
        'ancak', 'ama', 'fakat', 'veya', 'hem', 'de', 'ki', 'olan', 'olarak'
    }
    
    # Category keywords for validation
    CATEGORY_KEYWORDS = {
        'aşk': ['aşk', 'sevgi', 'partner', 'flört', 'ilişki', 'kalp', 'duygusal', 'evlilik', 'romantik'],
        'para': ['para', 'maddi', 'harcama', 'birikim', 'yatırım', 'kazanç', 'finans', 'maaş', 'gelir'],
        'sağlık': ['sağlık', 'enerji', 'stres', 'egzersiz', 'spor', 'beslenme', 'uyku', 'yorgun', 'dinlen']
    }
    
    def __init__(self, similarity_threshold: float = 0.7):
        """
        Initialize the summarizer.
        
        Args:
            similarity_threshold: Threshold for considering sentences as duplicates (0.0-1.0)
        """
        self.similarity_threshold = similarity_threshold
        
    def load_data(self, json_path: str) -> Dict:
        """Load horoscope data from JSON file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"✅ Loaded data from {json_path}")
            return data
        except Exception as e:
            logger.error(f"❌ Error loading {json_path}: {e}")
            raise
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common prefixes from sources
        prefixes_to_remove = [
            r'Aygül Aydın.*?burç yorumları;?\s*',
            r'Günlük burç yorumları.*?;?\s*',
            r'Burç yorumu.*?:?\s*',
            r'Uzman Astrolog\s*'
        ]
        for prefix in prefixes_to_remove:
            text = re.sub(prefix, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def remove_discourse_marker(self, text: str) -> str:
        """Remove sentence-initial discourse markers that don't work standalone."""
        if not text:
            return ""
        
        discourse_markers = [
            r'^Ayrıca,?\s+',
            r'^Aynı zamanda,?\s+',
            r'^Bunun yanında,?\s+',
            r'^Bunun yanı sıra,?\s+',
            r'^Öte yandan,?\s+',
            r'^Diğer yandan,?\s+',
            r'^Bununla birlikte,?\s+',
            r'^Ancak,?\s+',
            r'^Fakat,?\s+',
            r'^Ama,?\s+',
            r'^Aslında,?\s+',
            r'^Dahası,?\s+',
            r'^Hatta,?\s+'
        ]
        
        for marker in discourse_markers:
            text = re.sub(marker, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def split_sentences(self, text: str) -> List[str]:
        """Split text into sentences (Turkish-aware)."""
        if not text:
            return []
        
        # Simple sentence splitting for Turkish
        sentences = re.split(r'[.!?]+\s+', text)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for s in sentences:
            s = s.strip()
            # Remove leading punctuation (commas, etc.)
            s = re.sub(r'^[,;:\s]+', '', s)
            # Only keep if still has content
            if s:
                cleaned_sentences.append(s)
        
        return cleaned_sentences
    
    def calculate_sentence_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate similarity between two sentences using word overlap.
        Returns value between 0.0 (no similarity) and 1.0 (identical).
        """
        if not sent1 or not sent2:
            return 0.0
        
        # Normalize and tokenize
        words1 = set(sent1.lower().split()) - self.TURKISH_STOPWORDS
        words2 = set(sent2.lower().split()) - self.TURKISH_STOPWORDS
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def remove_duplicate_sentences(self, sentences: List[str]) -> List[str]:
        """Remove duplicate or highly similar sentences."""
        if not sentences:
            return []
        
        unique_sentences = []
        
        for sentence in sentences:
            is_duplicate = False
            for existing in unique_sentences:
                similarity = self.calculate_sentence_similarity(sentence, existing)
                if similarity > self.similarity_threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_sentences.append(sentence)
        
        return unique_sentences
    
    def score_sentence_importance(self, sentence: str, category: str) -> float:
        """
        Score sentence importance for a given category.
        Higher score = more relevant to category.
        """
        sentence_lower = sentence.lower()
        score = 0.0
        
        # Check for category-specific keywords
        if category in self.CATEGORY_KEYWORDS:
            for keyword in self.CATEGORY_KEYWORDS[category]:
                if keyword in sentence_lower:
                    score += 1.0
        
        return score
    
    def extract_top_sentences(self, sentences: List[str], category: str, max_sentences: int = 3) -> List[str]:
        """Extract top N most important sentences for a category."""
        if not sentences:
            return []
        
        # Score each sentence
        scored_sentences = [
            (sent, self.score_sentence_importance(sent, category))
            for sent in sentences
        ]
        
        # Sort by score (descending)
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        # Get top sentences
        top_sentences = [sent for sent, score in scored_sentences[:max_sentences]]
        
        return top_sentences
    
    def summarize_category(self, 
                          zodiac_sign: str, 
                          category: str, 
                          source_data: Dict[str, Dict]) -> str:
        """
        Summarize predictions for a specific zodiac sign and category.
        
        Args:
            zodiac_sign: e.g., "Koç", "Boğa", etc.
            category: "aşk", "para", "sağlık", or "genel"
            source_data: Dictionary of all sources and their predictions
        
        Returns:
            Summarized text combining insights from all sources
        """
        all_sentences = []
        
        # Collect sentences from all sources
        for source_name, source_content in source_data.items():
            if zodiac_sign not in source_content:
                continue
            
            zodiac_data = source_content[zodiac_sign]
            
            # Get text for this category
            text = zodiac_data.get(category)
            
            # Skip null/empty values
            if not text or text == "null":
                continue
            
            # Clean and split into sentences
            clean = self.clean_text(text)
            sentences = self.split_sentences(clean)
            all_sentences.extend(sentences)
        
        if not all_sentences:
            return None
        
        # Remove duplicates
        unique_sentences = self.remove_duplicate_sentences(all_sentences)
        
        if not unique_sentences:
            return None
        
        # For general category, take more sentences
        max_sentences = 4 if category == 'genel' else 3
        
        # Extract top sentences
        top_sentences = self.extract_top_sentences(unique_sentences, category, max_sentences)
        
        if not top_sentences:
            return None
        
        # Join into coherent summary - ensure proper punctuation
        # Add period to sentences that don't end with punctuation
        # Capitalize first letter of each sentence
        # Remove discourse markers ONLY from first sentence
        formatted_sentences = []
        for i, sentence in enumerate(top_sentences):
            sentence = sentence.strip()
            if sentence:
                # Remove discourse marker from FIRST sentence only
                if i == 0:
                    sentence = self.remove_discourse_marker(sentence)
                    if not sentence:  # If entire sentence was just a marker, skip
                        continue
                
                # Capitalize first letter
                sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
                # Add period if missing
                if not sentence[-1] in '.!?':
                    sentence += '.'
                formatted_sentences.append(sentence)
        
        summary = ' '.join(formatted_sentences)
        
        return summary
    
    def summarize_all(self, data: Dict, output_path: Optional[str] = None) -> Dict:
        """
        Generate summaries for all zodiac signs and categories.
        
        Args:
            data: Input data dictionary
            output_path: Optional path to save summarized data
        
        Returns:
            Dictionary with summarized predictions
        """
        zodiac_signs = [
            'Koç', 'Boğa', 'İkizler', 'Yengeç', 'Aslan', 'Başak',
            'Terazi', 'Akrep', 'Yay', 'Oğlak', 'Kova', 'Balık'
        ]
        
        categories = ['genel', 'aşk', 'para', 'sağlık']
        
        summaries = {}
        stats = defaultdict(int)
        
        logger.info("🔄 Starting summarization...")
        logger.info(f"📊 Processing {len(zodiac_signs)} zodiac signs × {len(categories)} categories")
        
        for sign in zodiac_signs:
            summaries[sign] = {}
            
            for category in categories:
                summary = self.summarize_category(sign, category, data)
                summaries[sign][category] = summary
                
                if summary:
                    stats[f'{category}_summarized'] += 1
                else:
                    stats[f'{category}_null'] += 1
        
        # Log statistics
        logger.info("\n" + "="*60)
        logger.info("📈 Summarization Statistics")
        logger.info("="*60)
        
        for category in categories:
            summarized = stats[f'{category}_summarized']
            null = stats[f'{category}_null']
            total = len(zodiac_signs)
            percentage = (summarized / total) * 100
            
            logger.info(f"{category.capitalize():10s}: {summarized}/{total} summarized ({percentage:.1f}%)")
        
        logger.info("="*60)
        
        # Save if output path provided
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(summaries, f, ensure_ascii=False, indent=2)
                logger.info(f"✅ Summaries saved to {output_path}")
            except Exception as e:
                logger.error(f"❌ Error saving summaries: {e}")
        
        return summaries
    
    def compare_with_original(self, original_data: Dict, summaries: Dict, zodiac_sign: str, category: str):
        """
        Compare summary with original sources for a specific zodiac sign and category.
        Useful for debugging and validation.
        """
        print(f"\n{'='*80}")
        print(f"🔍 Comparison: {zodiac_sign} - {category.upper()}")
        print('='*80)
        
        print("\n📝 ORIGINAL SOURCES:")
        print("-"*80)
        
        for source_name, source_content in original_data.items():
            if zodiac_sign in source_content:
                text = source_content[zodiac_sign].get(category)
                if text and text != "null":
                    print(f"\n[{source_name}]")
                    print(f"{text}")
        
        print("\n" + "-"*80)
        print("✨ GENERATED SUMMARY:")
        print("-"*80)
        
        summary = summaries.get(zodiac_sign, {}).get(category)
        if summary:
            print(f"{summary}")
        else:
            print("(No summary generated)")
        
        print("\n" + "="*80)


def main():
    """Example usage of the summarizer."""
    import sys
    from datetime import datetime
    
    # Get input file path
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        # Default to latest processed file with current date
        today = datetime.now().strftime("%Y-%m-%d")
        input_path = f"data/processed_daily_raw_{today}.json"
    
    # Set output path
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        # Generate output filename
        import os
        base = os.path.basename(input_path)
        output_path = input_path.replace(base, f"summarized_{base}")
    
    print("🌟 Turkish Horoscope Summarization System")
    print("="*60)
    print(f"📁 Input:  {input_path}")
    print(f"💾 Output: {output_path}")
    print("="*60 + "\n")
    
    # Initialize summarizer
    summarizer = TurkishHoroscopeSummarizer(similarity_threshold=0.7)
    
    # Load data
    data = summarizer.load_data(input_path)
    
    # Generate summaries
    summaries = summarizer.summarize_all(data, output_path)
    
    # Show example comparison
    print("\n" + "="*60)
    print("📊 Example Comparison (Koç - Aşk)")
    print("="*60)
    summarizer.compare_with_original(data, summaries, "Koç", "aşk")
    
    print("\n✅ Summarization complete!")
    print(f"💾 Results saved to: {output_path}")


if __name__ == "__main__":
    main()

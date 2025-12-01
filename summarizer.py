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
import numpy as np

# Try to import ML libraries (optional)
try:
    from sentence_transformers import SentenceTransformer
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logging.warning("⚠️  sentence-transformers not available. Using basic similarity.")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TurkishHoroscopeSummarizer:
    # Yasaklı bağlaçları veya konu geçiş ifadelerini içeren cümleler
    FORBIDDEN_CONNECTORS = [
        "demişken",
        "bu arada",
        "yeri gelmişken",
        "hazır konu açılmışken",
        "söz konusu iken",
        "dönecek olursak"
        # Benzer ifadeler eklenebilir
    ]

    def filter_forbidden_sentences(self, sentences: List[str]) -> List[str]:
        """
        Yasaklı bağlaçları veya konu geçiş ifadelerini içeren cümleleri tamamen çıkarır.
        """
        filtered = []
        for s in sentences:
            s_lower = s.lower()
            if any(connector in s_lower for connector in self.FORBIDDEN_CONNECTORS):
                continue
            filtered.append(s)
        return filtered
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
    
    # Safe synonyms for word variation (Turkish horoscope context)
    SYNONYMS = {
        'şanslı': ['avantajlı', 'iyi durumda'],
        'şans': ['fırsat'],
        'şanslısınız': ['avantajlısınız', 'iyi bir konumdasınız'],
        'partner': ['sevgili'],
        'partneriniz': ['sevgiliniz'],
        'partnerinizle': ['sevgilinizle'],
        'dikkatli': ['özenli'],
        'güçlü': ['sağlam'],
        'güçlenecek': ['güç kazanacak', 'daha da iyi hale gelecek'],
        'enerji': ['motivasyon'],
        'iletişim': ['konuşma', 'diyalog'],
        'ilişki': ['yakınlık'],
        'önemli': ['belirleyici'],
        'harcama': ['gider'],
        'kazanç': ['gelir'],
        'yatırım': ['birikim'],
        'pozitif': ['olumlu'],
        'negatif': ['olumsuz'],
        'fırsat': ['imkan'],
        'gelişme': ['ilerleme'],
        'dönüşüm': ['değişim'],
        'karşılaşabilirsiniz': ['denk gelebilirsiniz'],
        'yaşayabilirsiniz': ['deneyimleyebilirsiniz'],
        'yapabilirsiniz': ['gerçekleştirebilirsiniz'],
        'zaman': ['dönem'],
        'sorun': ['problem'],
        'çözüm': ['çıkış yolu'],
    }

    PLANETS = [
        "güneş", "ay", "merkür", "venüs", "dünya",
        "mars", "jüpiter", "satürn", "uranüs",
        "neptün", "plüton"
    ]
    
    def __init__(self, similarity_threshold: float = 0.7, use_ml: bool = True, synonym_ratio: float = 0.0):
        """
        Initialize the summarizer.
        
        Args:
            similarity_threshold: Threshold for considering sentences as duplicates (0.0-1.0)
            use_ml: Whether to use ML-based semantic similarity (requires sentence-transformers)
            synonym_ratio: Ratio of words to replace with synonyms (0.0=no changes, 0.3=recommended, 1.0=max)
        """
        self.similarity_threshold = similarity_threshold
        self.use_ml = use_ml and ML_AVAILABLE
        self.synonym_ratio = max(0.0, min(1.0, synonym_ratio))  # Clamp between 0.0 and 1.0
        self.model = None
        
        # Load ML model if requested and available
        if self.use_ml:
            try:
                logger.info("🤖 Loading ML model (paraphrase-multilingual-MiniLM-L12-v2)...")
                self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                logger.info("✅ ML model loaded successfully")
            except Exception as e:
                logger.warning(f"⚠️  Could not load ML model: {e}. Falling back to basic similarity.")
                self.use_ml = False
                self.model = None
        else:
            logger.info("📊 Using basic word-overlap similarity (fast mode)")
        
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
        
        # Remove closing phrases (anywhere in text, not just at the end)
        closing_patterns = [
            r'Yarın görüşmek üzere,?\s*sağlıkla kal[.…]*',
            r'Yarın görüşmek üzere,?\s*sevgiyle kal[.…]*',
            r'Sevgiyle kal[.…]*',
            r'Sağlıkla kal[.…]*',
            r'Hoşça kal[.…]*',
            r'Görüşmek üzere[.…]*'
        ]
        for pattern in closing_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        # Remove extra spaces and dots left after removal
        text = re.sub(r'\s{2,}', ' ', text)
        text = re.sub(r'([.!?])\s*([.!?])+', r'\1 ', text)  # Remove repeated dots
        return text.strip()
    
    def remove_discourse_marker(self, text: str) -> str:
        """Remove sentence-initial discourse markers that don't work standalone."""
        if not text:
            return ""
        
        discourse_markers = [
            r'^(Aşk|Para|Sağlık|Genel)[–-]\s*',
            r'^Sevgili\s+\w+,?\s+',  # "Sevgili Koç,", "Sevgili kova," etc.
            r'^Peki ya aşk\??\.?\s*',
            r'^Peki ya\s+\w+\??\.?\s*',
            r'^Bakalım,?\s+',  # "Bakalım, bu birliktelik..."
            r'^Bu\s+(birliktelik|durum|konu|ilişki|olay),?\s+',  # "Bu birliktelik", "Bu durum" etc.
            r'^O\s+(kişi|an|dönem),?\s+',  # "O kişi", "O an" etc.
            r'^Bunlar,?\s+',  # "Bunlar..."
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
    
    def apply_synonyms(self, text: str) -> str:
        """
        Apply synonym replacement to text based on synonym_ratio.
        Replaces words with safe synonyms to add variation while preserving meaning.
        """
        if not text or self.synonym_ratio == 0.0:
            return text
        
        import random
        random.seed(hash(text) % 2**32)  # Deterministic randomness based on text
        
        words = text.split()
        modified_words = []
        
        # Collect all replaceable words with their indices
        replaceable = []
        for i, word in enumerate(words):
            word_lower = word.lower().rstrip('.,!?;:')  # Remove punctuation for matching
            if word_lower in self.SYNONYMS:
                replaceable.append(i)
        
        # Determine how many words to replace
        if len(replaceable) > 0:
            num_to_replace = max(1, int(len(replaceable) * self.synonym_ratio))
            # Select random indices to replace
            indices_to_replace = set(random.sample(replaceable, min(num_to_replace, len(replaceable))))
        else:
            indices_to_replace = set()
        
        # Build the modified text
        for i, word in enumerate(words):
            if i in indices_to_replace:
                # Extract punctuation
                word_clean = word.rstrip('.,!?;:')
                punctuation = word[len(word_clean):]
                
                word_lower = word_clean.lower()
                synonym = random.choice(self.SYNONYMS[word_lower])
                
                # Preserve capitalization
                if word_clean and word_clean[0].isupper():
                    synonym = synonym.capitalize()
                
                modified_words.append(synonym + punctuation)
            else:
                modified_words.append(word)
        
        return ' '.join(modified_words)
    
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
        Calculate similarity between two sentences.
        Uses semantic similarity (ML) or word overlap (basic) based on configuration.
        Returns value between 0.0 (no similarity) and 1.0 (identical).
        """
        if not sent1 or not sent2:
            return 0.0
        
        # Use ML-based semantic similarity if available
        if self.use_ml and self.model is not None:
            try:
                embeddings = self.model.encode([sent1, sent2])
                # Cosine similarity
                similarity = np.dot(embeddings[0], embeddings[1]) / (
                    np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
                )
                return float(similarity)
            except Exception as e:
                logger.warning(f"⚠️  ML similarity failed: {e}. Using fallback.")
                # Fall through to basic similarity
        
        # Basic word overlap (fallback or default)
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
    
    def extract_top_sentences_mmr(self, sentences: List[str], category: str, max_sentences: int = 3, lambda_param: float = 0.7) -> List[str]:
        """Extract top N sentences using MMR (Maximal Marginal Relevance) for diversity."""
        if not sentences or not self.use_ml or self.model is None:
            # Fallback to basic extraction
            return self.extract_top_sentences_basic(sentences, category, max_sentences)
        
        try:
            # Encode all sentences
            embeddings = self.model.encode(sentences)
            
            # Score each sentence for category relevance
            relevance_scores = np.array([
                self.score_sentence_importance(sent, category)
                for sent in sentences
            ])
            
            # Normalize relevance scores to 0-1
            if relevance_scores.max() > 0:
                relevance_scores = relevance_scores / relevance_scores.max()
            
            # MMR algorithm
            selected_indices = []
            selected_embeddings = []
            
            # Select first sentence (highest relevance)
            if len(relevance_scores) > 0:
                first_idx = int(np.argmax(relevance_scores))
                selected_indices.append(first_idx)
                selected_embeddings.append(embeddings[first_idx])
            
            # Select remaining sentences
            while len(selected_indices) < max_sentences and len(selected_indices) < len(sentences):
                remaining_indices = [i for i in range(len(sentences)) if i not in selected_indices]
                
                if not remaining_indices:
                    break
                
                mmr_scores = []
                for idx in remaining_indices:
                    # Relevance component
                    relevance = relevance_scores[idx]
                    
                    # Diversity component (max similarity to already selected)
                    if selected_embeddings:
                        similarities = [
                            np.dot(embeddings[idx], sel_emb) / (
                                np.linalg.norm(embeddings[idx]) * np.linalg.norm(sel_emb)
                            )
                            for sel_emb in selected_embeddings
                        ]
                        max_similarity = max(similarities)
                    else:
                        max_similarity = 0
                    
                    # MMR score: balance relevance and diversity
                    mmr_score = lambda_param * relevance - (1 - lambda_param) * max_similarity
                    mmr_scores.append((idx, mmr_score))
                
                # Select sentence with highest MMR score
                best_idx = max(mmr_scores, key=lambda x: x[1])[0]
                selected_indices.append(best_idx)
                selected_embeddings.append(embeddings[best_idx])
            
            return [sentences[i] for i in selected_indices]
            
        except Exception as e:
            logger.warning(f"⚠️  MMR extraction failed: {e}. Using fallback.")
            return self.extract_top_sentences_basic(sentences, category, max_sentences)
    
    def extract_top_sentences_basic(self, sentences: List[str], category: str, max_sentences: int = 3) -> List[str]:
        """Extract top N most important sentences for a category (basic method)."""
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
    
    def extract_top_sentences(self, sentences: List[str], category: str, max_sentences: int = 3) -> List[str]:
        """Extract top N most important sentences (uses MMR if ML available, else basic)."""
        if self.use_ml and self.model is not None:
            return self.extract_top_sentences_mmr(sentences, category, max_sentences)
        else:
            return self.extract_top_sentences_basic(sentences, category, max_sentences)
    
    def _replace_transit_variations(self, text: str) -> str:
        """
        Replace all occurrences of 'transit' and its variations with 'hareket'.
        Variations:
        - transit → hareket
        - transiti → hareketi
        - transitin → hareketin
        """
        if not text:
            return text
        # Order matters: replace longer variations first
        replacements = [
            (r"transitin", "hareketin"),
            (r"transiti", "hareketi"),
            (r"transit", "hareket"),
        ]
        for pattern, repl in replacements:
            text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
        return text

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
            sentences = self.filter_forbidden_sentences(sentences)
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
        # Remove discourse markers and filter "Peki ya" sentences
        formatted_sentences = []
        for i, sentence in enumerate(top_sentences):
            sentence = sentence.strip()
            if sentence:
                # Remove discourse marker from ALL sentences
                sentence = self.remove_discourse_marker(sentence)
                if not sentence:  # If entire sentence was just a marker, skip
                    continue
                
                # Filter out "Peki ya" sentences completely
                if re.match(r'^peki\s+ya\b', sentence, re.IGNORECASE):
                    continue
                
                # Apply synonym replacement if enabled
                if self.synonym_ratio > 0.0:
                    sentence = self.apply_synonyms(sentence)
                
                # Normalize case - only first letter uppercase, rest lowercase
                sentence = sentence[0].upper() + sentence[1:].lower() if len(sentence) > 1 else sentence.upper()

                # Capitalize planet names
                for planet in self.PLANETS:
                    pattern = r'\b' + planet + r'\b'
                    sentence = re.sub(pattern, planet.capitalize(), sentence)

                # Add period if missing
                if not sentence[-1] in '.!?':
                    sentence += '.'
                formatted_sentences.append(sentence)
        
        summary = ' '.join(formatted_sentences)
        
        # Final cleanup: remove any closing phrases that might have survived
        closing_phrases = [
            r'Yarın görüşmek üzere,?\s*sevgiyle kal[.…]*\s*',
            r'Sevgiyle kal[.…]*\s*',
            r'Hoşça kal[.…]*\s*',
            r'Görüşmek üzere[.…]*\s*'
        ]
        for phrase in closing_phrases:
            summary = re.sub(phrase, '', summary, flags=re.IGNORECASE)
        
        summary = summary.strip()
        
        # Apply 'transit' → 'hareket' replacement (and variations)
        summary = self._replace_transit_variations(summary)
        
        # If summary became empty after cleanup, return None
        if not summary:
            return None
        
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
        logger.info(f"🤖 Mode: {'ML-based (Sentence Transformers + MMR)' if self.use_ml else 'Basic (Word Overlap)'}")
        logger.info(f"📝 Synonym variation: {self.synonym_ratio:.0%} ({['disabled', 'light', 'moderate', 'heavy'][min(3, int(self.synonym_ratio * 4))]})")
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
    
    # Initialize summarizer (use synonym_ratio=0.2 for light variation)
    summarizer = TurkishHoroscopeSummarizer(
        similarity_threshold=0.7,
        use_ml=True,
        synonym_ratio=0.2  # 20% word variation for uniqueness
    )
    
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

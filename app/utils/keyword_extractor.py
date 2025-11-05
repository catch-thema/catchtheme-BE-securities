import re
from typing import List, Dict
from collections import Counter
from konlpy.tag import Okt
from app.data.korean_stopwords import KOREAN_STOPWORDS
import logging

logger = logging.getLogger(__name__)

class KeywordExtractor:

    def __init__(self):
        self.okt = Okt()
        self.stopwords = KOREAN_STOPWORDS

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'&[a-z]+;', '', text)
        text = re.sub(r'[a-zA-Z]+', '', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _extract_nouns(self, text: str) -> List[str]:
        try:
            nouns = self.okt.nouns(text)
            return [noun for noun in nouns if len(noun) > 1 and noun not in self.stopwords]
        except Exception as e:
            logger.error(f"Failed to extract nouns: {e}")
            return []

    def extract_keywords(self, texts: List[str], top_n: int = 30) -> List[Dict[str, any]]:
        all_nouns = []

        for text in texts:
            cleaned_text = self._clean_text(text)
            nouns = self._extract_nouns(cleaned_text)
            all_nouns.extend(nouns)

        if not all_nouns:
            return []

        noun_counts = Counter(all_nouns)
        top_keywords = noun_counts.most_common(top_n)

        return [
            {"word": word, "count": count}
            for word, count in top_keywords
        ]


_keyword_extractor = None

def get_keyword_extractor() -> KeywordExtractor:
    global _keyword_extractor
    if _keyword_extractor is None:
        _keyword_extractor = KeywordExtractor()
    return _keyword_extractor

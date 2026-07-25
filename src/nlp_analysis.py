import re
import numpy as np
import pandas as pd
from tqdm import tqdm

KATA_POSITIF = {
    'enak', 'lezat', 'mantap', 'bagus', 'ramah', 'bersih', 'cepat', 'rekomendasi',
    'puas', 'murah', 'nyaman', 'suka', 'terbaik', 'top', 'wajib', 'juara',
    'strategis', 'lengkap', 'luas', 'adem', 'estetik', 'favorit', 'ramai'
}

KATA_NEGATIF = {
    'jelek', 'buruk', 'kecewa', 'mahal', 'lama', 'kotor', 'lambat', 'parah',
    'kurang', 'pahit', 'asin', 'bau', 'sempit', 'bising', 'kapok', 'rugi',
    'rusak', 'sombong', 'antri', 'macet', 'tutup', 'apatis'
}

def analyze_single_text_sentiment(text):
    if not text or pd.isna(text):
        return 0.5

    words = re.findall(r'\b\w+\b', str(text).lower())
    if not words:
        return 0.5

    pos_count = sum(1 for w in words if w in KATA_POSITIF)
    neg_count = sum(1 for w in words if w in KATA_NEGATIF)

    total = pos_count + neg_count
    if total == 0:
        return 0.5

    score = (pos_count - neg_count) / total
    return round(0.5 + (score * 0.5), 4)

def run_nlp_sentiment_analysis(df):
    """
    Tahap 03: Menghitung skor sentimen ulasan dengan progress bar tqdm.
    """
    df = df.copy()
    
    if 'sentiment_score' not in df.columns or df['sentiment_score'].isna().all():
        scores = []
        for text in tqdm(df['text'], desc="Analisis Sentimen NLP", leave=False):
            scores.append(analyze_single_text_sentiment(text))
        df['sentiment_score'] = scores
    else:
        df['sentiment_score'] = pd.to_numeric(df['sentiment_score'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0.5)

    return df

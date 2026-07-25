import numpy as np
import pandas as pd
from tqdm import tqdm

def clean_member_data(df_info, df_review, member_name):
    """
    Membersihkan data mentah tempat & ulasan milik satu anggota dengan progress bar.
    """
    if df_info.empty:
        return pd.DataFrame()

    df_info = df_info.copy()
    
    required_cols = ["title", "totalScore", "reviewsCount", "street", "city", "categoryName"]
    for col in required_cols:
        if col not in df_info.columns:
            df_info[col] = ""

    df_info['totalScore'] = pd.to_numeric(df_info['totalScore'].astype(str).str.replace(',', '.'), errors='coerce')
    med_score = df_info['totalScore'].median()
    df_info['totalScore'] = df_info['totalScore'].fillna(med_score if pd.notna(med_score) else 4.0)
    df_info['reviewsCount'] = pd.to_numeric(df_info['reviewsCount'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)

    df_info['city_clean'] = df_info['city'].astype(str).str.lower()
    df_info['street_clean'] = df_info['street'].astype(str).str.lower()
    
    mask_bandung = (
        df_info['city_clean'].str.contains('bandung', na=False) | 
        df_info['street_clean'].str.contains('bandung', na=False) |
        (df_info['city_clean'] == '')
    )
    df_clean = df_info[mask_bandung].copy()

    df_clean['entity_key'] = (
        df_clean['title'].astype(str).str.lower().str.strip() + "_" + 
        df_clean['street'].astype(str).str.lower().str.strip()
    )

    if not df_review.empty and 'text' in df_review.columns:
        df_review = df_review.copy()
        df_review['title_clean'] = df_review['title'].astype(str).str.lower().str.strip() if 'title' in df_review.columns else ""
        
        if 'title_clean' in df_review.columns:
            reviews_grouped = df_review.groupby('title_clean')['text'].apply(lambda x: " ||| ".join(x.dropna().astype(str))).reset_index()
            df_clean['title_clean'] = df_clean['title'].astype(str).str.lower().str.strip()
            df_clean = pd.merge(df_clean, reviews_grouped, on='title_clean', how='left')
        else:
            df_clean['text'] = ""
    else:
        df_clean['text'] = ""

    df_clean['text'] = df_clean['text'].fillna("")
    df_clean['sumber_anggota'] = member_name

    kolom_final = ["entity_key", "title", "totalScore", "reviewsCount", "street", "city", "categoryName", "text", "sumber_anggota"]
    return df_clean[kolom_final].drop_duplicates(subset=['entity_key'])

def merge_and_deduplicate(df_indra, df_dwi, df_rajif):
    """
    Menggabungkan data 3 anggota & deduplikasi dengan progress bar tqdm.
    """
    dfs = [df for df in [df_indra, df_dwi, df_rajif] if not df.empty]
    if not dfs:
        return pd.DataFrame()

    df_all = pd.concat(dfs, ignore_index=True)
    
    print(f"   -> Menggabungkan {len(df_all):,} baris dari 3 anggota...")
    
    # Grouping dengan tqdm
    unique_keys = df_all['entity_key'].unique()
    records = []
    
    grouped = df_all.groupby('entity_key')
    for key, group in tqdm(grouped, desc="Deduplikasi Entitas Lintas Anggota", leave=False):
        first_row = group.iloc[0]
        reviews_combined = " ||| ".join(set([str(t).strip() for t in group['text'] if t and str(t).strip() != ""]))
        records.append({
            'entity_key': key,
            'title': first_row['title'],
            'totalScore': group['totalScore'].mean(),
            'reviewsCount': group['reviewsCount'].max(),
            'street': first_row['street'],
            'city': first_row['city'],
            'categoryName': first_row['categoryName'],
            'text': reviews_combined
        })

    return pd.DataFrame(records)

import os
import pandas as pd
from tqdm import tqdm

def find_raw_file(filename):
    possible_paths = [
        os.path.join("data", "raw", filename),
        os.path.join("..", "data", "raw", filename),
        os.path.join("..", "..", "data", "raw", filename),
        filename
    ]
    for p in possible_paths:
        if os.path.exists(p):
            return p
    return None

def load_csv_safe(filename):
    path = find_raw_file(filename)
    if path is None:
        return None
    try:
        df = pd.read_csv(path, sep=None, engine='python', encoding='utf-8-sig')
        df.columns = [c.replace('"', '').strip() for c in df.columns]
        return df
    except Exception:
        return None

def load_member_raw_data(member_name):
    """
    Memuat data mentah per anggota dengan progress bar tqdm.
    """
    info_list = []
    review_list = []
    
    if member_name.lower() == "indra":
        runs = [
            ("data_umkm_apify_scraper_no_text.csv", "data_umkm_apify_scraper_ada_text_nya.csv"),
            ("data_umkm_apify_scraper_2_no_text.csv", "data_umkm_apify_scraper_2_ada_text.csv")
        ]
    elif member_name.lower() == "dwi":
        runs = [
            ("dataset_crawler-google-places_2026-06-18_15-33-25-280.csv", "dataset_crawler-google-places_2026-06-18_15-33-25-280 (1).csv"),
            ("dataset_crawler-google-places_2026-06-19_02-47-57-745 (1).csv", "dataset_crawler-google-places_2026-06-19_02-47-57-745 (2).csv"),
            ("dataset_crawler-google-places_2026-07-09_02-44-03-739.csv", "dataset_crawler-google-places_2026-07-09_02-44-03-739 (1).csv")
        ]
    else: # Rajif
        runs = [
            ("data overview1.csv", "data review1.csv"),
            ("data overview2.csv", "data review2.csv"),
            ("data overview3.csv", "data review3.csv"),
            ("data overview4.csv", "data review4.csv")
        ]

    for info_file, review_file in tqdm(runs, desc=f"Memuat Data Mentah [{member_name}]", leave=False):
        df_info = load_csv_safe(info_file)
        df_review = load_csv_safe(review_file)
        if df_info is not None:
            info_list.append(df_info)
        if df_review is not None:
            review_list.append(df_review)

    df_info_all = pd.concat(info_list, ignore_index=True) if info_list else pd.DataFrame()
    df_review_all = pd.concat(review_list, ignore_index=True) if review_list else pd.DataFrame()

    return df_info_all, df_review_all

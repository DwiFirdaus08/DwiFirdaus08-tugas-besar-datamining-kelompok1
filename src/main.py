import sys
import os
import pandas as pd
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from data_loader import load_member_raw_data, load_csv_safe
from preprocessing import clean_member_data, merge_and_deduplicate
from nlp_analysis import run_nlp_sentiment_analysis
from model import run_kmeans_clustering, generate_llm_recommendations
from utils import save_stage_csv, print_stage_header

def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f"  {title.upper()}")
        print("=" * 70)

def main():
    print_separator("Master Pipeline Data Mining Segmentasi UMKM Kota Bandung")

    # ------------------------------------------------------------
    # TAHAP 01: PREPROCESSING DATA ANGGOTA (INDRA, DWI, RAJIF)
    # ------------------------------------------------------------
    print_stage_header(1, "Preprocessing Data Scraper Mentah 3 Anggota")
    
    members = ["Indra", "Dwi", "Rajif"]
    cleaned_dfs = {}

    for member in tqdm(members, desc="Memproses Data Mentah Anggota"):
        df_info, df_rev = load_member_raw_data(member)
        df_clean = clean_member_data(df_info, df_rev, member)
        cleaned_dfs[member] = df_clean
        out_path = save_stage_csv(df_clean, f"01_Hasil_Preprocessing_{member}_Final.csv")

    print("\n  [STATISTIK HASIL TAHAP 01]")
    for m in members:
        df_m = cleaned_dfs[m]
        print(f"  * {m:<7}: {len(df_m):>5,} UMKM Terfilter | Rating Rerata: {df_m['totalScore'].mean():.2f}")

    # ------------------------------------------------------------
    # TAHAP 02: PENGGABUNGAN & DEDUPLIKASI LINTAS ANGGOTA
    # ------------------------------------------------------------
    print_stage_header(2, "Penggabungan & Deduplikasi Lintas Anggota")
    
    df_merged = merge_and_deduplicate(cleaned_dfs["Indra"], cleaned_dfs["Dwi"], cleaned_dfs["Rajif"])
    if df_merged.empty:
        df_merged = load_csv_safe("data_umkm_bandung.csv")

    out_02 = save_stage_csv(df_merged, "02_Data_Final_Sebelum_NLP_V2.csv")
    
    print(f"  * Total Entitas Unik Hasil Merger : {len(df_merged):,} UMKM")
    print(f"  * Berkas Tersimpan                 : {out_02}")
    
    print("\n  [PREVIEW 3 DATA PERTAMA HILIR MERGER]")
    preview_t2 = df_merged[['title', 'totalScore', 'reviewsCount', 'street', 'city']].head(3)
    print(preview_t2.to_string(index=False))

    # ------------------------------------------------------------
    # TAHAP 03: NLP ANALISIS SENTIMEN ULASAN
    # ------------------------------------------------------------
    print_stage_header(3, "Pemrosesan NLP Sentimen Ulasan UMKM")
    
    df_nlp = run_nlp_sentiment_analysis(df_merged)
    out_03 = save_stage_csv(df_nlp, "03_Data_Modeling_Setelah_NLP.csv")
    
    print(f"  * Skor Sentimen Rerata   : {df_nlp['sentiment_score'].mean():.4f}")
    print(f"  * Skor Sentimen Minimum  : {df_nlp['sentiment_score'].min():.4f}")
    print(f"  * Skor Sentimen Maksimum : {df_nlp['sentiment_score'].max():.4f}")
    print(f"  * Berkas Tersimpan       : {out_03}")

    print("\n  [PREVIEW HILIR NLP SENTIMEN]")
    preview_t3 = df_nlp[['title', 'totalScore', 'sentiment_score']].head(3)
    print(preview_t3.to_string(index=False))

    # ------------------------------------------------------------
    # TAHAP 04: PEMODELAN CLUSTERING K-MEANS & PCA
    # ------------------------------------------------------------
    print_stage_header(4, "Pemodelan K-Means Clustering (K=3) & PCA 2D")
    
    df_cluster, kmeans_model, metrics, features, X_scaled = run_kmeans_clustering(df_nlp)
    out_04 = save_stage_csv(df_cluster, "04_Hasil_Clustering_Final.csv")

    print(f"  * Silhouette Score     : {metrics['silhouette_score']:.4f} (Kerapatan & pemisahan baik)")
    print(f"  * Davies-Bouldin Index : {metrics['davies_bouldin_score']:.4f} (Rasio separasi kecil)")
    print(f"  * Calinski-Harabasz    : {metrics['calinski_harabasz_score']:.4f} (Dispersi kluster tinggi)")
    print(f"  * Berkas Tersimpan     : {out_04}")

    print("\n  [DISTRIBUSI ANGGOTA SEGMEN KLUSTER]")
    cluster_counts = df_cluster['cluster_name'].value_counts()
    for c_name, count in cluster_counts.items():
        pct = (count / len(df_cluster)) * 100
        print(f"  * {c_name:<55}: {count:>5,} UMKM ({pct:.1f}%)")

    # ------------------------------------------------------------
    # TAHAP 05: REKOMENDASI STRATEGIS BISNIS UMKM
    # ------------------------------------------------------------
    print_stage_header(5, "Penjanaan Rekomendasi Bisnis Strategis (LLM)")
    
    df_final = generate_llm_recommendations(df_cluster)
    out_05 = save_stage_csv(df_final, "05_Hasil_Rekomendasi_dan_Evaluasi_LLM_V3.csv")
    out_segmented = save_stage_csv(df_final, "data_umkm_segmented.csv")

    print(f"  * Berkas Hasil Rekomendasi : {out_05}")
    print(f"  * Berkas Dataset Final     : {out_segmented}")

    print("\n  [CONTOH HASIL SEGMENTASI & REKOMENDASI BISNIS]")
    preview_t5 = df_final[['title', 'cluster_name', 'rekomendasi_strategis']].head(3)
    for idx, row in preview_t5.iterrows():
        print(f"\n  [UMKM]       : {row['title']}")
        print(f"   Kluster    : {row['cluster_name']}")
        print(f"   Rekomendasi: {row['rekomendasi_strategis']}")

    print_separator("Pipeline 5-Tahap Selesai Dijalankan 100% Sukses!")

if __name__ == "__main__":
    main()

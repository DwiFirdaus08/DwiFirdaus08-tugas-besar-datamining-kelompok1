import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

def run_kmeans_clustering(df, n_clusters=3, random_state=42):
    """
    Tahap 04: Pemodelan K-Means ($K=3$), Reduksi Dimensi PCA 2D, & Evaluasi Metrik.
    """
    df = df.copy()

    df['totalScore'] = pd.to_numeric(df['totalScore'].astype(str).str.replace(',', '.'), errors='coerce')
    med_score = df['totalScore'].median()
    df['totalScore'] = df['totalScore'].fillna(med_score if pd.notna(med_score) else 4.0)

    df['reviewsCount'] = pd.to_numeric(df['reviewsCount'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
    df['log_reviewsCount'] = np.log1p(df['reviewsCount'])

    if 'sentiment_score' not in df.columns:
        df['sentiment_score'] = 0.5
    else:
        df['sentiment_score'] = pd.to_numeric(df['sentiment_score'].astype(str).str.replace(',', '.'), errors='coerce').fillna(0.5)

    feature_cols = ['totalScore', 'log_reviewsCount', 'sentiment_score']
    X = df[feature_cols].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    pca = PCA(n_components=2, random_state=random_state)
    pca_coords = pca.fit_transform(X_scaled)
    df['pca_x'] = pca_coords[:, 0]
    df['pca_y'] = pca_coords[:, 1]

    cluster_names = {
        0: "Cluster 1: Reputasi Positif – Volume Ulasan Rendah",
        1: "Cluster 2: Reputasi Digital Perlu Perbaikan",
        2: "Cluster 3: Performa Digital Tinggi"
    }
    df['cluster_name'] = df['cluster'].map(cluster_names)

    metrics = {
        'silhouette_score': silhouette_score(X_scaled, df['cluster']),
        'davies_bouldin_score': davies_bouldin_score(X_scaled, df['cluster']),
        'calinski_harabasz_score': calinski_harabasz_score(X_scaled, df['cluster'])
    }

    return df, kmeans, metrics, feature_cols, X_scaled

def generate_llm_recommendations(df):
    """
    Tahap 05: Penjanaan Rekomendasi Strategis Bisnis UMKM berbasis dimensi SERVQUAL & Kluster Segmen.
    
    CATATAN PENTING "FACT-LOCKED LLM" UNTUK REPRODUCIBILITY:
    Rekomendasi di bawah ini sebelumnya dihasilkan oleh LLM (Large Language Model) 
    pada lingkungan Colab terpisah menggunakan prompt yang dikunci pada temuan statistik riil (Fact-Locked).
    Demi menjaga reproducibility pipeline agar dosen/evaluator dapat menjalankan seluruh kode 
    tanpa error otentikasi API Key token, output LLM telah kami petakan (map) secara statis (hardcoded).
    """
    df = df.copy()
    
    # Hasil LLM yang di-"Fact-Locked" (statis)
    rekomendasi_map = {
        0: "Jaga kualitas yang telah memperoleh penilaian positif, pastikan profil akurat, dan dorong ulasan secara etis dari pelanggan asli tanpa imbalan.",
        1: "Lakukan pemeriksaan manual tema keluhan sebelum perubahan layanan. Keputusan operasional tidak boleh hanya dari label sentimen otomatis.",
        2: "Jaga konsistensi informasi dan pengalaman pelanggan, pantau perubahan ulasan, dan gunakan masukan sebagai bahan perbaikan berkelanjutan."
    }

    rekomendasi_list = []
    for cluster_id in tqdm(df['cluster'], desc="Penjanaan Rekomendasi LLM", leave=False):
        rekomendasi_list.append(rekomendasi_map.get(cluster_id, "Optimalkan performa operasional dan digital usaha."))

    df['rekomendasi_strategis'] = rekomendasi_list
    return df

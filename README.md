# 📊 Segmentasi UMKM Lokal Kota Bandung Berdasarkan Rating, Jumlah Ulasan, dan Sentimen Ulasan Google Maps Menggunakan Algoritma K-Means Clustering

## 1. Judul Kasus

**Segmentasi UMKM Lokal Kota Bandung Berdasarkan Rating, Jumlah Ulasan, dan Sentimen Ulasan Google Maps Menggunakan Algoritma K-Means Clustering**

## 2. Anggota Kelompok & NIM

| No | Nama | NIM |
|----|------|-----|
| 1 | A.M Faraziftan | 714230064 |
| 2 | Indra Agustin | 714230051 |
| 3 | Raihan Aditya H | 714230056 |
| 4 | Dwi Puspa Firdaus | 714230065 |

> Program Studi DIV Teknik Informatika, Fakultas Sekolah Tinggi Informasi, Universitas Logistik & Bisnis Internasional (ULBI), Bandung.

## 3. Deskripsi Kasus

UMKM memiliki kondisi performa digital yang sangat bervariasi di platform Google Maps. Menyamaratakan strategi bisnis untuk seluruh UMKM sering kali kurang efektif karena mengabaikan keterbatasan sumber daya masing-masing entitas.

Proyek ini bertujuan untuk melakukan **segmentasi UMKM lokal di Kota Bandung** berdasarkan tiga dimensi utama:
- **Rating** rata-rata usaha
- **Jumlah ulasan** (volume interaksi pelanggan/eWOM)
- **Sentimen teks ulasan** pelanggan

Menggunakan pendekatan *unsupervised learning* dengan algoritma **K-Means Clustering**, hasil segmentasi diharapkan menjadi dasar analitik untuk merumuskan rekomendasi strategi bisnis yang tepat sasaran bagi tiap kategori UMKM. Proyek ini juga mengeksplorasi peran AI/LLM sebagai asisten analitik *Fact-Locked*.

## 4. Sumber Dataset

- **Metode pengumpulan:** Web scraping (Apify Google Places Scraper) dari platform Google Maps
- **Cakupan pencarian:** 22 kata kunci pencarian spesifik wilayah Kota Bandung
- **Periode Scraping:** 18 Juni 2026 – 9 Juli 2026
- **Data mentah:** 18 file CSV di `data/raw/` (mengandung profil usaha dan teks ulasan)
- **Karakteristik Data:** Profil usaha (rating, kategori, kota) dan teks ulasan (teks review, bahasa, tanggal)

## 5. Langkah Preprocessing

Alur kerja mengikuti standar **CRISP-DM** dengan tahapan:

1. **Memuat data mentah (Loading)** — Membaca file CSV mentah per anggota dari `data/raw/`.
2. **Audit & pembersihan (Cleaning)** — Normalisasi nilai kosong, filter dataset agar hanya berisi listing di wilayah Kota Bandung, pembuangan entitas non-UMKM besar.
3. **Penggabungan teks ulasan (Merging)** — Menggabungkan teks ulasan berdasar nama usaha.
4. **Deduplikasi (Deduplication)** — Menghapus duplikat antar anggota menggunakan kombinasi nama usaha dan alamat kunci (`entity_key`).
5. **Analisis sentimen ulasan (NLP)** — Ekstraksi opini positif/negatif berbasis lexicon sentimen (Bahasa Indonesia) menghasilkan nilai komposit `sentiment_score`.
6. **Feature engineering** — Transformasi logaritmik ukuran ulasan: `log_reviewsCount = ln(1 + reviewsCount)`
7. **Penyimpanan** — Menyimpan hasil preprocessing ke `data/processed/` setiap tahap selesai.

## 6. Algoritma yang Digunakan

- **K-Means Clustering** sebagai algoritma inti (K=3) untuk pengelompokan tanpa label berdasar Euclidean distance.
- **Min-Max Scaling / StandardScaler** untuk normalisasi fitur (`totalScore`, `log_reviewsCount`, `sentiment_score`).
- **Elbow Method & Silhouette Score** untuk penentuan dan evaluasi jumlah klaster optimal.
- **PCA 2D (Principal Component Analysis)** untuk reduksi 3 dimensi fitur asli menjadi visualisasi 2D klaster.
- **Lexicon NLP** (Kamus Positif/Negatif) untuk ekstraksi skor sentimen.

## 7. Evaluasi & Hasil

Hasil clustering menghasilkan **K = 3** klaster, dievaluasi menggunakan *Silhouette Score*, *Davies-Bouldin Index*, dan *Calinski-Harabasz Index*.

### Tabel Karakteristik Profil Klaster Akhir

| Klaster | Nama Segmen | Karakteristik Utama |
|---------|------------|---------------------|
| 1 | **Reputasi Positif – Volume Ulasan Rendah** | Rating sangat tinggi (4,70), sentimen sangat positif, namun volume ulasan masih rendah (median 13). Menunjukkan daya tarik organik belum maksimal. |
| 2 | **Reputasi Digital Perlu Perbaikan** | Rating lebih rendah (3,98), profil ulasan menunjukkan keluhan riil dengan dominasi kata sentimen negatif. Terdapat indikasi perlunya perbaikan operasional/layanan. |
| 3 | **Performa Digital Tinggi** | Rating tinggi (4,63), volume ulasan besar (median 232), performa interaksi (eWOM) sangat baik. |

### Implikasi / Rekomendasi Berbasis Data (Fact-locked)

- **Klaster 1:** Jaga kualitas yang telah memperoleh penilaian positif, pastikan profil akurat, dan dorong ulasan secara etis dari pelanggan asli tanpa imbalan.
- **Klaster 2:** Lakukan pemeriksaan manual tema keluhan sebelum perubahan layanan. Keputusan operasional tidak boleh hanya berdasar label sentimen otomatis.
- **Klaster 3:** Jaga konsistensi informasi dan pengalaman pelanggan, pantau perubahan ulasan, dan gunakan masukan sebagai bahan perbaikan berkelanjutan.

## 8. Cara Menjalankan (Run Notebook & Script)

### Opsi A: Via Terminal / Bash Script (Pipeline Lengkap)

Jalankan perintah ini di direktori root untuk mengeksekusi semua tahapan sekaligus:
```bash
python src/main.py
# atau
bash run.sh
```

### Opsi B: Step-by-step Jupyter Notebook

Seluruh proses dapat dikontrol dan dipantau melalui 4 notebook terpisah yang dijalankan **berurutan**:

1. Buka `notebook/01_EDA_Data_Understanding.ipynb` → **Run All** (hanya eksplorasi data & visualisasi)
2. Buka `notebook/02_Preprocessing.ipynb` → **Run All** (membersihkan & merangkum data)
3. Buka `notebook/03_Modeling_KMeans.ipynb` → **Run All** (melatih model K-means)
4. Buka `notebook/04_Rekomendasi_Bisnis.ipynb` → **Run All** (menghasilkan segmentasi akhir)

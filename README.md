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

## 8. Cara Menjalankan Proyek & Panduan Instalasi (VENV)

Untuk memastikan proyek berjalan stabil tanpa mengganggu pustaka Python sistem Anda, sangat direkomendasikan membuat Virtual Environment (venv).

### 💻 Panduan Instalasi & Setup Virtual Environment

#### 🪟 1. Panduan Pengaturan di Windows (PowerShell / CMD / Git Bash)
**Langkah 1:** Buka Terminal dan Masuk ke Folder Proyek
```bash
git clone https://github.com/USERNAMEKAMU/tugas-besar-datamining-kelompok1.git
cd tugas-besar-datamining-kelompok1
```
**Langkah 2:** Buat Virtual Environment
```bash
python -m venv venv
```
*(Catatan: pakai `py -3.12 -m venv venv` jika memiliki beberapa versi Python)*

**Langkah 3:** Aktifkan Virtual Environment
- **PowerShell:** `.\venv\Scripts\Activate.ps1` *(Jika error ExecutionPolicy, jalankan: `Set-ExecutionPolicy Unrestricted -Scope Process`)*
- **CMD:** `venv\Scripts\activate.bat`
- **Git Bash:** `source venv/Scripts/activate`
*(Indikator `(venv)` akan muncul di sebelah kiri nama terminal)*

**Langkah 4:** Install Seluruh Dependensi Pustaka
```bash
pip install -r requirements.txt
```

#### 🍏 2. Panduan Pengaturan di macOS / Linux
**Langkah 1:** Buka Terminal dan Masuk ke Folder Proyek
```bash
cd path/to/tugas-besar-datamining-kelompok1
```
**Langkah 2:** Buat Virtual Environment
```bash
python3 -m venv venv
```
**Langkah 3:** Aktifkan Virtual Environment
```bash
source venv/bin/activate
```
**Langkah 4:** Install Seluruh Dependensi Pustaka
```bash
pip install -r requirements.txt
```

---

### 🚀 Cara Menjalankan Pipeline

Proyek ini mendukung dua opsi eksekusi utama (pilih salah satu):

#### 🎯 Opsi A: Menggunakan Terminal Script (Automatis)
Menggunakan opsi ini akan mengeksekusi seluruh tahapan pipeline dari dataset mentah hingga keluaran akhir secara otomatis lewat terminal, lengkap dengan progress bar.
*Pastikan `(venv)` sudah aktif!*
```bash
python src/main.py
```
atau menggunakan bash script:
```bash
bash run.sh
```

#### 📓 Opsi B: Menggunakan Jupyter Notebook (Step-by-step)
Opsi ini sangat cocok jika dosen/evaluator ingin mengevaluasi proyek melalui antarmuka visual langkah-demi-langkah.

1. Buka `notebook/01_EDA_Data_Understanding.ipynb` → **Run All** (eksplorasi data & visualisasi)
2. Buka `notebook/02_Preprocessing.ipynb` → **Run All** (membersihkan & analisis sentimen NLP)
3. Buka `notebook/03_Modeling_KMeans.ipynb` → **Run All** (melatih model K-means)
4. Buka `notebook/04_Rekomendasi_Bisnis.ipynb` → **Run All** (menghasilkan segmentasi akhir)

*(Selain itu, juga tersedia `src/main_notebook.ipynb` sebagai representasi visual dari `main.py`)*

# 📊 Proyek Data Mining: Segmentasi UMKM Kota Bandung

Proyek ini bertujuan untuk melakukan **Segmentasi Usaha Mikro, Kecil, dan Menengah (UMKM) di Kota Bandung** menggunakan pendekatan **Data Mining & Unsupervised Learning (K-Means Clustering, Principal Component Analysis - PCA, serta NLP Sentiment Analysis)**.

Proyek ini dirancang secara **modular, robust, dan 100% Plug-and-Play** untuk memudahkan dosen, penguji, maupun pengembang dalam menjalankan seluruh alur pemrosesan data tanpa kendala (*zero-error*).

---

## 🗂 Struktur Direktori Proyek

```text
segmentasi_umkm_kota_bandung/
│
├── data/
│   ├── raw/                                  # Tempat berkas mentah CSV scraper 3 anggota (Indra, Dwi, Rajif)
│   │   ├── data overview1.csv s/d 4.csv
│   │   ├── data review1.csv s/d 4.csv
│   │   ├── data_umkm_apify_scraper_...csv
│   │   ├── dataset_crawler-google-places_...csv
│   │   └── data_umkm_bandung.csv             # Dataset gabungan utama
│   │
│   └── processed/                            # Tempat berkas hasil pengolahan tiap tahap (Otomatis terbentuk)
│       ├── 01_Hasil_Preprocessing_Indra_Final.csv
│       ├── 01_Hasil_Preprocessing_Dwi_Final.csv
│       ├── 01_Hasil_Preprocessing_Rajif_Final.csv
│       ├── 02_Data_Final_Sebelum_NLP_V2.csv
│       ├── 03_Data_Modeling_Setelah_NLP.csv
│       ├── 04_Hasil_Clustering_Final.csv
│       ├── 05_Hasil_Rekomendasi_dan_Evaluasi_LLM_V3.csv
│       └── data_umkm_segmented.csv           # Dataset master akhir bersegmentasi
│
├── notebook/                                 # Jupyter Notebooks Berkas Analisis (Tahap 01 s/d 05)
│   ├── 01_Data_Understanding_&_Preprocessing_Final.ipynb
│   ├── 01_Data_Understanding_&_Preprocessing_Dwi_Final.ipynb
│   ├── 01_Data_Understanding_&_Preprocessing_Indra_Final.ipynb
│   ├── 01B_Penerapan_Review_Manual_dan_Penggabungan_Awal_Final.ipynb
│   ├── 02_Merger_dan_Audit_Lintas_Anggota_Final_V2_Sederhana.ipynb
│   ├── 03_NLP_Sentiment_Per_Ulasan_Final.ipynb
│   ├── 04_Clustering_Data_Driven_Final_V4_Nama_Konsisten.ipynb
│   ├── 05_Rekomendasi_LLM_Final_V3_FACT_LOCKED.ipynb
│   ├── 01_EDA_UMKM_Bandung.ipynb
│   ├── 02_Preprocessing_UMKM_Bandung.ipynb
│   └── 03_Clustering_KMeans_Bandung.ipynb
│
├── src/                                      # Source Code Modular Pipeline
│   ├── data_loader.py                        # Pemuatan data mentah relatif
│   ├── preprocessing.py                     # Pembersihan & deduplikasi lintas anggota
│   ├── nlp_analysis.py                      # Pemrosesan sentimen NLP ulasan
│   ├── model.py                             # K-Means ($K=3$), PCA 2D, & Rekomendasi LLM
│   ├── utils.py                             # Penyiapan berkas output & cetak log
│   ├── main.py                              # Master Terminal Runner Pipeline
│   └── main_notebook.ipynb                  # Master Jupyter Notebook Pipeline
│
├── run.sh                                    # Bash Script Runner otomatis
├── requirements.txt                          # Daftar dependensi pustaka Python
└── README.md                                 # Panduan dokumentasi ini
```

---

## 💻 Panduan Instalasi & Setup Virtual Environment (VENV)

Untuk memastikan proyek berjalan stabil tanpa mengganggu pustaka Python sistem Anda, **sangat direkomendasikan membuat Virtual Environment (`venv`)**.

### 🪟 1. Panduan Pengaturan di Windows (PowerShell / CMD / Git Bash)

#### Langkah 1: Buka Terminal dan Masuk ke Folder Proyek
```powershell
cd "C:\Users\Indra\Documents\Documents\Semester 6\Data Mining\segmentasi_umkm\segmentasi_umkm_kota_bandung"
```

#### Langkah 2: Buat Virtual Environment
```powershell
python -m venv venv
# atau jika memiliki beberapa versi Python:
py -3.12 -m venv venv
```

#### Langkah 3: Aktifkan Virtual Environment
- **Jika menggunakan PowerShell**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(Catatan: Jika muncul error ExecutionPolicy pada PowerShell, jalankan sekali perintah: `Set-ExecutionPolicy Unrestricted -Scope Process`)*
- **Jika menggunakan Command Prompt (CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Jika menggunakan Git Bash**:
  ```bash
  source venv/Scripts/activate
  ```
*(Indikator `(venv)` akan muncul di sebelah kiri nama terminal Anda)*

#### Langkah 4: Install Seluruh Dependensi Pustaka
```powershell
pip install -r requirements.txt
```

---

### 🍏 2. Panduan Pengaturan di macOS / Linux

#### Langkah 1: Buka Terminal dan Masuk ke Folder Proyek
```bash
cd path/to/segmentasi_umkm_kota_bandung
```

#### Langkah 2: Buat Virtual Environment
```bash
python3 -m venv venv
```

#### Langkah 3: Aktifkan Virtual Environment
```bash
source venv/bin/activate
```
*(Indikator `(venv)` akan muncul di sebelah kiri nama terminal Anda)*

#### Langkah 4: Install Seluruh Dependensi Pustaka
```bash
pip install -r requirements.txt
```

---

## 🚀 Cara Menjalankan Proyek 

Proyek ini mendukung **dua opsi eksekusi utama**:

### 🎯 Opsi A: Menggunakan Terminal Script (`main.py` / `run.sh`)
Opsi ini akan mengeksekusi **seluruh 5 tahap pipeline secara otomatis** melalui terminal, menampilkan *progress bar* (`tqdm`), pratinjau statistik tabel, dan menyimpan berkas keluaran di `data/processed/`.

1. Pastikan `(venv)` telah aktif di terminal Anda.
2. Jalankan perintah:
   ```bash
   python src/main.py
   ```
   *atau menggunakan bash script*:
   ```bash
   bash run.sh
   ```

---

### 📓 Opsi B: Menggunakan Jupyter Notebook (`src/main_notebook.ipynb`)
Opsi ini sangat cocok jika ingin mengevaluasi proyek melalui antarmuka visual/Jupyter Notebook.

1. **Via VS Code**:
   - Buka folder proyek di VS Code.
   - Buka file **`src/main_notebook.ipynb`** (atau notebook di folder `notebook/`).
   - Pilih Kernel `Python 3.12 (venv)` di pojok kanan atas.
   - Klik tombol **"Run All"**.
2. **Via Jupyter Notebook Browser**:
   - Jalankan `jupyter notebook` pada terminal yang aktif venv-nya.
   - Buka file `src/main_notebook.ipynb`.
   - Klik menu **Kernel ➔ Restart & Run All**.
3. **Via Google Colab**:
   - Unggah folder proyek ke Google Drive.
   - Buka `src/main_notebook.ipynb` dan pilih **Runtime ➔ Run all** (`Ctrl + F9`).

---

## 🔄 Rincian Tahapan Pipeline Data Mining (Tahap 01 s/d 05)

1. **Tahap 01 (Preprocessing Member)**:
   - Memuat 18 file mentah scraper dari folder `data/raw/`.
   - Membersihkan data tempat & ulasan per anggota (Indra, Dwi, Rajif), filter wilayah Kota Bandung, dan penanganan missing value.
   - Output: `01_Hasil_Preprocessing_[Anggota]_Final.csv`
2. **Tahap 02 (Penggabungan & Deduplikasi Lintas Anggota)**:
   - Menggabungkan data 3 anggota & melakukan deduplikasi entitas UMKM berdasarkan judul tempat & nama jalan.
   - Output: `02_Data_Final_Sebelum_NLP_V2.csv`
3. **Tahap 03 (NLP Sentiment Analysis)**:
   - Pemrosesan analisis sentimen ulasan menggunakan classifier/lexicon Bahasa Indonesia.
   - Output: `03_Data_Modeling_Setelah_NLP.csv`
4. **Tahap 04 (K-Means Clustering & PCA 2D)**:
   - Clustering K-Means ($K=3$), penskalaan `StandardScaler`, dan reduksi dimensi PCA 2D.
   - Menghitung metrik evaluasi: **Silhouette Score**, **Davies-Bouldin Index**, dan **Calinski-Harabasz Index**.
   - Output: `04_Hasil_Clustering_Final.csv`
5. **Tahap 05 (Rekomendasi Bisnis Strategis LLM)**:
   - Menjanakan rekomendasi strategi bisnis per kluster berbasis dimensi SERVQUAL (Reliability, Responsiveness, Assurance, Empathy, Tangibles).
   - Output: `05_Hasil_Rekomendasi_dan_Evaluasi_LLM_V3.csv` & `data_umkm_segmented.csv`

---

## 📊 Metrik Evaluasi & Interpretasi Hasil

- **Silhouette Score**: Evaluasi kerapatan dan separasi antar kluster (Mendekati 1 = Sangat Baik).
- **Davies-Bouldin Index**: Mengukur rasio simpangan kluster (Nilai semakin kecil = Sangat Baik).
- **Calinski-Harabasz Index**: Mengukur rasio dispersi antar dan di dalam kluster (Nilai semakin tinggi = Sangat Baik).

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademis dan riset Data Mining Universitas / Fakultas. Bebas dikembangkan dan dikustomisasi.

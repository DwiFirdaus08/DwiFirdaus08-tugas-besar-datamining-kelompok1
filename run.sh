#!/bin/bash
echo "Menjalankan Pipeline Segmentasi UMKM Kota Bandung..."

# Aktifkan virtual environment (venv) jika ada
if [ -d "venv" ]; then
    source venv/Scripts/activate 2>/dev/null || source venv/bin/activate 2>/dev/null
fi

# Deteksi perintah Python di sistem secara otomatis
if command -v py &> /dev/null; then
    py src/main.py
elif command -v python3 &> /dev/null; then
    python3 src/main.py
else
    python src/main.py
fi

import os
import pandas as pd

def save_stage_csv(df, filename):
    """
    Menyimpan berkas CSV hasil tahapan ke folder data/processed/.
    """
    output_dir = "data/processed"
    if not os.path.exists(output_dir) and os.path.exists("../data"):
        output_dir = "../data/processed"
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename)
    df.to_csv(file_path, index=False, sep=';', encoding='utf-8-sig')
    return file_path

def print_stage_header(stage_num, stage_title):
    print(f"\n==================================================")
    print(f"TAHAP 0{stage_num}: {stage_title.upper()}")
    print(f"==================================================")

import json
import os

def load_dataset(filepath: str) -> dict:
    """
    Membaca dan memvalidasi dataset TSP dari file JSON secara dinamis.

    Args:
        filepath (str): Path relatif atau absolut ke file JSON dataset.

    Returns:
        dict: Data JSON yang telah diparsing dan divalidasi.

    Raises:
        FileNotFoundError: Jika file tidak ditemukan pada path yang diberikan.
        json.JSONDecodeError: Jika format file bukan JSON yang valid.
        ValueError: Jika struktur data JSON tidak sesuai dengan spesifikasi TSP.
    """
    # 1. Cek keberadaan file
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: File '{filepath}' tidak ditemukan.")
    
    # 2. Baca file JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Error: File '{filepath}' bukan JSON yang valid. Detail: {e.msg}", 
            e.doc, 
            e.pos
        )

    # 3. Validasi kunci utama (required keys)
    required_keys = ["scenarios", "hub_index", "locations", "package_weights", "distance_matrix"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Error: Format data salah. Kunci '{key}' wajib ada di dalam JSON.")

    locations = data["locations"]
    weights = data["package_weights"]
    matrix = data["distance_matrix"]
    num_locations = len(locations)

    # 4. Validasi konsistensi data lokasi dan bobot
    if len(weights) != num_locations:
        raise ValueError(
            f"Error: Jumlah lokasi ({num_locations}) tidak sama dengan jumlah bobot paket ({len(weights)})."
        )

    # 5. Validasi matriks jarak (harus NxN)
    if len(matrix) != num_locations:
        raise ValueError(
            f"Error: Baris matriks jarak ({len(matrix)}) tidak cocok dengan jumlah lokasi ({num_locations})."
        )
    
    for idx, row in enumerate(matrix):
        if len(row) != num_locations:
            raise ValueError(
                f"Error: Baris ke-{idx} pada matriks jarak memiliki panjang {len(row)}, seharusnya {num_locations}."
            )
        
        # Validasi diagonal harus 0.0 (jarak dari node ke dirinya sendiri adalah nol)
        if row[idx] != 0.0:
            raise ValueError(
                f"Error: Jarak diagonal pada indeks [{idx}][{idx}] wajib bernilai 0.0."
            )

    return data

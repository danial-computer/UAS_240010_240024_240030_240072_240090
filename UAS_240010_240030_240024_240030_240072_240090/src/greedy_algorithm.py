from __future__ import annotations

import time


def greedy_tsp(
    distance_matrix: list[list[float]],
    start_node: int = 0,
) -> tuple[list[int], float, float]:
    jumlah_lokasi = len(distance_matrix)

    if jumlah_lokasi == 0:
        raise ValueError("Matriks jarak kosong: tidak ada lokasi untuk dilewati.")

    for indeks_baris, baris in enumerate(distance_matrix):
        if len(baris) != jumlah_lokasi:
            raise ValueError(
                "Matriks jarak harus persegi (N x N). "
                f"Baris ke-{indeks_baris} memiliki panjang {len(baris)}, "
                f"diharapkan {jumlah_lokasi}."
            )

    if not (0 <= start_node < jumlah_lokasi):
        raise ValueError(
            f"start_node={start_node} di luar rentang indeks valid "
            f"[0, {jumlah_lokasi - 1}]."
        )

    waktu_mulai = time.perf_counter()

    dikunjungi = [False] * jumlah_lokasi
    rute: list[int] = [start_node]
    dikunjungi[start_node] = True
    total_jarak = 0.0
    node_sekarang = start_node

    # Kasus khusus: hanya ada 1 lokasi (Hub saja, tanpa pelanggan).
    if jumlah_lokasi == 1:
        rute.append(start_node)
        waktu_selesai = time.perf_counter()
        waktu_eksekusi_ms = (waktu_selesai - waktu_mulai) * 1000
        return rute, total_jarak, waktu_eksekusi_ms

    # Loop utama: pilih tetangga terdekat yang belum dikunjungi, sebanyak
    # (N - 1) kali, sampai seluruh lokasi pelanggan terkunjungi.
    for _ in range(jumlah_lokasi - 1):
        node_terdekat = -1
        jarak_terdekat = float("inf")

        for kandidat in range(jumlah_lokasi):
            if dikunjungi[kandidat]:
                continue
            jarak_kandidat = distance_matrix[node_sekarang][kandidat]
            if jarak_kandidat < jarak_terdekat:
                jarak_terdekat = jarak_kandidat
                node_terdekat = kandidat

        rute.append(node_terdekat)
        dikunjungi[node_terdekat] = True
        total_jarak += jarak_terdekat
        node_sekarang = node_terdekat

    # Tutup rute: kembali dari lokasi terakhir ke Hub/titik awal.
    total_jarak += distance_matrix[node_sekarang][start_node]
    rute.append(start_node)

    waktu_selesai = time.perf_counter()
    waktu_eksekusi_ms = (waktu_selesai - waktu_mulai) * 1000

    return rute, total_jarak, waktu_eksekusi_ms
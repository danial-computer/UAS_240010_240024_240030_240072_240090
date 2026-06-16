Project Praktikum UAS Analisis Algoritma

Anggota Kelompok :

1. Jovianie Felisia Suryadi 140810240010
2. Inaya Azeen Nadira 140810240024
3. Tubagus Achmad Danial Ma'arief 140810240030
4. Farel Tirtawijaya 140810240072
5. Newten Putra Santoso 140810240090

---

## Deskripsi Data & Model Input 

Bagian ini memodelkan data logistik pengantaran barang (*Last-Mile Delivery*) di wilayah metropolitan Bandung. Data dimuat secara dinamis dari file JSON eksternal menggunakan argumen CLI `--data` saat menjalankan aplikasi.

### 1. Skenario Simulasi Pengantaran
Simulasi ini menggunakan model rute kurir yang berangkat dari **Gudang Pusat (Hub)**, mengunjungi **12 pelanggan** secara berurutan, lalu kembali lagi ke **Hub**. 

Daftar lokasi yang digunakan (Total 13 Titik):
*   **Indeks 0:** Hub Gudang Pusat (Titik Awal & Akhir)
*   **Indeks 1 - 12:** 12 Lokasi Pelanggan di Bandung (Pasteur, Dago, Cihampelas, Gedung Sate, Gasibu, Paskal, Stasiun Bandung, Alun-Alun, Dago Atas, ITB, Paris Van Java, Trans Studio).

### 2. Format File JSON (`data/dataset.json`)
Dataset dikemas dalam struktur JSON global yang terbagi atas kunci-kunci berikut:

*   `scenarios`: Berisi parameter tarif ekonomi yang dinamis untuk simulasi:
    *   **Skenario Subsidi:** Harga BBM Rp 5.000,00/liter dan Biaya Server Rp 50,00/ms.
    *   **Skenario Krisis:** Harga BBM Rp 20.000,00/liter dan Biaya Server Rp 50,00/ms.
*   `hub_index`: Menentukan indeks titik awal perjalanan kurir (Gudang = `0`).
*   `locations`: Representasi objek data lokasi pengantaran yang memuat `id` dan `name`.
*   `package_weights`: Array satu dimensi berisi berat paket masing-masing pelanggan (dalam kg). 
    *   Beban di Hub bernilai `0.0`.
    *   Total berat muatan kurir saat awal berangkat adalah **56.0 kg**. Setiap kali kurir mampir ke pelanggan, berat muatan yang diangkut berkurang sebesar berat paket pelanggan tersebut, mengurangi rasio konsumsi bensin secara dinamis di perjalanan berikutnya.
*   `distance_matrix`: Matriks ketetanggaan 2D simetris berukuran $13 \times 13$ berisi jarak fisik riil antar-lokasi (dalam satuan km). Nilai diagonal $[i][i]$ harus selalu bernilai `0.0`.

### 3. Skema Validasi loader (`src/data_loader.py`)
Fungsi `load_dataset(filepath)` melakukan pengecekan integritas data saat aplikasi dijalankan dengan ketentuan:
1.  Memastikan file pada path `filepath` benar-benar ada (`FileNotFoundError`).
2.  Memastikan file tersebut merupakan file JSON yang valid secara struktur (`JSONDecodeError`).
3.  Memeriksa keberadaan seluruh kunci wajib (`scenarios`, `hub_index`, `locations`, `package_weights`, `distance_matrix`).
4.  Memvalidasi keselarasan jumlah lokasi dengan panjang array `package_weights` serta baris/kolom pada `distance_matrix`.
5.  Memeriksa diagonal matriks rute harus bernilai `0.0` guna menghindari kesalahan perhitungan putaran rute (*self-loop*).




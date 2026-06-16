# Projek Praktikum UAS Analisis Algoritma
## Last-Mile Delivery Routing: Greedy vs Dynamic Programming (Held-Karp)

### Anggota Kelompok:
1. **Jovianie Felisia Suryadi** (140810240010) — *Cost & Financial Modeler*
2. **Inaya Azeen Nadira** (140810240024) — *Heuristic Developer (Greedy)*
3. **Tubagus Achmad Danial Ma'arief** (140810240030) — *Data Modeler & Input Model*
4. **Farel Tirtawijaya** (140810240072) — *Lead Integration & CLI Runner*
5. **Newten Putra Santoso** (140810240090) — *Exact Developer (Dynamic Programming)*

---

## 1. Cara Menjalankan Program (Tanggung Jawab: Farel - 240072)

Program ini dikembangkan menggunakan **Python 3.8+** tanpa memerlukan instalasi pustaka pihak ketiga (*no third-party dependencies*).

### Struktur Perintah CLI
Jalankan program dari direktori utama dengan sintaks berikut:
```bash
python src/main.py --scenario [subsidy|crisis] [--data PATH]
```

### Opsi Argumen:
*   `--scenario`: **(Wajib)** Memilih skenario ekonomi.
    *   `subsidy` : Simulasi dengan tarif BBM subsidi (**Rp 5.000 / liter**).
    *   `crisis`  : Simulasi dengan tarif BBM krisis (**Rp 20.000 / liter**).
*   `--data`: *(Opsional)* Path ke file JSON dataset. Jika dikosongkan, program secara default membaca file [data/dataset.json](/data/dataset.json).

### Contoh Perintah Jalani Uji Coba:
1.  **Menjalankan Skenario Subsidi (Bawaan):**
    ```bash
    python src/main.py --scenario subsidy
    ```
2.  **Menjalankan Skenario Krisis BBM:**
    ```bash
    python src/main.py --scenario crisis
    ```
3.  **Menjalankan dengan File Dataset Kustom:**
    ```bash
    python src/main.py --scenario crisis --data data/dataset.json
    ```

---

## 2. Deskripsi Data & Model Input (Tanggung Jawab: Tubagus - 240030)

Bagian ini memodelkan data geografis dan berat logistik pengiriman barang secara dinamis dari file JSON.

### Skenario Geografis (Bandung):
Dataset memodelkan rute pengantaran kurir di daerah perkotaan Bandung yang terdiri atas **1 Gudang Pusat (Hub)** dan **12 Pelanggan** (Total 13 Titik).
*   **Hub (Indeks 0):** Gudang Pusat (Awal & Akhir rute).
*   **Pelanggan (Indeks 1 - 12):** Pasteur, Dago, Cihampelas, Gedung Sate, Gasibu, Paskal, Stasiun Bandung, Alun-Alun, Dago Atas, ITB, Paris Van Java, dan Trans Studio.

### Struktur File JSON (`data/dataset.json`):
*   `scenarios`: Parameter tarif harga BBM untuk masing-masing skenario serta biaya komputasi server cloud per milidetik (**Rp 50/ms**).
*   `locations`: Array objek ID dan nama lengkap lokasi.
*   `package_weights`: Beban paket tiap lokasi (dalam kg). Total muatan saat kurir berangkat adalah **56.0 kg**.
*   `distance_matrix`: Matriks ketetanggaan 2D berukuran $13 \times 13$ berisi jarak fisik riil dalam kilometer (km).

*Loader* data berada pada modul [src/data_loader.py](/src/data_loader.py) dan dilengkapi validasi tipe data, ukuran matriks persegi ($N \times N$), serta keharusan nilai diagonal $[i][i] = 0.0$.

---

## 3. Pemilihan Algoritma & Rationale (Tanggung Jawab: Inaya & Newten - 240024 & 240090)

Kami membandingkan dua pendekatan algoritmik yang bertolak belakang untuk menganalisis trade-off antara efisiensi BBM dan biaya komputasi:

### A. Algoritma Heuristik: Greedy (Nearest Neighbor)
*   **Modul:** [src/greedy_algorithm.py](/src/greedy_algorithm.py)
*   **Mengapa Dipilih:** Sangat cepat dan memakan sumber daya komputasi minimal. Dari titik aktif saat ini, algoritma selalu memilih pelanggan terdekat berikutnya yang belum dikunjungi.
*   **Trade-off:** Rute yang dihasilkan cenderung sub-optimal karena bersifat *lokal-optimum* (tidak memperhitungkan rute sisa).

### B. Algoritma Eksak: Dynamic Programming (Held-Karp)
*   **Modul:** [src/dp_algorithm.py](/src/dp_algorithm.py)
*   **Mengapa Dipilih:** Menjamin temuan rute terpendek secara absolut (global optimum) dengan waktu eksekusi yang jauh lebih efisien dibandingkan Brute Force murni ($O(N!)$).
*   **Trade-off:** Kebutuhan memori dan waktu komputasi tumbuh secara eksponensial seiring bertambahnya jumlah lokasi pelanggan ($N$).

---

## 4. Analisis Kompleksitas (Big-O) (Tanggung Jawab: Inaya & Newten - 240024 & 240090)

### A. Kompleksitas Algoritma Greedy (Nearest Neighbor)
1.  **Kompleksitas Waktu: $\mathcal{O}(N^2)$**
    *   *Penelusuran:* Algoritma memiliki satu loop luar untuk mengunjungi $N - 1$ pelanggan. Di setiap iterasi, loop dalam memeriksa seluruh $N$ kandidat lokasi untuk mencari jarak terpendek yang belum dikunjungi. Total operasi dasar:
        $$(N-1) \times N \approx N^2$$
2.  **Kompleksitas Ruang (Memori): $\mathcal{O}(N)$**
    *   *Penelusuran:* Memori hanya dialokasikan untuk array boolean `dikunjungi` berukuran $N$ dan list `rute` berukuran $N + 1$.

### B. Kompleksitas Algoritma Dynamic Programming (Held-Karp)
1.  **Kompleksitas Waktu: $\mathcal{O}(N^2 \cdot 2^N)$**
    *   *Penelusuran:* State DP didefinisikan sebagai pasangan `(mask, current)`, di mana `mask` merepresentasikan set lokasi yang sudah dikunjungi (dalam format biner $2^N$ kemungkinan) dan `current` adalah node terakhir saat ini ($N$ kemungkinan). Total jumlah *unique states* adalah $N \cdot 2^N$. Pada tiap state, dilakukan transisi ke $N$ node lain. Sehingga total kompleksitas waktunya adalah:
        $$\mathcal{O}(N \cdot 2^N \times N) = \mathcal{O}(N^2 \cdot 2^N)$$
2.  **Kompleksitas Ruang (Memori): $\mathcal{O}(N \cdot 2^N)$**
    *   *Penelusuran:* Tabel *memoization* (kamus memori) perlu menyimpan hasil dari setiap *unique state* yang dikunjungi, yaitu maksimal sebanyak $N \cdot 2^N$ entri. Kedalaman maksimum *recursion call stack* adalah $N$.

---

## 5. Ringkasan Hasil Uji & TCO (Tanggung Jawab: Jovianie - 240010)

Hasil pengujian eksekusi terminal CLI untuk kedua skenario tersimpan secara detail di folder docs:
*   [Output Skenario Subsidi](/docs/subsidy_terminal_output.txt)
*   [Output Skenario Krisis](/docs/crisis_terminal_output.txt)

### Tabel Komparasi Utama ($N = 13$):

| Metrik | GREEDY (Heuristik) | DP / HELD-KARP (Eksak) |
| :--- | :---: | :---: |
| **Jarak Total (km)** | 42.90 km | **38.40 km** |
| **Bensin Habis (Liter)** | 1.3593 L | **1.2304 L** |
| **Waktu Running (ms)** | **0.019 ms** | 75.92 ms |
| **Biaya Server (Subsidi & Krisis)** | **Rp 1** | Rp 3.796 |
| **TCO Skenario Subsidi (BBM Rp5.000)** | **Rp 6.798** | Rp 10.244 |
| **TCO Skenario Krisis (BBM Rp20.000)** | **Rp 27.188** | Rp 28.469 |

*Catatan: Rumus rasio bensin pada lintasan dihitung secara dinamis mengikuti penurunan beban muatan kurir:*
$$\text{Rasio BBM} = 0.02 + 0.03 \times \left( \frac{\text{Beban Sisa}}{\text{Beban Total}} \right) \text; L/km$$

---

## 6. Kesimpulan Keputusan Bisnis & Titik Impas (Break-Even) (Tanggung Jawab: Jovianie - 240010)

Bagian ini merumuskan rekomendasi bisnis bagi manajemen berdasarkan kalkulasi finansial TCO:

1.  **Skenario BBM Bersubsidi (Rp 5.000 / Liter):**
    Manajemen direkomendasikan untuk **tetap bertahan menggunakan Algoritma Greedy (A)**. Selisih penghematan bensin dari DP (sebesar 0.1289 Liter atau setara Rp 645) tidak sebanding dengan tingginya biaya sewa cloud server (*pay-as-you-go*) sebesar Rp 3.796 yang disebabkan oleh waktu komputasi 75.92 ms.
2.  **Skenario Krisis BBM (Rp 20.000 / Liter):**
    Meskipun harga BBM melambung tinggi, **Algoritma Greedy (A) secara keseluruhan masih sedikit lebih murah** (selisih TCO Rp 1.282) dibanding DP. Hal ini karena efisiensi BBM yang dihasilkan oleh DP (sebesar Rp 2.579) masih lebih rendah dibanding biaya komputasi cloud servernya.
3.  **Analisis Titik Impas (Break-Even Point) BBM:**
    Agar investasi pada Algoritma Eksak (DP) ini menjadi menguntungkan secara finansial, harga BBM dunia nyata harus melampaui **Rp 29.945 / Liter** (atau dibulatkan menjadi **Rp 30.000 / Liter**):
    $$\text{Titik Impas BBM} = \frac{\text{Biaya Server DP} - \text{Biaya Server Greedy}}{\text{Hemat Bensin (Liter)}} = \frac{\text{Rp } 3.796 - \text{Rp } 1}{0.1289 \text{ L}} \approx \text{Rp } 29.945/\text{Liter}$$
    
    *Rekomendasi Strategis:* Jika harga BBM di bawah Rp 30.000/liter, perusahaan harus menggunakan **Algoritma Greedy**. Namun, jika di masa depan perusahaan melayani lebih banyak pelanggan ($N \ge 15$) dan harga minyak melambung tinggi di atas Rp 30.000/liter, transisi ke **Algoritma DP** sangat dianjurkan, dengan catatan program DP harus dioptimalkan (misal dengan bahasa C/C++) agar running time berada di bawah **50 ms** untuk mereduksi tagihan server.
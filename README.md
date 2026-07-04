# Sistem Pengelolaan Produk dan Stok

Program CLI berbasis **Python murni** untuk mengelola data produk dan stok, dilengkapi analisis perbandingan kinerja **Linear Search vs Hash Search** — tugas mata kuliah Analisis Algoritma.

## Fitur

- **Pilih Dataset** — muat file CSV dari folder `dataset/` (100, 500, 1000, 5000 produk)
- **CRUD Produk** — Tambah, Lihat, Update, Hapus data produk
- **Pencarian** — Cari produk menggunakan dua algoritma berbeda:
  - *Linear Search* — periksa satu per satu dari awal list
  - *Hash Search* — akses langsung via Dictionary (hash table)
- **Benchmark** — uji dan bandingkan waktu eksekusi + jumlah iterasi kedua algoritma
- **Export CSV** — simpan hasil benchmark ke file

## Struktur Proyek

```
├── main.py            # Menu utama (CLI loop)
├── algoritma.py       # Implementasi Linear Search & Hash Search
├── models.py          # Class Product (model data)
├── struktur_data.py   # DataManager — kelola List + Dictionary
├── dataset_io.py      # Baca file CSV, daftar dataset
├── testing.py         # Benchmark dan analisis Big O
├── dataset/
│   ├── products_100.csv
│   ├── products_500.csv
│   ├── products_1000.csv
│   └── products_5000.csv
└── README.md
```

## Cara Menjalankan

```bash
python main.py
```

Pastikan file CSV dataset tersedia di folder `dataset/`. Program akan mendeteksinya secara otomatis.

## Algoritma

| Algoritma | Best Case | Average Case | Worst Case | Memori |
|-----------|-----------|--------------|------------|--------|
| Linear Search | O(1) | O(n) | O(n) | O(1) |
| Hash Search | O(1) | O(1) | O(n)\* | O(n) |

\*Worst case teoritis saat terjadi collision parah. Python menangani collision dengan sangat baik sehingga hampir tidak pernah terjadi.

## Teknologi

- Python 3 — tanpa framework, database, atau GUI
- Modul bawaan: `csv`, `time`, `os`

## Dataset

4 file CSV dengan format:

```
kode_produk,nama_produk,kategori,harga,stok
PRD0001,Kabel USB,Elektronik,15000,50
```

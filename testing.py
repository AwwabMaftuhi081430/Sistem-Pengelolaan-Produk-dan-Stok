import time
import csv
import os
from models import Product
from struktur_data import DataManager
from algoritma import linear_search, hash_search
from dataset_io import baca_dataset, daftar_dataset


def _dataset_tersedia() -> list[tuple[str, str]]:
    tersedia = daftar_dataset()
    hasil = []
    for nama, path, jumlah in tersedia:
        hasil.append((path, str(jumlah)))
    return hasil


JUMLAH_PENGUJIAN = 5


def benchmark() -> list[dict]:
    hasil = []

    for path, label in _dataset_tersedia():
        print(f"  Benchmark dataset {label} produk...", end=" ", flush=True)

        daftar_produk = baca_dataset(path)
        dm = DataManager()
        dm.muat_data(daftar_produk)

        langkah_linear_total = 0
        langkah_hash_total = 0

        waktu_linear = []
        waktu_hash = []

        for _ in range(JUMLAH_PENGUJIAN):
            kode_target = daftar_produk[len(daftar_produk) // 2].kode_produk

            mulai = time.perf_counter()
            _, langkah_l = linear_search(dm.produk_list, kode_target)
            selesai = time.perf_counter()
            waktu_linear.append(selesai - mulai)
            langkah_linear_total += langkah_l

            mulai = time.perf_counter()
            _, langkah_h = hash_search(dm.produk_dict, kode_target)
            selesai = time.perf_counter()
            waktu_hash.append(selesai - mulai)
            langkah_hash_total += langkah_h

        hasil.append({
            "dataset": label,
            "jumlah_data": len(daftar_produk),
            "linear_rata": sum(waktu_linear) / len(waktu_linear),
            "linear_tercepat": min(waktu_linear),
            "linear_terlambat": max(waktu_linear),
            "linear_langkah": langkah_linear_total // JUMLAH_PENGUJIAN,
            "hash_rata": sum(waktu_hash) / len(waktu_hash),
            "hash_tercepat": min(waktu_hash),
            "hash_terlambat": max(waktu_hash),
            "hash_langkah": langkah_hash_total // JUMLAH_PENGUJIAN,
        })

        print("OK")

    return hasil


def tampilkan_benchmark(hasil: list[dict]) -> None:
    print()
    print("=" * 95)
    print("HASIL BENCHMARK")
    print("=" * 95)

    header = (
        f"{'Dataset':<10} {'Algoritma':<18} {'Rata-rata':<15} "
        f"{'Tercepat':<15} {'Terlambat':<15} {'Langkah':<10}"
    )
    print(header)
    print("-" * 95)

    for h in hasil:
        print(
            f"{'':<10} {'Linear Search':<18} "
            f"{h['linear_rata']* 1e3:<15.4f} "
            f"{h['linear_tercepat']* 1e3:<15.4f} "
            f"{h['linear_terlambat']* 1e3:<15.4f} "
            f"{h['linear_langkah']:<10}"
        )

        print(
            f"{h['dataset'] + ' data':<10} {'Hash Search':<18} "
            f"{h['hash_rata']* 1e3:<15.4f} "
            f"{h['hash_tercepat']* 1e3:<15.4f} "
            f"{h['hash_terlambat']* 1e3:<15.4f} "
            f"{h['hash_langkah']:<10}"
        )
        print("-" * 95)

    print("Satuan waktu: ms (1 detik = 1.000 ms)")
    print()


def tampilkan_analisis(hasil: list[dict]) -> None:
    data_linear = {}
    data_hash = {}
    for h in hasil:
        data_linear[int(h["dataset"])] = h["linear_rata"]
        data_hash[int(h["dataset"])] = h["hash_rata"]

    print("=" * 95)
    print("ANALISIS ALGORITMA")
    print("=" * 95)

    print()
    print("=" * 95)
    print("1. LINEAR SEARCH")
    print("=" * 95)
    print()
    print("CARA KERJA:")
    print("  Linear Search bekerja dengan memeriksa setiap elemen")
    print("  dalam list satu per satu, dari awal hingga akhir.")
    print("  Bayangkan Anda mencari kartu nama dalam setumpuk --")
    print("  Anda lihat kartu pertama, kedua, ketiga... sampai ketemu.")
    print()
    h_terbesar = max(hasil, key=lambda h: int(h["dataset"]))
    n_terbesar = int(h_terbesar["dataset"])

    print("  Ilustrasi:")
    print(f"    List: [PRD0001, PRD0002, PRD0003, ..., PRD{n_terbesar:04d}]")
    print(f"    Cari: PRD{n_terbesar // 2:04d}")
    print(f"    Langkah: 1 -> 2 -> 3 -> ... -> {n_terbesar // 2} (ketemu!)")
    print()

    print(f"  Dataset terbesar ({n_terbesar} data):")
    print(f"    Rata-rata : {h_terbesar['linear_rata']* 1e3:.2f} ms")
    print(f"    Tercepat  : {h_terbesar['linear_tercepat']* 1e3:.2f} ms")
    print(f"    Terlambat : {h_terbesar['linear_terlambat']* 1e3:.2f} ms")
    print(f"    Langkah   : {h_terbesar['linear_langkah']} iterasi")
    print()
    print("  Pola waktu:")
    for ukuran in sorted(data_linear.keys()):
        print(f"    {ukuran:>5} data -> {data_linear[ukuran]* 1e3:.2f} ms")
    print()

    analisis_linear = """
  BEST CASE: O(1)  -- Terjadi ketika produk yang dicari ada di
                       posisi pertama list. Hanya perlu 1 langkah.

  AVERAGE CASE: O(n) -- Rata-rata, produk berada di tengah list.
                       Perlu n/2 langkah. Karena O(n) dibaca
                       "linear" -- waktu bertambah seiring data.

  WORST CASE: O(n)   -- Terjadi ketika produk berada di posisi
                       terakhir atau tidak ada sama sekali.
                       Harus memeriksa seluruh n elemen.

  BIG O: O(n)
         Waktu eksekusi berbanding lurus dengan jumlah data.
         Jika data 2x lipat, waktu juga ~2x lipat.

  PENGGUNAAN MEMORI: O(1) -- hanya menggunakan variabel counter,
                              tidak perlu memori tambahan.

  KELEBIHAN:
    - Sederhana, mudah diimplementasikan
    - Tidak perlu struktur data tambahan
    - Bisa digunakan pada data yang tidak terurut
    - Cocok untuk dataset kecil (< 100 data)

  KEKURANGAN:
    - Lambat untuk dataset besar
    - Semakin banyak data, semakin lama waktu pencarian
    - Tidak efisien jika banyak operasi pencarian
"""
    print(analisis_linear)

    print("=" * 95)
    print("2. HASH SEARCH")
    print("=" * 95)
    print()
    print("CARA KERJA:")
    print("  Hash Search menggunakan Dictionary (hash table).")
    print("  Setiap kode_produk diubah menjadi nilai hash (angka unik)")
    print("  oleh fungsi hash(). Nilai hash ini menentukan 'laci'")
    print("  tempat produk disimpan. Saat mencari, Python tinggal")
    print("  hitung hash kode yang dicari, buka laci yang sesuai,")
    print("  dan langsung dapatkan produknya.")
    print()
    print("  Ilustrasi:")
    print("    Dictionary: {'PRD0001': <objek>, 'PRD0002': <objek>, ...}")
    print(f"    Cari: 'PRD{n_terbesar // 2:04d}'")
    print(f"    hash('PRD{n_terbesar // 2:04d}') -> 12345678 (contoh)")
    print("    langsung akses dictionary[12345678] -> dapat produk!")
    print()

    print(f"  Dataset terbesar ({n_terbesar} data):")
    print(f"    Rata-rata : {h_terbesar['hash_rata']* 1e3:.2f} ms")
    print(f"    Tercepat  : {h_terbesar['hash_tercepat']* 1e3:.2f} ms")
    print(f"    Terlambat : {h_terbesar['hash_terlambat']* 1e3:.2f} ms")
    print(f"    Langkah   : {h_terbesar['hash_langkah']} iterasi (1)")
    print()
    print("  Pola waktu:")
    for ukuran in sorted(data_hash.keys()):
        print(f"    {ukuran:>5} data -> {data_hash[ukuran]* 1e3:.2f} ms")
    print()

    analisis_hash = """
  BEST CASE: O(1)  -- Tidak ada tabrakan hash (collision).
                       Langsung dapat di bucket yang tepat.

  AVERAGE CASE: O(1) -- Rata-rata, akses ke hash table langsung
                        menuju bucket yang benar. Waktu konstan.

  WORST CASE: O(n)   -- Teoritis: jika semua key memiliki hash
                        yang SAMA (collision parah), semua produk
                        ada di satu bucket -- jadi seperti linear
                        search. Namun, Python menangani collision
                        dengan sangat baik, jadi hampir tidak
                        pernah terjadi.

  BIG O: O(1) rata-rata
         Waktu eksekusi KONSTAN, tidak peduli berapa jumlah data.
         100 data atau 1.000.000 data -- waktunya tetap sama.

  PENGGUNAAN MEMORI: O(n) -- Hash table membutuhkan memori tambahan
                              untuk menyimpan struktur bucket.

  KELEBIHAN:
    - Sangat cepat -- akses langsung tanpa loop
    - Waktu konstan meski data sangat besar
    - Cocok untuk dataset besar dan sering dicari

  KEKURANGAN:
    - Membutuhkan memori tambahan untuk hash table
    - Key harus unik (tidak bisa duplikat kode_produk)
    - Tidak bisa mencari berdasarkan sebagian kata/kode
"""
    print(analisis_hash)

    print("=" * 95)
    print("3. PERBANDINGAN DAN KESIMPULAN")
    print("=" * 95)
    print()
    print("  KAPAN MENGGUNAKAN LINEAR SEARCH:")
    print("    - Dataset kecil (< 100 data)")
    print("    - Data tidak memiliki identifier unik")
    print("    - Pencarian hanya dilakukan sesekali")
    print("    - Memori terbatas")
    print("    - Belum/tidak ingin membangun struktur tambahan")
    print()
    print("  KAPAN MENGGUNAKAN HASH SEARCH:")
    print("    - Dataset besar (ratusan ribu hingga jutaan)")
    print("    - Pencarian sangat sering dilakukan")
    print("    - Membutuhkan respon cepat")
    print("    - Ada identifier unik (kode_produk)")
    print("    - Memori tidak menjadi masalah")
    print()
    print("  KESIMPULAN:")
    print("    Hash Search JAUH lebih cepat dari Linear Search")
    print("    untuk dataset besar. Perbedaan waktu semakin")
    print("    signifikan seiring bertambahnya jumlah data.")
    print("    Namun, Linear Search tetap berguna karena")
    print("    kesederhanaannya -- tidak perlu memori tambahan")
    print("    dan mudah di-debug jika ada masalah.")
    print()


def export_csv(hasil: list[dict], nama_file: str = "hasil_benchmark.csv") -> None:
    with open(nama_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Dataset",
            "Jumlah Data",
            "Linear Rata-rata (detik)",
            "Linear Tercepat (detik)",
            "Linear Terlambat (detik)",
            "Linear Langkah",
            "Hash Rata-rata (detik)",
            "Hash Tercepat (detik)",
            "Hash Terlambat (detik)",
            "Hash Langkah",
        ])
        for h in hasil:
            writer.writerow([
                h["dataset"],
                h["jumlah_data"],
                f"{h['linear_rata']:.10f}",
                f"{h['linear_tercepat']:.10f}",
                f"{h['linear_terlambat']:.10f}",
                h["linear_langkah"],
                f"{h['hash_rata']:.10f}",
                f"{h['hash_tercepat']:.10f}",
                f"{h['hash_terlambat']:.10f}",
                h["hash_langkah"],
            ])
    print(f"  Hasil benchmark diekspor ke: {nama_file}")

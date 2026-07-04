import os
from models import Product
from struktur_data import DataManager
from dataset_io import baca_dataset, daftar_dataset
from testing import benchmark, tampilkan_benchmark, tampilkan_analisis, export_csv
from algoritma import linear_search


data_manager = DataManager()
dataset_terpilih = ""
jumlah_data_terpilih = 0


def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")


def tunggu_enter():
    input("\nTekan Enter untuk kembali ke menu...")


def tampilkan_header():
    print("=" * 60)
    print("  SISTEM PENGELOLAAN PRODUK DAN STOK")
    print("  Analisis Algoritma -- Linear Search vs Hash Search")
    print("=" * 60)
    if dataset_terpilih:
        print(f"  Dataset aktif: {dataset_terpilih} "
              f"({jumlah_data_terpilih} produk)")
    else:
        print("  Dataset aktif: BELUM DIPILIH")
    print("-" * 60)


def format_harga(harga: int) -> str:
    return f"Rp{harga:,}"


def menu_pilih_dataset():
    global dataset_terpilih, jumlah_data_terpilih, data_manager

    bersihkan_layar()
    tampilkan_header()
    print("\n  PILIH DATASET")
    print("-" * 60)

    tersedia = daftar_dataset()

    if not tersedia:
        print("  TIDAK ADA dataset di folder 'dataset/'.")
        print("  Pastikan file CSV tersedia.")
        tunggu_enter()
        return

    for i, (nama, path, jumlah) in enumerate(tersedia, 1):
        print(f"  {i}. {nama} ({jumlah} produk)")

    print(f"  0. Kembali")

    try:
        pilihan = int(input("\n  Pilih nomor dataset: "))
        if pilihan == 0:
            return
        if 1 <= pilihan <= len(tersedia):
            nama, path, jumlah = tersedia[pilihan - 1]

            print(f"\n  Membaca {nama}...", end=" ")
            daftar_produk = baca_dataset(path)
            data_manager = DataManager()
            data_manager.muat_data(daftar_produk)

            dataset_terpilih = nama
            jumlah_data_terpilih = jumlah
            print(f"OK ({jumlah} produk dimuat)")
        else:
            print("\n  Pilihan tidak valid.")
    except ValueError:
        print("\n  Masukkan angka yang valid.")

    tunggu_enter()


def menu_lihat_semua():
    bersihkan_layar()
    tampilkan_header()

    if not dataset_terpilih:
        print("\n  Pilih dataset terlebih dahulu (Menu 1).")
        tunggu_enter()
        return

    produk_list = data_manager.dapatkan_semua()

    if not produk_list:
        print("\n  Tidak ada produk.")
        tunggu_enter()
        return

    print("\n  DAFTAR SEMUA PRODUK")
    print(f"  Total: {len(produk_list)} produk")
    print("-" * 60)

    print(f"  {'Kode':<12} {'Nama':<25} {'Kategori':<22} "
          f"{'Harga':<15} {'Stok':<8}")
    print("  " + "-" * 80)

    for p in produk_list:
        print(f"  {p.kode_produk:<12} {p.nama_produk:<25} "
              f"{p.kategori:<22} {format_harga(p.harga):<15} "
              f"{p.stok:<8}")

    print("  " + "-" * 80)
    print(f"  Total: {len(produk_list)} produk")

    tunggu_enter()


def menu_tambah():
    bersihkan_layar()
    tampilkan_header()

    if not dataset_terpilih:
        print("\n  Pilih dataset terlebih dahulu (Menu 1).")
        tunggu_enter()
        return

    print("\n  TAMBAH PRODUK BARU")
    print("-" * 60)

    kode = input("  Kode produk   : ").strip()
    if not kode:
        print("\n  Kode produk tidak boleh kosong.")
        tunggu_enter()
        return

    if data_manager.dapatkan(kode):
        print(f"\n  Kode '{kode}' sudah ada! Gunakan menu Update.")
        tunggu_enter()
        return

    nama = input("  Nama produk   : ").strip()
    kategori = input("  Kategori      : ").strip()

    try:
        harga = int(input("  Harga         : "))
        stok = int(input("  Stok          : "))
    except ValueError:
        print("\n  Harga dan stok harus berupa angka.")
        tunggu_enter()
        return

    if harga < 0 or stok < 0:
        print("\n  Harga dan stok tidak boleh negatif.")
        tunggu_enter()
        return

    produk_baru = Product(kode, nama, kategori, harga, stok)
    data_manager.tambah(produk_baru)

    print(f"\n  Produk '{kode}' berhasil ditambahkan!")

    tunggu_enter()


def menu_cari_linear():
    bersihkan_layar()
    tampilkan_header()

    if not dataset_terpilih:
        print("\n  Pilih dataset terlebih dahulu (Menu 1).")
        tunggu_enter()
        return

    print("\n  CARI PRODUK -- Linear Search")
    print("-" * 60)

    kode = input("  Masukkan kode produk: ").strip()
    if not kode:
        print("\n  Kode produk tidak boleh kosong.")
        tunggu_enter()
        return

    print(f"\n  Mencari '{kode}' dengan Linear Search...")

    import time
    mulai = time.perf_counter()
    produk, iterasi = linear_search(data_manager.produk_list, kode)
    selesai = time.perf_counter()
    waktu = (selesai - mulai) * 1e3

    print(f"  Waktu: {waktu:.2f} ms")
    print(f"  Iterasi: {iterasi}")
    print()

    if produk:
        print("  PRODUK DITEMUKAN:")
        print("-" * 40)
        print(produk)
    else:
        print(f"  Produk dengan kode '{kode}' TIDAK DITEMUKAN.")

    tunggu_enter()


def menu_cari_hash():
    bersihkan_layar()
    tampilkan_header()

    if not dataset_terpilih:
        print("\n  Pilih dataset terlebih dahulu (Menu 1).")
        tunggu_enter()
        return

    print("\n  CARI PRODUK -- Hash Search (Dictionary)")
    print("-" * 60)

    kode = input("  Masukkan kode produk: ").strip()
    if not kode:
        print("\n  Kode produk tidak boleh kosong.")
        tunggu_enter()
        return

    print(f"\n  Mencari '{kode}' dengan Hash Search...")

    import time
    mulai = time.perf_counter()
    produk = data_manager.dapatkan(kode)
    selesai = time.perf_counter()
    waktu = (selesai - mulai) * 1e3

    print(f"  Waktu: {waktu:.2f} ms")
    print(f"  Iterasi: 1 (akses langsung via hash table)")
    print()

    if produk:
        print("  PRODUK DITEMUKAN:")
        print("-" * 40)
        print(produk)
    else:
        print(f"  Produk dengan kode '{kode}' TIDAK DITEMUKAN.")

    tunggu_enter()


def menu_update():
    bersihkan_layar()
    tampilkan_header()

    if not dataset_terpilih:
        print("\n  Pilih dataset terlebih dahulu (Menu 1).")
        tunggu_enter()
        return

    print("\n  UPDATE PRODUK")
    print("-" * 60)

    kode = input("  Masukkan kode produk: ").strip()

    produk = data_manager.dapatkan(kode)
    if not produk:
        print(f"\n  Produk dengan kode '{kode}' TIDAK DITEMUKAN.")
        tunggu_enter()
        return

    print("\n  Data saat ini:")
    print(produk)
    print()

    nama = input(f"  Nama baru [{produk.nama_produk}]: ").strip()
    kategori = input(f"  Kategori baru [{produk.kategori}]: ").strip()

    try:
        harga_input = input(f"  Harga baru [{produk.harga}]: ").strip()
        harga = int(harga_input) if harga_input else None
    except ValueError:
        print("\n  Harga harus angka. Data tidak diubah.")
        tunggu_enter()
        return

    try:
        stok_input = input(f"  Stok baru [{produk.stok}]: ").strip()
        stok = int(stok_input) if stok_input else None
    except ValueError:
        print("\n  Stok harus angka. Data tidak diubah.")
        tunggu_enter()
        return

    nama = nama if nama else None
    kategori = kategori if kategori else None

    berhasil = data_manager.update(kode, nama, kategori, harga, stok)
    if berhasil:
        print(f"\n  Produk '{kode}' berhasil diupdate!")
    else:
        print(f"\n  Gagal mengupdate produk '{kode}'.")

    tunggu_enter()


def menu_hapus():
    bersihkan_layar()
    tampilkan_header()

    if not dataset_terpilih:
        print("\n  Pilih dataset terlebih dahulu (Menu 1).")
        tunggu_enter()
        return

    print("\n  HAPUS PRODUK")
    print("-" * 60)

    kode = input("  Masukkan kode produk: ").strip()

    produk = data_manager.dapatkan(kode)
    if not produk:
        print(f"\n  Produk dengan kode '{kode}' TIDAK DITEMUKAN.")
        tunggu_enter()
        return

    print("\n  Data yang akan dihapus:")
    print(produk)
    print()

    konfirmasi = input(f"  Yakin hapus {kode}? (y/n): ").strip().lower()
    if konfirmasi != "y":
        print("  Penghapusan dibatalkan.")
        tunggu_enter()
        return

    berhasil = data_manager.hapus(kode)
    if berhasil:
        print(f"\n  Produk '{kode}' berhasil dihapus!")
    else:
        print(f"\n  Gagal menghapus produk '{kode}'.")

    tunggu_enter()


def menu_benchmark():
    bersihkan_layar()
    tampilkan_header()

    print("\n  BENCHMARK")
    print("-" * 60)
    print("  Akan menjalankan pengujian pada 4 dataset:")
    print("   - 100 produk")
    print("   - 500 produk")
    print("   - 1000 produk")
    print("   - 5000 produk")
    print("  Masing-masing diuji 5 kali.")
    print()

    konfirmasi = input("  Jalankan benchmark? (y/n): ").strip().lower()
    if konfirmasi != "y":
        print("  Benchmark dibatalkan.")
        tunggu_enter()
        return

    print()
    hasil = benchmark()
    tampilkan_benchmark(hasil)
    tampilkan_analisis(hasil)
    tunggu_enter()


def menu_export():
    bersihkan_layar()
    tampilkan_header()

    print("\n  EXPORT BENCHMARK KE CSV")
    print("-" * 60)

    if not os.path.exists("hasil_benchmark.csv"):
        print("  Menjalankan benchmark terlebih dahulu...")
        hasil = benchmark()
        export_csv(hasil)
    else:
        print("  File 'hasil_benchmark.csv' sudah ada.")
        konfirmasi = input("  Jalankan ulang benchmark? (y/n): ").strip().lower()
        if konfirmasi == "y":
            print()
            hasil = benchmark()
            export_csv(hasil)
        else:
            print("  Menggunakan file yang sudah ada.")

    print("\n  File 'hasil_benchmark.csv' siap digunakan.")
    tunggu_enter()


def menu_tentang():
    bersihkan_layar()
    tampilkan_header()

    print("""
  TENTANG PROGRAM
  ----------------
  Nama    : Sistem Pengelolaan Produk dan Stok
  Tujuan  : Tugas Mata Kuliah Analisis Algoritma

  ALGORITMA:
    1. Linear Search  -- mencari dengan cek satu per satu
    2. Hash Search    -- mencari menggunakan Dictionary (hash table)

  STRUKTUR DATA:
    1. List       -- penyimpanan utama produk
    2. Dictionary -- indeks cepat berdasarkan kode_produk

  DATASET:
    - 4 file CSV di folder dataset/
    - 100, 500, 1000, 5000 produk

  TEKNOLOGI:
    Python murni -- tanpa framework, database, atau GUI
""")
    tunggu_enter()


def main():
    while True:
        bersihkan_layar()
        tampilkan_header()

        print("""
  MENU UTAMA
  -------------------------------------------
   1. Pilih Dataset
   2. Lihat Semua Produk
   3. Tambah Produk
   4. Cari Produk (Linear Search)
   5. Cari Produk (Hash Search)
   6. Update Produk
   7. Hapus Produk
   8. Benchmark
   9. Export Benchmark ke CSV
  10. Tentang Program
   0. Keluar
  -------------------------------------------
""")

        try:
            pilihan = int(input("  Pilih menu: "))
        except ValueError:
            print("\n  Masukkan angka yang valid!")
            tunggu_enter()
            continue

        if pilihan == 1:
            menu_pilih_dataset()
        elif pilihan == 2:
            menu_lihat_semua()
        elif pilihan == 3:
            menu_tambah()
        elif pilihan == 4:
            menu_cari_linear()
        elif pilihan == 5:
            menu_cari_hash()
        elif pilihan == 6:
            menu_update()
        elif pilihan == 7:
            menu_hapus()
        elif pilihan == 8:
            menu_benchmark()
        elif pilihan == 9:
            menu_export()
        elif pilihan == 10:
            menu_tentang()
        elif pilihan == 0:
            print("\n  Terima kasih telah menggunakan program ini.")
            break
        else:
            print("\n  Pilihan tidak valid (0-10).")
            tunggu_enter()


if __name__ == "__main__":
    main()

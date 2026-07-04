import csv
import os
from models import Product


FOLDER_DATASET = "dataset"


def baca_dataset(nama_file: str) -> list[Product]:
    daftar_produk: list[Product] = []

    with open(nama_file, mode="r", newline="", encoding="utf-8") as file_csv:
        pembaca = csv.DictReader(file_csv)

        for baris in pembaca:
            produk = Product(
                kode_produk=baris["kode_produk"].strip(),
                nama_produk=baris["nama_produk"].strip(),
                kategori=baris["kategori"].strip(),
                harga=int(baris["harga"].strip()),
                stok=int(baris["stok"].strip()),
            )
            daftar_produk.append(produk)

    return daftar_produk


def daftar_dataset() -> list[tuple[str, str, int]]:
    tersedia = []

    if not os.path.isdir(FOLDER_DATASET):
        return tersedia

    for nama_file in sorted(os.listdir(FOLDER_DATASET)):
        if nama_file.endswith(".csv"):
            path = os.path.join(FOLDER_DATASET, nama_file)
            with open(path, "r", encoding="utf-8") as f:
                jumlah = sum(1 for _ in f) - 1
            tersedia.append((nama_file, path, jumlah))

    return tersedia

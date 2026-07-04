from models import Product


def linear_search(daftar: list[Product], kode_cari: str) \
        -> tuple[Product | None, int]:
    for i, produk in enumerate(daftar):
        if produk.kode_produk == kode_cari:
            return produk, i + 1
    return None, len(daftar)


def hash_search(indeks: dict[str, Product], kode_cari: str) \
        -> tuple[Product | None, int]:
    produk = indeks.get(kode_cari)
    if produk is not None:
        return produk, 1
    return None, 1

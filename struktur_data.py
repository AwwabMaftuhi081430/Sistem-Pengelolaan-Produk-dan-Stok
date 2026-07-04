from models import Product


class DataManager:
    def __init__(self):
        self.produk_list: list[Product] = []
        self.produk_dict: dict[str, Product] = {}

    def muat_data(self, daftar_produk: list[Product]) -> None:
        self.produk_list = daftar_produk
        self._bangun_dict()

    def _bangun_dict(self) -> None:
        self.produk_dict = {}
        for produk in self.produk_list:
            self.produk_dict[produk.kode_produk] = produk

    def tambah(self, produk: Product) -> None:
        self.produk_list.append(produk)
        self.produk_dict[produk.kode_produk] = produk

    def dapatkan(self, kode_produk: str) -> Product | None:
        return self.produk_dict.get(kode_produk)

    def dapatkan_semua(self) -> list[Product]:
        return self.produk_list

    def update(self, kode_produk: str, nama_baru: str = None,
               kategori_baru: str = None, harga_baru: int = None,
               stok_baru: int = None) -> bool:
        produk = self.produk_dict.get(kode_produk)
        if produk is None:
            return False

        if nama_baru is not None:
            produk.nama_produk = nama_baru
        if kategori_baru is not None:
            produk.kategori = kategori_baru
        if harga_baru is not None:
            produk.harga = harga_baru
        if stok_baru is not None:
            produk.stok = stok_baru

        return True

    def hapus(self, kode_produk: str) -> bool:
        if kode_produk not in self.produk_dict:
            return False

        del self.produk_dict[kode_produk]

        for i, produk in enumerate(self.produk_list):
            if produk.kode_produk == kode_produk:
                self.produk_list.pop(i)
                break

        return True

    def panjang(self) -> int:
        return len(self.produk_list)

    def kosongkan(self) -> None:
        self.produk_list.clear()
        self.produk_dict.clear()

    def cari_di_list(self, kode_produk: str) -> Product | None:
        for produk in self.produk_list:
            if produk.kode_produk == kode_produk:
                return produk
        return None

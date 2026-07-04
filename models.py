class Product:
    def __init__(self, kode_produk: str, nama_produk: str,
                 kategori: str, harga: int, stok: int):
        self.kode_produk = kode_produk
        self.nama_produk = nama_produk
        self.kategori = kategori
        self.harga = harga
        self.stok = stok

    def __str__(self) -> str:
        return (
            f"Kode    : {self.kode_produk}\n"
            f"Nama    : {self.nama_produk}\n"
            f"Kategori: {self.kategori}\n"
            f"Harga   : Rp{self.harga:,}\n"
            f"Stok    : {self.stok} unit"
        )

    def to_dict(self) -> dict:
        return {
            "kode_produk": self.kode_produk,
            "nama_produk": self.nama_produk,
            "kategori": self.kategori,
            "harga": self.harga,
            "stok": self.stok,
        }

    def to_list(self) -> list:
        return [self.kode_produk, self.nama_produk,
                self.kategori, self.harga, self.stok]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return False
        return self.kode_produk == other.kode_produk

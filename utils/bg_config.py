import os

# ==========================================
# FOLDER BACKGROUND
# ==========================================
BG_FOLDER = "bg"

# ==========================================
# DAFTAR BACKGROUND
# ==========================================
BG_MAP = {
    "Tirai Hitam": "black.jpg",
    "Tirai Biru": "blue.jpg",
    "Tirai Perunggu": "bronze.jpg",
    "Tirai Denim": "denim.jpg",
    "Tirai Navy": "navy.jpg",
    "Koran": "newspaper.jpg",
    "Kotak-kotak": "plaid.jpg",
    "Tirai Merah": "red.jpg",
    "American Yearbook": "usyearbook.jpg",
    "Tirai Putih": "white.jpg",
    "Wood": "wood.jpg",
    "Yellow Stained": "yellow.jpg",
}

# ==========================================
# PILIHAN BACKGROUND UNTUK SIDEBAR
# ==========================================
BACKGROUND_OPTIONS = (
    list(BG_MAP.keys())
    + [
        "Warna Solid Pasfoto",
        "Transparan (PNG)"
    ]
)


# ==========================================
# AMBIL PATH BACKGROUND
# ==========================================
def get_bg_path(bg_name: str):
    """
    Mengembalikan path file background.

    Parameters
    ----------
    bg_name : str
        Nama background yang dipilih user.

    Returns
    -------
    str | None
        Path background jika ada,
        None jika bukan background gambar.
    """

    filename = BG_MAP.get(bg_name)

    if filename is None:
        return None

    return os.path.join(BG_FOLDER, filename)
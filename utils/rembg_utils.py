from rembg import remove
from PIL import Image
import io
import hashlib
import streamlit as st
import time # 1. Tambahkan library time untuk menghitung durasi inferensi
from rembg import remove, new_session


# ==========================================
# MEMBETULKAN ORIENTASI FOTO
# ==========================================
def fix_image_orientation(image: Image.Image) -> Image.Image:
    """
    Memperbaiki orientasi foto berdasarkan EXIF.
    Berguna untuk foto dari HP yang kadang terbalik.
    """
    try:
        return Image.Image.exif_transpose(image)
    except:
        return image


# ==========================================
# MEMBUAT HASH GAMBAR
# ==========================================
def get_image_hash(image: Image.Image) -> str:
    """
    Membuat hash unik dari gambar
    untuk kebutuhan cache.
    """
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return hashlib.md5(buffer.getvalue()).hexdigest()


# ==========================================
# REMOVE BACKGROUND DENGAN REMBG (CACHED)
# ==========================================
@st.cache_data(show_spinner=False)
def remove_background_cached(image_bytes: bytes):
    """
    Menjalankan rembg menggunakan model khusus manusia (u2net_human_seg)
    atau isnet-general-use untuk memisahkan objek tiang/dinding secara presisi.
    """
    # Langkah 1: Inisialisasi session model yang lebih cerdas
    # Pilihan alternatif jika 'u2net_human_seg' kurang, ganti dengan 'isnet-general-use'
    session = new_session(model_name="u2net_human_seg") 
    
    # Langkah 2: Jalankan pemotongan dengan session tersebut
    output = remove(
        image_bytes,
        session=session,
        alpha_matting=False # Matikan matting dulu agar fokus ke bentuk objek utama
    )
    return output


# ==========================================
# FUNGSI UTAMA DENGAN PENCATATAN STATISTIK (DASHBOARD COMPATIBLE)
# ==========================================
def remove_background(image: Image.Image) -> Image.Image:
    """
    Menghapus background gambar, menghasilkan foreground transparan,
    sekaligus mencatat metrik inferensi ke session_state untuk Dashboard.
    """
    # Mulai hitung stopwatch tepat sebelum pemrosesan AI dimulai
    start_time = time.time()

    image = fix_image_orientation(image)
    image = image.convert("RGB")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    # Eksekusi Model Deep Learning U²-Net
    output_bytes = remove_background_cached(image_bytes)

    # Hentikan stopwatch setelah AI selesai memproses gambar
    end_time = time.time()
    inference_duration = end_time - start_time

    # --- INTEGRASI KE SESSION STATE DASHBOARD ---
    # 1. Simpan durasi inferensi terakhir
    st.session_state.last_inference_time = inference_duration

    # 2. Tambahkan ke riwayat rekam jejak untuk grafik tren (maksimal simpan 20 data agar memori hemat)
    if "inference_history" not in st.session_state:
        st.session_state.inference_history = []
    
    # Hanya masukkan jika data waktu valid dan bukan duplikasi instan akibat rerun
    if len(st.session_state.inference_history) == 0 or inference_duration != st.session_state.inference_history[-1]:
        st.session_state.inference_history.append(inference_duration)
        if len(st.session_state.inference_history) > 20:
            st.session_state.inference_history.pop(0)

    # 3. Naikkan angka total gambar yang berhasil diuji selama pameran
    if "total_processed_images" not in st.session_state:
        st.session_state.total_processed_images = 0
    st.session_state.total_processed_images += 1
    # --------------------------------------------

    foreground = Image.open(
        io.BytesIO(output_bytes)
    ).convert("RGBA")

    return foreground


# ==========================================
# KECILKAN GAMBAR UNTUK INFERENSI
# ==========================================
def prepare_image(
    image: Image.Image,
    max_size=(1000, 1000)
):
    """
    Mengecilkan gambar agar rembg lebih cepat.
    """
    image = image.copy()
    image.thumbnail(
        max_size,
        Image.Resampling.LANCZOS
    )
    return image
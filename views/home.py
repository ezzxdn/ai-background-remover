import streamlit as st

def home_page():

    st.title("🖼️ AI Background Remover")

    st.subheader(
        "Implementasi AI Background Remover Berbasis Web"
    )

    st.markdown(
        """
**Nama Mahasiswa:** Ezza Addini

**Deskripsi Singkat:**

Aplikasi ini memanfaatkan teknologi Artificial Intelligence
berbasis model U²-Net melalui library rembg untuk melakukan
segmentasi objek dan menghapus background foto secara otomatis.

Pengguna dapat mengunggah gambar, memperoleh hasil background
removal, mengganti background sesuai kebutuhan, serta mengunduh
hasil akhir dalam berbagai format.

Fitur utama:
- Upload gambar JPG/PNG
- Penghapusan background otomatis
- Penggantian background
- Download hasil PNG transparan
- Download hasil JPG
- Dashboard statistik inferensi
"""
    )
import streamlit as st
from PIL import Image, ImageColor
import io
import time

from utils.rembg_utils import (
    remove_background,
    prepare_image
)

from utils.bg_config import (
    BACKGROUND_OPTIONS,
    get_bg_path
)


# ==========================================
# COMPOSITE BACKGROUND
# ==========================================
def apply_background(
    foreground_rgba,
    bg_choice,
    solid_color="#0090FF"
):
    """
    Menggabungkan foreground transparan
    dengan background pilihan.
    """

    width, height = foreground_rgba.size

    # Transparan
    if bg_choice == "Transparan (PNG)":
        return foreground_rgba

    # Warna solid
    elif bg_choice == "Warna Solid Pasfoto":

        rgb = ImageColor.getrgb(solid_color)

        bg = Image.new(
            "RGBA",
            (width, height),
            rgb + (255,)
        )

        return Image.alpha_composite(
            bg,
            foreground_rgba
        )

    # Background gambar
    else:

        bg_path = get_bg_path(bg_choice)

        try:
            bg = (
                Image.open(bg_path)
                .convert("RGBA")
                .resize(
                    (width, height),
                    Image.Resampling.LANCZOS
                )
            )

        except Exception:
            bg = Image.new(
                "RGBA",
                (width, height),
                (200, 200, 200, 255)
            )

        return Image.alpha_composite(
            bg,
            foreground_rgba
        )


# ==========================================
# HALAMAN REMOVER
# ==========================================
def remover_page():

    st.header("🖼️ AI Background Remover")

    st.caption(
        "Upload foto, hapus background menggunakan rembg, "
        "lalu ganti dengan background pilihan."
    )

    uploaded_file = st.file_uploader(
        "Upload foto",
        type=["jpg", "jpeg", "png"],
        key="rembg_upload"
    )

    if uploaded_file is None:
        st.info("Silakan upload foto terlebih dahulu.")
        return

    # ======================================
    # LOAD IMAGE
    # ======================================
    image = Image.open(uploaded_file)

    image = prepare_image(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Foto Asli")

        st.image(
            image,
            use_container_width=True
        )

    # ======================================
    # REMOVE BACKGROUND
    # ======================================
    start = time.time()

    with st.spinner(
        "AI sedang menghapus background..."
    ):

        foreground = remove_background(image)

    elapsed = time.time() - start

    st.session_state.last_inference_time = elapsed

    st.session_state.total_processed_images += 1

    st.session_state.inference_history.append(
        elapsed
    )


    # ======================================
    # SIDEBAR OPTION
    # ======================================
    bg_choice = st.selectbox(
        "Pilih Background Baru",
        BACKGROUND_OPTIONS,
        key="rembg_bg"
    )

    selected_color = "#0090FF"

    if bg_choice == "Warna Solid Pasfoto":

        selected_color = st.color_picker(
            "Pilih warna",
            "#0090FF",
            key="passport_color"
        )

    # ======================================
    # APPLY BACKGROUND
    # ======================================
    result = apply_background(
        foreground,
        bg_choice,
        selected_color
    )

    with col2:

        st.subheader("✨ Hasil")

        st.image(
            result,
            use_container_width=True
        )

    st.divider()

    # ======================================
    # DOWNLOAD PNG
    # ======================================
    png_buffer = io.BytesIO()

    foreground.save(
        png_buffer,
        format="PNG"
    )

    st.download_button(
        "⬇️ Download PNG Transparan",
        data=png_buffer.getvalue(),
        file_name="background_removed.png",
        mime="image/png",
        use_container_width=True
    )

    # ======================================
    # DOWNLOAD JPG
    # ======================================
    jpg_buffer = io.BytesIO()

    result.convert("RGB").save(
        jpg_buffer,
        format="JPEG",
        quality=95
    )

    st.download_button(
        "⬇️ Download Hasil JPG",
        data=jpg_buffer.getvalue(),
        file_name="edited_photo.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

    st.success(
        "Selesai! Kamu bisa download PNG transparan "
        "atau hasil dengan background baru."
    )
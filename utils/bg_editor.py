from PIL import Image
from rembg import remove
import io
import hashlib
import streamlit as st

from utils.bg_config import get_bg_path


def apply_background(images, bg_name):
    """
    Parameters
    ----------
    images : list[PIL.Image]
        Foto hasil photobox.

    bg_name : str
        Nama background pilihan user.

    Returns
    -------
    list[PIL.Image]
        Foto yang sudah diganti background.
    """

    # ==============================
    # CACHE FOREGROUND
    # ==============================
    if "foreground_cache" not in st.session_state:
        st.session_state.foreground_cache = {}

    cache = st.session_state.foreground_cache

    edited_images = []

    bg_path = get_bg_path(bg_name)

    # kalau background tidak ditemukan
    if bg_path is None:
        return images

    bg = Image.open(bg_path).convert("RGBA")

    for image in images:

        image_rgba = image.convert("RGBA")

        buffer = io.BytesIO()

        image_rgba.save(
            buffer,
            format="PNG"
        )

        input_bytes = buffer.getvalue()

        # hash unik untuk tiap foto
        cache_key = hashlib.md5(
            input_bytes
        ).hexdigest()

        # ==============================
        # REMBG HANYA SEKALI
        # ==============================
        if cache_key not in cache:

            output_bytes = remove(
                input_bytes
            )

            foreground = Image.open(
                io.BytesIO(output_bytes)
            ).convert("RGBA")

            cache[cache_key] = foreground

        foreground = cache[cache_key]

        # resize background
        bg_resized = bg.resize(
            foreground.size
        )

        # gabungkan
        final = Image.alpha_composite(
            bg_resized,
            foreground
        )

        edited_images.append(
            final.convert("RGB")
        )

    return edited_images
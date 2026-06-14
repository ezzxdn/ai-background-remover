from PIL import Image, ImageDraw
import io

# ==========================================
# ANALOG PHOTOSTRIP CONFIG
# ==========================================
PHOTO_WIDTH = 500
PHOTO_HEIGHT = 375      # rasio 4:3

PHOTO_GAP = 20

SIDE_MARGIN = 60
TOP_MARGIN = 50
BOTTOM_MARGIN = 50

FILM_MARK_SIZE = 8
FILM_MARK_GAP = 18


# ==========================================
# MEMBUAT PHOTOSTRIP ANALOG
# ==========================================
def create_photostrip(
    photos,
    frame_style="Putih"
):
    """
    photos : list[PIL.Image]
        Harus berisi tepat 4 foto.

    frame_style :
        "Putih" atau "Hitam"
    """

    if len(photos) != 4:
        raise ValueError(
            "Photostrip membutuhkan tepat 4 foto."
        )

    # ======================================
    # WARNA FRAME
    # ======================================
    if frame_style == "Hitam":
        frame_color = (15, 15, 15)
        mark_color = (235, 235, 235)

    else:
        frame_color = (250, 250, 250)
        mark_color = (25, 25, 25)

    strip_width = (
        PHOTO_WIDTH
        + SIDE_MARGIN * 2
    )

    strip_height = (
        TOP_MARGIN
        + (PHOTO_HEIGHT * 4)
        + (PHOTO_GAP * 3)
        + BOTTOM_MARGIN
    )

    strip = Image.new(
        "RGB",
        (strip_width, strip_height),
        frame_color
    )

    draw = ImageDraw.Draw(strip)

    # ======================================
    # TEMPEL FOTO
    # ======================================
    y = TOP_MARGIN

    for photo in photos:

        photo = photo.convert("RGB")

        photo = photo.resize(
            (PHOTO_WIDTH, PHOTO_HEIGHT),
            Image.Resampling.LANCZOS
        )

        strip.paste(
            photo,
            (
                SIDE_MARGIN,
                y
            )
        )

        y += PHOTO_HEIGHT + PHOTO_GAP

    # ======================================
    # FILM MARK KIRI
    # ======================================
    y_mark = TOP_MARGIN + 15

    while y_mark < strip_height - 15:

        draw.rectangle(
            (
                18,
                y_mark,
                18 + FILM_MARK_SIZE,
                y_mark + FILM_MARK_SIZE
            ),
            fill=mark_color
        )

        y_mark += FILM_MARK_GAP

    # ======================================
    # FILM MARK KANAN
    # ======================================
    y_mark = TOP_MARGIN + 15

    while y_mark < strip_height - 15:

        draw.rectangle(
            (
                strip_width - 18 - FILM_MARK_SIZE,
                y_mark,
                strip_width - 18,
                y_mark + FILM_MARK_SIZE
            ),
            fill=mark_color
        )

        y_mark += FILM_MARK_GAP

    return strip


# ==========================================
# KONVERSI KE BYTES
# ==========================================
def photostrip_to_bytes(
    photostrip,
    quality=95
):
    """
    Mengubah photostrip menjadi bytes JPEG.
    """

    buffer = io.BytesIO()

    photostrip.save(
        buffer,
        format="JPEG",
        quality=quality
    )

    return buffer.getvalue()


# ==========================================
# RESET SESSION CAPTURE
# ==========================================
def reset_capture_state():
    """
    Helper untuk mengosongkan foto
    setelah sesi selesai.
    """

    return []
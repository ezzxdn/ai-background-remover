import cloudinary
import cloudinary.uploader
import cloudinary.utils
import qrcode
import io
from PIL import Image
import streamlit as st


# ==========================================
# KONFIGURASI CLOUDINARY
# ==========================================
cloudinary.config(
    cloud_name="dmwyzklq5",
    api_key="683735498582468",
    api_secret="8fAAsxdBcFDA4UDUS57ib5yhKXU",
    secure=True
)


# ==========================================
# UPLOAD PHOTOSTRIP KE CLOUDINARY
# ==========================================
def upload_photostrip(image):
    """
    Upload PIL Image ke Cloudinary,
    lalu mengembalikan URL download.
    """

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=95
    )

    buffer.seek(0)

    result = cloudinary.uploader.upload(
        buffer,
        folder="ai_photobox",
        resource_type="image",
        format="jpg"
    )

    public_id = result["public_id"]

    # URL download dengan nama file photostrip.jpg
    download_url, _ = cloudinary.utils.cloudinary_url(
        public_id,
        resource_type="image",
        type="upload",
        format="jpg",
        flags="attachment:photostrip"
    )

    return download_url


# ==========================================
# GENERATE QR CODE
# ==========================================
def generate_qr_code(url):

    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=4
    )

    qr.add_data(url)

    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    return qr_image.convert("RGB")


# ==========================================
# TAMPILKAN QR DI STREAMLIT
# ==========================================
def show_download_qr(image):

    with st.spinner(
        "☁️ Mengunggah hasil photobox..."
    ):

        url = upload_photostrip(image)

    qr_image = generate_qr_code(url)

    return url, qr_image
import streamlit as st
import cv2
import av
import time
import numpy as np
import mediapipe as mp
from PIL import Image

from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    WebRtcMode
)

from utils.bg_config import BG_MAP, get_bg_path
from utils.photostrip import (
    create_photostrip,
    photostrip_to_bytes
)

from utils.bg_editor import (
    apply_background
)

from utils.cloudinary_utils import (
    show_download_qr
)


# ==========================================
# SESSION STATE
# ==========================================
if "captures" not in st.session_state:
    st.session_state.captures = []

if "session_started" not in st.session_state:
    st.session_state.session_started = False

if "locked_background" not in st.session_state:
    st.session_state.locked_background = None

if "frame_style" not in st.session_state:
    st.session_state.frame_style = "Putih"

if "session_finished" not in st.session_state:
    st.session_state.session_finished = False


# ==========================================
# VIDEO PROCESSOR
# ==========================================
class VideoProcessor(VideoProcessorBase):

    def __init__(self):

        self.latest_frame = None

        # Countdown overlay
        self.countdown = None
        self.photo_number = None

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        # Mirror preview seperti cermin
        img = cv2.flip(img, 1)

        output = img.copy()

        # ======================================
        # TIMER OVERLAY
        # ======================================
        if self.countdown is not None:

            h, w = output.shape[:2]

            # Foto ke berapa
            cv2.putText(
                output,
                f"Foto {self.photo_number}/4",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                3
            )

            # Countdown besar di tengah
            text = str(self.countdown)

            (tw, th), _ = cv2.getTextSize(
                text,
                cv2.FONT_HERSHEY_DUPLEX,
                4,
                8
            )

            x = (w - tw) // 2
            y = (h + th) // 2

            cv2.putText(
                output,
                text,
                (x, y),
                cv2.FONT_HERSHEY_DUPLEX,
                4,
                (255, 255, 255),
                8
            )

        # Simpan frame terbaru (sudah mirror dan timer)
        self.latest_frame = output.copy()

        return av.VideoFrame.from_ndarray(
            output,
            format="bgr24"
        )

        # ======================================
        # TIMER OVERLAY DI VIDEO
        # ======================================
        if self.countdown is not None:

            h, w = output.shape[:2]

            # Tampilkan foto ke berapa
            cv2.putText(
                output,
                f"Foto {self.photo_number}/4",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                3
            )

            # Countdown besar di tengah
            text = str(self.countdown)

            (tw, th), _ = cv2.getTextSize(
                text,
                cv2.FONT_HERSHEY_DUPLEX,
                4,
                8
            )

            x = (w - tw) // 2
            y = (h + th) // 2

            cv2.putText(
                output,
                text,
                (x, y),
                cv2.FONT_HERSHEY_DUPLEX,
                4,
                (255, 255, 255),
                8
            )

        # Simpan frame terbaru (mirror + timer)
        self.latest_frame = output.copy()

        return av.VideoFrame.from_ndarray(
            output,
            format="bgr24"
        )


# ==========================================
# HALAMAN PHOTOBOX
# ==========================================
def photobox_page():

    st.header("🎞️ AI Photobox")

    st.caption(
        "Ambil 4 foto terlebih dahulu. "
        "Setelah selesai, kamu bisa memilih background dan mengunduh hasilnya."
    )

    # ======================================
    # RESET SESSION
    # ======================================
    if st.button(
        "🔄 Reset Session",
        use_container_width=True
    ):

        st.session_state.captures = []

        st.session_state.pop(
            "foreground_cache",
            None
        )

        st.session_state.session_started = False

        st.session_state.session_finished = False

        st.session_state.frame_style = "Putih"

        st.rerun()

    st.divider()

    # ======================================
    # PILIH WARNA FRAME
    # ======================================
    if not st.session_state.session_started:

        frame_style = st.radio(
            "🎨 Pilih Warna Frame",
            ["Putih", "Hitam"],
            horizontal=True
        )

    else:

        frame_style = st.session_state.frame_style

        st.info(
            "📸 Session sedang berlangsung..."
        )

    # ======================================
    # REALTIME CAMERA PREVIEW
    # ======================================
    ctx = webrtc_streamer(
        key="photobox",

        mode=WebRtcMode.SENDRECV,

        media_stream_constraints={
            "video": True,
            "audio": False
        },

        video_processor_factory=VideoProcessor,

        async_processing=True
    )

    st.divider()

        # ======================================
    # START SESSION
    # ======================================
    if (
        not st.session_state.session_started
        and ctx.video_processor
    ):

        if st.button(
            "📸 Start Photobox",
            use_container_width=True
        ):

            st.session_state.session_started = True

            st.session_state.frame_style = frame_style

            st.rerun()


    # ======================================
    # PHOTO SESSION
    # ======================================
    if (
        st.session_state.session_started
        and not st.session_state.session_finished
        and ctx.video_processor
    ):

        st.success(
            "📸 Session dimulai!"
        )

        progress = st.progress(0)

        preview_placeholder = st.empty()

        total_photo = 4

        for photo_index in range(total_photo):

            # ==============================
            # COUNTDOWN
            # ==============================
            for sec in range(5, 0, -1):

                ctx.video_processor.countdown = sec

                ctx.video_processor.photo_number = (
                    photo_index + 1
                )

                time.sleep(1)

            # Hilangkan timer
            ctx.video_processor.countdown = None
            ctx.video_processor.photo_number = None

            # Kasih jeda supaya frame tanpa timer masuk
            time.sleep(1)

            # Ambil frame
            frame = ctx.video_processor.latest_frame

            if frame is None:

                st.error(
                    "Gagal mengambil frame webcam."
                )

                st.session_state.session_started = False

                st.stop()

            frame_rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            captured = Image.fromarray(
                frame_rgb
            )

            st.session_state.captures.append(
                captured
            )

            # Preview hasil
            preview_placeholder.image(
                captured,
                caption=(
                    f"Hasil Foto {photo_index + 1}/4"
                ),
                use_container_width=True
            )

            progress.progress(
                (photo_index + 1) / total_photo
            )

            time.sleep(2)

            preview_placeholder.empty()

        st.session_state.session_finished = True

        st.rerun()


    # ======================================
    # HASIL PHOTOBOX
    # ======================================
    if st.session_state.session_finished:

        st.success(
            "🎉 Photobox selesai!"
        )

        st.subheader(
            "🎨 Pilih Background"
        )

        selected_bg = st.selectbox(
            "Pilih background untuk photostrip",
            list(BG_MAP.keys())
        )

        edited_images = apply_background(
            st.session_state.captures,
            selected_bg
        )

        preview_strip = create_photostrip(
            edited_images,
            st.session_state.frame_style
        )

        st.image(
            preview_strip,
            caption="Preview Hasil Final",
            use_container_width=False
        )


        # ==============================
        # DOWNLOAD LANGSUNG
        # ==============================
        strip_bytes = photostrip_to_bytes(
            preview_strip
        )

        st.download_button(
            "⬇️ Download Photostrip",
            data=strip_bytes,
            file_name="photostrip.jpg",
            mime="image/jpeg",
            use_container_width=True
        )

        st.divider()


        # ==============================
        # QR DOWNLOAD
        # ==============================
        st.subheader(
            "📱 QR Download"
        )

        st.caption(
            "Jika sudah puas dengan hasilnya, "
            "buat QR agar pengguna bisa mengunduh photostrip."
        )

        if st.button(
            "Generate QR Download",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Mengunggah hasil..."
                ):

                    url, qr = show_download_qr(
                        preview_strip
                    )

                st.success(
                    "QR berhasil dibuat!"
                )

                st.image(
                    qr,
                    caption=(
                        "Scan QR untuk mengunduh hasil"
                    ),
                    width=250
                )

                st.code(
                    url,
                    language=None
                )

            except Exception as e:

                st.error(
                    "Gagal upload ke Cloudinary."
                )

                st.exception(e)

        st.divider()


        # ==============================
        # SESSION BARU
        # ==============================
        if st.button(
            "🎉 Mulai Sesi Baru",
            use_container_width=True
        ):

            st.session_state.captures = []

            st.session_state.pop(
                "foreground_cache",
                None
            )

            st.session_state.session_started = False

            st.session_state.session_finished = False

            st.session_state.frame_style = "Putih"

            st.rerun()     
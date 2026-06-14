import streamlit as st
import numpy as np

from views.home import home_page
from views.remover import remover_page

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="🖼️",
    layout="wide"
)

# ==============================================================================
# SESSION STATE
# ==============================================================================
if "total_processed_images" not in st.session_state:
    st.session_state.total_processed_images = 0

if "last_inference_time" not in st.session_state:
    st.session_state.last_inference_time = 0.0

if "inference_history" not in st.session_state:
    st.session_state.inference_history = []

# ==============================================================================
# SIDEBAR
# ==============================================================================
st.sidebar.title("AI Background Remover")

menu = st.sidebar.radio(
    "📂 Navigasi",
    [
        "🏠 Beranda",
        "🖼️ Prediksi",
        "📊 Dashboard"
    ]
)

# ==============================================================================
# BERANDA
# ==============================================================================
if menu == "🏠 Beranda":

    home_page()

# ==============================================================================
# PREDIKSI
# ==============================================================================
elif menu == "🖼️ Prediksi":

    remover_page()

# ==============================================================================
# DASHBOARD
# ==============================================================================
elif menu == "📊 Dashboard":

    st.title("📊 Dashboard Statistik")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jumlah Data Diuji",
            st.session_state.total_processed_images
        )

    with col2:
        avg_time = (
            np.mean(st.session_state.inference_history)
            if st.session_state.inference_history
            else 0
        )

        st.metric(
            "Waktu Inferensi Rata-rata",
            f"{avg_time:.2f} detik"
        )

    with col3:
        st.metric(
            "Akurasi Model",
            "N/A"
        )

    st.divider()

    st.subheader("Grafik Waktu Inferensi")

    if st.session_state.inference_history:

        st.line_chart(
            st.session_state.inference_history
        )

    else:

        st.info(
            "Belum ada data inferensi."
        )
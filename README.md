# 🖼️ AI Background Remover Berbasis Web

Aplikasi berbasis web untuk menghapus background gambar secara otomatis menggunakan teknologi Artificial Intelligence (AI) berbasis model U²-Net melalui library `rembg`.

Pengguna dapat mengunggah gambar, menghapus background, mengganti background baru, serta mengunduh hasil dalam format PNG transparan maupun JPG.

Selain fitur utama background remover, aplikasi juga dilengkapi fitur pengembangan berupa photobox interaktif berbasis webcam.

---

## 👨‍🎓 Informasi Proyek

**Judul:**
Implementasi AI Background Remover Berbasis Web dengan Fitur Photobox Interaktif

**Mata Kuliah:**
Image Processing

**Mahasiswa:**
Ezza Addini

---

## ✨ Fitur Utama

### AI Background Remover
- Upload gambar JPG, JPEG, atau PNG.
- Penghapusan background otomatis menggunakan AI.
- Pilihan background baru:
  - Transparan (PNG)
  - Warna solid pasfoto
  - Background gambar
- Download hasil PNG transparan.
- Download hasil JPG.

### Dashboard Statistik
- Total gambar yang diproses.
- Waktu inferensi terakhir.
- Rata-rata waktu inferensi.
- Grafik tren performa inferensi.

### Photobox Interaktif (Pengembangan)
- Webcam realtime.
- Countdown otomatis.
- Photostrip 4-cut.
- Preview hasil.
- QR Code download menggunakan Cloudinary.

---

## 🛠️ Teknologi yang Digunakan

| Teknologi | Fungsi |
|---|---|
| Streamlit | Framework web |
| rembg | Background remover |
| U²-Net | Model segmentasi |
| ONNX Runtime | Menjalankan model AI |
| Pillow | Manipulasi gambar |
| NumPy | Operasi numerik |
| Streamlit-WebRTC | Webcam realtime |
| OpenCV | Pengolahan citra |
| Cloudinary | Penyimpanan hasil |
| qrcode | QR download |

---

## 📁 Struktur Proyek

```text
ai-background-remover/
│
├── app.py
├── requirements.txt
├── README.md
│
├── bg/
├── utils/
├── views/
└── .streamlit/
```

---

## 🚀 Instalasi

Clone repository:

```bash
git clone https://github.com/ezzxdn/ai-background-remover.git
cd ai-background-remover
```

Buat virtual environment:

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/Mac:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

---

## ▶️ Menjalankan Aplikasi

```bash
streamlit run app.py
```

Akses melalui browser:

```
http://localhost:8501
```

---

## 🤖 Cara Kerja AI Background Remover

1. Pengguna mengunggah gambar.
2. Gambar diproses menggunakan model U²-Net melalui library rembg.
3. Model melakukan segmentasi foreground dan background.
4. Background dihapus secara otomatis.
5. Pengguna dapat memilih background baru.
6. Hasil dapat diunduh sesuai kebutuhan.

---

## 📄 Lisensi

Dikembangkan untuk keperluan akademik pada mata kuliah Image Processing.
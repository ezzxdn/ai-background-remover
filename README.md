# 🎞️ AI Photobox with Background Remover

AI Photobox adalah aplikasi photobooth berbasis web yang memungkinkan pengguna mengambil empat foto layaknya photobooth modern, kemudian mengganti background secara otomatis menggunakan teknologi background removal berbasis AI.

Aplikasi dikembangkan menggunakan Streamlit sebagai antarmuka utama, Streamlit-WebRTC untuk akses webcam, serta rembg untuk proses penghapusan background. Hasil photostrip dapat diunduh secara langsung maupun melalui QR Code yang terhubung dengan Cloudinary.

---

## ✨ Fitur Utama

* 📷 Realtime webcam preview dengan efek mirror.
* ⏳ Countdown otomatis 5 detik sebelum pengambilan foto.
* 🎞️ Photobooth 4-cut (empat foto dalam satu strip).
* 🎨 Pilihan warna frame photostrip.
* 🖼️ Penggantian background menggunakan AI (rembg).
* 👀 Preview hasil photostrip sebelum finalisasi.
* ⬇️ Download hasil photostrip dalam format JPG.
* 📱 QR Code untuk mengunduh hasil photostrip.
* ⚡ Caching foreground agar pergantian background lebih cepat.
* 🔄 Reset session untuk memulai sesi baru.

---

## 🛠️ Teknologi yang Digunakan

| Teknologi        | Fungsi                         |
| ---------------- | ------------------------------ |
| Streamlit        | Antarmuka aplikasi web         |
| Streamlit-WebRTC | Akses webcam secara realtime   |
| OpenCV           | Pengolahan citra               |
| Pillow           | Manipulasi gambar              |
| rembg            | Background removal berbasis AI |
| ONNX Runtime     | Menjalankan model rembg        |
| Cloudinary       | Penyimpanan hasil photostrip   |
| qrcode           | Pembuatan QR Code              |
| NumPy            | Operasi array numerik          |
| AV               | Konversi frame video           |

---

## 📁 Struktur Project

```text
bg-remover-app/
│
├── app.py
├── requirements.txt
├── README.md
│
├── bg/
│   ├── backgrounds/
│   └── frames/
│
├── views/
│   ├── photobox.py
│   └── bg_remover.py
│
├── utils/
│   ├── bg_config.py
│   ├── bg_editor.py
│   ├── photostrip.py
│   └── cloudinary_utils.py
│
└── .streamlit/
    └── secrets.toml
```

---

## 🚀 Instalasi

### 1. Clone repository

```bash
git clone <repository-url>
cd bg-remover-app
```

### 2. Buat virtual environment

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

### 3. Install dependency

```bash
pip install -r requirements.txt
```

---

## ▶️ Menjalankan Aplikasi

Jalankan perintah berikut:

```bash
streamlit run app.py
```

Buka browser pada alamat:

```text
http://localhost:8501
```

---

## 📸 Cara Menggunakan

1. Pilih warna frame photostrip.
2. Klik tombol **Start Photobox**.
3. Ambil empat foto dengan countdown otomatis.
4. Setelah sesi selesai, pilih background yang diinginkan.
5. Lihat preview hasil photostrip.
6. Unduh hasil secara langsung atau buat QR Code untuk diunduh melalui perangkat lain.

---

## ☁️ Konfigurasi Cloudinary

Buat file:

```text
.streamlit/secrets.toml
```

Isi dengan:

```toml
CLOUD_NAME="your_cloud_name"
API_KEY="your_api_key"
API_SECRET="your_api_secret"
```

---

## 🤖 Tentang Background Removal

Proses penghapusan background dilakukan menggunakan library rembg yang memanfaatkan model U²-Net. Untuk menjaga stabilitas aplikasi, proses background removal dilakukan setelah sesi pemotretan selesai, bukan secara realtime.

Selain itu, hasil foreground disimpan dalam cache sehingga pengguna dapat mencoba berbagai background tanpa perlu menjalankan proses segmentasi ulang.

---

## 📄 Lisensi

Project ini dikembangkan untuk keperluan pembelajaran dan tugas akhir/UAS mata kuliah Image Processing.

Silakan gunakan dan modifikasi sesuai kebutuhan akademik.
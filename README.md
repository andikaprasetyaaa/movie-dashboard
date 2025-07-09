# 🎬 Movie Analytics Dashboard (TMDB)

Dashboard ini adalah **aplikasi interaktif berbasis Streamlit** untuk menganalisis ribuan data film dari TMDB (The Movie Database). Dengan fitur visualisasi yang kaya dan sistem rekomendasi berbasis konten, pengguna dapat menjelajahi film berdasarkan genre, popularitas, tahun rilis, rating, dan bahasa.

## 🚀 Fitur Utama

- 📊 **Ringkasan Statistik Film**: Lihat total film, rata-rata rating, total vote, genre dominan, film terbaik, dan paling populer.
- 🎭 **Distribusi Film per Genre**: Visualisasi jumlah film berdasarkan genre menggunakan bar chart dan word cloud.
- 📈 **Tren Popularitas per Tahun**: Grafik garis yang menampilkan rata-rata popularitas film dari tahun ke tahun.
- 📉 **Korelasi Popularitas vs Jumlah Vote**: Scatter plot interaktif untuk memahami hubungan antara vote dan popularitas.
- 🎯 **Rekomendasi Film**: Sistem rekomendasi berbasis TF-IDF dan cosine similarity berdasarkan genre dan sinopsis.
- 🔍 **Filter Dinamis**: Filter berdasarkan tahun rilis, bahasa, genre, dan minimal rating.

## 📁 Struktur File

- `app.py` atau `main.py`: File utama Streamlit.
- `requirements.txt`: Berisi dependensi yang diperlukan untuk menjalankan aplikasi.
- `README.md`: Dokumentasi ini.
- Dataset: Diambil dari HuggingFace → [`9000plus.csv`](https://huggingface.co/datasets/Pablinho/movies-dataset/resolve/main/9000plus.csv)

## 🛠 Instalasi Lokal

1. **Clone repo ini**:
   ```bash
   git clone https://github.com/username/movie-dashboard.git
   cd movie-dashboard

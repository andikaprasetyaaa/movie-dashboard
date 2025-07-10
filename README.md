
# 🎬 Movie Analytics Dashboard (TMDB)

🔗 **Akses Aplikasi Langsung**: [Klik di sini untuk mencoba aplikasi](https://streamlit-app-751346175396.asia-southeast2.run.app/)

Sebuah dasbor interaktif berbasis **Streamlit** untuk menjelajahi ribuan film berdasarkan data dari The Movie Database (TMDB). Aplikasi ini memungkinkan pengguna untuk menggali tren industri film, menemukan rekomendasi film, dan menganalisis genre, popularitas, serta rating film secara visual.

---

## 🌟 Fitur Utama

- ✅ **Filter Dinamis**  
  Saring film berdasarkan:
  - Tahun rilis
  - Bahasa
  - Genre
  - Rating minimum

- 📊 **Ringkasan Statistik**
  - Total jumlah film
  - Rata-rata rating
  - Total vote
  - Genre teratas
  - Film rating tertinggi
  - Film terpopuler

- 📈 **Visualisasi Data Interaktif**
  - Histogram Distribusi Rating Film  
  - Word Cloud Genre Paling Dominan  
  - Bar Chart Top 10 Film Terpopuler  
  - Scatter Plot Popularitas vs Rating  
  - Bar Chart Jumlah Film per Genre  
  - Line Chart Tren Popularitas per Tahun  
  - Scatter Plot Korelasi Popularitas vs Vote  

- 🎯 **Sistem Rekomendasi Film**  
  Temukan film-film serupa berdasarkan **genre** dan **overview**, menggunakan:
  - TF-IDF Vectorizer  
  - Cosine Similarity  

- 🖼️ **Tampilan Grid Film**  
  Galeri film dengan poster, rating, popularitas, dan jumlah vote.

---

## ⚙️ Instalasi & Penggunaan Lokal

1. **Clone Repositori**
   ```bash
   git clone https://github.com/andikaprasetyaaa/movie-dashboard.git
   cd movie-dashboard
   ```

2. **Buat & Aktifkan Virtual Environment (Direkomendasikan)**  
   - **Windows**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependensi**
   ```bash
   pip install -r requirements.txt
   ```

   > Jika belum ada file `requirements.txt`, buat secara manual setelah install:
   ```bash
   pip freeze > requirements.txt
   ```

4. **Jalankan Aplikasi**
   ```bash
   streamlit run app.py
   ```

---

## 📊 Dataset

Dataset yang digunakan: [`Pablinho/movies-dataset`](https://huggingface.co/datasets/Pablinho/movies-dataset)

- File: `9000plus.csv`
- Jumlah film: 9000+
- Sumber: Hugging Face Datasets
- Kolom penting:

| Kolom             | Tipe Data    | Deskripsi                                                  | Contoh                            |
|------------------|--------------|-------------------------------------------------------------|-----------------------------------|
| Release_Date      | string        | Tanggal rilis film                                          | `2021-12-15`                      |
| Title             | string        | Judul film                                                  | `Spider-Man: No Way Home`         |
| Overview          | string        | Ringkasan plot untuk sistem rekomendasi                     | `Peter Parker is unmasked...`     |
| Popularity        | float64       | Skor popularitas film                                       | `5083.954`                        |
| Vote_Count        | string        | Jumlah vote film (akan dikonversi ke numerik)               | `8940`                            |
| Vote_Average      | string        | Rata-rata rating (akan dikonversi ke numerik)               | `8.3`                             |
| Original_Language | string        | Kode bahasa asli film (misalnya: `en`, `ja`)                | `en`                              |
| Genre             | string        | Daftar genre dipisahkan koma (akan diproses menjadi tuple)  | `Action, Adventure, Sci-Fi`       |
| Poster_Url        | string        | URL gambar poster film                                      | `https://image.tmdb.org/...jpg`   |

---

## 🧠 Alur Kerja Aplikasi

### 1. 📥 Pemuatan & Pembersihan Data
- Konversi `Release_Date` ke datetime
- Konversi `Vote_Count`, `Vote_Average`, `Popularity` ke numerik
- Hapus nilai yang hilang
- Proses `Genre` jadi format tuple
- Mapping `Original_Language` ke nama bahasa

### 2. 🤖 Sistem Rekomendasi
- Buat kolom `combined_features` dari `Genre + Overview`
- Transformasi teks menggunakan `TfidfVectorizer`
- Hitung kemiripan antar film dengan `cosine_similarity`
- Cache matriks kemiripan untuk efisiensi

### 3. 📚 Sidebar & Filter
- Rentang tahun rilis
- Bahasa
- Genre
- Minimal rating
- Data difilter dinamis berdasarkan pilihan pengguna

### 4. 🧭 Navigasi Halaman
- Summary
- Rekomendasi Film
- Film per Genre
- Visualisasi lainnya

### 5. 🖼️ UI & Visualisasi
- Layout lebar dengan `st.set_page_config`
- CSS kustom untuk styling kartu dan KPI

---

## 🛠️ Library yang Digunakan

- `streamlit` – antarmuka pengguna
- `pandas` – manipulasi data
- `numpy` – operasi numerik
- `plotly.express` – visualisasi interaktif
- `matplotlib.pyplot` – dasar visualisasi
- `wordcloud` – visualisasi genre
- `scikit-learn` – TF-IDF dan Cosine Similarity

---

## 🤝 Kontributor

| Nama | NIM |
|------|-----|
| I Made Adiguna Arya Riastha | 2205551132 |
| I Gede Bagus Kelvin Andhika | 2205551136 |
| **I Putu Andika Prasetya** | **2205551137** |
| Ida Dyah Diwya Paramita | 2205551140 |

---

Jika Anda menyukai proyek ini, beri bintang ⭐ di GitHub dan jangan ragu untuk memberi kontribusi!

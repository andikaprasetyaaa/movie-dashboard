🎬 Movie Analytics Dashboard (TMDB)
Akses Aplikasi Langsung: https://streamlit-app-751346175396.asia-southeast2.run.app/

Sebuah dasbor interaktif yang didukung oleh Streamlit, dirancang untuk menjelajahi ribuan film berdasarkan data dari The Movie Database (TMDB). Aplikasi ini memungkinkan pengguna untuk menggali tren industri film, menemukan rekomendasi film serupa, dan menganalisis genre, popularitas, serta rating secara visual. Dengan filter dinamis, Anda dapat menyesuaikan tampilan data sesuai preferensi tahun rilis, bahasa, genre, dan rating minimum.

🌟 Fitur Utama
Filter Dinamis: Saring film berdasarkan rentang tahun rilis, bahasa, genre, dan rating minimum.

Ringkasan Statistik: Dapatkan gambaran cepat tentang total film, rata-rata rating, total vote, genre teratas, film rating tertinggi, dan film terpopuler.

Visualisasi Data Interaktif:

Distribusi Rating Film: Histogram yang menunjukkan sebaran rating film.

Genre Paling Dominan: Word Cloud yang menampilkan genre-genre film yang paling sering muncul.

Top 10 Film Terpopuler: Bar chart horizontal dari 10 film terpopuler dalam data terfilter.

Popularitas vs. Rating: Scatter plot yang menunjukkan hubungan antara popularitas dan rata-rata rating film.

Jumlah Film per Genre: Bar chart yang menampilkan jumlah film untuk setiap genre.

Tren Popularitas Film per Tahun: Line chart yang menggambarkan rata-rata popularitas film dari waktu ke waktu.

Korelasi Popularitas vs Vote: Scatter plot yang menunjukkan korelasi antara popularitas dan jumlah vote.

Sistem Rekomendasi Film: Temukan film-film serupa berdasarkan kesamaan genre dan ringkasan (Overview) menggunakan Cosine Similarity dan TF-IDF Vectorizer.

Tampilan Grid Film: Menampilkan daftar film terfilter atau hasil rekomendasi dalam format galeri yang menarik dengan poster, rating, popularitas, dan vote count.

🚀 Instalasi dan Penggunaan
Untuk menjalankan aplikasi ini secara lokal, ikuti langkah-langkah berikut:

Kloning Repositori:

Bash

git clone https://github.com/andikaprasetyaaa/movie-dashboard.git
cd movie-dashboard
Buat dan Aktifkan Virtual Environment (Direkomendasikan):

Bash

python -m venv venv
# Di Windows
.\venv\Scripts\activate
# Di macOS/Linux
source venv/bin/activate
Instal Dependensi:

Bash

pip install -r requirements.txt
Jika file requirements.txt belum ada, Anda bisa membuatnya secara manual dengan daftar library di bagian "Library yang Digunakan", atau jalankan perintah berikut setelah menginstal library secara manual:

Bash

pip freeze > requirements.txt
Jalankan Aplikasi Streamlit:

Bash

streamlit run app.py
(Asumsikan nama file utama aplikasi Anda adalah app.py. Sesuaikan jika berbeda.)

Setelah menjalankan perintah di atas, aplikasi akan terbuka secara otomatis di browser web default Anda (biasanya http://localhost:8501).

📊 Penjelasan Dataset
Dataset yang digunakan dalam proyek ini adalah 9000plus.csv, yang bersumber dari Hugging Face Datasets (Pablinho/movies-dataset). Dataset ini berisi informasi tentang lebih dari 9000 film dan memiliki struktur kolom penting sebagai berikut:

Kolom

Tipe Data Asli

Deskripsi

Contoh Data

Release_Date

string

Tanggal rilis film. Ini akan dikonversi menjadi tipe data datetime.

2021-12-15

Title

string

Judul film.

Spider-Man: No Way Home

Overview

string

Ringkasan plot atau deskripsi singkat tentang film. Digunakan dalam sistem rekomendasi.

Peter Parker is unmasked and no longer able to separate his normal life from the high-stakes...

Popularity

float64

Skor popularitas film, menunjukkan seberapa populer film tersebut saat ini.

5083.954

Vote_Count

string

Jumlah total vote yang diterima film. Akan dikonversi menjadi numerik.

8940

Vote_Average

string

Rata-rata rating film. Akan dikonversi menjadi numerik.

8.3

Original_Language

string

Kode bahasa asli film (misalnya, 'en' untuk Inggris, 'ja' untuk Jepang).

en

Genre

string

Genre film, sering kali berupa daftar genre yang dipisahkan koma. Akan diproses menjadi tuple genre.

Action, Adventure, Science Fiction

Poster_Url

string

URL gambar poster film.

https://image.tmdb.org/t…PXvft6k4YLjm.jpg


Ekspor ke Spreadsheet
Data ini kemudian melalui proses pembersihan dan persiapan di mana tipe data disesuaikan, nilai yang hilang ditangani, dan kolom Genre diubah menjadi format yang lebih mudah diolah. Kolom Original_Language juga dipetakan ke nama bahasa yang lebih mudah dibaca untuk visualisasi.

💻 Library yang Digunakan
Proyek ini memanfaatkan beberapa library Python untuk pemrosesan data, visualisasi, dan pembangunan antarmuka pengguna:

streamlit: Kerangka kerja utama untuk membangun aplikasi web data interaktif.

pandas: Digunakan untuk manipulasi dan analisis data, termasuk pemuatan, pembersihan, dan transformasi DataFrame.

numpy: Digunakan untuk operasi numerik, terutama dalam perhitungan matriks.

plotly.express: Library visualisasi data tingkat tinggi yang digunakan untuk membuat plot interaktif seperti bar chart, line chart, dan scatter plot.

matplotlib.pyplot: Library visualisasi dasar yang digunakan sebagai backend untuk wordcloud.

wordcloud: Digunakan untuk membuat visualisasi "word cloud" dari genre film.

scikit-learn (khususnya TfidfVectorizer dan cosine_similarity): Digunakan untuk mengubah teks menjadi representasi numerik dan menghitung kemiripan antar film untuk sistem rekomendasi.

⚙️ Alur Kerja Aplikasi
Aplikasi ini mengikuti alur kerja yang logis, mulai dari pemuatan data hingga penyajian visualisasi interaktif dan rekomendasi:

Pemuatan dan Persiapan Data:

Data film dimuat dari URL dataset.

Kolom tanggal (Release_Date) dan numerik (Vote_Count, Vote_Average, Popularity) dikonversi ke tipe data yang sesuai.

Baris dengan nilai yang hilang pada kolom-kolom penting (tanggal rilis, rating, popularitas, jumlah vote, bahasa asli, dan overview) dihapus untuk memastikan kualitas data.

Kolom Genre yang awalnya string dipisahkan dan diubah menjadi format tuple untuk memudahkan pemrosesan multi-genre.

Kode bahasa asli film (Original_Language) dipetakan ke nama bahasa yang lebih mudah dibaca (Language_Name) untuk antarmuka pengguna.

Data yang sudah bersih ini di-cache untuk mempercepat performa aplikasi.

Komputasi Kemiripan Film:

Untuk sistem rekomendasi, fitur gabungan (combined_features) dibuat dengan menggabungkan informasi Genre dan Overview dari setiap film.

TfidfVectorizer dari scikit-learn digunakan untuk mengubah combined_features menjadi representasi numerik. Ini membantu komputer memahami konten tekstual.

cosine_similarity kemudian dihitung dari representasi numerik ini untuk mendapatkan skor kemiripan antara setiap pasang film. Matriks kemiripan ini juga di-cache agar tidak perlu dihitung ulang setiap kali aplikasi dijalankan.

Sidebar dan Filter Dinamis:

Di sidebar Streamlit, pengguna diberikan opsi untuk memfilter data film berdasarkan:

Rentang Tahun Rilis: Memungkinkan pemilihan film dalam rentang tahun tertentu.

Bahasa: Memungkinkan pemilihan satu atau lebih bahasa film dari daftar yang tersedia.

Genre: Memungkinkan pemilihan satu atau lebih genre untuk fokus pada kategori film tertentu.

Minimal Rating: Menetapkan ambang batas rating rata-rata film yang ditampilkan.

DataFrame utama difilter secara dinamis berdasarkan semua pilihan filter ini, menghasilkan subset data yang relevan untuk visualisasi.

Navigasi Halaman:

Pengguna dapat berpindah antar bagian utama dasbor (Summary, Rekomendasi Film, Film per Genre, dll.) menggunakan opsi radio button di sidebar.

Penyajian Konten Utama:

Setiap halaman menyajikan visualisasi dan informasi yang berbeda berdasarkan data film yang sudah difilter:

Halaman "Summary" menampilkan metrik utama dan visualisasi umum tentang seluruh dataset yang difilter.

Halaman "Rekomendasi Film" memungkinkan pengguna memilih film dan mendapatkan rekomendasi film serupa berdasarkan model kemiripan yang telah dihitung. Hasil rekomendasi ini juga dapat difilter berdasarkan rating minimum.

Halaman lainnya menampilkan visualisasi spesifik seperti distribusi genre, tren popularitas, atau daftar top film.

Desain Antarmuka Pengguna (UI):

Aplikasi menggunakan konfigurasi halaman Streamlit (st.set_page_config) untuk layout yang lebar.

Styling CSS kustom diinjeksi untuk memberikan tampilan yang lebih menarik dan konsisten pada elemen-elemen seperti kartu film dan metrik KPI.

🤝 Kontributor
I Made Adiguna Arya Riastha (NIM: 2205551132)

I Gede Bagus Kelvin Andhika (NIM: 2205551136)

I Putu Andika Prasetya (NIM: 2205551137)

Ida Dyah Diwya Paramita (NIM: 2205551140)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- FUNGSI-FUNGSI UTAMA ---

@st.cache_data
def load_and_prepare_data(url):
    """Memuat dan membersihkan data dari URL."""
    df = pd.read_csv(url, encoding='utf-8-sig', engine='python', on_bad_lines='skip')
    df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
    df['Vote_Count'] = pd.to_numeric(df['Vote_Count'], errors='coerce')
    df['Vote_Average'] = pd.to_numeric(df['Vote_Average'], errors='coerce')
    df['Popularity'] = pd.to_numeric(df['Popularity'], errors='coerce')
    df = df.dropna(subset=['Release_Date', 'Vote_Average', 'Popularity', 'Vote_Count', 'Original_Language', 'Overview'])
    # BARIS INI YANG DIUBAH: Mengubah list menjadi tuple
    df['Genre'] = df['Genre'].fillna('').apply(lambda x: tuple(g.strip() for g in x.split(',') if g.strip()))
    LANGUAGE_MAP = {
        "en": "Inggris", "fr": "Prancis", "ja": "Jepang", "ko": "Korea", "es": "Spanyol", "de": "Jerman",
        "hi": "Hindi", "zh": "Mandarin", "it": "Italia", "pt": "Portugis", "ru": "Rusia", "id": "Indonesia",
        "ar": "Arab", "tr": "Turki", "nl": "Belanda", "sv": "Swedia", "pl": "Polandia", "da": "Denmark",
        "fi": "Finlandia", "no": "Norwegia", "cs": "Ceko", "el": "Yunani", "he": "Ibrani", "ro": "Rumania",
        "hu": "Hungaria", "th": "Thai", "vi": "Vietnam", "uk": "Ukraina", "ms": "Melayu", "fa": "Persia",
        "ta": "Tamil", "bn": "Bengali", "te": "Telugu", "ml": "Malayalam", "kn": "Kannada", "mr": "Marathi",
        "pa": "Punjabi", "ur": "Urdu", "sr": "Serbia", "hr": "Kroasia", "bg": "Bulgaria", "sl": "Slovenia",
        "sk": "Slovakia", "et": "Estonia", "lv": "Latvia", "lt": "Lituania", "is": "Islandia", "ka": "Georgia",
        "az": "Azerbaijan", "hy": "Armenia", "kk": "Kazakh", "uz": "Uzbek", "bs": "Bosnia", "tl": "Filipina",
        "my": "Burma", "ne": "Nepali", "si": "Sinhala", "km": "Khmer", "lo": "Lao", "am": "Amharik",
        "af": "Afrikaans", "sw": "Swahili", "zu": "Zulu", "xh": "Xhosa", "yo": "Yoruba", "ig": "Igbo",
        "ha": "Hausa", "ca": "Katalan", "cn": "Tionghoa", "eu": "Basque", "la": "Latin", "nb": "Norwegia Bokmål"
    }

    df['Language_Name'] = df['Original_Language'].map(LANGUAGE_MAP).fillna(df['Original_Language'])
    df = df.reset_index(drop=True)
    return df

@st.cache_data
def compute_similarity(df):
    """Menghitung matriks kemiripan kosinus berbasis TF-IDF."""
    # Untuk TF-IDFVectorizer, Anda perlu mengubah tuple kembali ke string jika diperlukan
    # Namun, `join` pada tuple secara langsung sudah berfungsi.
    df['combined_features'] = df['Genre'].apply(lambda x: ' '.join(x)) + " " + df['Overview']
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def create_genre_wordcloud(df):
    """Membuat dan mengembalikan figure Word Cloud dari genre film."""
    genres = df.explode('Genre')['Genre'].dropna()
    text = ' '.join(genres.tolist())
    if not text: return None
    wordcloud = WordCloud(width=800, height=400, background_color=None, mode='RGBA', colormap='YlOrRd', max_words=100).generate(text)
    fig, ax = plt.subplots(figsize=(10, 5)); ax.imshow(wordcloud, interpolation='bilinear'); ax.axis('off'); fig.patch.set_alpha(0.0)
    return fig

# --- FUNGSI VISUALISASI ---

def display_movie_grid(df_to_display):
    """Menampilkan daftar film dalam format galeri/grid."""
    num_columns = 4
    cols = st.columns(num_columns)
    for index, row in df_to_display.iterrows():
        with cols[index % num_columns]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            if pd.notna(row.get('Poster_Url')):
                st.image(row['Poster_Url'])
            else:
                st.image("https://via.placeholder.com/300x450.png?text=No+Poster", use_column_width=True)
            
            st.markdown(f'<h5>{index + 1}. {row["Title"]}</h5>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="movie-details">
                <span>⭐ {row['Vote_Average']:.1f}</span>
                <span>🔥 {row['Popularity']:.0f}</span>
                <span>🗳️ {row['Vote_Count']:,}</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<p class="genre-text">{", ".join(row["Genre"])}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

def genre_distribution(df):
    exploded = df.explode('Genre'); genre_count = exploded['Genre'].value_counts().reset_index(); genre_count.columns = ['Genre', 'Count']
    fig = px.bar(genre_count, x='Genre', y='Count', color='Genre', title="Jumlah Film per Genre")
    st.plotly_chart(fig, use_container_width=True)

def popularity_over_time(df):
    df['Year'] = df['Release_Date'].dt.year; pop_year = df.groupby('Year')['Popularity'].mean().reset_index()
    fig = px.line(pop_year, x='Year', y='Popularity', title="Rata-rata Popularitas Film per Tahun")
    st.plotly_chart(fig, use_container_width=True)

def popularity_vs_votes(df):
    fig = px.scatter(df, x='Vote_Count', y='Popularity', size='Vote_Average', color='Language_Name', hover_name='Title', title="Korelasi Popularitas vs Vote Count")
    st.plotly_chart(fig, use_container_width=True)


# --- KONFIGURASI HALAMAN & CSS GLOBAL ---
st.set_page_config(page_title="🎬 Movie Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .metric-container { background-color: #2C2F33; border-radius: 10px; padding: 15px; text-align: center; color: white; border: 1px solid #4F545C; margin-bottom: 10px; }
    .metric-label { font-size: 16px; color: #A9A9A9; }
    .metric-value { font-size: 28px; font-weight: bold; color: #FFD700; }
    .metric-subvalue { font-size: 14px; color: #00BFFF; }
    .movie-card { background-color: #2C2F33; border-radius: 10px; padding: 10px; border: 1px solid #4F545C; text-align: center; height: 100%; }
    .movie-card h5 { color: #FFFFFF; font-weight: bold; font-size: 16px; margin-top: 10px; height: 40px; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
    .movie-details { display: flex; justify-content: space-around; font-size: 14px; color: #A9A9A9; margin-bottom: 10px; }
    .genre-text { font-size: 12px; color: #A9A9A9; font-style: italic; }
</style>
""", unsafe_allow_html=True)


# --- PEMUATAN DATA & KOMPUTASI AWAL ---
DATA_URL = "https://huggingface.co/datasets/Pablinho/movies-dataset/resolve/main/9000plus.csv"
df_raw = load_and_prepare_data(DATA_URL)
cosine_sim = compute_similarity(df_raw)
indices = pd.Series(df_raw.index, index=df_raw['Title']).drop_duplicates()

# --- SIDEBAR & FILTER DINAMIS ---
st.sidebar.header("🔍 Filter Film")
min_year, max_year = int(df_raw['Release_Date'].dt.year.min()), int(df_raw['Release_Date'].dt.year.max())
year_range = st.sidebar.slider("Rentang Tahun Rilis", min_year, max_year, (min_year, max_year))

available_langs = sorted(df_raw['Language_Name'].unique())
lang_options = ["All"] + available_langs
selected_langs = st.sidebar.multiselect("Bahasa", options=lang_options, default=["All"])

all_genres = sorted({g for sublist in df_raw['Genre'] for g in sublist})
selected_genres = st.sidebar.multiselect("Genre", options=all_genres, default=[])

min_rating = st.sidebar.slider("Minimal Rating", 0.0, 10.0, 5.0)

# --- LOGIKA FILTER DINAMIS ---
active_lang_filter = available_langs if "All" in selected_langs else selected_langs
df = df_raw[(df_raw['Release_Date'].dt.year.between(year_range[0], year_range[1])) & (df_raw['Language_Name'].isin(active_lang_filter)) & (df_raw['Vote_Average'] >= min_rating)]
if selected_genres: df = df[df['Genre'].apply(lambda genres: any(g in selected_genres for g in genres))]

# --- NAVIGASI HALAMAN ---
st.sidebar.markdown("---")
page = st.sidebar.radio("📊 Visualisasi", ["Summary", "Rekomendasi Film", "Film per Genre", "Popularitas per Tahun", "Top 20 Film Populer", "Korelasi Popularitas vs Vote"])

# --- KONTEN UTAMA ---
st.title("🎥 Movie Analytics Dashboard (TMDB)")

if page == "Summary":
    if df.empty:
        st.warning("Tidak ada data film yang cocok dengan filter yang Anda pilih.")
    else:
        st.markdown("Dasboard Movie Analytics ini adalah alat interaktif untuk menjelajahi ribuan film berdasarkan data dari TMDB, memungkinkan Anda menggali tren industri, menemukan rekomendasi film serupa, dan menganalisis genre, popularitas, serta rating secara visual. Dengan filter dinamis di sidebar, Anda dapat menyesuaikan tampilan data sesuai preferensi tahun rilis, bahasa, genre, dan rating minimum. Setiap halaman menyajikan visualisasi yang informatif mulai dari ringkasan statistik, distribusi genre, tren popularitas per tahun, hingga hubungan antara jumlah vote dan popularitas ditambah fitur rekomendasi film berbasis konten menggunakan machine learning untuk menemukan film yang mirip dengan favorit Anda.") # Deskripsi singkat
        st.markdown("---")
        st.markdown("### 📊 Ringkasan")
        
        total_films, avg_rating, total_votes = len(df), df['Vote_Average'].mean(), df['Vote_Count'].sum()
        top_genre = df.explode('Genre')['Genre'].value_counts().idxmax() if not df.explode('Genre')['Genre'].empty else "N/A"
        highest_rated_movie, most_popular_movie = df.loc[df['Vote_Average'].idxmax()], df.loc[df['Popularity'].idxmax()]
        
        kpi_cols = st.columns(3)
        kpi_cols[0].markdown(f'<div class="metric-container"><div class="metric-label">🎞️ Total Film</div><div class="metric-value">{total_films:,}</div></div>', unsafe_allow_html=True)
        kpi_cols[1].markdown(f'<div class="metric-container"><div class="metric-label">⭐ Rata-rata Rating</div><div class="metric-value">{avg_rating:.2f}</div></div>', unsafe_allow_html=True)
        kpi_cols[2].markdown(f'<div class="metric-container"><div class="metric-label">🗳️ Total Vote</div><div class="metric-value">{total_votes:,.0f}</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        kpi_cols2 = st.columns(3)
        kpi_cols2[0].markdown(f'<div class="metric-container"><div class="metric-label">🎭 Genre Teratas</div><div class="metric-value">{top_genre}</div></div>', unsafe_allow_html=True)
        kpi_cols2[1].markdown(f'<div class="metric-container"><div class="metric-label">🏆 Rating Tertinggi</div><div class="metric-value">{highest_rated_movie["Vote_Average"]:.1f}</div><div class="metric-subvalue">{highest_rated_movie["Title"]}</div></div>', unsafe_allow_html=True)
        kpi_cols2[2].markdown(f'<div class="metric-container"><div class="metric-label">🔥 Paling Populer</div><div class="metric-value">{most_popular_movie["Popularity"]:.0f}</div><div class="metric-subvalue">{most_popular_movie["Title"]}</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        summary_text = f"""
        Berdasarkan filter Anda, ditemukan **{total_films:,}** film yang dirilis antara tahun **{year_range[0]}** dan **{year_range[1]}**. 
        Secara kolektif, film-film ini telah mengumpulkan total **{total_votes:,.0f}** suara dengan rata-rata rating **{avg_rating:.2f}**. 
        Genre **'{top_genre}'** menjadi yang paling dominan dalam seleksi ini. 
        Film **"{highest_rated_movie['Title']}"** menonjol dengan rating tertinggi (**{highest_rated_movie['Vote_Average']:.1f}**), 
        sementara **"{most_popular_movie['Title']}"** menjadi yang terpopuler dengan skor **{most_popular_movie['Popularity']:.0f}**.
        """
        st.info(summary_text)

        st.markdown("---")
        st.markdown("### 📈 Analisis Visual Umum")
        
        viz_cols1 = st.columns(2)
        with viz_cols1[0]:
            st.subheader("⭐ Distribusi Rating Film")
            fig = px.histogram(df, x='Vote_Average', nbins=30, marginal='rug', color_discrete_sequence=['#FFD700'], labels={'Vote_Average': 'Rating Rata-rata'}); fig.update_layout(bargap=0.1); st.plotly_chart(fig, use_container_width=True)
        with viz_cols1[1]:
            st.subheader("☁️ Genre Paling Dominan")
            wordcloud_fig = create_genre_wordcloud(df)
            if wordcloud_fig: st.pyplot(wordcloud_fig, use_container_width=True)
            else: st.info("Tidak ada data genre untuk ditampilkan.")
        
        viz_cols2 = st.columns(2)
        with viz_cols2[0]:
            st.subheader("🔥 Top 10 Film Terpopuler (di Summary)")
            top_10_pop = df.nlargest(10, 'Popularity').sort_values('Popularity', ascending=True)
            fig = px.bar(top_10_pop, x='Popularity', y='Title', orientation='h', color='Vote_Average', color_continuous_scale='YlOrRd', labels={'Title': 'Judul Film', 'Popularity': 'Tingkat Popularitas', 'Vote_Average': 'Rating'}, text='Popularity'); fig.update_traces(texttemplate='%{text:.2s}', textposition='outside'); st.plotly_chart(fig, use_container_width=True)
        with viz_cols2[1]:
            st.subheader("⚖️ Popularitas vs. Rating")
            plot_df = df.sample(n=min(500, len(df)))
            fig = px.scatter(plot_df, x="Vote_Average", y="Popularity", size="Vote_Count", color="Vote_Average", color_continuous_scale=px.colors.sequential.YlOrRd, hover_name="Title", size_max=60, labels={'Vote_Average': 'Rata-rata Rating', 'Popularity': 'Tingkat Popularitas'}); st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📜 Detail Data Film Terfilter")
        df_display = df[['Title', 'Genre', 'Release_Date', 'Vote_Average', 'Popularity']].copy(); df_display.index = np.arange(1, len(df_display) + 1)
        st.dataframe(df_display.style.format({'Vote_Average': '{:.2f}', 'Popularity': '{:,.0f}', 'Release_Date': '{:%d %b %Y}'}).bar(subset=['Popularity'], color='#FFD700').bar(subset=['Vote_Average'], color='#00BFFF', vmin=0, vmax=10), use_container_width=True)

# --- HALAMAN REKOMENDASI FILM DENGAN LOGIKA YANG DIPERBAIKI ---
elif page == "Rekomendasi Film":
    st.header("🎬 Rekomendasi Film Berbasis Konten")
    st.markdown("Pilih film yang Anda sukai, dan kami akan merekomendasikan film lain yang paling mirip berdasarkan genre dan ringkasan ceritanya.")
    
    # --- KONTROL PENGGUNA ---
    col1, col2 = st.columns([3, 1])
    with col1:
        movie_list = df_raw['Title'].sort_values().tolist()
        selected_movie = st.selectbox("Pilih sebuah film:", movie_list)
    with col2:
        num_recommendations = st.slider("Jumlah Rekomendasi:", 5, 20, 12)
    
    min_rating_rec = st.slider("Hanya rekomendasikan film dengan rating di atas:", 0.0, 10.0, 6.0, 0.1)

    if st.button("Dapatkan Rekomendasi", type="primary"):
        try:
            idx = indices[selected_movie]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Ambil 50 kandidat teratas untuk memastikan ada cukup pilihan setelah filter
            sim_scores = sim_scores[1:51]
            movie_indices = [i[0] for i in sim_scores]
            
            # Ambil data lengkap dari kandidat
            recommended_movies = df_raw.iloc[movie_indices]
            
            # Terapkan filter rating dari slider
            final_recommendations = recommended_movies[recommended_movies['Vote_Average'] >= min_rating_rec]
            
            # Ambil jumlah rekomendasi sesuai slider dari hasil yang sudah terfilter
            final_recommendations = final_recommendations.head(num_recommendations).reset_index(drop=True)
            
            st.subheader(f"Karena Anda menyukai '{selected_movie}', mungkin Anda juga akan menyukai:")
            
            if final_recommendations.empty:
                st.warning("Tidak ada film rekomendasi yang memenuhi kriteria rating minimum Anda. Coba turunkan filter rating.")
            else:
                display_movie_grid(final_recommendations)

        except KeyError:
            st.error(f"Tidak dapat menemukan film '{selected_movie}' dalam data. Coba judul lain.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

elif page == "Film per Genre":
    st.header("🎭 Jumlah Film Berdasarkan Genre")
    genre_distribution(df)
elif page == "Popularitas per Tahun":
    st.header("📈 Tren Popularitas Film per Tahun")
    popularity_over_time(df)
elif page == "Top 20 Film Populer":
    st.header("🔥 Top 20 Film Paling Populer")
    lang_desc = "Semua Bahasa" if "All" in selected_langs else ", ".join(selected_langs)
    genre_desc = "Semua Genre" if not selected_genres else ", ".join(selected_genres)
    st.subheader(f"Menampilkan hasil untuk tahun: `{year_range[0]}-{year_range[1]}`")
    st.caption(f"Bahasa: `{lang_desc}` | Genre: `{genre_desc}` | Rating Min: `{min_rating}`")
    st.markdown("---")
    
    if df.empty:
        st.warning("Tidak ada film yang cocok dengan filter yang Anda pilih.")
    else:
        display_movie_grid(df.sort_values(by='Popularity', ascending=False).head(20).reset_index(drop=True))

elif page == "Korelasi Popularitas vs Vote":
    st.header("📉 Korelasi Popularitas dan Jumlah Vote")
    popularity_vs_votes(df)

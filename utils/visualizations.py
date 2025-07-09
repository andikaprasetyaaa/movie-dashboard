import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd

def show_summary(df):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎞️ Total Film", len(df))
    col2.metric("⭐ Rata-rata Rating", round(df['Vote_Average'].mean(), 2))
    col3.metric("🗳️ Total Vote", int(df['Vote_Count'].sum()))
    col4.metric("🌐 Bahasa Unik", df['Original_Language'].nunique())
    st.markdown("---")


def rating_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df['Vote_Average'], bins=20, kde=True, ax=ax, color="skyblue")
    ax.set_title("Distribusi Rating Film")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Jumlah Film")
    st.pyplot(fig)


def genre_distribution(df):
    exploded = df.explode('Genre')
    genre_count = exploded['Genre'].value_counts().reset_index()
    genre_count.columns = ['Genre', 'Count']
    fig = px.bar(genre_count, x='Genre', y='Count', color='Genre', title="Jumlah Film per Genre")
    st.plotly_chart(fig)


def popularity_over_time(df):
    df['Year'] = df['Release_Date'].dt.year
    pop_year = df.groupby('Year')['Popularity'].mean().reset_index()
    fig = px.line(pop_year, x='Year', y='Popularity', title="Rata-rata Popularitas Film per Tahun")
    st.plotly_chart(fig)


def top_10_popular(df):
    top10 = df.sort_values(by='Popularity', ascending=False).head(10)
    for _, row in top10.iterrows():
        st.markdown(f"### 🎬 {row['Title']} ({row['Vote_Average']}/10)")
        if pd.notna(row.get('Poster_Url')):
            st.image(row['Poster_Url'], width=200)
        st.markdown(f"**Genre:** {', '.join(row['Genre'])}  \n"
                    f"**Popularitas:** {round(row['Popularity'], 2)}  \n"
                    f"**Vote:** {int(row['Vote_Count'])}")
        st.markdown("---")


def popularity_vs_votes(df):
    fig = px.scatter(df, x='Vote_Count', y='Popularity',
                     size='Vote_Average', color='Language_Name',
                     hover_name='Title', title="Korelasi Popularitas vs Vote Count")
    st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import re
import string
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

st.set_page_config(page_title="NLP Text Analytics", layout="wide")

st.title("🧠 Aplikasi NLP Text Preprocessing & Visualisasi")

uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Data Awal")
    st.dataframe(df.head())

    text_column = st.selectbox("Pilih kolom teks", df.columns)

    st.sidebar.header("⚙️ Preprocessing")

    remove_url = st.sidebar.checkbox("Remove URL")
    remove_user = st.sidebar.checkbox("Remove Username")
    remove_symbol = st.sidebar.checkbox("Remove Symbol")
    remove_number = st.sidebar.checkbox("Remove Number")
    lowercase = st.sidebar.checkbox("Case Folding")

    def clean_text(text):
        text = str(text)
        if remove_url:
            text = re.sub(r"http\S+|www\S+", "", text)
        if remove_user:
            text = re.sub(r"@\w+", "", text)
        if remove_number:
            text = re.sub(r"\d+", "", text)
        if remove_symbol:
            text = text.translate(str.maketrans("", "", string.punctuation))
        if lowercase:
            text = text.lower()
        return text.strip()

    if st.button("🚀 Jalankan Analisis"):
        df["clean_text"] = df[text_column].apply(clean_text)

        # =========================
        # STATISTIK DASAR
        # =========================
        st.subheader("📊 Statistik Dataset")

        col1, col2, col3 = st.columns(3)
        col1.metric("Jumlah Data", len(df))
        col2.metric("Total Kata", df["clean_text"].str.split().str.len().sum())
        col3.metric("Rata-rata Panjang Teks", round(df["clean_text"].str.len().mean(), 2))

        # =========================
        # WORD FREQUENCY
        # =========================
        words = " ".join(df["clean_text"]).split()
        freq = Counter(words)
        top_words = freq.most_common(20)

        st.subheader("📈 20 Kata Paling Sering Muncul")
        word_df = pd.DataFrame(top_words, columns=["Kata", "Frekuensi"])

        fig, ax = plt.subplots()
        ax.barh(word_df["Kata"], word_df["Frekuensi"])
        ax.invert_yaxis()
        st.pyplot(fig)

        # =========================
        # WORDCLOUD
        # =========================
        st.subheader("☁️ WordCloud")
        wc = WordCloud(
            width=800,
            height=400,
            background_color="white"
        ).generate(" ".join(df["clean_text"]))

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

        # =========================
        # SENTIMENT SEDERHANA
        # =========================
        positive_words = ["baik", "bagus", "suka", "senang", "mantap"]
        negative_words = ["buruk", "jelek", "benci", "sedih", "kecewa"]

        def sentiment(text):
            pos = sum(word in text for word in positive_words)
            neg = sum(word in text for word in negative_words)
            if pos > neg:
                return "Positif"
            elif neg > pos:
                return "Negatif"
            else:
                return "Netral"

        df["sentiment"] = df["clean_text"].apply(sentiment)

        st.subheader("😊 Statistik Sentimen")
        sentiment_count = df["sentiment"].value_counts()

        fig, ax = plt.subplots()
        ax.pie(sentiment_count, labels=sentiment_count.index, autopct="%1.1f%%")
        st.pyplot(fig)

        # =========================
        # DOWNLOAD
        # =========================
        st.download_button(
            "⬇️ Download Hasil CSV",
            df.to_csv(index=False),
            "hasil_nlp.csv",
            "text/csv"
        )

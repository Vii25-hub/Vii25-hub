import streamlit as st
import pandas as pd
import re
import string
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

st.set_page_config(page_title="NLP Text Analytics", layout="wide")
st.title("🧠 NLP Text Analytics & Preprocessing")

uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Data Awal (SEMUA DATA)")
    st.dataframe(df)

    text_col = st.selectbox("Pilih kolom teks", df.columns)

    # ===== SIDEBAR PREPROCESSING =====
    st.sidebar.title("⚙️ Preprocessing")
    remove_duplicate = st.sidebar.checkbox("Remove Duplicate")
    remove_url = st.sidebar.checkbox("Remove URL")
    remove_username = st.sidebar.checkbox("Remove Username")
    remove_symbol = st.sidebar.checkbox("Remove Symbol")
    remove_number = st.sidebar.checkbox("Remove Number")
    remove_emoji = st.sidebar.checkbox("Remove Emoji")
    lowercase = st.sidebar.checkbox("Case Folding")

    def clean_text(text):
        text = str(text)
        if remove_url:
            text = re.sub(r"http\S+|www\S+", "", text)
        if remove_username:
            text = re.sub(r"@\w+", "", text)
        if remove_emoji:
            text = re.sub(r"[^\w\s]", "", text)
        if remove_number:
            text = re.sub(r"\d+", "", text)
        if remove_symbol:
            text = text.translate(str.maketrans("", "", string.punctuation))
        if lowercase:
            text = text.lower()
        return text.strip()

    if st.button("🚀 Jalankan Analisis"):
        if remove_duplicate:
            df = df.drop_duplicates(subset=[text_col])

        df["clean_text"] = df[text_col].apply(clean_text)

        st.subheader("📊 Statistik Data")
        col1, col2, col3 = st.columns(3)
        col1.metric("Jumlah Data", len(df))
        col2.metric("Total Kata", df["clean_text"].str.split().str.len().sum())
        col3.metric("Rata-rata Panjang Teks", round(df["clean_text"].str.len().mean(), 2))

        # ===== FREKUENSI KATA =====
        words = " ".join(df["clean_text"]).split()
        freq = Counter(words)
        top_words = freq.most_common(20)

        st.subheader("📈 20 Kata Paling Sering")
        word_df = pd.DataFrame(top_words, columns=["Kata", "Frekuensi"])
        st.dataframe(word_df)

        fig, ax = plt.subplots()
        ax.barh(word_df["Kata"], word_df["Frekuensi"])
        ax.invert_yaxis()
        st.pyplot(fig)

        # ===== WORDCLOUD =====
        st.subheader("☁️ WordCloud")
        text_wc = " ".join(df["clean_text"])
        if text_wc.strip():
            wc = WordCloud(
                width=800,
                height=400,
                background_color="white"
            ).generate(text_wc)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wc)
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.warning("Tidak ada teks untuk WordCloud")

        # ===== SENTIMENT SEDERHANA =====
        positive_words = ["baik", "bagus", "suka", "senang", "mantap", "puas"]
        negative_words = ["buruk", "jelek", "kecewa", "lambat", "error"]

        def sentiment(text):
            pos = sum(w in text for w in positive_words)
            neg = sum(w in text for w in negative_words)
            if pos > neg:
                return "Positif"
            elif neg > pos:
                return "Negatif"
            return "Netral"

        df["Sentimen"] = df["clean_text"].apply(sentiment)

        st.subheader("😊 Statistik Sentimen")
        sent = df["Sentimen"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(sent, labels=sent.index, autopct="%1.1f%%")
        st.pyplot(fig)

        st.download_button(
            "⬇️ Download Hasil CSV",
            df.to_csv(index=False),
            "hasil_nlp.csv",
            "text/csv"
        )

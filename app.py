import streamlit as st
import pandas as pd
import re
import string
import matplotlib.pyplot as plt

from collections import Counter
from wordcloud import WordCloud

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

st.set_page_config(page_title="NLP Text Analytics", layout="wide")
st.title("🧠 NLP Text Analytics Lengkap")

uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Data CSV (SEMUA BARIS)")
    st.write(f"Total baris terbaca: {len(df)}")
    st.dataframe(df, use_container_width=True)

    text_col = st.selectbox("Pilih kolom teks", df.columns)

    st.sidebar.title("⚙️ Preprocessing")
    remove_duplicate = st.sidebar.checkbox("Remove Duplicate")
    remove_url = st.sidebar.checkbox("Remove URL")
    remove_username = st.sidebar.checkbox("Remove Username")
    remove_symbol = st.sidebar.checkbox("Remove Symbol")
    remove_number = st.sidebar.checkbox("Remove Number")
    lowercase = st.sidebar.checkbox("Case Folding")

    def clean_text(text):
        text = str(text)
        if remove_url:
            text = re.sub(r"http\S+|www\S+", "", text)
        if remove_username:
            text = re.sub(r"@\w+", "", text)
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

        words = " ".join(df["clean_text"]).split()
        freq = Counter(words)
        top_words = freq.most_common(20)
        word_df = pd.DataFrame(top_words, columns=["Kata", "Frekuensi"])

        st.subheader("📈 20 Kata Terbanyak")
        st.dataframe(word_df)

        fig, ax = plt.subplots()
        ax.barh(word_df["Kata"], word_df["Frekuensi"])
        ax.invert_yaxis()
        st.pyplot(fig)

        st.subheader("☁️ WordCloud")
        if len(words) > 0:
            wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(words))
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wc)
            ax.axis("off")
            st.pyplot(fig)

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

        df["sentiment"] = df["clean_text"].apply(sentiment)

        st.subheader("😊 Statistik Sentimen")
        sent = df["sentiment"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(sent, labels=sent.index, autopct="%1.1f%%")
        st.pyplot(fig)

        st.subheader("📐 TF-IDF Feature Extraction")
        vectorizer = TfidfVectorizer(max_features=1000)
        X = vectorizer.fit_transform(df["clean_text"])
        y = df["sentiment"]

        tfidf_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
        st.dataframe(tfidf_df.head())

        st.subheader("🤖 Machine Learning – Naive Bayes")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = MultinomialNB()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        st.metric("Akurasi Model", round(accuracy_score(y_test, y_pred) * 100, 2))

        st.text("Classification Report")
        st.text(classification_report(y_test, y_pred))

        st.text("Confusion Matrix")
        st.write(confusion_matrix(y_test, y_pred))

        st.download_button(
            "⬇️ Download Hasil Lengkap",
            df.to_csv(index=False),
            "hasil_nlp_lengkap.csv",
            "text/csv"
        )

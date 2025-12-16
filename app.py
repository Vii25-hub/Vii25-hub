import streamlit as st
import pandas as pd
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

st.set_page_config(page_title="Text Preprocessing NLP", layout="wide")

st.title("🧹 Aplikasi Text Preprocessing NLP")
st.caption("Upload file CSV (harus memiliki kolom bernama `text`)")

# ===============================
# Upload CSV
# ===============================
uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "text" not in df.columns:
        st.error("CSV harus memiliki kolom bernama `text`")
        st.stop()

    st.subheader("📄 Data Awal")
    st.dataframe(df.head())

    st.sidebar.header("⚙️ Pilih Langkah Preprocessing")

    opt_duplicate = st.sidebar.checkbox("Remove Duplicate")
    opt_url = st.sidebar.checkbox("Remove URL")
    opt_username = st.sidebar.checkbox("Remove Username (@user)")
    opt_html = st.sidebar.checkbox("Remove HTML")
    opt_emoji = st.sidebar.checkbox("Remove Emoji")
    opt_symbol = st.sidebar.checkbox("Remove Symbols")
    opt_number = st.sidebar.checkbox("Remove Numbers")
    opt_casefold = st.sidebar.checkbox("Case Folding (Lowercase)")
    opt_stopword = st.sidebar.checkbox("Stopword Removal")
    opt_stemming = st.sidebar.checkbox("Stemming")

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    stop_factory = StopWordRemoverFactory()
    stopwords = set(stop_factory.get_stop_words())

    def preprocess(text):
        if opt_url:
            text = re.sub(r"http\S+|www\S+", "", text)
        if opt_username:
            text = re.sub(r"@\w+", "", text)
        if opt_html:
            text = re.sub(r"<.*?>", "", text)
        if opt_emoji:
            text = re.sub(r"[^\w\s,]", "", text)
        if opt_number:
            text = re.sub(r"\d+", "", text)
        if opt_symbol:
            text = text.translate(str.maketrans("", "", string.punctuation))
        if opt_casefold:
            text = text.lower()
        if opt_stopword:
            text = " ".join([w for w in text.split() if w not in stopwords])
        if opt_stemming:
            text = stemmer.stem(text)
        return text.strip()

    if st.button("🚀 Jalankan Preprocessing"):
        data = df.copy()

        if opt_duplicate:
            data = data.drop_duplicates(subset="text")

        data["clean_text"] = data["text"].astype(str).apply(preprocess)

        st.subheader("✅ Hasil Preprocessing")
        st.dataframe(data.head())

        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Hasil CSV",
            csv,
            "hasil_preprocessing.csv",
            "text/csv"
        )

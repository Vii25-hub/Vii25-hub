import streamlit as st
from PIL import Image
import time
import random

st.set_page_config(page_title="AI Deteksi Sampah", layout="centered")

st.title("🗑️ Prototipe AI Deteksi Sampah")
st.write("Upload gambar sampah lalu sistem akan menampilkan hasil deteksi (dummy).")

uploaded_file = st.file_uploader("Upload gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Gambar yang diupload", use_column_width=True)

    st.write("🔍 Mendeteksi sampah...")
    progress = st.progress(0)

    for i in range(100):
        progress.progress(i + 1)
        time.sleep(0.01)

    jenis_sampah = ["Organik", "Anorganik", "B3 (Berbahaya)", "Kertas", "Plastik"]
    hasil = random.choice(jenis_sampah)

    st.success(f"✔ Hasil Deteksi: **{hasil}**)

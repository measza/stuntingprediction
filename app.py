import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load model KNN
model = joblib.load('model_stunting_knn.pkl')

# Label mapping manual
label_map = {
    0: "normal",
    1: "severely stunted",
    2: "tinggi",
    3: "stunted"
}

# Deskripsi berdasarkan status gizi
deskripsi_map = {
    "normal": "Anak memiliki tinggi badan yang sesuai dengan usianya, menandakan pertumbuhan yang baik.",
    "severely stunted": "Anak sangat pendek untuk usianya. Ini merupakan kondisi serius yang menunjukkan masalah gizi kronis.",
    "tinggi": "Anak memiliki tinggi badan di atas rata-rata untuk usianya. Ini menunjukkan pertumbuhan yang sangat baik.",
    "stunted": "Anak lebih pendek dari standar usianya. Ini menunjukkan adanya kemungkinan masalah gizi kronis."
}

# Gambar berdasarkan hasil prediksi (dari GitHub)
gambar_map = {
    "normal": "https://raw.githubusercontent.com/measza/stunting_assets/main/normal.jpg",
    "severely stunted": "https://raw.githubusercontent.com/measza/stunting_assets/main/sangat%20terhambat.jpg",
    "tinggi": "https://raw.githubusercontent.com/measza/stunting_assets/main/tinggi.jpg",
    "stunted": "https://raw.githubusercontent.com/measza/stunting_assets/main/stunting.jpg"
}

# Gambar default (belum ada hasil)
default_image = "https://raw.githubusercontent.com/measza/stunting_assets/main/bertanya.jpg"

# Konfigurasi halaman
st.set_page_config(page_title="Klasifikasi Gizi Balita", layout="wide")
st.title("Klasifikasi Permasalahan Gizi Balita")

# Kolom input dan hasil
col1, col2 = st.columns([1, 1])

# ====================
# Form Input
# ====================
with col1:
    st.subheader("Masukkan Data Balita")
    with st.form("form_stunting"):
        jenis_kelamin = st.selectbox('Pilih jenis kelamin:', ['Laki-laki', 'Perempuan'])
        umur = st.number_input('Masukkan umur dalam bulan (0-60):', min_value=0, max_value=60, step=1)
        tinggi_badan = st.number_input('Masukkan tinggi badan balita (Cm):', min_value=30.0, max_value=130.0, step=0.1)
        submitted = st.form_submit_button("Prediksi Gizi")

# ====================
# Hasil Prediksi
# ====================
with col2:
    st.subheader("Hasil Klasifikasi")

    if submitted:
        jk_encoded = 0 if jenis_kelamin == 'Laki-laki' else 1

        # Format input untuk prediksi
        input_data = pd.DataFrame({
            'Umur (bulan)': [umur],
            'Jenis Kelamin': [jk_encoded],
            'Tinggi Badan (cm)': [tinggi_badan]
        })

        prediction = model.predict(input_data)[0]
        label = label_map.get(prediction, "Tidak diketahui")
        deskripsi = deskripsi_map.get(label, "")
        gambar = gambar_map.get(label, default_image)

        st.image(gambar, width=250)
        st.markdown(f"### Status Gizi: **{label.capitalize()}**")
        st.info(deskripsi)
    else:
        st.image(default_image, width=250)
        st.markdown("### Tidak ada hasil")
        st.write("Silakan masukkan data terlebih dahulu untuk melihat hasil prediksi tumbuh kembang balita.")

    st.markdown("""
    <hr>
    <p style='font-size: 14px;'>Standar Antropometri Anak digunakan untuk menilai status gizi berdasarkan perbandingan berat badan dan panjang/tinggi badan anak.
    Klasifikasi ini mengacu pada WHO Growth Standards untuk anak usia 0–5 tahun dan WHO Reference 2007 untuk usia 5–18 tahun.</p>
    """, unsafe_allow_html=True)

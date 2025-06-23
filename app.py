import streamlit as st
import numpy as np
import pandas as pd
import joblib

# ========================
# Load Model dan Encoder
# ========================
model = joblib.load('model_stunting_knn.pkl')

# Mapping manual label prediksi
label_map = {
    0: "normal",
    1: "severely stunted",
    2: "tinggi",
    3: "stunted"
}

# ========================
# UI Streamlit
# ========================
st.set_page_config(page_title="Prediksi Gizi Balita", layout="centered")
st.title("Prediksi Status Gizi Balita")
st.markdown("Gunakan aplikasi ini untuk memprediksi status gizi balita berdasarkan umur, jenis kelamin, dan tinggi badan.")

# ========================
# Form Input User
# ========================
with st.form("form_stunting"):
    umur = st.number_input('Umur (bulan)', min_value=0, max_value=60, step=1)
    jenis_kelamin = st.selectbox('Jenis Kelamin', ['Laki-laki', 'Perempuan'])
    tinggi_badan = st.number_input('Tinggi Badan (cm)', min_value=30.0, max_value=120.0, step=0.1)

    submit = st.form_submit_button("Prediksi")

# ========================
# Prediksi dan Output
# ========================
if submit:
    # Konversi jenis kelamin ke angka
    jk_encoded = 0 if jenis_kelamin == "Laki-laki" else 1

    # Format input menjadi dataframe
    input_data = pd.DataFrame({
        'Umur (bulan)': [umur],
        'Jenis Kelamin': [jk_encoded],
        'Tinggi Badan (cm)': [tinggi_badan]
    })

    # Lakukan prediksi
    prediction = model.predict(input_data)[0]
    prediction_label = label_map.get(prediction, "Tidak diketahui")

    # Tampilkan hasil prediksi
    st.subheader("Hasil Prediksi:")
    st.success(f"Status Gizi: {prediction_label.capitalize()}")

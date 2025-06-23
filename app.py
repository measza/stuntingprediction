import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load model dan label encoder
model = joblib.load('model_stunting_knn.pkl')
label_encoder = joblib.load('label_encoder.pkl')

st.title("Prediksi Status Gizi Balita (KNN Model)")

# Form input
with st.form("form_stunting"):
    umur = st.number_input('Umur (bulan)', min_value=0, max_value=60)
    jenis_kelamin = st.selectbox('Jenis Kelamin', ['Laki-laki', 'Perempuan'])
    tinggi_badan = st.number_input('Tinggi Badan (cm)', min_value=30.0, max_value=120.0)

    submit = st.form_submit_button("Prediksi")

# Saat tombol ditekan
if submit:
    # Konversi jenis kelamin ke angka
    jk_encoded = 0 if jenis_kelamin == "Laki-laki" else 1

    # Format input
    input_data = pd.DataFrame({
        'Umur (bulan)': [umur],
        'Jenis Kelamin': [jk_encoded],
        'Tinggi Badan (cm)': [tinggi_badan]
    })

    # Prediksi
    prediction = model.predict(input_data)[0]
    prediction_label = label_encoder.inverse_transform([prediction])[0]

    # Tampilkan hasil
    st.subheader("Hasil Prediksi:")
    st.success(f"Status Gizi: {prediction_label}")

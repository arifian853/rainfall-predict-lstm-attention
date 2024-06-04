<h1 align="center">  Rainfall Prediction with LSTM Attention </h1>

<p align="center"> 
IMPLEMENTASI ATTENTION MECHANISM PADA
ARSITEKTUR LONG SHORT-TERM MEMORY 
UNTUK PENINGKATAN AKURASI PREDIKSI
CURAH HUJAN DI KOTA BATAM
</p>

<div align="center">
    <!-- Your badges here -->
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
    <img src="https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white">
    <img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white">
    <img src="https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white">
    <img src="https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white">
    <img src="https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white">
    <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white">
    <img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white">
    <img src="https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB">
    <img src="https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white">
</div>

## Konten 

### 1. Folder ```/dataset```
Berisikan dataset mentah, proses preprocessing hingga data final.
Terdiri atas beberapa sub-folder.
- Data terisi
- Folder praproses data
- Data mentah dari BMKG
- Data mentah terolah sesuai variabel per bulan

#### Informasi dataset
Data merupakan variabel prediksi terdiri atas : 
- Tavg: Temperatur rata-rata (°C)
- RH_avg: Kelembapan rata-rata (%)
- RR: Curah hujan (mm) (yang akan diprediksi)
- ddd_x: Arah angin saat kecepatan maksimum (°)
- ff_avg: Kecepatan angin rata-rata (m/s)
- ddd_car: Arah angin terbanyak (°)
- ss: Lamanya penyinaran matahari (jam)

Variabel yang dipakai dalam pelatihan model (predictor) :
- Tavg: Temperatur rata-rata (°C)
- RH_avg: Kelembapan rata-rata (%)
- ff_avg: Kecepatan angin rata-rata (m/s)
- ss: Lamanya penyinaran matahari (jam)

Keempat variabel akan menjadi predictor untuk variabel : 
- RR: Curah hujan (mm) (yang akan diprediksi)

Data berupa angka dan arah angin pada variabel ddd_car (Arah angin terbanyak) yang belum dinormalisasi dan masih tidak beraturan pada data mentah dan yang sudah rapi dan diisi rusak dan kosongnya pada hasil preprocessing dan cleaning final, dengan jangka waktu data mulai dari 1 Januari 2019 hingga 31 Desember 2023 (5 tahun) dengan pembagian acuan data sebagai berikut : 

- Training Set: 1 Januari 2019 - 31 Desember 2021
- Validation Set: 1 Januari 2022 - 31 Desember 2022
- Testing Set: 1 Januari 2023 - 31 Desember 2023

Data akan ditambah menjadi jangka 1 Januari 2014 hingga 31 Mei 2024 untuk penambahan variasi data.

Sumber data : https://dataonline.bmkg.go.id/ [DataOnline BMKG.]
Stasiun UPT, Provinsi Kepulauan Riau, Kota Batam, 96087 - Stasiun Meteorologi Hang Nadim 

### 2. Folder ``` /code ```
Berisi: 
- Kode untuk LSTM
- Kode untuk LSTM Attention Mechanism
- Beberapa kode tes algoritma

### 3. Folder ``` /notebook ```
- Kode untuk Jupyter Notebook kode LSTM Attention Mechanism
- Beberapa kode tes algoritma dengan bentuk Jupyter Notebook

### 4. Folder ``` /tools ```
- Kode untuk untuk mengisi (fill) data kosong / hilang dengan berbagai cara seperti mean imputation, interpolation dll.
- Kode untuk normalisasi data menggunakan MinMaxScaler

### 5. Folder ``` /backend ```
- Kode backend untuk penyajian dan aplikasi prediksi dan penghubungan model prediksi.
- Cara menjalankan
```
pip install Flask
```
```
pip install flask-cors
```
- Setelahnya, jalankan server: 
```
python server.py
```
- Server akan aktif di : ```localhost:5000``` atau ```127.0.0.1:5000```

- Pergi ke browser lalu ketikkan ```localhost:5000/data``` atau ```127.0.0.1:5000/data``` untuk melihat hasil data.

### 6. Folder ``` /frontend ```
- Kode frontend untuk penyajian dan aplikasi prediksi.
- Cara menjalankan : 
```
npm install
```
- Lalu jalankan dengan : 
```
npm run dev
```
- Server akan aktif di : ```localhost:5173 ```
- Pergi ke browser lalu ketikan ```localhost:5173``` dan akan menampilkan data dari backend.

## Tech stack

### A. Model dan backend
- Python
- Flask
- Jupyter Notebook
- TensorFlow
- Keras

### B. Penyajian data / UI
- React
- TailwindCSS
- Shadcn/ui
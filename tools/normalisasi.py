import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Baca data dari file CSV
data = pd.read_csv('rr.csv')  # Ganti 'data.csv' dengan nama file CSV Anda

# Pilih kolom yang ingin dinormalisasi
selected_columns = ['RR']
data_selected = data[selected_columns]

# Inisialisasi MinMaxScaler
scaler = MinMaxScaler()

# Normalisasi data
data_normalized = scaler.fit_transform(data_selected)

# Konversi hasil normalisasi menjadi dataframe
data_normalized_df = pd.DataFrame(data_normalized, columns=selected_columns)

# Tampilkan data setelah normalisasi
print("Data setelah normalisasi:")
print(data_normalized_df)

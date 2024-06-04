import pandas as pd

# Read the CSV file
dataset_url = "https://raw.githubusercontent.com/arifian853/rainfall-predict-lstm-attention/master/dataset/cleaned/data_cleaned.csv"
df = pd.read_csv(dataset_url)

# Check for missing values in the DataFrame
missing_values = df.isnull().sum()

# Print columns with missing values, if any
print("Columns with missing values:")
print(missing_values[missing_values > 0])

# If you want to check for missing values in any row
missing_rows = df[df.isnull().any(axis=1)]
print("Rows with missing values:")
print(missing_rows)

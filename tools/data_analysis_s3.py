import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the concatenated 5-year dataset
input_file_all_years = '../dataset/filled/scenario3/final/final-data-2014-2024.csv'
df_all_years = pd.read_csv(input_file_all_years, parse_dates=['Tanggal'], index_col='Tanggal', dayfirst=True)

# Ensure the index is datetime
df_all_years.index = pd.to_datetime(df_all_years.index, dayfirst=True)

# Separate the ddd_car column
ddd_car = df_all_years['ddd_car']
df = df_all_years.drop(columns=['ddd_car'])

# Exploratory Data Analysis (EDA)
print("First few rows of the dataset (excluding ddd_car):")
print(df.head())

print("\nSummary statistics of the dataset (excluding ddd_car):")
print(df.describe())

print("\nChecking for missing values (excluding ddd_car):")
print(df.isna().sum())

# Trend Analysis
plt.figure(figsize=(14, 7))
for column in df.columns:
    plt.plot(df.index, df[column], label=column)
plt.title('Trend Analysis (2019)')
plt.xlabel('Year')
plt.ylabel('Values')
plt.legend()
plt.show()

# Correlation Analysis
correlation_matrix = df.corr()
print("\nCorrelation matrix (excluding ddd_car):")
print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()

# Anomaly Detection
# Here we use a simple method to identify anomalies: data points that are beyond 3 standard deviations from the mean
anomalies = (df - df.mean()).abs() > 3 * df.std()
print("\nAnomalies detected in the dataset (excluding ddd_car):")
print(anomalies.sum())

# Seasonal Analysis
df['Month'] = df.index.month
monthly_average = df.groupby('Month').mean()

plt.figure(figsize=(14, 7))
for column in monthly_average.columns:
    plt.plot(monthly_average.index, monthly_average[column], marker='o', label=column)
plt.title('Seasonal Analysis')
plt.xlabel('Month')
plt.ylabel('Average Values')
plt.legend()
plt.show()

# Cleanup: remove the 'Month' column added for seasonal analysis
df.drop(columns='Month', inplace=True)

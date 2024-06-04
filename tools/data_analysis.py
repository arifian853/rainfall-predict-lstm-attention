import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the concatenated 5-year dataset
input_file_all_years = '../dataset/filled/scenario3/filled_per_year/2019/2019-filled.csv'
df_all_years = pd.read_csv(input_file_all_years, parse_dates=['Tanggal'], index_col='Tanggal', dayfirst=True)

# Ensure the index is datetime
df_all_years.index = pd.to_datetime(df_all_years.index, dayfirst=True)

# Exploratory Data Analysis (EDA)
print("First few rows of the dataset:")
print(df_all_years.head())

print("\nSummary statistics of the dataset:")
print(df_all_years.describe())

print("\nChecking for missing values:")
print(df_all_years.isna().sum())

# Trend Analysis
plt.figure(figsize=(14, 7))
for column in df_all_years.columns:
    plt.plot(df_all_years.index, df_all_years[column], label=column)
plt.title('Trend Analysis (2019)')
plt.xlabel('Year')
plt.ylabel('Values')
plt.legend()
plt.show()

# Correlation Analysis
correlation_matrix = df_all_years.corr()
print("\nCorrelation matrix:")
print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()

# Anomaly Detection
# Here we use a simple method to identify anomalies: data points that are beyond 3 standard deviations from the mean
anomalies = (df_all_years - df_all_years.mean()).abs() > 3 * df_all_years.std()
print("\nAnomalies detected in the dataset:")
print(anomalies.sum())

# Seasonal Analysis
df_all_years['Month'] = df_all_years.index.month
monthly_average = df_all_years.groupby('Month').mean()

plt.figure(figsize=(14, 7))
for column in monthly_average.columns:
    plt.plot(monthly_average.index, monthly_average[column], marker='o', label=column)
plt.title('Seasonal Analysis')
plt.xlabel('Month')
plt.ylabel('Average Values')
plt.legend()
plt.show()

# Cleanup: remove the 'Month' column added for seasonal analysis
df_all_years.drop(columns='Month', inplace=True)

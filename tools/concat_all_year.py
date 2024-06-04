import pandas as pd
import os

# Directory containing the yearly CSV files
input_dir = '../dataset/filled_per_year'

# Output file path
output_file_all_years = os.path.join(input_dir, 'all_years_filled-ext.csv')

# List to hold the yearly DataFrames
df_list = []

# Loop through the files in the directory
for year in range(2019, 2024):  # Adjust the range as needed
    # Construct the filename
    input_file = os.path.join(input_dir, str(year), f'{year}-filled.csv')
    
    # Check if the file exists
    if os.path.exists(input_file):
        # Load the yearly dataset
        df_year = pd.read_csv(input_file, parse_dates=['Date'], index_col='Date')
        
        # Append the DataFrame to the list
        df_list.append(df_year)
    else:
        print(f"File for year {year} does not exist. Skipping...")

# Concatenate all yearly DataFrames into one DataFrame
df_all_years = pd.concat(df_list)

# Save the combined DataFrame to a CSV file
df_all_years.to_csv(output_file_all_years)

print(f"All yearly data has been combined and saved to {output_file_all_years}.")

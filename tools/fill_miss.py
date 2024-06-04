import pandas as pd
import os

# Define the list of filenames for each month
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Directory paths
input_dir = '../dataset/raw_per_month/2020-ext'
output_dir = '../dataset/filled_per_month/2020-ext'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each month's data file
for month in months:
    # Construct the filename
    input_file = os.path.join(input_dir, f'{month}-2020.csv')
    output_file = os.path.join(output_dir, f'{month}-2020-filled.csv')
    
    # Load the dataset
    df = pd.read_csv(input_file, parse_dates=['Date'], index_col='Date')
    
    # Replace '8888' with NaN for easier handling
    df.replace(8888, pd.NA, inplace=True)
    
    # Convert object types to more appropriate types before interpolation
    df = df.infer_objects()
    
    # Apply Interpolation
    df_interpolated = df.interpolate(method='linear')
    
    # Check for any remaining missing values
    if df_interpolated.isna().sum().sum() > 0:
        # Apply forward fill
        df_interpolated = df_interpolated.ffill()
        
        # Apply backward fill for any remaining NaNs
        df_interpolated = df_interpolated.bfill()
        
        # Optionally, you can fill with a constant value (e.g., column mean) as a last resort
        df_interpolated = df_interpolated.fillna(df_interpolated.mean())

    # Round to 1 decimal place
    df_interpolated = df_interpolated.round(1)
    
    # Save the processed data to a new file
    df_interpolated.to_csv(output_file)
    
    # Optional: Print the missing data info for verification
    missing_data_before = df.isna().sum()
    missing_data_interpolated = df_interpolated.isna().sum()
    print(f"{month} 2020:")
    print("Missing data before filling:", missing_data_before)
    print("Missing data after interpolation and additional filling:", missing_data_interpolated)
    print("-" * 50)

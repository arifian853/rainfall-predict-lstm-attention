import pandas as pd

    # Load the dataset
df = pd.read_csv('Sulawesi.csv', parse_dates=['Tanggal'], index_col='Tanggal')
    
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
df_interpolated.to_csv('Sulawesi-filled.csv')
    
    # Optional: Print the missing data info for verification
missing_data_before = df.isna().sum()
missing_data_interpolated = df_interpolated.isna().sum()
print("Missing data before filling:", missing_data_before)
print("Missing data after interpolation and additional filling:", missing_data_interpolated)
print("-" * 50)

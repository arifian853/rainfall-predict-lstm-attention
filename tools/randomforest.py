import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# Load your data (replace 'your_data.csv' with your file)
data = pd.read_csv('../dataset/preprocessing_cleaning/data2/data_cleaning-5y.csv')

# Handle 8888 placeholders
data = data.replace(8888, pd.NA) 

# Separate features and target variables
features = ['Tavg', 'RH_avg', 'ff_avg']
target_rr = data['RR']
target_ss = data['ss']

# Split data into training and testing sets
X_train, X_test, y_train_rr, y_test_rr = train_test_split(
    data[features], target_rr, test_size=0.2, random_state=42
)
X_train, X_test, y_train_ss, y_test_ss = train_test_split(
    data[features], target_ss, test_size=0.2, random_state=42
)

# Impute missing values in training data
imputer = SimpleImputer(strategy='mean')
imputer.fit(X_train)
X_train = imputer.transform(X_train)
X_test = imputer.transform(X_test)

# Train Random Forest models
rf_rr = RandomForestRegressor(random_state=42)
rf_rr.fit(X_train, y_train_rr)

rf_ss = RandomForestRegressor(random_state=42)
rf_ss.fit(X_train, y_train_ss)

# Predict missing values
predicted_rr = rf_rr.predict(X_test)
predicted_ss = rf_ss.predict(X_test)

# Replace missing values with predictions
predictions_df = pd.DataFrame({
    'RR': predicted_rr,
    'ss': predicted_ss,
})

filled_data = pd.concat([data, predictions_df], axis=1)
filled_data['RR'] = filled_data['RR'].fillna(filled_data['RR'].values)
filled_data['ss'] = filled_data['ss'].fillna(filled_data['ss'].values)

filled_data.to_csv('./result/predictive_model.csv')
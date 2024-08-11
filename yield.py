import pandas as pd
import numpy as np
import json
import sys
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Load the dataset
df = pd.read_csv("/home/shree/Test/crop_production_karnataka.csv")

# Drop the Crop_Year column
df = df.drop(['Crop_Year'], axis=1)

# Separate the features and target variables
X = df.drop(['Production'], axis=1)
y = df['Production']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Categorical columns for one-hot encoding
categorical_cols = ['State_Name', 'District_Name', 'Season', 'Crop']

# One-hot encode the categorical columns
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_train_categorical = ohe.fit_transform(X_train[categorical_cols])

# Convert categorical columns to one-hot encoding
X_test_categorical = ohe.transform(X_test[categorical_cols])

# Combine the one-hot encoded categorical columns and numerical columns
X_train_final = np.hstack((X_train_categorical, X_train.drop(categorical_cols, axis=1).values))
X_test_final = np.hstack((X_test_categorical, X_test.drop(categorical_cols, axis=1).values))

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_final, y_train)

# Get the input parameters as command line arguments
Jstate = sys.argv[1]
Jdistrict = sys.argv[2]
Jseason = sys.argv[3]
Jcrops = sys.argv[4]
Jarea = sys.argv[5]

# Create a DataFrame for the user input
user_input_df = pd.DataFrame(
    [[Jstate, Jdistrict, Jseason, Jcrops, Jarea]],
    columns=categorical_cols + ['Area']  # Ensure this matches the columns used for fitting
)

# Convert the categorical columns to one-hot encoding
user_input_categorical = ohe.transform(user_input_df[categorical_cols])

# Combine the one-hot encoded categorical columns and numerical columns
user_input_final = np.hstack((user_input_categorical, user_input_df[['Area']].astype(float)))

# Make the prediction
prediction = model.predict(user_input_final)

# Return the prediction as a string
print(str(prediction[0]))

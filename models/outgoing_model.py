import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def aggregate_traffic_data(traffic_data_tuples):
    # Aggregate each tuple into a fixed-size feature vector
    aggregated_features = []
    for sequence in traffic_data_tuples:
        if not sequence:  # Skip empty sequences
            continue
        # Example: Use mean and std of 'l' values as features
        l_values = [item[1] for item in sequence]  # Assuming item[1] is the 'l' value
        mean_l = np.mean(l_values)
        std_l = np.std(l_values)
        aggregated_features.append([mean_l, std_l])
    return np.array(aggregated_features)

# Load the data from the pickle files
with open('../data_preprocess/processed_data/vectorized_text_tuples.pkl', 'rb') as f:
    vectorized_text_tuples = pickle.load(f)

with open('../data_preprocess/processed_data/traffic_data_tuples.pkl', 'rb') as f:
    traffic_data_tuples = pickle.load(f)

X = aggregate_traffic_data(traffic_data_tuples)
y = np.vstack(vectorized_text_tuples)  # Assuming y is correctly shaped

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model using mean squared error
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Save the trained model for later use
with open('trained_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Training completed and model saved to 'trained_model.pkl'")

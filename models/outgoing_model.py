import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Function to clean and preprocess text
def preprocess_text(text):
    # Add your text preprocessing steps here
    # Example: Lowercasing and removing punctuation
    text = text.lower()
    return text

# Load and preprocess text data
def load_text_data(text_directory):
    text_data = []
    for filename in os.listdir(text_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(text_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned_text = preprocess_text(text)
                text_data.append(cleaned_text)
    return text_data

# Load traffic data
def load_traffic_data(traffic_data_file):
    return pd.read_csv(traffic_data_file)

# Main script starts here
if __name__ == "__main__":
    # Paths to the text data directory and traffic data file
    text_directory = '../data_collection/ground_truth/text_A'
    traffic_data_file = '../data_collection/ground_truth/traffic_W_incoming_timeSeries.csv'

    # Load and preprocess text and traffic data
    text_data = load_text_data(text_directory)
    traffic_data = load_traffic_data(traffic_data_file)

    # Vectorize the text data
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(text_data)
    
    # Assuming the first column of traffic_data is the target variable
    y = traffic_data.iloc[:, 0]
    features = traffic_data.iloc[:, 1:]

    # Combine text features and traffic features
    X_combined = pd.concat([pd.DataFrame(X.toarray()), features.reset_index(drop=True)], axis=1)

    # Split the combined dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

    # Initialize the RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")

    # Save the model and vectorizer for later use
    # You can use joblib or pickle for this purpose
    # joblib.dump(model, 'traffic_model.joblib')
    # joblib.dump(vectorizer, 'text_vectorizer.joblib')

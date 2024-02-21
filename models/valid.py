import pickle
import numpy as np

# Load the trained model
with open('trained_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the TF-IDF vectorizer to reverse the vectorization process
with open('../data_preprocess/processed_data/tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Function to reverse the vectorization process
def inverse_transform(vectorized_text, vectorizer):
    feature_names = vectorizer.get_feature_names_out()
    # Sort each row in the vectorized text to get the indices of the highest values
    sorted_indices = np.argsort(vectorized_text, axis=1)[:, ::-1]
    # Get the top n indices for each row
    top_n_indices = sorted_indices[:, :10]
    # Map indices to words
    top_words = feature_names[top_n_indices]
    # Join the words
    text_list = [" ".join(words) for words in top_words]
    return text_list

# Assuming you have a function `aggregate_traffic_data` similar to the training phase
def aggregate_traffic_data(traffic_data_sequence):
    # Aggregate the traffic data sequence into a fixed-size feature vector
    # This is a simplified example; adjust according to your actual aggregation logic
    l_values = [item[1] for item in traffic_data_sequence]  # Assuming item[1] is the 'l' value
    mean_l = np.mean(l_values)
    std_l = np.std(l_values)
    return np.array([[mean_l, std_l]])

def load_traffic_data_from_pickle(pickle_file_path, index):
    # Load the traffic data tuples from the pickle file
    with open(pickle_file_path, 'rb') as f:
        traffic_data_tuples = pickle.load(f)
    
    # Access the specific traffic data tuple by index
    specific_traffic_data = traffic_data_tuples[index]
    
    return specific_traffic_data

# Usage
pickle_file_path = '../data_preprocess/processed_data/traffic_data_tuples.pkl'
index_to_access = 0  # Replace with the index of the data you want to use
traffic_data_at_index = load_traffic_data_from_pickle(pickle_file_path, index_to_access)



# Prepare new input data (this should be replaced with actual new data)
# Here, we're simulating a new traffic data sequence
# new_traffic_data_sequence = [(1, 2.5, 0), (2, 3.0, 0), (3, 2.8, 0)]  # Example new traffic data

# Prepare the input data in the same way as during training
X_new = aggregate_traffic_data(traffic_data_at_index)

# Use the model to make predictions
predicted_vectorized_text = model.predict(X_new)

# Convert the vectorized text back to words
predicted_text = inverse_transform(predicted_vectorized_text, vectorizer)

# Output the predicted text
print(predicted_text)

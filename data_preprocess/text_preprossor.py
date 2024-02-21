import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os
import pickle

def clean_text(text):
    """
    A function to clean text data
    """
    # Remove punctuation and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
    # Convert to lowercase
    text = text.lower()
    # Remove leading and trailing spaces
    text = text.strip()
    return text

def load_and_preprocess_text_data(directory_path):
    # Get all text files and sort them by the numeric value in the filename
    file_paths = sorted(
        [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if filename.endswith('.txt')],
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0])
    )

    text_data = []
    file_names = []

    # Load and clean text data
    for file_path in file_paths:
        print(f"Loading file: {file_path}")  # Print the current file name
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            cleaned_text = clean_text(text)
            text_data.append(cleaned_text)
            file_names.append(os.path.basename(file_path))
    
    # Convert text data into DataFrame
    return pd.DataFrame({'filename': file_names, 'text': text_data})

def vectorize_text(df, max_features=1000):
    """
    Vectorize text data using TF-IDF
    """
    vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(df['text'])
    feature_names = vectorizer.get_feature_names_out()
    return pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

if __name__ == "__main__":
    directory_path = '../data_collection/ground_truth/text_A'
    df = load_and_preprocess_text_data(directory_path)
    vectorized_text_df = vectorize_text(df)
    
    # Convert the DataFrame into a list of tuples
    vectorized_text_tuples = list(vectorized_text_df.itertuples(index=False, name=None))
    
    # Save the list of tuples using pickle
    with open('processed_data/vectorized_text_tuples.pkl', 'wb') as f:
        pickle.dump(vectorized_text_tuples, f)

    print("Vectorized text data has been saved to 'processed_data/vectorized_text_tuples.pkl'")
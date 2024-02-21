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
    """
    Load text files from a directory, clean, and vectorize the text data
    """
    text_data = []
    file_names = []

    # Load and clean text data
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned_text = clean_text(text)
                text_data.append(cleaned_text)
                file_names.append(filename)
    
    # Convert text data into DataFrame
    df = pd.DataFrame({'filename': file_names, 'text': text_data})
    
    return df

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
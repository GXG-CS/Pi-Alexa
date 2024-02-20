import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os

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

# Example usage
if __name__ == "__main__":
    directory_path = '../data_collection/ground_truth/text_A'
    df = load_and_preprocess_text_data(directory_path)
    vectorized_text = vectorize_text(df)
    print(vectorized_text.head())
    # Set option to display all rows
    # pd.set_option('display.max_rows', None)
    
    # Print the entire DataFrame
    # print(vectorized_text)

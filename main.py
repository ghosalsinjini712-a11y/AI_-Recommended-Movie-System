# main.py

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# --- Data Loading and Initial Processing ---
# Assuming 'dataset.csv' is in the same directory as the script or provide the full path
# If the file is in Google Drive, you would need to mount Drive and adjust the path
# For this script, we assume the dataset is accessible directly.
# If you downloaded 'movies_list.pkl' and 'similarity.pkl', you can skip the data loading and processing parts below
# and directly load the pickle files.

# Option 1: Load and process data (if you don't have the pickle files)
try:
    data = pd.read_csv('dataset.csv') # Adjust path if necessary

    # Select relevant columns
    movies = data[['id', 'title', 'overview', 'genre']]

    # Handle missing values (simple imputation for demonstration)
    movies['genre'] = movies['genre'].fillna('')
    movies['overview'] = movies['overview'].fillna('')

    # Create the 'tags' column
    movies['tags'] = movies['overview'] + movies['genre']

    # Drop original overview and genre columns
    new_data = movies.drop(columns=['overview', 'genre'])

    # --- Text Vectorization ---
    cv = CountVectorizer(max_features=10000, stop_words='english')
    vector = cv.fit_transform(new_data['tags'].values.astype('U')).toarray()

    # --- Calculate Similarity ---
    similarity = cosine_similarity(vector)

    # Save the processed data and similarity matrix (optional in the script, you already did this in notebook)
    # with open('movies_list.pkl', 'wb') as f:
    #     pickle.dump(new_data, f)
    # with open('similarity.pkl', 'wb') as f:
    #     pickle.dump(similarity, f)

    print("Data loaded and processed successfully.")

# Option 2: Load data and similarity matrix from pickle files (if you have them)
except FileNotFoundError:
    print("dataset.csv not found. Attempting to load from pickle files...")
    try:
        with open('movies_list.pkl', 'rb') as f:
            new_data = pickle.load(f)
        with open('similarity.pkl', 'rb') as f:
            similarity = pickle.load(f)
        print("Data and similarity matrix loaded from pickle files.")
    except FileNotFoundError:
        print("Neither dataset.csv nor pickle files found. Please ensure your data or pickle files are in the correct directory.")
        # Exit or handle the situation where data cannot be loaded
        exit()
    except Exception as e:
        print(f"An error occurred loading pickle files: {e}")
        exit()
except Exception as e:
    print(f"An error occurred during data loading or processing: {e}")
    exit()

# --- Recommendation Function ---
def recommand(movie_title):
    """
    Recommends similar movies based on the provided movie title.

    Args:
        movie_title (str): The title of the movie to get recommendations for.
    """
    if movie_title not in new_data['title'].values:
        print(f"Movie '{movie_title}' not found in the dataset.")
        return

    try:
        index = new_data[new_data['title'] == movie_title].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])

        print(f"\nTop 5 recommendations for '{movie_title}':")
        # Skip the first one as it's the movie itself
        for i in distance[1:6]:
            print(new_data.iloc[i[0]].title)
    except Exception as e:
        print(f"An error occurred during recommendation: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    # You can call the recommand function with a movie title here
    recommand("Iron Man")
    recommand("The Godfather")
    recommand("Movie That Does Not Exist") # Example for a movie not in the dataset

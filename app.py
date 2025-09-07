import streamlit as st
import pickle
import requests

# 🎨 Custom CSS for digital blue theme
st.markdown("""
    <style>
    /* Background and font */
    .stApp {
        background-color: #0f1c2e;
        color: #e0e0e0;
        font-family: 'Segoe UI', sans-serif;
    }
    /* Header styling */
    h1, h2, h3 {
        color: #00bfff;
        text-shadow: 1px 1px 2px #000;
    }
    /* Button styling */
    .stButton>button {
        background-color: #00bfff;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5em 1em;
    }
    /* Selectbox styling */
    .stSelectbox label {
        color: #00bfff;
        font-weight: bold;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1c2e4a;
        color: white;
        border-radius: 5px;
    }
    /* Text styling */
    .stText {
        color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# 🧠 Load data
import zipfile
import os
import pickle

# Unzip the file (only if not already unzipped)
if not os.path.exists("similarity.pkl"):
    with zipfile.ZipFile("similarity.zip", "r") as zip_ref:
        zip_ref.extractall()

# Now load the pickle file
# Now load the pickle file
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

movies = pickle.load(open("movies_list.pkl", 'rb'))

movies_list = movies['title'].values

# 🔍 Poster fetcher
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# 🎞️ Trailer fetcher
def fetch_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    for video in data.get("results", []):
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

# 🎬 App UI
st.header("🎥 MOVIE RECOMMENDATION SYSTEM")
st.subheader("By Sinjini Ghosal")
st.text("This is a simple movie recommendation system built using Streamlit.")

selected_movie = st.selectbox("Select a movie from the dropdown", movies_list)

# 🔁 Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    recommended_trailers = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        recommended_trailers.append(fetch_trailer(movie_id))
    return recommended_movies, recommended_posters, recommended_trailers
if st.button("Show Recommendations"):
    names, posters, trailers = recommend(selected_movie)
    cols = st.columns(5)  # ✅ Fixed here
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
            if trailers[i]:
                st.markdown("**Watch Trailer:**")
                st.video(trailers[i])
            else:
                st.markdown("**Trailer not available on YouTube.**")
                st.markdown("[🔗 View more on TMDB](https://www.themoviedb.org/movie/{})".format(movies.iloc[i].id))
                st.video("https://www.youtube.com/watch?v=3GwjfUFyY6M")  # Optional placeholder


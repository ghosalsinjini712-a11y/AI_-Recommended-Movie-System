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
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# 🔍 Poster fetcher
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path
        bg_url = "https://image.tmdb.org/t/p/original/" + poster_path
    else:
        poster_url = "https://via.placeholder.com/500x750?text=No+Image"
        bg_url = ""
    return poster_url, bg_url


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
    bg_url = ""

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        title = movies.iloc[i[0]].title
        poster, bg = fetch_poster(movie_id)
        trailer = fetch_trailer(movie_id)

        recommended_movies.append(title)
        recommended_posters.append(poster)
        recommended_trailers.append(trailer)

        if i == distances[1]:  # First recommendation's poster becomes background
            bg_url = bg

    return recommended_movies, recommended_posters, recommended_trailers, bg_url
if st.button("Show Recommendations"):
    names, posters, trailers, bg_url = recommend(selected_movie)

    if bg_url:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("{bg_url}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            </style>
        """, unsafe_allow_html=True)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
            if trailers[i]:
                st.markdown("**Watch Trailer:**")
                st.video(trailers[i])
            else:
                st.markdown("**Trailer not available on YouTube.**")

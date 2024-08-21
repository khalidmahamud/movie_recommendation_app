import streamlit as st
import pickle
import requests
import json

# Load data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Hide fullscreen button for images
hide_img_fs = """
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
"""

# Disable horizontal scrolling in the sidebar
no_scrollbar_css = """
<style>
    .css-1d391kg {
        overflow-x: hidden;
    }
</style>
"""

st.markdown(hide_img_fs, unsafe_allow_html=True)
st.markdown(no_scrollbar_css, unsafe_allow_html=True)

# Fetch movie poster
def fetch_poster(id):
    data = requests.get(
        f"https://api.themoviedb.org/3/movie/{id}?api_key=352c482dab24783531f1750348bf52be"
    ).content
    parsed_data = json.loads(data)
    poster_path = parsed_data.get("poster_path")
    return f"https://image.tmdb.org/t/p/w500{poster_path}"

# Recommend movies
def recommend(title):
    index = movies[movies["title"] == title].index[0]
    distances = similarity[index]
    indexed_distances = list(enumerate(distances))
    indexed_distances = sorted(indexed_distances, key=lambda x: x[1], reverse=True)
    top5 = indexed_distances[1:6]
    recommended_movie_ids = movies.iloc[[item[0] for item in top5]]["id"].values
    recommend_movie_titles = movies.iloc[[item[0] for item in top5]]["title"].values
    return recommended_movie_ids, recommend_movie_titles

# Streamlit app structure
st.title("🎬 Movie Recommendation")

# Movie selection
selected_movie = st.sidebar.selectbox(
    "\u00A0",  # Non-breaking space as the label
    movies["title"].values,
)

# Display selected movie details
selected_movie_id = movies[movies["title"] == selected_movie]["id"].values[0]
poster_url = fetch_poster(selected_movie_id)
st.sidebar.image(poster_url, use_column_width=True)

# Recommendations section
if st.sidebar.button("Get Recommendations"):
    recommended_movie_ids, recommend_movie_titles = recommend(selected_movie)
    posters = [fetch_poster(id) for id in recommended_movie_ids]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommend_movie_titles[0])
        st.image(posters[0])

    with col2:
        st.text(recommend_movie_titles[1])
        st.image(posters[1])

    with col3:
        st.text(recommend_movie_titles[2])
        st.image(posters[2])

    with col4:
        st.text(recommend_movie_titles[3])
        st.image(posters[3])

    with col5:
        st.text(recommend_movie_titles[4])
        st.image(posters[4])

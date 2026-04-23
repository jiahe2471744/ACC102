import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import streamlit as st
import base64


feature_cols = ['valence', 'danceability', 'energy', 'acousticness', 'tempo', 'instrumentalness', 'speechiness']

# Mood-based threshold configuration
mood_thresholds = {
    'Happy': {'valence': 0.7, 'danceability': 0.6, 'energy': 0.6},
    'Calm': {'energy': 0.4, 'acousticness': 0.6},
    'Energetic': {'energy': 0.7, 'tempo': 120},
    'Sad': {'valence': 0.4, 'energy': 0.5},
    'Focus': {'speechiness': 0.05, 'instrumentalness': 0.5}
}

# Ideal audio feature values for each mood
ideal_values = {
    'Happy': {'valence': 0.9, 'danceability': 0.8, 'energy': 0.7, 'acousticness': 0.2},
    'Calm': {'energy': 0.2, 'acousticness': 0.8, 'valence': 0.6},
    'Energetic': {'energy': 0.9, 'tempo': 0.4, 'danceability': 0.7},
    'Sad': {'valence': 0.2, 'energy': 0.3, 'acousticness': 0.7},
    'Focus': {'speechiness': 0.02, 'instrumentalness': 0.7, 'acousticness': 0.5}
}

# Feature weights for scoring calculation
weights = {
    'Happy': {'valence': 0.4, 'danceability': 0.3, 'energy': 0.2, 'acousticness': 0.1},
    'Calm': {'energy': 0.4, 'acousticness': 0.4, 'valence': 0.2},
    'Energetic': {'energy': 0.4, 'tempo': 0.3, 'danceability': 0.3},
    'Sad': {'valence': 0.5, 'energy': 0.3, 'acousticness': 0.2},
    'Focus': {'speechiness': 0.2, 'instrumentalness': 0.7, 'acousticness': 0.1}

}


# ===================== Core Recommendation Function =====================
def recommend_songs(df, mood, top_n=10, use_weighted=True, use_similarity=True):
    thresholds = mood_thresholds.get(mood, {})
    candidate_df = df.copy()

    # Filter songs based on mood thresholds
    for feat, val in thresholds.items():
        if feat in candidate_df.columns:
            if feat == 'tempo':
                candidate_df = candidate_df[candidate_df[feat] >= val]
            else:
                candidate_df = candidate_df[candidate_df[feat] >= val]

    ideal = ideal_values[mood]
    w = weights[mood]

    # Calculate weighted matching score
    def compute_score(song):
        score = 0
        for feat in ideal.keys():
            if feat in song:
                score += w[feat] * (1 - abs(song[feat] - ideal[feat]))
        return score

    if use_weighted:
        candidate_df['weighted_score'] = candidate_df.apply(compute_score, axis=1)
    else:
        candidate_df['weighted_score'] = 0

    # Calculate cosine similarity
    if use_similarity:
        vector_feats = list(thresholds.keys())
        if not vector_feats:
            vector_feats = feature_cols[:4]

        user_vector = np.array([ideal.get(f, 0.5) for f in vector_feats]).reshape(1, -1)
        song_vectors = candidate_df[vector_feats].values
        sims = cosine_similarity(user_vector, song_vectors)[0]
        candidate_df['similarity'] = sims
    else:
        candidate_df['similarity'] = 0

    # Final recommendation score
    candidate_df['final_score'] = candidate_df['weighted_score'] + candidate_df['similarity']
    recommendations = candidate_df.sort_values(by='final_score', ascending=False).head(top_n)

    return recommendations[
        ['track_name', 'artist_name', 'popularity', 'weighted_score', 'similarity', 'final_score'] + feature_cols]


# ===================== Radar Chart Plotting Function (English Version) =====================
def plot_top1_radar(top1_song, mood):
    # Radar chart feature labels (6 core audio features)
    radar_labels = ['Energy', 'Danceability', 'Valence', 'Acousticness', 'Instrumentalness', 'Tempo']
    radar_feats = ['energy', 'danceability', 'valence', 'acousticness', 'instrumentalness', 'tempo']

    # Extract real features from top 1 recommended song
    song_vals = []
    for f in radar_feats:
        val = top1_song[f]
        # Normalize tempo to 0-1 range for visualization
        if f == 'tempo':
            val = val / 200
        song_vals.append(val)

    # Extract ideal feature values for selected mood
    ideal = ideal_values[mood]
    ideal_vals = []
    for f in radar_feats:
        ideal_vals.append(ideal.get(f, 0.5))

    # Polar chart angle calculation
    angles = np.linspace(0, 2 * np.pi, len(radar_labels), endpoint=False).tolist()
    song_vals += song_vals[:1]
    ideal_vals += ideal_vals[:1]
    angles += angles[:1]

    # Create radar chart
    fig, ax = plt.subplots(figsize=(7, 6), subplot_kw=dict(projection='polar'))

    # Plot song actual features
    ax.plot(angles, song_vals, 'o-', linewidth=2, color='#722ed1', label='Top1 Song Real Feature')
    ax.fill(angles, song_vals, alpha=0.25, color='#722ed1')

    # Plot mood ideal standard
    ax.plot(angles, ideal_vals, 'o--', linewidth=2, color='#ff7d00', label=f'{mood} Mood Ideal Standard')
    ax.fill(angles, ideal_vals, alpha=0.1, color='#ff7d00')

    # Chart styling
    ax.set_thetagrids(np.degrees(angles[:-1]), radar_labels)
    ax.set_ylim(0, 1)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    return fig


# -----------------------
# streamlit ui
# -----------------------

def set_background_image(image_path):
    """
    Set a background image to cover the entire page, including the sidebar, main content area, and header

    Parameters:
    image_path: Local file path to the background image
    """
    # Read the image file and encode it as base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    # Determine the image format based on the file extension
    if image_path.lower().endswith(('.png')):
        img_format = "png"
    elif image_path.lower().endswith(('.jpg', '.jpeg')):
        img_format = "jpeg"
    else:
        img_format = "png"

    # CSS style to apply background image to the entire page
    bg_css = f"""
    <style>
    /* Set background for the entire application */
    .stApp {{
        background: url(data:image/{img_format};base64,{encoded_string}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Set the same background image for the sidebar */
    section[data-testid="stSidebar"] {{
        background: url(data:image/{img_format};base64,{encoded_string}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Apply the same background to the top header area */
    header[data-testid="stHeader"] {{
        background: url(data:image/{img_format};base64,{encoded_string}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Make the top toolbar transparent so the background image shows through */
    .stApp header {{
        background: transparent !important;
    }}

    /* Add semi-transparent background to sidebar content to improve text readability */
    section[data-testid="stSidebar"] .stMarkdown,
    # section[data-testid="stSidebar"] .stSelectbox,
    # section[data-testid="stSidebar"] .stButton,
    section[data-testid="stSidebar"] .stNumberInput,
    section[data-testid="stSidebar"] .stContainer {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 8px;
        border-radius: 8px;
        margin: 4px 0;
    }}

    /* Sidebar title styling */
    section[data-testid="stSidebar"] .stSubheader,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 8px;
        border-radius: 8px;
    }}

    /* Main content area - add semi-transparent background to improve text readability */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1rem;
    }}

    /* Title styling - with semi-transparent background */
    .main h1, .main h2, .main h3, .main h4 {{
        background-color: rgba(0, 0, 0, 0.5);
        display: inline-block;
        padding: 10px 20px;
        border-radius: 10px;
        color: black !important;
        backdrop-filter: blur(5px);
    }}

    /* Normal text styling */
    .stMarkdown, .stTextInput, .stSelectbox, .stButton {{
        color: black;
    }}

    /* Text background in main content area */
    .main .stMarkdown {{
        background-color: rgba(0, 0, 0, 0.4);
        padding: 5px 10px;
        border-radius: 5px;
    }}

    /* DataFrame background */
    .stDataFrame {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 10px;
    }}

    /* Alert box styling */
    .stAlert {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    </style>
    """

    st.markdown(bg_css, unsafe_allow_html=True)


@st.cache_data
def get_df():
    df_data = pd.read_csv("C:\\Users\\HUAWEI\\Desktop\\songs20260419\\SpotifyFeatures.csv")
    df_data = df_data[['track_name', 'artist_name', 'popularity'] + feature_cols].dropna()
    return df_data


st.set_page_config(page_title='Song Mood Recommender',
                   page_icon='🎵',
                   layout='centered',
                   initial_sidebar_state='expanded')

set_background_image("C:\\Users\\HUAWEI\\Desktop\\songs20260419\\pic2.jpg")

df = get_df()

with st.sidebar:
    st.subheader("⚙ Recommendations Setting:")
    st.markdown("")
    with st.container(border=True):
        mood = st.selectbox('🎭 Select Your Mood', ['Happy', 'Calm', 'Energetic', 'Sad', 'Focus'])
        setting = st.number_input('🎵 Number of songs', min_value=1, max_value=50, value=10)
    gen = st.button("Generate Recommendations", type="primary", use_container_width=True)

# Main Content Area
# No additional background set here, use the background image directly
st.markdown("# 🎼 Music Recommendations")
st.markdown("## Find songs that match your current mood!")

if gen:
    if mood and setting:
        st.markdown(f"### ✨ Recommended Songs for {mood} Mood:")
        top_songs = recommend_songs(df, mood, top_n=setting)
        top_songs = top_songs.reset_index(drop=True)
        st.dataframe(top_songs, hide_index=True, use_container_width=True)

        st.markdown("### 📈 Top 1 Song Feature Radar Chart:")
        top1 = top_songs.iloc[0]
        fig_radar = plot_top1_radar(top1, mood)
        st.pyplot(fig_radar, use_container_width=True)
    else:
        st.warning("Please select a mood and number of songs!")
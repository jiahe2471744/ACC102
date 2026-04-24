# Mood-Based Music Recommendation Dashboard

## Problem & User
This Streamlit tool uses Spotify audio features and mood-matching algorithms to solve a key commercial problem: traditional music recommendations overlook users’ changing emotions and reduce platform engagement and revenue.It brings practical business value by improving user retention, content discoverability and overall customer experience for all related users and industries.It serves daily listeners, streaming platforms and independent artists with tailored music suggestions.

## Data
The dataset used in this project is the public Spotify Tracks Dataset, retrieved from Kaggle.  
- **Access Date**: April 2026
- **Key Fields**:
  - `valence`, `danceability`, `energy`, `acousticness`, `tempo`, `instrumentalness`, `speechiness` : Audio features used to categorize songs into different moods.
  - `track_name`, `artist_name`: Basic song and artist information for display in the dashboard.
  - `popularity`: Used to filter and recommend songs that are currently popular on Spotify.
 
## Methods
1. **Data Preprocessing**: Use Python to collect the raw Spotify music dataset. Conduct data cleaning by selecting core audio features and removing missing values. Perform feature transformation and tempo normalization to standardize feature scales.
2.  **Emotion Mapping Rule Definition**: Define five mood categories (Happy, Calm, Energetic, Sad, Focus). Set corresponding feature thresholds, ideal feature vectors, and weight configurations for each mood.
3.  **Recommendation Algorithm**: Filter songs using mood-specific thresholds; calculate weighted matching scores and cosine similarity; combine scores to rank and output top-N recommendations.
4.  **Visualization**: Generate a radar chart with matplotlib to compare the top-1 recommended song’s features against the ideal mood profile.
5.  **Interactive Dashboard**: Build a Streamlit web UI with mood selection, recommendation count adjustment, and dynamic display of results and visualizations.

## Key Findings
- The weighted scoring and cosine similarity algorithm effectively filters songs that match different mood profiles, such as high `valence` and `danceability` for "Happy" mood.
- The radar chart visualization clearly shows how recommended songs align with the ideal audio feature profile for each mood category.
- The Streamlit dashboard provides an intuitive way for users to select moods and receive personalized music recommendations in real time.
- Different moods have distinct audio feature patterns, confirming that features like `energy`, `valence`, and `tempo` are strong indicators of emotional tone in music.

## How to run


## Demo

## Limitations & next steps
- **Limitations**: The project relies on predefined mood rules and static dataset, which cannot capture real-time user preferences or new releases on Spotify.
  - The rule-based matching may oversimplify the nuanced relationship between audio features and mood.

- **Next steps**:
  - Connect to the Spotify Web API to fetch live and personalized user data.
  - Add more mood categories and allow users to customize their own mood profiles.
  - Implement a simple feedback system to improve recommendation accuracy over time.

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
1. **Data preparation**: Load the Spotify Tracks dataset and extract key audio features and metadata.
2. **Mood matching setup**: Define thresholds, ideal values, and weights for 5 mood categories (Happy, Calm, Energetic, Sad, Focus).
3. **Recommendation algorithm**: Calculate weighted matching scores and cosine similarity to rank songs for the selected mood.
4. **Visualization**: Plot a radar chart to compare the recommended song's features with the ideal mood profile.
5. **Interactive dashboard**: Build a Streamlit UI for mood selection, recommendation generation, and result display.

## Key Findings
- The weighted scoring and cosine similarity algorithm effectively filters songs that match different mood profiles, such as high `valence` and `danceability` for "Happy" mood.
- The radar chart visualization clearly shows how recommended songs align with the ideal audio feature profile for each mood category.
- The Streamlit dashboard provides an intuitive way for users to select moods and receive personalized music recommendations in real time.
- Different moods have distinct audio feature patterns, confirming that features like `energy`, `valence`, and `tempo` are strong indicators of emotional tone in music.

## How to run

## Demo

## Limitations & next steps
- **Limitations**: The project relies on predefined mood rules and static dataset, which cannot capture real-time user preferences or new releases on Spotify.
- **Next steps**: 
  - Connect to the Spotify Web API to fetch live and personalized user data.
  - Add more mood categories and allow users to customize their own mood profiles.
  - Implement a simple feedback system to improve recommendation accuracy over time.

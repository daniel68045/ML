## Music Recommendation Web App

Began with practicing/learning Python and some machine learning scripts, and then creating a small protoype of a music recomendation script using fake data.

Eventually, using Spotify's Web API to retrieve user data (top artists, genres, listening history), created a Flask web application to recommend a user 15-20 new artists based on their Spotify data.

## To Run:

## Setup

1. Create a `.env` file in the root directory with the following:
   ```
   CLIENT_ID=your-spotify-client-id
   CLIENT_SECRET=your-spotify-client-secret
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python3 music_rec_system.py
   ```

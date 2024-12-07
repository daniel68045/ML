import requests
from flask import Flask, render_template, request, redirect, session
import os
from dotenv import load_dotenv

# SPOTIFY USER MUSIC RECOMMENDATION
# A script that takes user data (top artists, albums, listening history) and suggests artists
# using Spotify /search API to find similar artists less frequently found in the users library.

# Load environment variables from .env file
load_dotenv()

# Spotify credentials for API access
CLIENT_ID = os.getenv("CLIENT_ID") # My ClIENT_ID
CLIENT_SECRET = os.getenv("CLIENT_SECRET") # My ClIENT_SECRET
REDIRECT_URI = "http://localhost:8888/callback"  # URL where Spotify redirects after login
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"  # Spotify Authorization URL
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"  # Spotify Token URL
SPOTIFY_API_URL = "https://api.spotify.com/v1"  # Base URL for Spotify Web API
SCOPE = "user-top-read"  # Scope for accessing user's top artists

# Flask app setup
app = Flask(__name__)
access_token = None  # Global variable to store the Spotify access token
app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route("/")
def index():
    """Render the homepage where the user can start the login process."""
    return render_template("index.html")


@app.route("/login")
def login():
    """
    Redirect the user to Spotify's login page with forced authentication.
    """
    auth_url = (
        f"{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}"
        f"&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog=true"
    )
    return redirect(auth_url)


@app.route("/callback")
def callback():
    """
    Handle Spotify's callback after user login.
    Exchange the authorization code for an access token.
    """
    global access_token
    code = request.args.get("code")  # Get the authorization code from query parameters
    # Request access token from Spotify
    token_response = requests.post(
        SPOTIFY_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
    )
    token_data = token_response.json()
    access_token = token_data.get("access_token")  # Store the access token
    return redirect("/recommend")  # Redirect to the recommendation page


@app.route("/recommend")
def recommend():
    """
    Generate artist recommendations based on the user's top genres and listening history.
    """
    if not access_token:
        # Redirect to homepage if the user isn't logged in
        return redirect("/")

    # Headers for making Spotify API requests
    headers = {"Authorization": f"Bearer {access_token}"}

    # Fetch user's top artists from Spotify
    response = requests.get(f"{SPOTIFY_API_URL}/me/top/artists", headers=headers)
    if response.status_code != 200:
        return "Error fetching top artists."

    top_artists = response.json().get("items", [])
    if not top_artists:
        return "No top artists found."

    # Collect genres from the user's top artists
    user_genres = set()
    for artist in top_artists:
        user_genres.update(artist.get("genres", []))

    # Fetch user's saved tracks and albums to identify frequently listened artists
    saved_artists = set()

    # Fetch user's saved tracks
    track_response = requests.get(f"{SPOTIFY_API_URL}/me/tracks?limit=50", headers=headers)
    if track_response.status_code == 200:
        for item in track_response.json().get("items", []):
            saved_artists.add(item["track"]["artists"][0]["name"])

    # Fetch user's saved albums
    album_response = requests.get(f"{SPOTIFY_API_URL}/me/albums?limit=50", headers=headers)
    if album_response.status_code == 200:
        for item in album_response.json().get("items", []):
            saved_artists.add(item["album"]["artists"][0]["name"])

    # Use genres to search for related artists
    recommendations = []
    for genre in user_genres:
        search_response = requests.get(
            f"{SPOTIFY_API_URL}/search",
            headers=headers,
            params={"q": f"genre:{genre}", "type": "artist", "limit": 5}
        )
        if search_response.status_code == 200:
            search_results = search_response.json().get("artists", {}).get("items", [])
            for artist in search_results:
                # Filter out artists already in the user's library and prioritize popular artists
                if artist["name"] not in saved_artists and artist.get("popularity", 0) > 50:
                    recommendations.append(artist["name"])
        else:
            print(f"Error searching for genre '{genre}': {search_response.json()}")

    # Fallback to user's top artists if no recommendations are found
    if not recommendations:
        recommendations = [artist["name"] for artist in top_artists[:5]]

    # Remove duplicates and return the recommendations
    recommendations = list(set(recommendations))
    return render_template("recommended.html", recommendations=recommendations)

@app.route("/logout")
def logout():
    """
    Clear the session and guide the user back to the app's homepage.
    """
    session.pop('access_token', None)
    return redirect("/")

if __name__ == "__main__":
    # Run the Flask app on port 8888
    app.run(port=8888)

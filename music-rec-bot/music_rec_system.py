import requests
from flask import Flask, render_template, request, redirect, session
import os
from dotenv import load_dotenv

# SPOTIFY USER MUSIC RECOMMENDATION
# A script that takes user data (top artists, albums, listening history) and suggests artists
# using Spotify /search API to find similar artists less frequently found in the users library.

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8888/callback"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"
SCOPE = "user-top-read"

app = Flask(__name__)
access_token = None
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
        f"&response_type=code&redirect_uri={
            REDIRECT_URI}&scope={SCOPE}&show_dialog=true"
    )
    return redirect(auth_url)


@app.route("/callback")
def callback():
    """
    Handle Spotify's callback after user login.
    Exchange the authorization code for an access token.
    """
    global access_token
    code = request.args.get("code")
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
    access_token = token_data.get("access_token")
    return redirect("/recommend")


@app.route("/recommend")
def recommend():
    """
    Generate artist recommendations based on the user's top genres and listening history.
    """
    if not access_token:
        return redirect("/")

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(
        f"{SPOTIFY_API_URL}/me/top/artists", headers=headers)
    if response.status_code != 200:
        return "Error fetching top artists."

    top_artists = response.json().get("items", [])
    if not top_artists:
        return "No top artists found."

    user_genres = set()
    for artist in top_artists:
        user_genres.update(artist.get("genres", []))

    saved_artists = set()

    track_response = requests.get(
        f"{SPOTIFY_API_URL}/me/tracks?limit=50", headers=headers)
    if track_response.status_code == 200:
        for item in track_response.json().get("items", []):
            saved_artists.add(item["track"]["artists"][0]["name"])

    album_response = requests.get(
        f"{SPOTIFY_API_URL}/me/albums?limit=50", headers=headers)
    if album_response.status_code == 200:
        for item in album_response.json().get("items", []):
            saved_artists.add(item["album"]["artists"][0]["name"])

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
                if artist["name"] not in saved_artists and artist.get("popularity", 0) > 50:
                    recommendations.append(artist["name"])
        else:
            print(f"Error searching for genre '{
                  genre}': {search_response.json()}")

    if not recommendations:
        recommendations = [artist["name"] for artist in top_artists[:5]]

    recommendations = list(set(recommendations))
    return render_template("recommended.html", recommendations=recommendations)


if __name__ == "__main__":
    app.run(port=8888)

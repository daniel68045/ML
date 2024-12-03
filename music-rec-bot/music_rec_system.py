import requests
from flask import Flask, request, redirect


# MUSIC RECOMMENDATION BOT
# Script that takes a Spotify account and artist data and recommends the user 5 artists based on their top artist
# genres Spotify credentials
CLIENT_ID = "afe2675f96b2402283f7add8737844eb"
CLIENT_SECRET = "a2c45d6b356d42e19487fdba14c42a6d"
REDIRECT_URI = "http://localhost:8888/callback"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"
SCOPE = "user-top-read"

app = Flask(__name__)
access_token = None  # Global variable for access token


@app.route("/")
def login():
    # Redirect user to Spotify login page
    auth_url = f"{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return redirect(auth_url)


@app.route("/callback")
def callback():
    global access_token
    code = request.args.get("code")

    # Exchange authorization code for access token
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
    return "Authentication successful! You can now fetch your top artists."


@app.route("/test")
def test():
    if not access_token:
        return "Error: No access token. Please log in first."

    # Headers for the API call
    headers = {"Authorization": f"Bearer {access_token}"}

    # Fetch user's top artists
    response = requests.get(f"{SPOTIFY_API_URL}/me/top/artists", headers=headers)
    if response.status_code != 200:
        return f"Error fetching top artists: {response.status_code}, {response.json()}"

    top_artists = response.json().get("items", [])
    if not top_artists:
        return "No top artists found."

    recommendations = set()  # Use a set to avoid duplicates
    user_genres = set()

    # Collect genres from user's top artists
    for artist in top_artists:
        user_genres.update(artist.get("genres", []))

    # Fetch related artists for each top artist
    for artist in top_artists:
        artist_id = artist["id"]
        artist_name = artist["name"]

        # Fetch related artists
        related_response = requests.get(f"{SPOTIFY_API_URL}/artists/{artist_id}/related-artists", headers=headers)
        if related_response.status_code == 200:
            related_artists = related_response.json().get("artists", [])
            if related_artists:
                print(
                    f'Related artists for {artist_name}:'
                    f'{[related_artist["name"] for related_artist in related_artists]}')
                for related_artist in related_artists:
                    related_genres = set(related_artist.get("genres", []))
                    if related_genres & user_genres:  # Check for genre overlap
                        recommendations.add(related_artist["name"])
            else:
                print(f"No related artists found for {artist_name}.")
        else:
            print(f"Failed to fetch related artists for {artist_name}: {related_response.json()}")

    # Fallback to top artists if no recommendations found
    if not recommendations:
        recommendations = {artist["name"] for artist in top_artists[:5]}  # Top 5 artists
        return f"No related artists found. Recommending your top artists: {', '.join(recommendations)}"

    return f"Recommended artists based on your favorite genres: {', '.join(recommendations)}"


@app.route("/manual-test")
def manual_test():
    if not access_token:
        return "Error: No access token. Please log in first."

    # Headers for the API call
    headers = {"Authorization": f"Bearer {access_token}"}

    # Hardcoded artist ID for Drake
    artist_id = "06HL4z0CvFAxyc27GXpf02"  # Replace with another ID if needed
    artist_name = "Taylor Swift"

    # Fetch related artists for the hardcoded artist
    related_response = requests.get(f"{SPOTIFY_API_URL}/artists/{artist_id}/related-artists", headers=headers)
    if related_response.status_code == 200:
        related_artists = related_response.json().get("artists", [])
        if related_artists:
            related_artist_names = [artist["name"] for artist in related_artists]
            print(f"Related artists for {artist_name}: {related_artist_names}")
            return f"Related artists for {artist_name}: {', '.join(related_artist_names)}"
        else:
            print(f"No related artists found for {artist_name}.")
            return f"No related artists found for {artist_name}."
    else:
        print(f"Error fetching related artists for {artist_name}: {related_response.json()}")
        return f"Error fetching related artists for {artist_name}: {related_response.json()}"


if __name__ == "__main__":
    app.run(port=8888)

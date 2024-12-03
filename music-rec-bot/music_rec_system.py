import requests
from flask import Flask, request, redirect

# Spotify credentials
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

    # Redirect to the recommendation endpoint
    return redirect("/recommend")


@app.route("/recommend")
def recommend():
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

    # Extract genres from top artists
    user_genres = set()
    for artist in top_artists:
        user_genres.update(artist.get("genres", []))

    # Fetch user's saved tracks and albums to identify frequently listened artists
    saved_artists = set()

    # Fetch saved tracks
    track_response = requests.get(f"{SPOTIFY_API_URL}/me/tracks?limit=50", headers=headers)
    if track_response.status_code == 200:
        for item in track_response.json().get("items", []):
            saved_artists.add(item["track"]["artists"][0]["name"])

    # Fetch saved albums
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
                # Filter out artists already in the user's saved library
                if artist["name"] not in saved_artists and artist.get("popularity", 0) > 50:
                    recommendations.append(artist["name"])
        else:
            print(f"Error searching for genre '{genre}': {search_response.json()}")

    # Fallback to top artists if no recommendations found
    if not recommendations:
        recommendations = [artist["name"] for artist in top_artists[:5]]

    # Remove duplicates and return the recommendations
    recommendations = list(set(recommendations))
    return f"Recommended artists: {', '.join(recommendations)}"


if __name__ == "__main__":
    app.run(port=8888)

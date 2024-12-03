import requests


# Test script to make sure api is valid and endpoint /related-artists is working
# Basically a dupe of debug_related_artists.py - probably will delete this script
# Current access token as of 12/03/24 - 1:00 AM
ACCESS_TOKEN = ("BQAeOL2jF9EOT1b40RZbBPb_ZFx_cfCJy-LxKc0iM_RTvZduk_XVKQXRJeR0rPBKkvTZ"
                "xR6HZgSQ34YO_KRKPRyYYUc9FD2XD4XmkPqZm5MqkK6kmIs")

# Spotify API endpoints
SPOTIFY_API_URL = "https://api.spotify.com/v1"


def test_api():
    # Headers for authorization
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    # Test 1: Get user's top artists
    url_top_artists = f"{SPOTIFY_API_URL}/me/top/artists"
    response_top_artists = requests.get(url_top_artists, headers=headers)

    print("Fetching user's top artists...")
    if response_top_artists.status_code == 200:
        top_artists = response_top_artists.json()
        print("Top artists fetched successfully!")
        print("Sample artist:", top_artists["items"][0]["name"])
    else:
        print("Error fetching top artists:", response_top_artists.status_code)
        print(response_top_artists.json())
        return

    # Test 2: Get related artists for a specific artist
    artist_id = top_artists["items"][0]["id"]  # Use the first artist's ID
    url_related_artists = f"{SPOTIFY_API_URL}/artists/{artist_id}/related-artists"
    response_related_artists = requests.get(url_related_artists, headers=headers)

    print(f"\nFetching related artists for artist ID: {artist_id}...")
    if response_related_artists.status_code == 200:
        related_artists = response_related_artists.json()
        if related_artists["artists"]:
            print("Related artists fetched successfully!")
            print("Sample related artist:", related_artists["artists"][0]["name"])
        else:
            print("No related artists found.")
    else:
        print("Error fetching related artists:", response_related_artists.status_code)
        print(response_related_artists.json())


# Run the test
if __name__ == "__main__":
    test_api()

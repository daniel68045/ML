import requests


# Debug for /related-artists endpoint - after thorough testing, no artist ID's work - potential Spotify issue
ACCESS_TOKEN = ('BQCiC6gHvH3oQsfnRUR7u0t0C7V4XCIztFQ77yi4NJDQgaMSt9mgkty5mLaGk0JuhYo6Y'
                'YU2at8pkQAB8fHGfetRRpLTsJC06d9Dop1aLoVUHy7I6mw')  # Current valid access token
ARTIST_ID = "3TVXtAsR1Inumwj472S9r4"  # Test Spotify ID

url = f"https://api.spotify.com/v1/artists/{ARTIST_ID}/related-artists"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Related Artists:", response.json())
elif response.status_code == 404:
    print("Error: Artist not found or no related artists available.")
else:
    print(f"Error: {response.status_code}")
    print(response.json())

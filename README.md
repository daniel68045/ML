## Note

This app is in development mode, Spotify restricts the number of users that can access its Web API, please submit a response to this form so you can be added to the list of valid users: https://docs.google.com/forms/d/1RczCzGf9NKg6bcSy68FWf1kPq-NUKQZfLnEnpwsyWQ0/edit

## Music Recommendation System

A Flask app that uses Spotify's Web API to retrieve user data (top artists, genres, listening history) to recommend 30+ new artists based on the user’s Spotify library.

## How to Run

1. Clone into the repository with web URL:
   ```
   git clone https://github.com/daniel68045/Music-Rec.git
    ```
2. Create a new virtual enviroment (optional):
   ```
   python3 -m venv .venv
   source .venv/bin/activate #MacOS
   source .venv/Scripts/activate #Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up enviromental variables in .env files
   ```
   CLIENT_ID=<your-spotify-client-id>
   CLIENT_SECRET=<your-spotify-client-secret>
   FLASK_SECRET_KEY=<a-random-secret-key>
   ```
5. Run the application:
   ```
   python3 music_rec_system.py
   ```


Verify your Spotify at https://docs.google.com/forms/d/1RczCzGf9NKg6bcSy68FWf1kPq-NUKQZfLnEnpwsyWQ0/edit

## Spotify Music Recommendations

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

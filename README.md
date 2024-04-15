# Spotify Playlist Organizer

This project is a web application that allows you to sort your Spotify playlist by release date, album name, and artist name. You can also create a new playlist or update an existing one with the sorted tracks.

## Getting Started

To use this application, you need to have a Spotify account and create a Spotify application to obtain the client ID and client secret. You also need to have Python 3 installed on your computer.

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/tweiss9/Sort-Spotify-Playlist.git
   ```

2. Open your terminal and change the directory to where you saved the repository

   ```bash
   cd <YOUR_PROJECT_LOCATION>
   ```

3. Install the required Python packages using the following command:

   ```bash
   pip install -r requirements.txt
   ```

4. Generate a Spotify project through the [Spotify for Developers console](https://developer.spotify.com/) and a [Flask Secret Key](https://flask.palletsprojects.com/en/2.3.x/config/)
5. Create a .env file and fill in the following environment variables with your Spotify application credentials and your Flask secret key:

   ```bash
   PROJECT_SPOTIFY_FLASK_SECRET_KEY=<YOUR_SECRET_KEY>
   PROJECT_SPOTIFY_WEBSITE_SPOTIFY_CLIENT_ID=<YOUR_CLIENT_ID>
   PROJECT_SPOTIFY_WEBSITE_SPOTIFY_CLIENT_SECRET=<YOUR_CLIENT_SECRET>
   PROJECT_SPOTIFY_WEBSITE_SPOTIFY_REDIRECT_URI=<YOUR_REDIRECT_URI>
   ```

6. Run the following command to start the web application:

   ```bash
   python app.py
   ```

7. Open your web browser and go to [http://localhost:5000](http://localhost:5000) to access the application.

## Usage

1. Log in to your Spotify account using the web application.
2. Select the playlist you want to sort.
3. Choose the sorting criteria from the "Sort By" dropdown menu.
4. Choose whether to create a new playlist or update an existing one from the "Create or Update" dropdown menu.
5. Click the "Organize" button to sort the tracks.
6. Wait for the progress bar to complete.

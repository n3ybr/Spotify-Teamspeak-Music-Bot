# Spotify-Teamspeak Music Bot

A Python-based music bot that integrates Spotify playback with a TeamSpeak 3 server. The bot allows users to play, queue, and control music directly from TeamSpeak text commands.

## Features

- Play music from Spotify.
- Queue tracks for playback.
- Control playback (play, pause, next).
- Automatically handles Spotify device activation.
- Sends periodic keepalive messages to maintain the connection with the TeamSpeak server.

## Prerequisites

- Python 3.8 or higher
- TeamSpeak 3 client installed
- Spotify Premium account
- Spotify Developer API credentials
- A running TeamSpeak 3 server

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/spotify-teamspeak-bot.git
    cd spotify-teamspeak-bot
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up Spotify Developer API:

    - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    - Create a new application and note the `Client ID` and `Client Secret`.
    - Set the redirect URI to `http://localhost:8888/callback`.

4. Configure the bot:
      {
          "spotify": {
              "client_id": "your_spotify_client_id",
              "client_secret": "your_spotify_client_secret",
              "redirect_uri": "http://localhost:8888/callback",
              "scope": "user-read-playback-state user-modify-playback-state streaming"
          },
          "teamspeak": {
              "host": "your_teamspeak_server_ip",
              "port": 10011,
              "server_id": 1,
              "username": "serveradmin",
              "password": "your_teamspeak_password",
              "nickname": "MusicBot",
              "channel_id": 1
          }
      }
## Usage

1. Start the bot:

    ```bash
    python bot.py
    ```

2. Use the following commands in TeamSpeak:

    - `!play <track_name>`: Search and play a track from Spotify.
    - `!stop`: Stop the current playback.
    - `!next`: Skip to the next track in the queue.

## Example

1. Play a track:

    ```
    !play Despacito
    ```

    The bot will search for "Despacito" on Spotify, start playback, and notify the TeamSpeak channel.

2. Add a track to the queue:

    ```
    !play Shape of You
    ```

    If music is already playing, the bot will add "Shape of You" to the playback queue.

3. Skip to the next track:

    ```
    !next
    ```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Issues

If you encounter any issues, feel free to open an issue in the GitHub repository.

---

Enjoy using the Spotify-Teamspeak Music Bot! If you like this project, don't forget to star the repository.

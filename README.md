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
- [Virtual Audio Cable (VAC)](https://vb-audio.com/Cable/) for routing audio

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

     ```json
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
     ```

5. Set up Virtual Audio Cable:

   - Download and install [Virtual Audio Cable (VAC)](https://vb-audio.com/Cable/).
   - Open the VAC Control Panel and create at least one virtual cable.
   - In Spotify, set the output device to the virtual cable:
     - Go to Spotify settings > Advanced Settings > Playback > Select VAC as the output device.
   - In TeamSpeak, configure your input device to use the same VAC:
     - Open TeamSpeak > Options > Capture > Set Capture Device to the VAC cable.

## TeamSpeak Client Setup
    1. Download and install the [TeamSpeak 3 client](https://teamspeak.com/en/downloads/).
    2. Open the TeamSpeak client and connect to your server:
       - Go to `Connections > Connect`.
       - Enter your server address and port.
       - Click `Connect`.
    
    3. Set up your input and output devices:
       - Go to `Tools > Options > Capture`.
       - Set `Capture Device` to the virtual cable configured in Virtual Audio Cable (VAC).
       - Go to `Playback` and choose your desired output device.
    
    4. Save the configuration and ensure that the bot is able to join the server and send audio through the configured VAC channel.


## Usage

1. Start the bot:

   ```bash
   python main.py
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


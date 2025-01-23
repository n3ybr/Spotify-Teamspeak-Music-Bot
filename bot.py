import subprocess
import threading
import time
import ts3
import spotipy
from ts3.query import TS3TimeoutError
from spotipy.oauth2 import SpotifyOAuth

class SpotifyTeamSpeakBot:
    def __init__(self, config):
        self.TS3_PATH = config['TS3_PATH']
        self.TS3_HOST = config['TS3_HOST']
        self.TS3_PORT = config['TS3_PORT']
        self.TS3_SERVER_ID = config['TS3_SERVER_ID']
        self.TS3_USERNAME = config['TS3_USERNAME']
        self.TS3_PASSWORD = config['TS3_PASSWORD']
        self.TS3_NICKNAME = config['TS3_NICKNAME']
        self.CHANNEL_ID = config['CHANNEL_ID']

        self.SPOTIFY_CLIENT_ID = config['SPOTIFY_CLIENT_ID']
        self.SPOTIFY_CLIENT_SECRET = config['SPOTIFY_CLIENT_SECRET']
        self.SPOTIFY_REDIRECT_URI = config['SPOTIFY_REDIRECT_URI']
        self.SPOTIFY_SCOPE = config['SPOTIFY_SCOPE']

        self.track_queue = []
        self.spotify = self._initialize_spotify()

    def _initialize_spotify(self):
        sp_oauth = SpotifyOAuth(
            client_id=self.SPOTIFY_CLIENT_ID,
            client_secret=self.SPOTIFY_CLIENT_SECRET,
            redirect_uri=self.SPOTIFY_REDIRECT_URI,
            scope=self.SPOTIFY_SCOPE
        )
        access_token = sp_oauth.get_access_token(as_dict=False)
        return spotipy.Spotify(auth=access_token)

    def start_teamspeak_client(self):
        command = f'"{self.TS3_PATH}" ts3server://{self.TS3_HOST}?port={self.TS3_PORT}&nickname={self.TS3_NICKNAME}&channel={self.CHANNEL_ID}'
        try:
            subprocess.Popen(command, shell=True)
            print("TeamSpeak клиент запущен.")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка запуска TeamSpeak клиента: {e}")

    def search_track(self, query):
        results = self.spotify.search(q=query, type="track", limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_uri = track['uri']
            track_name = track['name']
            track_artist = ', '.join(artist['name'] for artist in track['artists'])
            return track_uri, track_name, track_artist
        return None, None, None

    def play_music(self, track_uri):
        try:
            track_info = self.spotify.track(track_uri)
            track_duration_ms = track_info['duration_ms']

            print(f"Запускаем трек: {track_info['name']} - {', '.join(artist['name'] for artist in track_info['artists'])}")
            print(f"Длительность: {track_duration_ms / 1000:.2f} секунд")

            devices = self.spotify.devices()
            active_device = None

            for device in devices['devices']:
                if device['is_active']:
                    active_device = device['id']
                    break

            if not active_device and devices['devices']:
                active_device = devices['devices'][0]['id']
                self.spotify.transfer_playback(device_id=active_device, force_play=False)
                print(f"Активировано устройство: {devices['devices'][0]['name']}")

            if not active_device:
                print("Нет доступных устройств для воспроизведения.")
                return

            playback = self.spotify.current_playback()

            if playback and playback['is_playing']:
                print("Трек уже играет, добавляем в очередь.")
                self.track_queue.append(track_uri)
                return

            self.spotify.start_playback(device_id=active_device, uris=[track_uri])

        except spotipy.exceptions.SpotifyException as e:
            print(f"Ошибка Spotify API: {e}")

    def play_next_track(self):
        while True:
            if self.track_queue:
                track_uri = self.track_queue.pop(0)
                self.play_music(track_uri)
            else:
                time.sleep(1)

    def handle_teamspeak_commands(self, ts3_conn):
        while True:
            try:
                event = ts3_conn.wait_for_event()
                if event and "msg" in event.parsed[0]:
                    message = event.parsed[0]["msg"]
                    invoker_id = event.parsed[0]["invokerid"]

                    if message.startswith("!play"):
                        query = message[len("!play "):].strip()
                        track_uri, track_name, track_artist = self.search_track(query)

                        if track_uri:
                            devices = self.spotify.devices()
                            is_playing = any(device['is_active'] for device in devices['devices'])

                            if is_playing:
                                self.track_queue.append(track_uri)
                                ts3_conn.send("sendtextmessage", {
                                    "targetmode": 2,
                                    "target": 2,
                                    "msg": f"Добавлено в очередь: {track_name} by {track_artist}"
                                })
                            else:
                                ts3_conn.send("sendtextmessage", {
                                    "targetmode": 2,
                                    "target": 2,
                                    "msg": f"Воспроизводится: {track_name} by {track_artist}"
                                })
                                self.play_music(track_uri)
                        else:
                            ts3_conn.send("sendtextmessage", {
                                "targetmode": 2,
                                "target": 2,
                                "msg": "Трек не найден."
                            })

                    elif message.startswith("!stop"):
                        devices = self.spotify.devices()
                        active_device = None

                        for device in devices['devices']:
                            if device['is_active']:
                                active_device = device['id']
                                break

                        if not active_device:
                            print("Нет активного устройства для воспроизведения.")
                            return

                        self.spotify.pause_playback(device_id=active_device)
                        print("Трек завершён. Воспроизведение остановлено.")
                        ts3_conn.send("sendtextmessage", {
                            "targetmode": 2,
                            "target": 2,
                            "msg": "Остановлено воспроизведение."
                        })
                        self.track_queue.clear()

            except TS3TimeoutError:
                pass
            except Exception as e:
                print(f"Ошибка TeamSpeak: {e}")

    def send_keepalive_periodically(self, ts3_conn, interval=540):
        while True:
            try:
                if ts3_conn is not None:
                    ts3_conn.send_keepalive()
                    print("Keepalive отправлен.")
                else:
                    print("Соединение с сервером отсутствует, пропускаем отправку keepalive.")
            except TS3TimeoutError:
                print("Ошибка таймаута при отправке keepalive.")
            except Exception as e:
                print(f"Ошибка при отправке keepalive: {e}")

            time.sleep(interval)

    def run(self):
        self.start_teamspeak_client()

        with ts3.query.TS3Connection(self.TS3_HOST, self.TS3_PORT) as ts3_conn:
            ts3_conn.login(client_login_name=self.TS3_USERNAME, client_login_password=self.TS3_PASSWORD)
            ts3_conn.send("use", {"sid": self.TS3_SERVER_ID})

            keepalive_thread = threading.Thread(target=self.send_keepalive_periodically, args=(ts3_conn,), daemon=True)
            keepalive_thread.start()

            ts3_conn.send("servernotifyregister", {"event": "textchannel", "id": self.CHANNEL_ID})
            print(f"Бот подключён и слушает канал ID {self.CHANNEL_ID}.")

            queue_thread = threading.Thread(target=self.play_next_track, daemon=True)
            queue_thread.start()

            self.handle_teamspeak_commands(ts3_conn)

# Пример использования
if __name__ == "__main__":
    config = {
        "TS3_PATH": r"C:\\Program Files\\TeamSpeak 3 Client\\ts3client_win64.exe",
        "TS3_HOST": "",
        "TS3_PORT": 10011,
        "TS3_SERVER_ID": 1,
        "TS3_USERNAME": "serveradmin",
        "TS3_PASSWORD": "",
        "TS3_NICKNAME": "MusicBot",
        "CHANNEL_ID": 1,
        "SPOTIFY_CLIENT_ID": "",
        "SPOTIFY_CLIENT_SECRET": "",
        "SPOTIFY_REDIRECT_URI": "http://localhost:8888/callback",
        "SPOTIFY_SCOPE": "user-read-playback-state user-modify-playback-state streaming"
    }

    bot = SpotifyTeamSpeakBot(config)
    bot.run()

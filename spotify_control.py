import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="65f1ceedce8f41039cbb3c7a091c9732",
        client_secret="b1af5a8a79ac4d55804964c55a34c9f7",
        redirect_uri="https://localhost:8888/callback",
        scope="user-read-playback-state,user-modify-playback-state"
    )
)

def play_song(song_name):

    results = sp.search(
        q=song_name,
        type="track",
        limit=1
    )

    tracks = results["tracks"]["items"]

    if tracks:

        uri = tracks[0]["uri"]

        devices = sp.devices()

        if devices["devices"]:

            device_id = devices["devices"][0]["id"]

            sp.start_playback(
                device_id=device_id,
                uris=[uri]
            )

            return True

    return False


def call_playlist(creator, playlist_id):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import pandas as pd
    import subprocess
    
    file = "secret.keys"
    while True:
        try:
            with open(file, "r") as f:
                keys = f.readlines()
                cid = keys[0].strip()
                secret = keys[1].strip()
            break
        except FileNotFoundError:
            with open(file, "w") as f:
                cid = input("Enter your client id: ")
                secret = input("Enter your client secret: ")
                f.write(cid + "\n" + secret)
            continue

    subprocess.check_call(["attrib","+H",file])


    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    
    #step1

    playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    #step2
    
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    for track in playlist:
        # Create empty dict
        playlist_features = {}
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]
        
        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)


    return playlist_df
    
#artist, album, track_name, track_id, danceability, energy, key, loudness, mode, speechiness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature
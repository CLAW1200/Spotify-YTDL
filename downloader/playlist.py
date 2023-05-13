
def call_playlist(window, creator, playlist_id, keys):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import pandas as pd
    import subprocess
    
    file = keys
    while True:
        try:
            with open(file, "r") as f:
                keys = f.readlines()
                cid = keys[0].strip()
                secret = keys[1].strip()
            f.close()
            break
        except FileNotFoundError:
            print ("\n")
            print ("Not sure what your client id is?")
            print ("Please visit https://developer.spotify.com/dashboard/applications and create an application to get your client id and secret.")
            print ("\n")
            continue
        except IndexError:
            print ("\n")
            print ("Your keys file is empty. Please enter your client id and secret and save them.")
            print ("\n")
            continue

    subprocess.check_call(["attrib","+H",file])


    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    
    #step1

    playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    #step2
    try:
        playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    except spotipy.client.SpotifyException as e:
        print ("\n")
        print ("Check Your Playlist Link.")
        print (e)
        print ("\n")
        """window.playlistLinkBox.setStyleSheet("color: red;")"""
        return
    except spotipy.oauth2.SpotifyOauthError as e:
        print ("\n")
        print ("Check Your API Keys.")
        print (e)
        print ("\n")
        """window.spotifyID.setStyleSheet("color: red;")
        window.spotifySecret.setStyleSheet("color: red;")"""
        return

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
def call_playlist(creator, playlist_id, keys):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import pandas as pd
    import subprocess
    import sys
    print ("Getting playlist data...")
    print ("This could take some time.")
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
            print("Not sure what your client id is?")
            print("Please visit https://developer.spotify.com/dashboard/applications and create an application to get your client id and secret.")
            break
        except IndexError:
            print("Your keys file is empty. Please enter your client id and secret and save them.")
            break

    try:
        if sys.platform == "win32":
            subprocess.check_call(["attrib","+H",file]) 
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
        playlist_df = pd.DataFrame(columns = playlist_features_list)
        counter = 0
        offset = 0
        while True:
            try:
                playlist = sp.user_playlist_tracks(creator, playlist_id, offset=offset, fields="items(track(name,id,album(artists(name),name)))")["items"]
                playlistName = sp.user_playlist(creator, playlist_id, fields="name")["name"]
                if len(playlist) == 0:
                    break
                offset += len(playlist)
            except spotipy.client.SpotifyException as e:
                print("\n")
                print("Check Your Playlist Link.")
                print(e)
                print("\n")
                return
            except spotipy.oauth2.SpotifyOauthError as e:
                print("\n")
                print("Check Your API Keys.")
                print(e)
                print("\n")
                return
            # create dictionary with plalist id 

            for track in playlist:
                counter+=1
                try:
                    # Create empty dict
                    playlist_features = {}
                    # Get metadata
                    playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
                    playlist_features["album"] = track["track"]["album"]["name"]
                    playlist_features["track_name"] = track["track"]["name"]
                    playlist_features["track_id"] = track["track"]["id"]

                    playlist_features["playlist"] = playlistName

                    
                    # Get audio features
                    audio_features = sp.audio_features(playlist_features["track_id"])[0]
                    for feature in playlist_features_list[4:]:
                        playlist_features[feature] = audio_features[feature]
                    
                    # Concat the dfs
                    track_df = pd.DataFrame(playlist_features, index = [0])
                    playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
                except Exception as e:
                    print(f"{e} at track {counter}. Skipping.")
                    pass
        return playlist_df
    except UnboundLocalError as e:
        print("Please enter your client id and secret and save them.")
        print(e)
        return
    except TypeError as e:
        print("Please enter your client id and secret and save them.")
        print(e)
        return
    except spotipy.oauth2.SpotifyOauthError as e:
        print("Please enter your client id and secret and save them.")
        print(e)
        return
    except spotipy.client.SpotifyException as e:
        print("Please enter your client id and secret and save them.")
        print(e)
        return
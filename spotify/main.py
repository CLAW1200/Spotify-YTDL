
from urllib import request
import spotify_playlist_handler as sph
import download_handler as dh

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def extractSpotifyLink(link):
    if "playlist" not in link:
        print ("Not a spotify playlist link")
        exit()
    link = link.split("/")[-1]
    link = link.split("?")[0]
    return link

cid = '3f45da55c2484df48105cf8705050028'
secret = '22384d0153914594b8ab8dc718bba01b'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

link = extractSpotifyLink(str(input("Enter the link of the playlist: ")))
username = str(input("Enter the username of the playlist creator: "))

data = (sph.call_playlist(username, link, sp))
for i in range(len(data)):
    row = data.iloc[i].tolist()
    
    request = str(f"{row[2]} {row[0]} {row[1]} topic")

    print (request)
    dh.download_video(request)






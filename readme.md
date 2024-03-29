

# Download your spotify playlists as FLAC or MP3
![newsmall](https://github.com/CLAW1200/Spotify-YTDL/assets/92749103/af7f8a63-f134-4686-8e3b-580b3331330e)


Requires FFMPEG to be installed and added to PATH.

- Download a Spotify Playlist by finding the corresponding audio on YouTube.
- Downloads as FLAC or MP3 with correct metadata.
- Choose Compression Level.

Getting Spotify's API access:   
- You just need a Spotify account.
- Login to https://developer.spotify.com/dashboard/applications and create an application.
- Open the app and copy the Client ID and Client Secret.
- You should only need to enter these once.
  
Run main.py to open the GUI.
(Your playlist will need to be public)

Limitations and accuracy:
The program will get the correct file ~99% of the time. However this can vary depending on if the song is **very** popular or **very** niche. I will do an actual test at some point to get a better idea of how accurate it can be.

Method of obtaining the audio (v2.2):

Currently, every search has the word "provided to youtube" appended to the request. The reason for this is due to the way artist's distribute music on platforms.
If a YouTube channel looks something like "Artist Name - Topic" then it means it came from the distributing platform that also sent the audio to platforms such as Spotify and Itunes.
Music from these channels are the exact same audio file as the ones released on Spotify (still compressed by youtube at 320kbps however), so prioritizing these in the search is a good way of getting the exact audio at a high quality (320kbps is the highest supported by YouTube at the moment). 

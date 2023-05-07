![Untitled-3](https://user-images.githubusercontent.com/92749103/184211319-5d444455-b21e-4d9c-ae07-5fced0d56e06.png)

Download a Spotify Playlist by finding the corresponding audio on YouTube.
Downloads as .FLAC with correct metadata.



Getting Spotify's API access:   
- You just need a Spotify account.
- Login to https://developer.spotify.com/dashboard/applications and create an application.
- Open the app and copy the Client ID and Client Secret.
- You will only need to enter these once.
  


Run either main.py or the executable and enter the link to the playlist you want to download.
(Make sure the playlist is public!)

Limitations and accuracy:

The program will get the correct file ~98% of the time. However this can vary depending on if the song is **very** popular or **very** niche.

Measures to increase chances of getting the correct audio:

v2.0:
Currently, every search has the word "provided to youtube" appended to the request. The reason for this is due to the way artist's distribute music on platforms.
If a YouTube channel looks something like "Artist Name - Topic" then it means it came from the distributing platform that also sent the audio to platforms such as Spotify and Itunes.
Music from these channels are the exact same audio file as the ones released on Spotify, so prioritizing these in the search is a good way of getting the exact audio at a high quality. 

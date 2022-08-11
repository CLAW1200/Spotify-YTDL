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

The program will get the correct file ~90% of the time. However this can vary depending on if the song is **very** popular or **very** niche.

Popular Music:

Popular songs often have music videos which contain diegetic audio (E.g. Sound effects, background noise, long intros before the music starts, etc...)
These music videos are often the top search result with popular songs and may be downloaded instead of the original audio.
There is also the smaller chance of getting a low quality reupload, not from the original artist's channel. However this is quite unlikely as these are almost never the top search result


Niche Music:

This normally applies to songs with <10,000 plays, however can happen to songs with more if YouTube feels like throwing something else into the search results.
If another video's title contains some of the key words in the search request and is vastly more popular, chances are it will be downloaded instead.

Measures to increase chances of getting the correct audio:

v1.0:
Currently, every search has the word "topic" appended to the request. The reason for this is due to the way artist's distribute music on platforms.
If a YouTube channel looks something like "Artist Name - Topic" then it means it came from the distributing platform that also sent the audio to platforms such as Spotify and Itunes.
Music from these channels are the exact same audio file as the ones released on Spotify, so prioritizing these in the search is a good way of getting the exact audio. 


Future versions:

I will look at improving the accuracy in future releases, but you are welcome to edit the code and change the search requests to better fit the genre of music you are downloading.

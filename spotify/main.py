import os
import download as dh
import playlist as pl

if __name__ == "__main__":

    def extractSpotifyLink(link):
        if "playlist" not in link:
            print ("Not a spotify playlist link")
            exit()
        link = link.split("/")[-1]
        link = link.split("?")[0]
        return link


    link = extractSpotifyLink(str(input("Enter the link of the playlist: ")))
    username = str(input("Enter the username of the playlist creator: "))

    data = pl.call_playlist(username, link)
    print (data)
    for i in range(len(data)):
        row = data.iloc[i].tolist()
        print (row)
        
        request = str(f"{row[2]} {row[0]} {row[1]} topic")
        #track, artist, album

        print (request)
        dh.download_video(request, row[2], row[0], row[1], {row[13]}, {row[6]}, {row[5]}, os.getcwd())






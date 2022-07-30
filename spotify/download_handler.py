
def download_video(request):
    import yt_dlp as ydl
    print ("requestTitle " + request)

    def my_hook(d):
        status = (d['status'])
        print (status)

    ydl_opts = {
    'format':'bestaudio/best',
    'extractaudio':True,
    'match-title':f"{request}",
    'audioformat':'mp3',
    'default_search': 'ytsearch',
    'outtmpl':'%(title)s.%(ext)s',
    'noplaylist':True,
    'nocheckcertificate':True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }]
}
    with ydl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([request])
    


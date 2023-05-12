
def download_video(request, title, artist, album, bpm, key, energy, path):
    import yt_dlp as ydl
    import data as data
    print ("requestTitle " + request)

    def my_hook(d):
        status = (d['status'])
        print ("status ", status)
        if status == 'finished':
            filename = (d['filename'])
            print ("filename ", filename)
            filename = str(data.convertType(filename, path, artist))
            data.metadata(filename, title, artist, album, bpm, key, energy)


    ydl_opts = {
    'progress_hooks': [my_hook],
    'quiet': True,
    'format':'bestaudio/best',
    'match-title':f"{request}",
    'default_search': 'ytsearch',
    'extract-audio': True,
    'audio-format': 'flac',
    'outtmpl':'%(title)s.%(ext)s',
    'noplaylist':True,
    'nocheckcertificate':True,
    }
    with ydl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([request])

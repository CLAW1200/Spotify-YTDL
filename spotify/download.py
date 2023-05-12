def download_video(self, request, title, artist, album, bpm, key, energy, path, audio_format):
    import yt_dlp as ydl
    import data as data
    import re
    print ("requestTitle " + request)

    def progress_hook(d):
        status = d['status']
        if status == 'downloading':
            # Extract download percentage from the colored string
            progress_str = d['_percent_str']
            progress_str = re.sub(r'\x1b\[[0-9;]*m', '', progress_str)
            progress_str = progress_str.strip()

            # Parse the percentage as a float
            try:
                progress = float(progress_str[:-1])
            except ValueError:
                progress = 0.0

            # emit the progress bar value
            self.songProgress_updated.emit(progress)
            
        if status == 'finished':
            filename = (d['filename'])
            print ("filename ", filename)
            overwrite = self.get_overwriteCheckBox()
            filename = str(data.convertType(filename, path, artist, audio_format, overwrite))
            data.metadata(filename, title, artist, album, bpm, key, energy)


    ydl_opts = {
    'progress_hooks': [progress_hook],
    'quiet': True,
    'format':'bestaudio/best',
    'match-title':f"{request}",
    'default_search': 'ytsearch',
    'extract-audio': True,
    'audio-format': '%(audio_format)s',
    'outtmpl':'%(title)s.%(ext)s',
    'noplaylist':True,
    'nocheckcertificate':True,
    }
    with ydl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([request])

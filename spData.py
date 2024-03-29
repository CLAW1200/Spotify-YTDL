def metadata(inputFile, title, artist, album, bpm, key, energy, comment):


    def proper_round(num, dec=0):
        num = str(num)[:str(num).index('.')+dec+2]
        if num[-1]>='5':
            return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
        return float(num[:-1])
    
    comment = str(comment)
    comment = comment[2:-2]
    
    if inputFile.endswith(".flac"):
        from mutagen.flac import FLAC
        audio = FLAC(inputFile)
        audio["TITLE"] = title
        audio["ALBUM"] = album
        audio["ARTIST"] = artist
        audio["COMMENT"] = comment
        audio["GENRE"] = str(list(energy)[0])
        audio["BPM"] = str(round(proper_round(list(bpm)[0])))
        audio.save()

    elif inputFile.endswith(".mp3"):
        from mutagen.id3 import ID3NoHeaderError
        from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, TRCK
        audio = ID3(inputFile)
        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio["TALB"] = TALB(encoding=3, text=album)
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        audio["COMM"] = COMM(encoding=3, text=comment)
        audio["TCON"] = TCON(encoding=3, text=str(list(energy)[0]))
        audio.save()


def convertType(inputFile, path, artist, fileFormat, overwrite, fileQuality, fileFlacCompressionLevel):
    import os
    import subprocess
    name = os.path.splitext(inputFile)[0]
    
    outputFile = str(f"{name}.{fileFormat}",)

    cmd = [
        "ffmpeg", "-i", f"{inputFile}",
        "-c:a", f"{fileFormat}", 
        "-compression_level", f"{fileFlacCompressionLevel}",
        
    ]
    if overwrite == True:
        cmd.append("-y")
    if overwrite == False:
        cmd.append("-n")

    if fileQuality != 0:
        cmd.append("-b:a")
        cmd.append(f"{fileQuality}k")
    
    cmd.append(f"{artist} - {outputFile}")
    print (path)
    try:
        subprocess.run(cmd, cwd=path)
    except:
        print("Error converting file")
        print("MAKE SURE FFMPEG IS INSTALLED AND IN PATH")
        raise SystemExit
    os.remove(inputFile)
    return f"{artist} - {outputFile}"

    #ffmpeg -i memento.webm -c:a flac audio.flac 
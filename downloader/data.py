def metadata(inputFile, title, artist, album, bpm, key, energy):

    def proper_round(num, dec=0):
        num = str(num)[:str(num).index('.')+dec+2]
        if num[-1]>='5':
            return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
        return float(num[:-1])

    from mutagen.flac import FLAC
    audio = FLAC(inputFile)
    audio["TITLE"] = title
    audio["ALBUM"] = album
    audio["ARTIST"] = artist
    audio["COMMENT"] = "github.com/CLAW1200"
    audio["GENRE"] = str(list(energy)[0])
    audio["BPM"] = str(round(proper_round(list(bpm)[0])))
    print(audio.pprint())
    audio.save()


def convertType(inputFile, path, artist, fileFormat, overwrite, fileQuality, fileFlacCompressionLevel):
    import os
    import subprocess
    name = os.path.splitext(inputFile)[0]
    
    outputFile = str(f"{name}.{fileFormat}",)

    cmd = [
        "ffmpeg", "-i", f"{inputFile}",
        "-c:a", "flac", 
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

    print ("cmd: " + str(cmd))
    subprocess.run(cmd, cwd=path)
    os.remove(inputFile)
    return f"{artist} - {outputFile}"

    #ffmpeg -i memento.webm -c:a flac audio.flac 
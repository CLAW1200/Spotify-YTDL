def metadata(inputFile, title, artist, album, bpm, path):
    import subprocess
    import os
    name = inputFile.split(".")[0]

    outputFile = str(f"{name}_metadata_.flac",)


    cmd = [
        "ffmpeg", "-y", "-i", f"{inputFile}",
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        "-metadata", f"album={album}",
        "-metadata", f"beats-per-minute={bpm}",
        "-codec", "copy", f"{outputFile}",
    ]
    print ("cmd: " + str(cmd))
    subprocess.run(cmd, cwd=path)
    
    newfilename = outputFile.replace("_metadata_", "")
    print ("newfilename: " + str(newfilename))
    os.replace(outputFile, newfilename)



def convertType(inputFile, path):
    import os
    import subprocess
    name = inputFile.split(".")[0]
    
    outputFile = str(f"{name}.flac",)
    

    cmd = [
        "ffmpeg", "-i", f"{inputFile}",
        "-c:a", "flac",
        f"{outputFile}",
    ]
    print ("cmd: " + str(cmd))
    subprocess.run(cmd, cwd=path)
    os.remove(inputFile)
    return outputFile

    #ffmpeg -i memento.webm -c:a flac audio.flac
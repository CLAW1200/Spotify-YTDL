import os
import re
from mutagen.flac import FLAC
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2

def compareStrings(fileNameShort, artistFromMetadata, titleFromMetadata):
    # Function to compare two strings word by word, ignoring symbols and making everything lowercase
    # True if strings match

    fileNameHold = fileNameShort

    # Filename (no extension) is fileNameShort
    fileNameShort = re.sub(r'[^\w\s]', '', fileNameShort.lower())
    fileNameShort = re.sub(r'\s+', ' ', fileNameShort)  # Replace double spaces with single spaces
    # Artist is artistFromMetadata
    artistFromMetadata = re.sub(r'[^\w\s]', '', artistFromMetadata.lower())
    artistFromMetadata = re.sub(r'\s+', ' ', artistFromMetadata)  # Replace double spaces with single spaces
    # Title is titleFromMetadata
    titleFromMetadata = re.sub(r'[^\w\s]', '', titleFromMetadata.lower())
    titleFromMetadata = re.sub(r'\s+', ' ', titleFromMetadata)  # Replace double spaces with single spaces

    # Check if artistFromMetadata is a substring of fileNameShort, or vice versa
    # if any word in artistFromMetadata is in fileNameShort and any word in titleFromMetadata is in fileNameShort, or if fileNameShort is a substring of artistFromMetadata + titleFromMetadata

    artistCondition = any(word in fileNameShort for word in artistFromMetadata.split()) # any word in artistFromMetadata is in fileNameShort

    fileNameHoldFormat = fileNameHold.rsplit(' - ', 1)[-1]
    fileNameHoldFormat = fileNameHoldFormat.strip().lower() #filename Title
    fileNameHoldFormat = re.sub(r'[^\w\s]', '', fileNameHoldFormat.lower())
    fileNameHoldFormat = re.sub(r'\s+', ' ', fileNameHoldFormat)
    titleCondition = fileNameHoldFormat in titleFromMetadata


    if artistCondition and titleCondition or (fileNameShort in artistFromMetadata + titleFromMetadata):
        return True
    #print(f"{fileNameShort} |-| {artistFromMetadata} | {titleFromMetadata}")
    #print (f"{fileNameHoldFormat} | {titleFromMetadata}")
    return False

def getMetadata(file):
    #returns metadataArtist and metadataTitle
    if not file.endswith((".flac", ".mp3")):  # Check for both FLAC, MP3
        metadataArtist = ""
        metadataTitle = ""
        filenameWithoutExtension = ""
        pass
    
    if file.endswith(".flac"):
        # Read FLAC metadata
        audio = FLAC(file)
        metadataArtist = audio.get("artist", [""])[0]
        metadataTitle = audio.get("title", [""])[0]

    elif file.endswith(".mp3"):
        # Read MP3 metadata
        audio = ID3(file)
        metadataArtist = audio.getall("TPE1")[0].text[0] if len(audio.getall("TPE1")) > 0 else ""
        metadataTitle = audio.getall("TIT2")[0].text[0] if len(audio.getall("TIT2")) > 0 else ""

    return metadataArtist, metadataTitle

def checkMetadata(filePath):
    # Function to check if the metadata is correct for artist and title
    # Returns a list of tuples with the filename, artist, and title if there is a mismatch
    os.chdir(filePath)
    mismatchedFiles = []  # Create a list to store mismatched filenames
    for file in os.listdir():
        # Loop through all files in the directory
        # Check if the metadata is correct for artist and title
        metadataArtist, metadataTitle = getMetadata(file)
        # Remove the file extension and compare to the original file name
        filenameWithoutExtension, _ = os.path.splitext(file)
        if not (compareStrings(filenameWithoutExtension, metadataArtist, metadataTitle)) and (file.endswith(".mp3") or file.endswith(".flac")):
            mismatchedFiles.append((file, metadataArtist, metadataTitle))
    return mismatchedFiles

def copyFilenameToMetadata(fileName, filePath):
    # Function to copy the filename to the metadata
    # Returns True if successful, False if unsuccessful
    if not fileName.endswith((".flac", ".mp3")):  # Check for both FLAC and MP3 files
        return False
    fileNameShort = _ = os.path.splitext(fileName)[0]
    #split filename after last -
    try:
        fileNameArtist, fileNameTitle = fileNameShort.rsplit(' - ', 1)
        fileNameArtist = fileNameArtist.strip()
        fileNameTitle = fileNameTitle.strip()
    except ValueError:
        print ("Error: Filename does not contain '-' to split artist and title")
        pass
    
    #Use FileName to update metadata
    try:
        if fileName.endswith(".flac"):
            # Read FLAC metadata
            audio = FLAC(filePath + fileName)
            audio["artist"] = fileNameArtist
            audio["title"] = fileNameTitle
            audio.save()

        elif fileName.endswith(".mp3"):
            # Read MP3 metadata
            audio = ID3(filePath + fileName)
            audio.setall("TPE1", [TPE2(fileNameArtist)]) if fileNameArtist != "" else audio.setall("TPE1", [TPE2("")])
            audio.setall("TIT2", [TALB(fileNameTitle)]) if fileNameTitle != "" else audio.setall("TIT2", [TALB("")])
            audio.save()

    except Exception as e:
        print(f"Error processing {fileName}: {e}")
        return False
    return True

def copyMetadataToFileName(fileName, filePath):
    #Use Metadata to update filename
    metadataArtist, metadataTitle = getMetadata(filePath + fileName)  
    if metadataArtist == "" and metadataTitle == "":
        print ("Error: Metadata is empty. File not renamed.\n")
        return False
    fileNameExtension = _ = os.path.splitext(fileName)[1]
    newFileName = metadataArtist + " - " + metadataTitle + fileNameExtension
    os.rename(filePath + fileName, filePath + newFileName)
    print (f"Renamed {fileName} to {newFileName}\n")

def copyAllFileNameToMetadata(fileNameList, filePath):
    for fileName in fileNameList:
        copyFilenameToMetadata(fileName[0], filePath)

def copyAllMetadataToFileName(fileNameList, filePath):
    for fileName in fileNameList:
        copyMetadataToFileName(fileName[0], filePath)

def decideForEachFile(fileName, filePath):
    for fileName in mismatchedFiles:
            print (f"Filename: {fileName[0]}")
            print (f"Artist: {fileName[1]}")
            print (f"Title: {fileName[2]}")
            print ("1. Use filenames")
            print ("2. Use metadata")
            print ("3. Delete file")
            print ("4. Skip")
            print ("5. Exit\n")
            choice = input("Enter your choice: ")
            if choice == "1":
                copyFilenameToMetadata(fileName[0], filePath)
            elif choice == "2":
                copyMetadataToFileName(fileName[0], filePath)
            elif choice == "3":
                if userConfirm():
                    deleteFile(fileName[0], filePath)
            elif choice == "4":
                continue
            elif choice == "5":
                break
            else:
                print ("Invalid choice\n")

def userConfirm():
    # Function to confirm that the user wants to make the changes
    # Returns True if the user confirms, False if the user does not confirm
    print ("Are you sure you want to make these changes? (Y/N)")
    choice = input("Enter your choice: ")
    if choice == "Y" or choice == "y":
        return True
    elif choice == "N" or choice == "n":
        return False
    else:
        print ("Invalid choice\n")
        return False

def deleteFile(fileName, filePath):
    os.remove(filePath + fileName)
    print (f"Deleted {fileName}")

def deleteFiles(fileNameList, filePath):
    for fileName in fileNameList:
        deleteFile(fileName[0], filePath)

def menu(mismatchedFiles, filePath):
    print(f"{len(mismatchedFiles)} mismatched files found.\n{mismatchedFiles}\n")

    if len(mismatchedFiles) < 1:
        print("No changes made.")
        exit()

    print ("1. Use filenames for all")
    print ("2. Use metadata for all")
    print ("3. Delete all files")
    print ("4. Let me decide for each file")
    print ("5. Exit\n")

    choice = input("Enter your choice: ")
    if choice == "1":
        if userConfirm():
            copyAllFileNameToMetadata(mismatchedFiles, filePath)
    elif choice == "2":
        if userConfirm():
            copyAllMetadataToFileName(mismatchedFiles, filePath)
    elif choice == "3":
        if userConfirm():
            deleteFiles(mismatchedFiles, filePath)
    elif choice == "4":
        decideForEachFile(mismatchedFiles, filePath)        
    elif choice == "5":
        print ("No changes made.\n")
        exit()
    else:
        print ("Invalid choice\n")

if __name__ == "__main__":
    """
    A command line interface to check and correct the metadata of all files in a directory
    """
    filePath = "C:\\Users\\User\\Music\\test\\"
    mismatchedFiles = checkMetadata(filePath)
    menu(mismatchedFiles, filePath)
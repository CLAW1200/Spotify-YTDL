from PyQt5.QtCore import QThread
import os
import download as dh
import playlist as pl
from PyQt5 import QtWidgets, uic
import sys

qtCreator_file  = "window.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreator_file)

class DownloadThread(QThread):
    def __init__(self, link, save_path):
        super().__init__()
        self.link = link
        self.save_path = save_path

    def run(self):
        username = ""
        try:
            os.chdir(self.save_path)
        except OSError:
            print ("Path not found")
            print ("Path set to current directory")
            os.chdir(os.getcwd())
        data = pl.call_playlist(username, self.link)
        print (data)
        for i in range(len(data)):
            row = data.iloc[i].tolist()
            print (row)
            request = str(f'{row[2]} {row[0]} {row[1]} "provided to youtube"')
            #track, artist, album
            print (request)
            dh.download_video(request, row[2], row[0], row[1], {row[13]}, {row[6]}, {row[5]}, os.getcwd())

        os.remove(".cache")

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
     
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #remove keys action 
        self.actionRemove_Keys.triggered.connect(self.removeKeys)
        #load keys action
        self.actionImport_Keys.triggered.connect(self.loadKeys)
        #save keys action
        self.actionSave_Keys.triggered.connect(self.saveKeys)
        #download playlist button
        self.downloadButton.clicked.connect(self.downloadPlaylist)

        self.download_thread = None


    def removeKeys(self):
        #edit the two line boxes to be empty
        self.spotifyID.setText("")
        self.spotifySecret.setText("")
        #empty the keys file
        open("secret.keys", "w").close()

    def saveKeys(self):
        #save the keys to the file
        f = open("secret.keys", "w")
        f.write(self.spotifyID.text() + "\n")
        f.write(self.spotifySecret.text())
        f.close()

    def loadKeys(self):
        #get first line of keys file
        f = open("secret.keys", "r")
        self.spotifyID.setText(f.readline().rstrip('\n'))
        #get second line of keys file
        self.spotifySecret.setText(f.readline().rstrip('\n'))
        f.close()


    def downloadPlaylist(self):
        if self.download_thread is not None and self.download_thread.isRunning():
            print("Download already in progress.")
            return

        link = self.playlistLinkBox.text()
        save_path = self.savePathBox.text()
        self.download_thread = DownloadThread(link, save_path)
        self.download_thread.finished.connect(self.downloadFinished)
        self.download_thread.start()

    def downloadFinished(self):
        print("Download completed.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    try:
        window.loadKeys()
    except FileNotFoundError:
        print ("No keys file found")
    sys.exit(app.exec_())


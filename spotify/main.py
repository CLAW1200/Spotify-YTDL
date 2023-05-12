from PyQt5.QtCore import QThread
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
import os
import download as dh
import playlist as pl
import sys
qtCreator_file  = "window.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreator_file)
keys = os.getcwd() + "\\secret.keys"
print (keys)


class DownloadThread(QThread):
    # Define a custom signal that emits the current progress percentage
    songProgress_updated = pyqtSignal(float)
    totalProgress_updated = pyqtSignal(float)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.link = None

    def set_link(self, link):
        self.link = link

    def set_save_path(self, save_path):
        self.save_path = save_path

    def set_fileFormat(self, fileFormat):
        self.fileFormat = fileFormat

    def get_overwriteCheckBox(self):
        return window.overwriteCheckBox.isChecked()

    def run(self):
        username = ""
        try:
            os.chdir(self.save_path)
        except OSError:
            print ("Path not found")
            print ("Path set to current directory")
            os.chdir(os.getcwd())
        data = pl.call_playlist(username, self.link, keys)
        #print (data)
        if data is not None:
            for i in range(len(data)):
                self.totalProgress_updated.emit((i+1)/len(data)*100)
                row = data.iloc[i].tolist()
                print (row)
                request = str(f'{row[2]} {row[0]} {row[1]} "provided to youtube"')
                #track, artist, album
                #print (request)
                dh.download_video(self, request, row[2], row[0], row[1], {row[13]}, {row[6]}, {row[5]}, os.getcwd(), self.fileFormat)

            if window.explorerCheckBox.isChecked():
                os.startfile(os.getcwd())

        try:
            os.remove(".cache")
        except FileNotFoundError:
            pass
        self.totalProgress_updated.emit(0)
        self.songProgress_updated.emit(0)


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.downloadThread = DownloadThread()

        #remove keys action 
        self.actionRemove_Keys.triggered.connect(self.removeKeys)
        #load keys action
        self.actionImport_Keys.triggered.connect(self.loadKeys)
        #save keys action
        self.actionSave_Keys.triggered.connect(self.saveKeys)
        #download playlist button
        self.downloadButton.clicked.connect(self.downloadPlaylist)
        #dark mode action
        self.darkModeCheckBox.stateChanged.connect(self.darkMode)
        # Connect the progress_updated signal to a slot that updates the progress bar
        self.downloadThread.songProgress_updated.connect(self.update_songProgress_bar)
        self.downloadThread.totalProgress_updated.connect(self.update_totalProgress_bar)

    
    def darkMode(self):
        if self.darkModeCheckBox.isChecked():
            self.setStyleSheet("background-color: rgb(54, 54, 54); color: rgb(255, 255, 255);")
        else:
            self.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")

    def removeKeys(self):
        #edit the two line boxes to be empty
        self.spotifyID.setText("")
        self.spotifySecret.setText("")
        #empty the keys file
        with open(keys, "w") as f:
            f.write("")
        f.close()


    def saveKeys(self):
        #save the keys to the file
        with open(keys, "w") as f:
            f.write(self.spotifyID.text() + "\n")
            f.write(self.spotifySecret.text())
        f.close()

    def loadKeys(self):
        #get first line of keys file
        f = open(keys, "r")
        self.spotifyID.setText(f.readline().rstrip('\n'))
        #get second line of keys file
        self.spotifySecret.setText(f.readline().rstrip('\n'))
        f.close()

    def fileFormat(self):
        #get the file format from the combo box
        format = self.formatComboBox.currentText()
        if format == "MP3":
            return "mp3"
        elif format == "FLAC":
            return "flac"

    def downloadPlaylist(self):
        # Get playlist link
        link = self.playlistLinkBox.text()

        # Set the link in the DownloadThread object
        self.downloadThread.set_link(link)
        self.downloadThread.set_save_path(self.savePathBox.text().replace("\\", "/"))
        self.downloadThread.set_fileFormat(self.fileFormat())

        # Start the DownloadThread
        self.downloadThread.start()

    def update_songProgress_bar(self, progress):
        # Update the progress bar with the received progress percentage
        self.songProgressBar.setValue(int(progress))
    
    def update_totalProgress_bar(self, progress):
        # Update the progress bar with the received progress percentage
        self.totalProgressBar.setValue(int(progress))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    try:
        window.loadKeys()
    except FileNotFoundError:
        print ("No keys file found")
    sys.exit(app.exec_())


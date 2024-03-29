import os
from PyQt5.QtCore import QThread
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
import spDownload as dh
import spPlaylist as pl
import sys
import subprocess

#check for ffmpeg in path
try:
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except FileNotFoundError:
    print("ffmpeg not found in path")
    sys.exit(1)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
qtCreator_file  = "window.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreator_file)
keys = os.path.join(os.getcwd() , "secret.keys")

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

    def set_fileQuality(self, fileQuality):
        self.fileQuality = fileQuality

    def set_fileFormat(self, fileFormat):
        self.fileFormat = fileFormat

    def set_fileFlacCompressionLevel(self, fileFlacCompressionLevel):
        self.fileFlacCompressionLevel = fileFlacCompressionLevel

    def get_explorerCheckBox(self):
        return window.explorerCheckBox.isChecked()
    
    def get_overwriteCheckBox(self):
        return window.overwriteCheckBox.isChecked()
    
    def run(self):      
        window.setObjectStates(False)
        window.saveKeys()
        username = ""
        try:
            os.chdir(self.save_path)
        except OSError:
            print("Path not found")
        data = pl.call_playlist(username, self.link, keys)
        print(data)
        if data is not None:
            for i in range(len(data)):
                self.totalProgress_updated.emit((i+1)/len(data)*100)
                row = data.iloc[i].tolist()
                print(row)
                request = str(f'{row[2]} {row[0]} "provided to youtube"')
                #track, artist, album
                print(request)
                dh.download_video(self, request, row[2], row[0], row[1], {row[13]}, {row[6]}, {row[5]}, os.getcwd(), self.fileFormat, self.fileQuality, self.fileFlacCompressionLevel, ({row[16]}))

        if window.explorerCheckBox.isChecked():
            if sys.platform == "win32":
                os.startfile(os.getcwd())
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, os.getcwd()])
            
        try:
            os.remove(".cache")
        except FileNotFoundError:
            pass
        self.totalProgress_updated.emit(0)
        self.songProgress_updated.emit(0)
        
        window.setObjectStates(True)
        if window.formatComboBox.currentIndex() == 0:
            window.compressionLevelSpinBox.setEnabled(True)
            window.qualityComboBox.setEnabled(False)
        elif window.formatComboBox.currentIndex() == 1:
            window.compressionLevelSpinBox.setEnabled(False)
            window.qualityComboBox.setEnabled(True)

    def write(self, text):
        #insert text at top of textbox
        self.text_edit.insertPlainText(text)
        #scroll to bottom
        self.text_edit.moveCursor(QtGui.QTextCursor.End)

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.downloadThread = DownloadThread()

        #get windows explorer user
        self.username = os.getlogin()
        #set the save path to the user's music folder
        self.savePathBox.setText(os.path.expanduser(os.path.join('~', "Music")))    
        #disable qualityComboBox
        self.qualityComboBox.setEnabled(False)
        #remove keys action 
        self.actionRemove_Keys.triggered.connect(self.removeKeys)
        #load keys action
        self.actionImport_Keys.triggered.connect(self.loadKeys)
        #save keys action
        self.actionSave_Keys.triggered.connect(self.saveKeys)
        #download playlist button
        self.downloadButton.clicked.connect(self.downloadPlaylist)
        # Connect the progress_updated signal to a slot that updates the progress bar
        self.downloadThread.songProgress_updated.connect(self.update_songProgress_bar)
        self.downloadThread.totalProgress_updated.connect(self.update_totalProgress_bar)
        #format state changed
        self.formatComboBox.currentIndexChanged.connect(self.formatComboBoxStateChange)
        #overwrite checkbox
        self.overwriteCheckBox.setChecked(False)

    def setObjectStates(self, state):
        self.downloadButton.setEnabled(state)
        self.playlistLinkBox.setEnabled(state)
        self.savePathBox.setEnabled(state)
        self.formatComboBox.setEnabled(state)
        self.compressionLevelSpinBox.setEnabled(state)
        self.qualityComboBox.setEnabled(state)
        #self.overwriteCheckBox.setEnabled(state)
        self.spotifyID.setEnabled(state)
        self.spotifySecret.setEnabled(state)

    def expandWindow(self):
        if self.expandWindowButton.isChecked():
            self.setFixedSize(800, 400)
        else:
            self.setFixedSize(500, 400)

    def removeKeys(self):
        try:
            if sys.platform == "win32":
                subprocess.run(["attrib", "-H", keys])
            with open(keys, "w") as f:
                f.write("")
            self.spotifyID.setText("")
            self.spotifySecret.setText("")
            print ("Keys Deleted")
            if sys.platform == "win32":
                subprocess.run(["attrib", "+H", keys])
        except FileNotFoundError as e:
            print(e)
        except PermissionError as e:
            print(e)

    def saveKeys(self):
        try:
            if sys.platform == "win32":
                subprocess.run(["attrib", "-H", keys])
            #save the keys to the file
            with open(keys, "w") as f:
                f.write(self.spotifyID.text() + "\n")
                f.write(self.spotifySecret.text())
            print("Keys Saved")
            if sys.platform == "win32":
                subprocess.run(["attrib", "+H", keys])
        except FileNotFoundError as e:
            print(e)
        except PermissionError as e:
            print(e)

    def loadKeys(self):
        try:
            if sys.platform == "win32":
                subprocess.run(["attrib", "-H", keys])
            #get first line of keys file
            f = open(keys, "r")
            self.spotifyID.setText(f.readline().rstrip('\n'))
            #get second line of keys file
            self.spotifySecret.setText(f.readline().rstrip('\n'))
            print("Keys Loaded")
            if sys.platform == "win32":
                subprocess.run(["attrib", "+H", keys])
        except FileNotFoundError as e:
            print(e)
        except PermissionError as e:
            print(e)

    def fileQuality(self):
        #get the file format from the combo box
        quality = self.qualityComboBox.currentIndex()
        if quality == 0:
            return "320"
        elif quality == 1:
            return "256"
        elif quality == 2:
            return "192"
        elif quality == 3:
            return "128"
        elif quality == 4:
            return "96"
        elif quality == 5:
            return "64"
        elif quality == 6:
            return "32"
        elif quality == 7:
            return "16"
        
    def fileFlacCompressionLevel(self):
        #get the file format from the combo box
        quality = self.compressionLevelSpinBox.value()
        return quality
        
    def fileFormat(self):
        #get the file format from the combo box
        format = self.formatComboBox.currentIndex()
        if format == 0:
            return "flac"
        elif format == 1:
            return "mp3"

    def downloadPlaylist(self):
        # Get playlist link
        link = self.playlistLinkBox.text()

        # Set the link in the DownloadThread object
        self.downloadThread.set_link(link)
        self.downloadThread.set_save_path(self.savePathBox.text().replace("\\", "/"))
        self.downloadThread.set_fileQuality(self.fileQuality())
        self.downloadThread.set_fileFormat(self.fileFormat())
        self.downloadThread.set_fileFlacCompressionLevel(self.fileFlacCompressionLevel())

        # Start the DownloadThread
        self.downloadThread.start()

    def update_songProgress_bar(self, progress):
        # Update the progress bar with the received progress percentage
        self.songProgressBar.setValue(int(progress))
    
    def update_totalProgress_bar(self, progress):
        # Update the progress bar with the received progress percentage
        self.totalProgressBar.setValue(int(progress))

    def formatComboBoxStateChange(self):
        if self.formatComboBox.currentIndex() == 0:
            self.compressionLevelSpinBox.setEnabled(True)
            self.qualityComboBox.setEnabled(False)
        elif self.formatComboBox.currentIndex() == 1:
            self.compressionLevelSpinBox.setEnabled(False)
            self.qualityComboBox.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.setWindowTitle("Spotify Playlist Downloader")
    window.show()
    try:
        window.loadKeys()
    except FileNotFoundError:
        print("No keys file found")
    sys.exit(app.exec_())

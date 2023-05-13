import os
from PyQt5.QtCore import QThread
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
import download as dh
import playlist as pl
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
qtCreator_file  = "window.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreator_file)
keys = os.getcwd() + "\\secret.keys"

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

    def get_overwriteCheckBox(self):
        return window.overwriteCheckBox.isChecked()
    
    

    def run(self):      
        window.setObjectStates(False)
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
                dh.download_video(self, request, row[2], row[0], row[1], {row[13]}, {row[6]}, {row[5]}, os.getcwd(), self.fileFormat, self.fileQuality, self.fileFlacCompressionLevel)

        if window.explorerCheckBox.isChecked():
            os.startfile(os.getcwd())

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

class ConsoleWidget:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        self.text_edit.insertPlainText(text)


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.downloadThread = DownloadThread()

        # Create a console widget
        console_widget = ConsoleWidget(self.consoleTextBox)

        # Redirect stdout and stderr to the console widget
        sys.stdout = console_widget
        sys.stderr = console_widget

        #get windows explorer user
        self.username = os.getlogin()
        #set the save path to the user's music folder
        self.savePathBox.setText("C:\\Users\\" + self.username + "\\Music")
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
        #expandWindow radio button
        self.expandWindowButton.clicked.connect(self.expandWindow)

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
            os.remove("secret.keys")
            self.spotifyID.setText("")
            self.spotifySecret.setText("")
            print ("Keys Deleted")
        except FileNotFoundError as e:
            print(e)
        except PermissionError as e:
            print(e)

    def saveKeys(self):
        try:
            #save the keys to the file
            with open(keys, "w") as f:
                f.write(self.spotifyID.text() + "\n")
                f.write(self.spotifySecret.text())
            f.close()
            print("Keys Saved")
        except FileNotFoundError as e:
            print(e)
        except PermissionError as e:
            print(e)

    def loadKeys(self):
        try:
            #get first line of keys file
            f = open(keys, "r")
            self.spotifyID.setText(f.readline().rstrip('\n'))
            #get second line of keys file
            self.spotifySecret.setText(f.readline().rstrip('\n'))
            f.close()
            print("Keys Loaded")
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


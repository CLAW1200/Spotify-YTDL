import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QVBoxLayout

class ConsoleWidget(QPlainTextEdit):
    def write(self, text):
        self.insertPlainText(text)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create a console widget
        console_widget = ConsoleWidget()

        # Redirect stdout to the console widget
        sys.stdout = console_widget

        # Create a layout for the window
        layout = QVBoxLayout()
        layout.addWidget(console_widget)

        # Set the layout for the window
        self.setLayout(layout)

        print ("Hello World!")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

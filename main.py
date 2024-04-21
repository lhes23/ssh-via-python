import sys
import config
from PyQt5.QtWidgets import *

# app = QApplication([])
# window = QWidget()
# layout = QVBoxLayout()
# button_send = QPushButton("Click Me!")
# layout.addWidget(QPushButton('Top'))
# layout.addWidget(QLabel("Hello World"))
# layout.addWidget(button_send)


# def on_button_clicked():
#     alert = QMessageBox()
#     alert.setText("You clicked")
#     alert.exec()

# button_send.clicked.connect(on_button_clicked)


# window.setLayout(layout)
# window.show()
# app.exec()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)

        self.labelImage = QLabel("Choose a File: ")
        self.button1 = QPushButton('Choose a File:')
        self.button1.clicked.connect(self.get_folder)
        self.button2 = QPushButton('Button2')

        cs1 = QRadioButton("Plugin",self)
        cs1.move(130, 20)

        cs2 = QRadioButton("Theme",self)
        cs2.move(130, 40)

        cs_group = QButtonGroup(self)
        cs_group.addButton(cs1)
        cs_group.addButton(cs2)

        formLayout = QFormLayout(self)
        formLayout.addRow(self.labelImage, self.button1)
        
        # self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle(config.app_name)
        self.show()

    def get_folder(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Project Data', r"", "")
        print(file_name)
        alert = QMessageBox()
        alert.setText(file_name)
        alert.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
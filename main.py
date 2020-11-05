from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
import sys
import pyperclip
from aes import AES
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AES')
        self.__output = QTextEdit()
        self.__output.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        keyLabel = QLabel("Key:")
        self.__keyEdit = QLineEdit()
        msgLabel = QLabel("Msg:")
        self.__msgEdit = QLineEdit()
        encryptButton = QPushButton("Encrypt")
        decryptButton = QPushButton("Decrypt")
        copyButton = QPushButton("Copy")

        vBoxLayout = QVBoxLayout()
        hBoxLayout = QHBoxLayout()

        formLayout = QFormLayout()
        formLayout.addRow(keyLabel,self.__keyEdit)
        formLayout.addRow(msgLabel,self.__msgEdit)

        hBoxLayout.addWidget(encryptButton)
        hBoxLayout.addWidget(decryptButton)

        vBoxLayout.addItem(formLayout)
        vBoxLayout.addItem(hBoxLayout)
        vBoxLayout.addWidget(self.__output)
        vBoxLayout.addWidget(copyButton)
        encryptButton.setObjectName('encryptBtn')
        decryptButton.setObjectName('decryptBtn')
        copyButton.setObjectName('copyBtn')
        encryptButton.clicked.connect(self.__handleEncryptClick)
        decryptButton.clicked.connect(self.__handleDecryptClick)
        copyButton.clicked.connect(self.__handleCopy) 
        self.setLayout(vBoxLayout)
        self.setStyleSheet(open('styles.css').read())
        self.setFixedSize(450,400)
        self.show()
    def __handleCopy(self):
        pyperclip.copy(self.__output.document().toPlainText())
        pyperclip.paste()
    def __handleDecryptClick(self):
        try:
            if(len(self.__output.toPlainText()) > 0):
                self.__output.document().clear()
            aes = AES(self.__msgEdit.text(),self.__keyEdit.text())
            aes.decrypt()
            self.__output.document().setPlainText(aes.getOutput())
        except:
            pass
        
    def __handleEncryptClick(self):
        try:
            if(len(self.__output.toPlainText()) > 0):
                self.__output.document().clear()
            aes = AES(self.__msgEdit.text(),self.__keyEdit.text())
            aes.encrypt()
            self.__output.document().setPlainText(aes.getOutput())
        except:
            pass
        

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyPDF2 import PdfFileMerger
from PyQt5 import QtCore, QtGui, QtWidgets
import os

fileslist = []

defaultStart = r"E:/Google Drive/Acads/"

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(652, 420)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.filesListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.filesListWidget.setGeometry(QtCore.QRect(20, 20, 371, 351))
        self.filesListWidget.setObjectName("filesListWidget")
        self.mergeFilesButton = QtWidgets.QPushButton(self.centralwidget)
        self.mergeFilesButton.setGeometry(QtCore.QRect(450, 290, 151, 81))
        self.mergeFilesButton.setObjectName("mergeFilesButton")
        self.moveUpButton = QtWidgets.QPushButton(self.centralwidget)
        self.moveUpButton.setGeometry(QtCore.QRect(410, 30, 41, 41))
        self.moveUpButton.setObjectName("moveUpButton")
        self.moveDownButton = QtWidgets.QPushButton(self.centralwidget)
        self.moveDownButton.setGeometry(QtCore.QRect(410, 70, 41, 41))
        self.moveDownButton.setObjectName("moveDownButton")
        self.addFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.addFileButton.setGeometry(QtCore.QRect(450, 190, 151, 81))
        self.addFileButton.setObjectName("addFileButton")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(520, 60, 71, 51))
        self.deleteButton.setObjectName("deleteButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 652, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.addFileButton.clicked.connect(self.openFileNamesDialog)
        self.deleteButton.clicked.connect(self.removeFile)
        self.moveUpButton.clicked.connect(self.moveUp)
        self.moveDownButton.clicked.connect(self.moveDown)
        self.mergeFilesButton.clicked.connect(self.mergeAll)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def moveUp(self):
        
        temp = self.filesListWidget.currentItem()
        index = self.filesListWidget.currentRow()
        if(index != 0 ):
            self.filesListWidget.takeItem(index)
            print(index, temp)

            self.filesListWidget.insertItem(index-1,temp)
            self.filesListWidget.setCurrentRow(index-1)
    def mergeAll(self):
        filesList = [raw(i.text()) for i in self.filesListWidget.findItems("", QtCore.Qt.MatchContains)]
        merger = PdfFileMerger()
        print(filesList)
        for pdf in filesList:
            merger.append(pdf)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()",defaultStart,"PDF Files (*.pdf)", options=options)
        if fileName: 
            print(fileName[::-1][0:3])           
            if(fileName[::-1][0:3] !="fdp"):
                fileName = fileName + ".pdf"
            merger.write(fileName)
            merger.close()
        buttonReply = QMessageBox.question(self, 'Saved', "Your PDF has been created! Do you want to open it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            path=os.path.realpath(fileName)
            os.startfile(fileName)
        else:
            print('No clicked.')

    def moveDown(self):
        temp = self.filesListWidget.currentItem()
        index = self.filesListWidget.currentRow()
        global filesList
        filesList = [i.text() for i in self.filesListWidget.findItems("", QtCore.Qt.MatchContains)]
        if(index != len(filesList) ):
            self.filesListWidget.takeItem(index)
            self.filesListWidget.insertItem(index+1,temp)
            self.filesListWidget.setCurrentRow(index+1)
    

    def removeFile(self):
        self.filesListWidget.takeItem(self.filesListWidget.currentRow())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.mergeFilesButton.setText(_translate("MainWindow", "Merge Files"))
        self.moveUpButton.setText(_translate("MainWindow", "Up"))
        self.moveDownButton.setText(_translate("MainWindow", "Down"))
        self.addFileButton.setText(_translate("MainWindow", "Add Files"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", r"E:/Google Drive/Acads/","PDF Files (*.pdf)", options=options)
        global filesList
        if files:
            filesList = files
            print(filesList)
        for item in filesList:
            self.filesListWidget.addItem(item)
        

def raw(text):
    """Returns a raw string representation of text"""
    escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())
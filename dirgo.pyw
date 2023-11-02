# Directory GO - Dir Go
import os, sys
try:
    from PyQt6 import QtCore, QtGui, QtWidgets, uic
    from PyQt6.QtCore import Qt
except ImportError:
    os.system("pip -v install --config-settings --confirm-license= --config-settings --qmake=/path/to/qmake PyQt6 && python .\\dirgo.py")

defpath = "C:/Users/"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Init window
        self.setWindowTitle("Dir Go")
        self.setFixedSize(800, 400)

        layout = QtWidgets.QVBoxLayout()
        inputL = QtWidgets.QHBoxLayout()
        inputLabel = QtWidgets.QLabel("Directory: ")
        inputL.addWidget(inputLabel)
        self.input = QtWidgets.QLineEdit(defpath)
        self.input.textChanged.connect(self.updateList)
        self.setToolTip("The Path to Navigate To")
        inputL.addWidget(self.input)
        layout.addLayout(inputL)

        self.cwdList = []
        self.list = QtWidgets.QListWidget()
        self.list.addItem(QtWidgets.QListWidgetItem("Start Typing ..."))
        # self.list.itemSelectionChanged.connect(self.listSelection)
        self.list.setToolTip("Path Suggestions")
        layout.addWidget(self.list)


        lowerLine = QtWidgets.QHBoxLayout()
        self.navingTo = QtWidgets.QLabel("Naviagating To: "+defpath)
        lowerLine.addWidget(self.navingTo, 1000)
        self.go = QtWidgets.QPushButton("Go>")
        self.go.clicked.connect(self.goto)
        self.go.pressed.connect(self.goto)
        lowerLine.addWidget(self.go)
        layout.addLayout(lowerLine)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def goto(self):
        print("Going to: "+self.input.text())
        path = os.path.realpath(self.input.text())
        os.startfile(path)
        self.close()

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        if e.key() == Qt.Key.Key_Up:
            if self.list.currentRow() <= 0:
                self.list.setCurrentRow(len(list(self.cwdList)) - 1)
            else:
                self.list.setCurrentRow(self.list.currentRow() - 1)
        if e.key() == Qt.Key.Key_Down:
            if self.list.currentRow() >= len(list(self.cwdList)) - 1:
                self.list.setCurrentRow(0)
            else:
                self.list.setCurrentRow(self.list.currentRow() + 1)
        if e.key() == Qt.Key.Key_Enter or e.key() == Qt.Key.Key_Return:
            if not self.go.hasFocus():
                self.listSelection()
            else:
                self.goto()
        
    def filterList(self, li):
        boo = self.input.text().split('/')[-1].lower() in li.lower()
        return boo
    def updateList(self):
        print("Update Needed")
        if self.input.text() != '':
            self.cwdList = []
            try:
                self.cwdList = os.listdir(self.input.text())
            except:
                print("Error")
                try:
                    finL = self.input.text().split('/')
                    finL.pop()
                    self.cwdList = os.listdir('/'.join(finL))
                    self.cwdList = filter(self.filterList, self.cwdList)
                except:
                    print("Couldn't do it!")
                    return
            self.cwdList = list(self.cwdList)
            self.list.clear()
            self.list.addItems(self.cwdList)
    def listSelection(self):
        listSelctions = self.list.currentRow()
        print(listSelctions)
        if listSelctions != -1:
            if self.cwdList[listSelctions] != "Start Typing ...":
                print("Selction: "+self.cwdList[listSelctions])
                finL = self.input.text().split('/')
                finL.pop()
                finL.append(self.cwdList[listSelctions]+'/')
                self.navingTo.setText("Naviagating To: "+'/'.join(finL))
                self.input.setText('/'.join(finL))
                self.input.setFocus()
                try: 
                    if os.path.isfile(os.path.realpath('/'.join(finL))):
                        self.goto()
                except:
                    print("Error :(")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit(app.exec())
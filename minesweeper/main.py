from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import mine
import sys
from functools import partial



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minesweeper")
        self.setFixedSize(930,520)
        self.central=QWidget(self)
        self.setCentralWidget(self.central)
        self.Mine=mine.Minesweeper()
        self.ctr=0
        self.layout()
        self.signal()
    def layout(self):
        self.vlayout=QVBoxLayout()
        self.grid=QGridLayout()
        self.buttons=[]
        for i in range(16):
            self.buttons.append([])
            for j in range(30):
                self.buttons[i].append(QPushButton())
                self.grid.addWidget(self.buttons[i][j],i,j)
                self.buttons[i][j].setFixedSize(30,30)
                self.buttons[i][j].setStyleSheet("border : solid black;""border-width : 1px 1px 1px 1px;")
                self.buttons[i][j].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.grid.setSpacing(0)
        self.vlayout.addLayout(self.grid)
        self.reset=QPushButton('Reset')
        self.vlayout.addWidget(self.reset)
        self.central.setLayout(self.vlayout)
    def signal(self):
        for i in range(16):
            for j in range(30):
                self.buttons[i][j].clicked.connect(partial(self.buttonclicked,i,j))
                self.buttons[i][j].customContextMenuRequested.connect(partial(self.rightclick,i,j))
        self.reset.clicked.connect(self.resetbutton)
    def buttonclicked(self,i,j):
        a=str(i)+','+str(j)
        number=self.Mine.clicked(a)
        if number!='M':
            self.buttons[i][j].setText(str(number))
            self.ctr+=1
            if self.ctr==381:
                self.wingame()
        else:
            self.buttons[i][j].setText('\U0001f4a5')
            for k in range(16):
                for m in range(30):
                    self.buttons[k][m].setEnabled(False)
            for k in self.Mine.mine:
                if k!=(i,j):
                    self.buttons[k[0]][k[1]].setText('\U0001f4a3')
        if number == 0:
            self.zeroclicked(i,j)
    def rightclick(self,i,j):
        if self.buttons[i][j].text()=='':
            self.buttons[i][j].setText('\U0001f6a9')
        elif self.buttons[i][j].text()=='\U0001f6a9':
            self.buttons[i][j].setText('')
    def wingame(self):
        for k in self.Mine.mine:
            self.buttons[k[0]][k[1]].setText('\U0001f4a3')
        for k in range(16):
            for m in range(30):
                self.buttons[k][m].setEnabled(False)
        win=QMessageBox(self)
        win.setWindowTitle('You Win')
        win.setText('Congratulations')
        win.setInformativeText('You won the game')
        win.setStandardButtons(QMessageBox.Ok)
        win.setDefaultButton(QMessageBox.Ok)
        win.show()
    def zeroclicked(self,i,j):
        search=set([(i,j-1),(i,j+1),(i+1,j),(i+1,j+1),(i+1,j-1),(i-1,j-1),(i-1,j),(i-1,j+1)])
        if i==0:
            search=search.difference(set([(i-1,j),(i-1,j-1),(i-1,j+1)]))
        if j==0:
            search=search.difference(set([(i,j-1),(i-1,j-1),(i+1,j-1)]))
        if i==15:
            search=search.difference(set([(i+1,j),(i+1,j-1),(i+1,j+1)]))
        if j==29:
            search=search.difference(set([(i,j+1),(i-1,j+1),(i+1,j+1)]))
        for k in search:
            if self.buttons[k[0]][k[1]].text()=='':
                value=self.Mine.m[k[0]][k[1]]
                self.buttons[k[0]][k[1]].setText(str(value))
                self.ctr+=1
                if self.ctr==381:
                    self.wingame()
                if value==0:
                    self.zeroclicked(k[0],k[1])
    def resetbutton(self):
        self.Mine.__init__()
        self.ctr=0
        for i in range(16):
            for j in range(30):
                self.buttons[i][j].setText('')
                self.buttons[i][j].setEnabled(True)
def main():
    app=QApplication(sys.argv)
    win=Window()
    win.show()
    sys.exit(app.exec_())
if __name__=='__main__':
    main()
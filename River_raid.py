#!python
# -*- coding: utf-8 -*-

"""
River Raid game
Mikołaj Waśniewski
"""

import sys, random
import numpy as np
from PyQt4 import QtCore, QtGui

class River_raid(QtGui.QMainWindow):
    
    def __init__(self):
        super(River_raid, self).__init__()

        self.initUI()
        
        
    def initUI(self):    
        
        # exit
        exitAction = QtGui.QAction('&Exit', self)        
        exitAction.setShortcut('Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        # options 
        optionsAction = QtGui.QAction("&Options", self)
        optionsAction.setShortcut('O')
        optionsAction.setStatusTip('Options')
        optionsAction.triggered.connect(self.optionsEvent)
        
        # new game
        newGameAction = QtGui.QAction("&New game", self)
        newGameAction.setShortcut('N')
        newGameAction.setStatusTip('New game')
        newGameAction.triggered.connect(self.newGameEvent)
        
        # help
        helpAction = QtGui.QAction('&Help', self)
        helpAction.setStatusTip('Help')
        helpAction.triggered.connect(self.showHelp)
        
        menubar = self.menuBar()
        
        game = menubar.addMenu('&game')
        game.addAction(newGameAction)
        game.addAction(optionsAction)
        game.addAction(exitAction)
        
        self.dialogTextBrowser = Help(self)
        help = menubar.addMenu('&help')
        help.addAction(helpAction)

        
        
        
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)
        self.tboard.start()
        

        
        self.statusbar = self.statusBar()        
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)     
        self.tboard.setFixedSize(300, 400)
        
        self.resize(300, 400)
        self.center()
        self.setWindowTitle('River raid')        
        self.show()
        

    def center(self):
        
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)
            
    def showHelp(self):
        if not self.tboard.isPaused:
            self.tboard.pause()
        self.dialogTextBrowser.exec_()
        
    def optionsEvent(self):
        if not self.tboard.isPaused:
            self.tboard.pause()
        
        self.optionsWin = optionsWindow(self)
        
    def newGameEvent(self):
        self.tboard.start()

class Help(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Help, self).__init__(parent)
        self.resize(300, 275)
        self.textBrowser = QtGui.QTextBrowser(self)
        self.textBrowser.append("""River Raid game\n\n
        How to play:
        To move left/rigth - use use arrow key left/right
        To move faster - use up arrow
        Fire - Space bar
                
        Keyboad shortcuts:
        - N - start new game,
        - P - pause/unpause game,
        - O - game options,
        - Q - quit game\n
        Mikołaj Waśniewski
        11.01.2016
        """)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)



class optionsWindow(QtGui.QDialog):
    """
    Class with option's window.
    """
    
    def __init__(self, parent = None):

        
        super(optionsWindow, self).__init__(parent)
        self.initUI()
        
    def initUI(self):

        mainLayout = QtGui.QVBoxLayout() 
        lbl1 = QtGui.QLabel('Select difficulty level:', self)
        buttonDifficult = QtGui.QPushButton("Save change")
        buttonDifficult.setAutoDefault(False)
        buttonDifficult.clicked.connect(self.difficultEvent)
        self.radioButtonDifficult1 = QtGui.QRadioButton("Easy")
        self.radioButtonDifficult2 = QtGui.QRadioButton("Normal")
        self.radioButtonDifficult3 = QtGui.QRadioButton("Hard")
        layoutDifficult = QtGui.QVBoxLayout()
        layoutDifficult.addWidget(self.radioButtonDifficult1)
        layoutDifficult.addWidget(self.radioButtonDifficult2)
        layoutDifficult.addWidget(self.radioButtonDifficult3)
        layoutDifficult.addWidget(buttonDifficult)
        

        self.groupDifficult = QtGui.QButtonGroup()
        self.groupDifficult.addButton(self.radioButtonDifficult1)
        self.groupDifficult.addButton(self.radioButtonDifficult2)
        self.groupDifficult.addButton(self.radioButtonDifficult3)

        
        buttonClose = QtGui.QPushButton("Close options")
        buttonClose.setAutoDefault(False)
        buttonClose.clicked.connect(self.close)
        
        mainLayout.addWidget(lbl1)
        mainLayout.addLayout(layoutDifficult)
        mainLayout.addWidget(buttonClose)
        self.setLayout(mainLayout)
        
        self.checkDifficultLevel()
        
        self.show()        
        
    def checkDifficultLevel(self):
        if Board.CheckDifficultLevel == -2:
            self.radioButtonDifficult1.setChecked(True)
        elif Board.CheckDifficultLevel == -3:
            self.radioButtonDifficult2.setChecked(True)
        elif Board.CheckDifficultLevel == -4:
            self.radioButtonDifficult3.setChecked(True)
       
    def difficultEvent(self):
        checked = self.groupDifficult.checkedId()
        if checked == -2:
            Board.CheckDifficultLevel = -2
            Board.Speed = 120
            Board.N = 3
        if checked == -3:
            Board.CheckDifficultLevel = -3
            River_raid.tboard.Speed = 100
            Board.N = 5
        if checked == -4:
            Board.CheckDifficultLevel = -4
            Board.Speed = 90
            Board.N = 6


            
class Board(QtGui.QFrame):
    
    msg2Statusbar = QtCore.pyqtSignal(str)
    winSize = 100
    BoardWidth = 75
    BoardHeight = 150
    CheckDifficultLevel = -3
    Speed = 100
    N = 4
    
    Plane = np.array([[0,0,0,1,0,0,0],
                      [0,0,0,1,0,0,0],
                      [0,0,1,1,1,0,0],
                      [0,1,1,1,1,1,0],
                      [1,1,0,1,0,1,1],
                      [1,0,0,1,0,0,1],
                      [0,0,0,1,0,0,0],
                      [0,1,1,1,1,1,0],
                      [0,1,0,1,0,1,0]
                      ])*101

    Fuel = np.array([[1,1,1,1],
                     [1,0,0,1],
                     [1,0,1,1],
                     [1,0,0,1],
                     [1,0,1,1],
                     [1,0,1,1],
                     [1,1,1,1]
                     ])
    def __init__(self, parent):
        super(Board, self).__init__(parent)
        

        self.initBoard()    

        
    def initBoard(self):     
        self.timer = QtCore.QBasicTimer()
        self.BoardM = np.zeros((Board.BoardHeight + 20, Board.BoardWidth))
        self.curPlaneX = 10
        
        self.curShipX = np.r_[np.array([10, 50, 10]), [0 for i in range(3)]]
        self.curShipY = np.r_[np.array([10, 60, 70]), [0 for i in range(3)]]
        self.curShipWay = np.r_[np.array([1, -1, 1]), [0 for i in range(3)]]
        self.ship = np.array([Vehicle() for i in range(8)])
        self.curShotX = np.array([0 for i in range(20)]) 
        self.curShotY = np.array([0 for i in range(20)])

        self.score = 0
        self.keylist = []
        self.lastshot = 100
        
        self.setStyleSheet("QWidget { background-color: aqua}")

        
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        

 

    def squareWidth(self):
        return self.contentsRect().width() / Board.BoardWidth
        

    def squareHeight(self):
        return self.contentsRect().height() / Board.BoardHeight
    
    def start(self):
    
        self.initBoard()
        self.isStarted = True
        self.isWaitingAfterLine = False
        self.firstrelease = False

        self.timer.start(Board.Speed, self)
        self.msg2Statusbar.emit(str(self.score))
        

        for i in range(self.N):
            self.ship[i].setRandomVehicle()
        self.update()
        
    def pause(self):
        
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        
        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")
            
        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str(self.score))

        self.update()
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.msg2Statusbar.emit(str(self.score))
            self.newShip()
            for i in range(self.N):
                if self.curShipY[i]>0:
                    for j in range(self.N):
                        if j == 0:
                            self.MoveVechicle(self.curShipX[i] + self.curShipWay[i], self.curShipY[i]+1, i)
                        else:
                            self.MoveVechicle(self.curShipX[i] + self.curShipWay[i], self.curShipY[i], i)
        [self.moveShot() for i in range(5)]            
        self.lastshot += 1

            
    def paintEvent(self, event):
        
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()
        for i in range(Board.BoardHeight+20):
            for j in range(Board.BoardWidth):
                if self.BoardM[i, j] > 0 and i <= Board.BoardHeight + 10 and i > 10:
                    self.drawSquare(painter,
                        rect.left() + j * self.squareWidth(),
                        boardTop + (i-10) * self.squareHeight(), self.BoardM[i, j])

    def drawSquare(self, painter, x, y, i):
        colorTable = np.array([0x00FFFF, 0xFFFF00, 0x000080, 0x008000, 0xFFD700,
                                0xD2691E, 0x000000, 0x7CFC00, 0xEE82EE, 0x00FF00])
        color = QtGui.QColor(colorTable[i%10])
        painter.fillRect(x, y+1, self.squareWidth(), 
            self.squareHeight(), color)
          
        painter.setPen(color)
        

        painter.drawLine(x, y + self.squareHeight(), x, y)
        painter.drawLine(x, y, x + self.squareWidth(), y)

        painter.drawLine(x , y + self.squareHeight(),
           x + self.squareWidth() , y + self.squareHeight())
        painter.drawLine(x + self.squareWidth(), 
            y + self.squareHeight(), x + self.squareWidth(), y )

    def keyPressEvent(self, event):

        key = event.key()
        
        if key == QtCore.Qt.Key_P:
            self.firstrelease = False
            self.pause()
            return
            
        if self.isPaused or not self.isStarted:
            self.firstrelease = False
            return
        
        self.firstrelease = True
        self.keylist.append(int(key))
        

    def keyReleaseEvent(self, event):
        
        if self.isPaused or not self.isStarted:
            return
        if self.firstrelease: 
            self.processmultikeys(self.keylist)

        self.firstrelease = False
        if len(self.keylist) > 0:
            del self.keylist[-1]

    def processmultikeys(self,keyspressed):

        for curkey in keyspressed:
            if curkey == QtCore.Qt.Key_Left:
                self.MovePlane(self.curPlaneX - 1)
                
            elif curkey == QtCore.Qt.Key_Right:
                self.MovePlane(self.curPlaneX + 1)
            
            elif curkey == QtCore.Qt.Key_Up:
                for j in range(self.N):
                    if self.curShipY[j] > 0: 
                        self.MoveVechicle(self.curShipX[j], self.curShipY[j] + 1, j)
            if curkey == QtCore.Qt.Key_Space:
                self.shot()

    
    def MovePlane(self, newX):
        if newX < 1 or newX > (Board.BoardWidth-8):
            return False
        else:
            # self.BoardM = np.zeros((Board.BoardHeight, Board.BoardWidth))  
            self.curPlaneX = newX
            self.currentBoard()
            self.update()
            return True     
            
    def MoveVechicle(self, newX, newY, i):
        if self.curShipX[i] <= 1 or  self.curShipX[i] == (Board.BoardWidth-11):
            self.curShipWay[i] = self.curShipWay[i]*(-1)
            self.curShipX[i] = newX +  2*self.curShipWay[i]
            return
            
        if newY + self.ship[i].vehicleHight == (Board.BoardHeight+20) :
            self.curShipY[i] = 0
            return
            
        self.curShipX[i] = newX
        self.curShipY[i] = newY
        self.currentBoard()
        self.update()
        if np.any(self.BoardM > 101):
            self.timer.stop()
            self.isStarted = False
            self.msg2Statusbar.emit("game over")

            
    def newShip(self):
        if np.sum(self.curShipY==0) > 0:
            if np.random.random() > 0.9: 
                i_temp = np.where(self.curShipY==0)[0]
                if i_temp[0] < self.N:
                    if np.sum(self.curShipY[:self.N] > 0) > 0:
                        if np.min(self.curShipY[:self.N][self.curShipY[:self.N]>0]) > 10:
                            self.curShipY[i_temp[0]] = 1
                            self.curShipX[i_temp[0]] = np.random.randint(10, Board.BoardWidth-11)
                            self.curShipWay[i_temp[0]] = np.random.choice(np.array([-1,1]), 1)
                            self.ship[i_temp[0]].setRandomVehicle()
                    else:
                        self.curShipY[i_temp[0]] = 1
                        self.curShipX[i_temp[0]] = np.random.randint(10, Board.BoardWidth-11)
                        self.curShipWay[i_temp[0]] = np.random.choice(np.array([-1,1]), 1)
                        self.ship[i_temp[0]].setRandomVehicle()
            
    def shot(self):
        if self.lastshot > 5:
            i = np.where(self.curShotY==0)[0][0]
            self.curShotX[i] = self.curPlaneX + 3
            self.curShotY[i] = Board.BoardHeight-12
            self.lastshot  = 0

    
    def moveShot(self):
        for i in range(self.N):
            if self.curShotY[i] > 0:
                self.curShotY[i] -= 1 
        self.currentBoard()
    
    def currentBoard(self):
        self.BoardM = np.zeros((Board.BoardHeight+20, Board.BoardWidth))

        for j in range(self.N):
            if self.curShipY[j] > 0:
                self.BoardM[self.curShipY[j]:self.curShipY[j]+self.ship[j].vehicleHight, self.curShipX[j]:self.curShipX[j]+self.ship[j].vehicleWidth] += self.ship[j].vehicleMatrix[:,::self.curShipWay[j]]

        for i in range(20):
            if self.curShotY[i] > 0:
                self.BoardM[self.curShotY[i]:self.curShotY[i]+3, self.curShotX[i]] += 11
                if self.BoardM[self.curShotY[i], self.curShotX[i]] > 11:
                    self.score += 100
                    # self.msg2Statusbar.emit(str(self.score))
                    j_shot = 0
                    dist = (self.curShipX[0]-self.curShotX[i])**2 + (self.curShipY[0]-self.curShotY[i])**2
                    for j in range(self.N):
                        if dist > (self.curShipX[j]-self.curShotX[i])**2 + (self.curShipY[j]-self.curShotY[i])**2:
                            j_shot = j
                    self.curShipY[j_shot] = 0
                    self.curShotY[i] = 0
        g = np.array([9 for i in range(Board.BoardHeight+20)])
        self.BoardM[:,0] = g
        self.BoardM[:,Board.BoardWidth-1] = g
        
        self.BoardM[(Board.BoardHeight):Board.BoardHeight+9, self.curPlaneX:self.curPlaneX+7] += Board.Plane

        
           


 

       
class Vehicle(object):
    
    matrixTable = ([
                    np.array([[0,0,0,0,0,0,6,6,0,0],
                             [0,0,0,0,0,6,6,6,0,0],
                             [5,5,5,5,5,5,5,5,5,5],
                             [0,0,5,5,5,5,5,5,5,5],
                             [0,0,0,5,5,5,5,5,5,0]
                            ])[:,::-1], # ship
                    np.array([[0,0,0,0,0,0,0,0,1],
                            [0,1,1,0,0,0,0,1,1],
                            [1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,0,0,1,0],
                            [0,0,0,0,1,1,1,1,0],
                            [0,0,0,0,0,1,1,0,0]
                          ])[:,::-1]*2, # plane 2
                    np.array([[0,0,0,0,4,4,4,0,0],
                           [0,0,0,0,0,0,4,4,4],
                           [0,0,0,0,0,0,4,0,0],
                           [3,0,0,0,3,3,3,3,0],
                           [3,3,3,3,3,3,3,3,3],
                           [3,0,0,0,3,3,3,3,3],
                           [0,0,0,0,0,0,3,0,0],
                           [0,0,0,0,0,3,3,3,0]
                        ]), # helicopter
                    np.array([[0,0,4,4,4,0,0],
                              [0,4,4,4,4,4,0],
                              [7,7,7,7,7,7,7],
                              [7,7,7,7,7,7,7],
                              [8,8,8,8,8,8,8],
                              [0,8,8,8,8,8,0],
                              [0,0,5,5,5,0,0],
                              [0,0,5,0,5,0,0],
                              [0,0,5,0,5,0,0],
                              [0,0,0,5,0,0,0]]) # baloon 
                    ])
                              

    def __init__(self):
        self.vehicleMatrix = np.array([])
        self.vehicleHight = 0
        self.vehicleWidth = 0
        self.num = 0

    def width(self):
        return self.vehicleWidth
        
    def hight(self):
        return self.vehicleHight
        

    def setVehicle(self, i):
        self.vehicleMatrix = Vehicle.matrixTable[i]
        self.vehicleHight = np.shape(self.vehicleMatrix)[0]
        self.vehicleWidth = np.shape(self.vehicleMatrix)[1]
        self.num = i
        

    def setRandomVehicle(self):
        self.setVehicle(np.random.randint(0, 4))


        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = River_raid()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()     
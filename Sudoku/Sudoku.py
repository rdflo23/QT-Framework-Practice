from PySide2.QtWidgets import *
from PySide2.QtCore import Qt

class MyButton(QPushButton):
    def __init__(self, val=0, row=0, col=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = row
        self.col = col
        self.invalid = False          #If this is true then there is a duplicate in same row or col
        self.value = int(val)   #getting type error so cast it to int
        self.fromFile = False
        self.fromConfig()           #check if got a non zero number from puzzle file
    def setval(self):   #set the text of button
        if self.value == 0:
            self.setText("")
            return          #leave it blank if it is 0
        self.setText(str(self.value))

    def mousePressEvent(self, event):
        self.invalid = False          #If this is true then there is a duplicate in same row or col
        if self.fromFile:           #do not want to change the initial numbers from files
            return
        if event.button() == Qt.LeftButton:
            self.value += 1
            if self.value == 10:
                self.value = 9
        if event.button() == Qt.RightButton:
            self.value -= 1
            if self.value == -1:
                self.value = 0
        self.setval()
        self.setColor("none")
    def fromConfig(self):
        """"
            Checks if button is a non zero number from the config file
        """
        if self.value > 0:
            self.fromFile = True
            self.setval()   #set value if got a non zero number from file
            self.setStyleSheet("background-color: green")
    def setColor(self,color):
        self.setStyleSheet("background-color: "+color)

    def isInvalid(self):
        if self.fromFile:
            return
        self.invalid = True
        if self.invalid:
            self.setColor("red")



class Frame(QWidget):         #the 3x3 grid
    def __init__(self, grid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = []   #list of 9 buttons in the grid
        self.grid = grid       #grid id
        self.line = []      #what lines to read
        self.char = []     #what chars to read in each line
        self.setLineChar()
        self.setButtons()
        layout = QGridLayout()
        for b in self.buttons:
            layout.addWidget(b, b.row, b.col)
        self.setLayout(layout)           #trying to use signals here but not working


    def setLineChar(self):                #I see a pattern but.....
        if self.grid == 1:              #HAD to hard code it
            self.line = [1,2,3]         #read first 3 lines
            self.char = [1,2,3]         #read first 3 chars in each line
        if self.grid == 2:
            self.line = [1, 2, 3]
            self.char = [4, 5, 6]
        if self.grid == 3:
            self.line = [1, 2, 3]
            self.char = [7, 8, 9]
        if self.grid == 4:
            self.line = [4, 5, 6]
            self.char = [1, 2, 3]
        if self.grid == 5:
            self.line = [4, 5, 6]
            self.char = [4, 5, 6]
        if self.grid == 6:
            self.line = [4, 5, 6]
            self.char = [7, 8, 9]
        if self.grid == 7:
            self.line = [7, 8, 9]
            self.char = [1, 2, 3]
        if self.grid == 8:
            self.line = [7, 8, 9]
            self.char = [4, 5, 6]
        if self.grid == 9:
            self.line = [7, 8, 9]
            self.char = [7, 8, 9]


    def setButtons(self):
        """
        Sets the button's value,row and column taken from a file
        """
        puzzle = open("puzzle.txt", "r")
        puzzle.seek(0)      #make sure file is at beginning each time
        row = 0  # after each char col should increment
        linecount = 0
        for line in puzzle:
            linecount += 1
            if linecount not in self.line:
                row += 1            #still need to increase row count
                continue
            col = 0  # after each line col should increment
                    #col needs to reset after each line
            line = line.strip()
            charcount = 0       #reset charcount to 0 after each line
            for char in line:
                if char == ",":
                    continue
                charcount += 1
                if charcount not in self.char:
                    col += 1        #still need to increase column count
                    continue
                b = MyButton(char,row,col)          #char should correspond with the value of the button
                self.buttons.append(b)
                col += 1
            row += 1
        puzzle.close()

    def checkRow(self,buttons):         #pass in the buttons of my adjacent grids
        #TODO I need to hilight both invalid buttons. it is leaving
        # the most recent button unchanged
        row1 = []
        row2 = []
        row3 = []
        r1 = self.buttons[0].row            #gets me the 3 rows i need
        r2 = self.buttons[4].row
        r3 = self.buttons[7].row
        for col in range(9):                     #get all same row buttons and append to each list
            for key in buttons:
                if key == (r1,col):
                    row1.append(buttons[key])
                if key == (r2,col):
                    row2.append(buttons[key])
                if key == (r3,col):
                    row3.append(buttons[key])
        values = []
        for b in row1:
            values.append(b.value)
        for b in row1:
            values.remove(b.value)      #remove itself's value from the values list
            for val in values:
                if b.value == 0:        #don't need to look at empty buttons
                    continue
                if b.fromFile:
                    continue            #these buttons are set from file
                if b.value == val:
                    b.isInvalid()       #not setting both buttons red. leaves current one the same
        values = []
        for b in row2:
            values.append(b.value)
        for b in row2:
            values.remove(b.value)      #remove itself's value from the values list
            for val in values:
                if b.value == 0:        #don't need to look at empty buttons
                    continue
                if b.fromFile:
                    continue            #these buttons are set from file
                if b.value == val:
                    b.isInvalid()
        values = []
        for b in row3:
            values.append(b.value)
        for b in row3:
            values.remove(b.value)      #remove itself's value from the values list
            for val in values:
                if b.value == 0:        #don't need to look at empty buttons
                    continue
                if b.fromFile:
                    continue            #these buttons are set from file
                if b.value == val:
                    b.isInvalid()

    def checkCol(self,buttons):
        col1 = []
        col2 = []
        col3 = []
        c1 = self.buttons[0].col            #gets me the 3 rows i need
        c2 = self.buttons[1].col
        c3 = self.buttons[2].col
        for row in range(9):                     #get all same row buttons and append to each list
            for key in buttons:
                if key == (row,c1):
                    col1.append(buttons[key])
                if key == (row,c2):
                    col2.append(buttons[key])
                if key == (row,c3):
                    col3.append(buttons[key])
        values = []
        for b in col1:
            values.append(b.value)
        for b in col1:
            values.remove(b.value)          #without this it would turn red even if not a duplicate
            for val in values:
                if b.value == 0:        #don't need to look at empty buttons
                    continue
                if b.fromFile:
                    continue            #these buttons are set from file
                if b.value == val:
                    b.isInvalid()
        values = []
        for b in col2:
            values.append(b.value)
        for b in col2:
            values.remove(b.value)
            for val in values:
                if b.value == 0:        #don't need to look at empty buttons
                    continue
                if b.fromFile:
                    continue            #these buttons are set from file
                if b.value == val:
                    b.isInvalid()
        values = []
        for b in col3:
            values.append(b.value)
        for b in col3:
            values.remove(b.value)      #remove itself's value from the values list
            for val in values:
                if b.value == 0:        #don't need to look at empty buttons
                    continue
                if b.fromFile:
                    continue            #these buttons are set from file
                if b.value == val:
                    b.isInvalid()


class Game(QWidget):           #hold the whole game
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = []        #all the frames
        self.buttons = {}       #all the buttons    #Try a dictionary with r,c as key and value is button
        self.addGrid()
        self.getAllButtons()    #this should populate the buttons dict
        btn = QPushButton("Check")
        btn2 = QPushButton("Reset")
        layout = QGridLayout()      #cant set a check everytime a button is pushed in grid so
        layout.addWidget(btn,3,1)       #added a check button
        layout.addWidget(btn2,3,2)       #added a check button
        btn.clicked.connect(self.checkWin)
        btn2.clicked.connect(self.reset)
        row = 0
        col = 0
        count = 0
        for f in self.frames:
            count +=1
            if count == 4 or count == 7:  #if placed 3 grids in a row
                row+=1                     #move one row done and reset column
                col = 0
            layout.addWidget(f,row,col)
            col += 1
        self.setLayout(layout)

    def addGrid(self):
        for i in range(9):
            f = Frame(i+1)
            self.frames.append(f)

    def getAllButtons(self):
        for f in self.frames: #iterate through frames
            for b in f.buttons: #iterate through the frame's button list
                self.buttons[(b.row,b.col)] = b  #add each button the the Game's button dict
                                                    #r,c tuple as key
        print(self.buttons.items())

    def checkSpot(self):
        for f in self.frames:
            if f.grid in [1,4,7]:
                f.checkRow(self.buttons)        #dont need to check all grids
            if f.grid in [1,2,3]:
                f.checkCol(self.buttons)

    def checkEmpty(self):
        for b in self.buttons:
            if self.buttons[b].value == 0:
                return False
        return True

    def checkButtons(self):
        for b in self.buttons:
            if self.buttons[b].invalid:
                return False
        return True

    # def mousePressEvent(self,event):            #I want every time a click
                                        #to check the values of the buttons
        # self.checkWin()                          #Only works if click on white space
                                                #and not buttons in grid
        # print("something happened in game")

    def checkWin(self):
        self.checkSpot()            #check all the spots
        if self.checkEmpty() and self.checkButtons(): #check if it is filled in and valid
            for b in self.buttons:
                self.buttons[b].setColor("green")
            qmb = QMessageBox(text="You Win")
            qmb.exec_()
        else:
            qmb = QMessageBox(text="Not a Winner")
            qmb.exec_()

    def reset(self):
        for b in self.buttons:
            if self.buttons[b].fromFile:
                continue
            self.buttons[b].value = 0
            self.buttons[b].setval()
            self.buttons[b].setColor("none")


app = QApplication()

g = Game()
g.show()
app.exec_()

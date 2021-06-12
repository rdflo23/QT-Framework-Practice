from PySide2.QtWidgets import *


class MyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.clicked.connect(self.click)
        self.isClicked = False
        self.turn=0
    def click(self):
        self.isClicked = True
        if self.isClicked and self.turn == 0:
            self.setText("X")
        else:
            self.setText("O")
        self.turn+=1


class Board(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        layout = QGridLayout()
        self.b_list = []
        for num in range(3):
            button = MyButton()
            button2 = MyButton()
            button3 = MyButton()
            self.b_list.append(button)
            self.b_list.append(button2)
            self.b_list.append(button3)
            layout.addWidget(button, 0, num)
            layout.addWidget(button2, 1, num)
            layout.addWidget(button3, 2, num)
        self.setLayout(layout)
    def checkwin(self):
        QMessageBox("Game Over")

app = QApplication()
game = Board()
game.show()
app.exec_()
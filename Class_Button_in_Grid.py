from PySide2.QtWidgets import *
class MyButton(QPushButton):
    num_list = ['1','2','3']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ind = -1
        self.clicked.connect(self.click)
    def click(self):
        self.ind=(self.ind+1) % len(MyButton.num_list)
        self.setText(MyButton.num_list[self.ind])


app = QApplication()
main_widget = QWidget()
                    # THis WORKS
                    # layout = QGridLayout()
                    # button = MyButton("Call func")
                    # button2 = MyButton("Call func")
                    # layout.addWidget(button,0,1)
                    # layout.addWidget(button2,0,2)
                    # main_widget.setLayout(layout)
layout = QGridLayout()
for num in range(5):
    button = MyButton("1st")
    button2 = MyButton("2nd")
    button3 = MyButton("3rd")
    layout.addWidget(button,0,num)
    layout.addWidget(button2,1,num)
    layout.addWidget(button3,2,num)
but = QPushButton("hello")
layout.addWidget(but,3,0)
main_widget.setLayout(layout)
main_widget.show()
app.exec_()
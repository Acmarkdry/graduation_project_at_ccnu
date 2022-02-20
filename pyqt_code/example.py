import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QLabel, QLineEdit, QDateEdit, \
    QComboBox, QTextEdit, QGridLayout


class Demo(QTabWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.tab1 = QWidget()                   # 1
        self.tab2 = QWidget()
        self.tab3 = QTextEdit()

        self.tab1_init()                        # 2
        self.tab2_init()

        self.addTab(self.tab1, 'Basic Info')    # 3
        self.addTab(self.tab2, 'Contact Info')
        self.addTab(self.tab3, QIcon('info.ico'), 'More Info')

        self.currentChanged.connect(lambda: print(self.currentIndex()))    # 4

    def tab1_init(self):
        name_label = QLabel('Name:', self.tab1)
        gender_label = QLabel('Gender:', self.tab1)
        bd_label = QLabel('Birth Date:', self.tab1)

        name_line = QLineEdit(self.tab1)
        items = ['Please choose your gender', 'Female', 'Male']
        gender_combo = QComboBox(self.tab1)
        gender_combo.addItems(items)

        bd_dateedit = QDateEdit(self.tab1)

        g_layout = QGridLayout()
        g_layout.addWidget(name_label, 0, 0, 1, 1)
        g_layout.addWidget(name_line, 0, 1, 1, 1)
        g_layout.addWidget(gender_label, 2, 0, 1, 1)
        g_layout.addWidget(gender_combo, 2, 1, 1, 1)
        g_layout.addWidget(bd_label, 3, 0, 1, 1)
        g_layout.addWidget(bd_dateedit, 3, 1, 1, 1)

        self.tab1.setLayout(g_layout)

    def tab2_init(self):
        tel_label = QLabel('Tel:', self.tab2)
        mobile_label = QLabel('Mobile:', self.tab2)
        add_label = QLabel('Address:', self.tab2)

        tel_line = QLineEdit(self.tab2)
        mobile_line = QLineEdit(self.tab2)
        add_line = QLineEdit(self.tab2)

        g_layout = QGridLayout()
        g_layout.addWidget(tel_label, 0, 0, 1, 1)
        g_layout.addWidget(tel_line, 0, 1, 1, 1)
        g_layout.addWidget(mobile_label, 1, 0, 1, 1)
        g_layout.addWidget(mobile_line, 1, 1, 1, 1)
        g_layout.addWidget(add_label, 2, 0, 1, 1)
        g_layout.addWidget(add_line, 2, 1, 1, 1)

        self.tab2.setLayout(g_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
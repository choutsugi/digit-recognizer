from MainWidget import MainWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.Qt import *

import sys


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('resource/icon/icon.ico'))
    main_widget = MainWidget()
    main_widget.show()
    exit(app.exec_())


if __name__ == '__main__':
    main()

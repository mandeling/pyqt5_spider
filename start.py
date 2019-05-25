from gui import Ico
import sys
from PyQt5.QtCore import QFile,QTextStream
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Ico()

    sys.exit(app.exec_())


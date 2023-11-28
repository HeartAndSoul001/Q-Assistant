from GUI.initMainGUI import *
import sys

def main():

    app = QApplication(sys.argv)
    ex = homepage()

    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
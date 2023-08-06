import sys
import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QThread
from pyqtgraph.dockarea import DockArea
from pymodaq.daq_scan.daq_scan_main import DAQ_Scan

def main():

    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    fname = ""
    win.setVisible(False)
    splash = QtGui.QPixmap(os.path.join('documentation','splash.png'))
    splash_sc = QtWidgets.QSplashScreen(splash, Qt.WindowStaysOnTopHint)
    splash_sc.show()
    splash_sc.raise_()
    splash_sc.showMessage('Loading Main components', color=Qt.white)
    QtWidgets.QApplication.processEvents()

    area = DockArea()
    win.setCentralWidget(area)
    win.resize(1000, 500)
    win.setWindowTitle('pymodaq Scan')
    win.setVisible(False)
    prog = DAQ_Scan(area, fname)
    QThread.sleep(2)
    splash_sc.finish(win)
    win.setVisible(True)

    sys.exit(app.exec_())
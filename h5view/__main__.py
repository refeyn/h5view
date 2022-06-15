import sys

from PySide6 import QtCore, QtWidgets

from h5view.app import H5ViewWindow

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

app = QtWidgets.QApplication(sys.argv)
mw = H5ViewWindow(None)
mw.show()
if len(sys.argv) > 1:
    mw.open(sys.argv[1])
app.exec()

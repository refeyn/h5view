# SPDX-FileCopyrightText: Copyright (c) 2024 Matthew Joyce and other h5view contributors
# SPDX-License-Identifier: MIT

import sys

from PySide6 import QtWidgets

from h5view.app import H5ViewWindow

__version__ = "0.1.0a0"


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("Refeyn Ltd")
    app.setApplicationName("h5view")
    mw = H5ViewWindow()
    mw.show()
    if len(sys.argv) > 1:
        mw.open(sys.argv[1])
    app.exec()

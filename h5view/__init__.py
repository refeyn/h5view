# SPDX-FileCopyrightText: Copyright (c) 2024 Refeyn Ltd and other h5view contributors
# SPDX-License-Identifier: MIT

import importlib.metadata
import sys

from PySide6 import QtWidgets

from h5view.app import H5ViewWindow

__version__ = importlib.metadata.version("h5view")


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("Refeyn Ltd")
    app.setApplicationName("h5view")
    app.setApplicationVersion(__version__)
    mw = H5ViewWindow()
    mw.show()
    if len(sys.argv) > 1:
        mw.open(sys.argv[1])
    app.exec()

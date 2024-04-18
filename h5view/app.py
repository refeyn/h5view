# SPDX-FileCopyrightText: Copyright (c) 2024 Refeyn Ltd and other h5view contributors
# SPDX-License-Identifier: MIT

import os
from typing import cast, List, Optional, Union

import h5py
import hdf5plugin  # pylint: disable=unused-import
from PySide6 import QtCore, QtGui, QtWidgets

import h5view
from h5view import gui, utils
from h5view.ui.app import Ui_MainWindow


class H5ViewWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        self._h5file: Optional[h5py.File] = None
        self._viewWidget: QtWidgets.QWidget = self.valueTableView
        self._regionSpins: List[QtWidgets.QSpinBox] = []
        self._settings = QtCore.QSettings()

        self.valueImageView = gui.PixmapWidget(self)
        self.valueImageView.setAutoscale(self.actionAutoscale_Image.isChecked())
        self.viewWidgetContainer.layout().addWidget(self.valueImageView)
        # Hide view widgets
        for i in range(self.viewWidgetContainer.layout().count()):
            widget = self.viewWidgetContainer.layout().itemAt(i).widget()
            if widget is not self.valueTableView:
                widget.hide()
        self.spinContainer.hide()

        self.pathLabel.setText("No file loaded")
        self.copyPathButton.hide()
        self.typeLabel.setText("")
        self.setWindowTitle(f"H5View {h5view.__version__}")

        self._connectSignals()

    def _connectSignals(self) -> None:
        self.actionOpen.triggered.connect(self._onOpen)
        self.actionShow_Image.triggered.connect(self._onUpdateShowIndex)
        self.actionAutoscale_Image.toggled.connect(self.valueImageView.setAutoscale)
        self.copyPathButton.clicked.connect(self._onCopyPathButtonClicked)

    def _onOpen(self) -> None:
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            dir=str(self._settings.value("openDir", ".")),
            filter="All files (*);;H5 files (*.h5 *.hdf5)",
        )
        if fname:
            self.open(fname)

    def _onShowIndex(self, idx: QtCore.QModelIndex) -> None:
        self._showIndex(idx)

    def _onUpdateShowIndex(self) -> None:
        if (
            self.treeView.selectionModel() is not None
            and len(self.treeView.selectionModel().selectedIndexes()) > 0
        ):
            self._showIndex(self.treeView.selectionModel().selectedIndexes()[0])

    def _onCopyPathButtonClicked(self) -> None:
        QtWidgets.QApplication.clipboard().setText(self.pathLabel.text())

    def open(self, fname: Union[str, os.PathLike]) -> None:
        self._settings.setValue("openDir", str(os.path.dirname(fname)))
        try:
            self._h5file = h5py.File(fname)
        except OSError as e:
            QtWidgets.QMessageBox.critical(self, "Could not open file", str(e))
        else:
            self._populateTreeView()
            self.setWindowTitle(
                f"H5View {h5view.__version__} - {os.path.abspath(fname)}"
            )

    def _populateTreeView(self) -> None:
        model = QtGui.QStandardItemModel()
        self._recursivePopulate(self._h5file, model.invisibleRootItem())
        self.treeView.setModel(model)
        self.treeView.selectionModel().select(
            model.index(0, 0), QtCore.QItemSelectionModel.SelectionFlag.SelectCurrent
        )
        self.treeView.selectionModel().currentChanged.connect(self._onShowIndex)
        self._showIndex(model.index(0, 0))

    def _recursivePopulate(
        self,
        group_or_dataset: Union[h5py.Group, h5py.Dataset],
        item: QtGui.QStandardItem,
    ) -> None:
        item.setData(group_or_dataset, cast(int, QtCore.Qt.ItemDataRole.UserRole))
        if isinstance(group_or_dataset, h5py.Group):
            for name, sub_grp_or_ds in group_or_dataset.items():
                subitem = QtGui.QStandardItem(name)
                subitem.setFlags(subitem.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self._recursivePopulate(sub_grp_or_ds, subitem)
                item.appendRow(subitem)
        elif isinstance(group_or_dataset, h5py.Dataset):
            pass
        else:
            raise RuntimeError()

    def _showIndex(self, idx: QtCore.QModelIndex) -> None:
        group_or_dataset = idx.data(cast(int, QtCore.Qt.ItemDataRole.UserRole))
        self.pathLabel.setText(group_or_dataset.name)
        self.copyPathButton.show()

        attrModel = QtGui.QStandardItemModel()
        for i, (name, value) in enumerate(sorted(group_or_dataset.attrs.items())):
            attrModel.setItem(i, 0, QtGui.QStandardItem(name))
            attrModel.setItem(i, 1, QtGui.QStandardItem(utils.formatAsStr(value)))
        self.attrTableView.setModel(attrModel)
        self.attrTableView.resizeColumnsToContents()
        self.tabWidget.setTabText(1, f"Attributes ({len(group_or_dataset.attrs)})")

        metadataModel = QtGui.QStandardItemModel()
        for i, (name, value) in enumerate(
            sorted(utils.metadataFor(group_or_dataset).items())
        ):
            metadataModel.setItem(i, 0, QtGui.QStandardItem(name))
            metadataModel.setItem(i, 1, QtGui.QStandardItem(utils.formatAsStr(value)))
        self.metadataTableView.setModel(metadataModel)
        self.metadataTableView.resizeColumnsToContents()

        viewWidget = None
        regionSpins = 0
        if isinstance(group_or_dataset, h5py.Group):
            self.typeLabel.setText("group")
            viewWidget = self.valueTableView
            model = QtGui.QStandardItemModel()
            for i, (name, value) in enumerate(group_or_dataset.items()):
                model.setItem(i, 0, QtGui.QStandardItem(name))
                model.setItem(i, 1, QtGui.QStandardItem(utils.formatAsStr(value)))
            viewWidget.setModel(model)
            viewWidget.resizeColumnsToContents()

        elif isinstance(group_or_dataset, h5py.Dataset):
            self.typeLabel.setText(
                utils.typeAndShapeAsStr(group_or_dataset.dtype, group_or_dataset.shape)
            )
            if group_or_dataset.shape == ():
                viewWidget = self.valueTextView
                viewWidget.setPlainText(utils.formatAsStr(group_or_dataset))
            elif self.actionShow_Image.isChecked() and group_or_dataset.ndim >= 2:
                viewWidget = self.valueImageView
                self.valueImageView.setDataset(group_or_dataset)
                regionSpins = len(self.valueImageView.region())
            else:
                viewWidget = self.valueTableView
                viewWidget.setModel(gui.DatasetModel(group_or_dataset))
                regionSpins = len(viewWidget.model().region())
                dtypeWidth = gui.columnWidthFromDtype(
                    viewWidget, group_or_dataset.dtype
                )
                for i in range(viewWidget.model().columnCount()):
                    viewWidget.setColumnWidth(
                        i, dtypeWidth or gui.columnWidthRandomized(viewWidget, i)
                    )
        else:
            raise RuntimeError()

        if self._viewWidget:
            self._viewWidget.hide()

        if viewWidget:
            viewWidget.show()
            self._viewWidget = viewWidget

        while len(self._regionSpins) > regionSpins:
            self._regionSpins.pop()
            # Remove label and then spin
            self.spinContainer.layout().itemAt(
                len(self._regionSpins) * 2
            ).widget().setParent(None)
            self.spinContainer.layout().itemAt(
                len(self._regionSpins) * 2
            ).widget().setParent(None)

        while len(self._regionSpins) < regionSpins:
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
            )
            label = QtWidgets.QLabel(f"Dim {len(self._regionSpins)}")
            label.setSizePolicy(sizePolicy)
            self.spinContainer.layout().insertWidget(len(self._regionSpins) * 2, label)

            spin = QtWidgets.QSpinBox(self)
            spin.setSizePolicy(sizePolicy)
            spin.valueChanged.connect(self._onRegionChanged)
            self.spinContainer.layout().insertWidget(
                len(self._regionSpins) * 2 + 1, spin
            )
            self._regionSpins.append(spin)

        for i, spin in enumerate(self._regionSpins):
            spin.setRange(0, group_or_dataset.shape[i] - 1)

        # Remember the spacer!
        self.spinContainer.setVisible(self.spinContainer.layout().count() != 1)
        self._setRegion()

    def _onRegionChanged(self) -> None:
        self._setRegion()

    def _setRegion(self) -> None:
        region = tuple(s.value() for s in self._regionSpins)
        if self._viewWidget is self.valueTableView and isinstance(
            self.valueTableView.model(), gui.DatasetModel
        ):
            self.valueTableView.model().setRegion(region)
        elif self._viewWidget is self.valueImageView:
            self.valueImageView.setRegion(region)

import math
import os
import random
from typing import Tuple, Union, Any, Optional, List

import h5py
import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets

from h5view.ui.h5view import Ui_MainWindow


class DatasetModel(QtCore.QAbstractTableModel):
    def __init__(self, dataset: h5py.Dataset):
        super().__init__()
        self._dataset = dataset
        self._rows = self._cols = 1
        if dataset.ndim == 1:
            self._rows = dataset.size
        elif dataset.ndim > 1:
            self._rows, self._cols = dataset.shape[-2:]
        self._region = (0,) * len(dataset.shape[:-2])

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return self._rows

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return self._cols

    def region(self) -> Tuple[int, ...]:
        return self._region

    def regionBounds(self) -> Tuple[int, ...]:
        return tuple(self._dataset.shape[:-2])

    def setRegion(self, region: Tuple[int, ...]) -> None:
        assert len(region) == len(self._region)
        self._region = region
        self.dataChanged.emit(self.index(0, 0), self.index(self._rows, self._cols), [])

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            didx = self._region + (index.row(), index.column())
            return str(self._dataset[didx[: self._dataset.ndim]])


class PixmapWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self._dataset: Optional[h5py.Dataset] = None
        self._rows: Optional[int] = None
        self._cols: Optional[int] = None
        self._region: Optional[Tuple[int, ...]] = None
        self._autoscale = False

    def setDataset(self, dataset: h5py.Dataset) -> None:
        self._dataset = dataset
        self._rows = self._cols = 1
        if dataset.ndim == 1:
            self._rows = dataset.size
        elif dataset.ndim > 1:
            self._rows, self._cols = dataset.shape[-2:]
        self._region = (0,) * len(dataset.shape[:-2])
        self.repaint()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        if self._dataset is None:
            return
        image = self.getImage()
        painter = QtGui.QPainter(self)
        imageRect = QtCore.QRect()
        imageRect.setSize(image.size().scaled(self.size(), QtCore.Qt.KeepAspectRatio))
        imageRect.moveCenter(QtCore.QPoint(self.width() // 2, self.height() // 2))
        painter.drawImage(imageRect, image)

    def region(self) -> Tuple[int, ...]:
        assert self._region is not None
        return self._region

    def regionBounds(self) -> Tuple[int, ...]:
        assert self._dataset is not None
        return tuple(self._dataset.shape[:-2])

    def setRegion(self, region: Tuple[int, ...]) -> None:
        assert self._region is not None
        assert len(region) == len(self._region)
        self._region = region
        self.repaint()

    def autoscale(self) -> bool:
        return self._autoscale

    def setAutoscale(self, autoscale: bool) -> None:
        self._autoscale = autoscale
        self.repaint()

    def getImage(self) -> QtGui.QImage:
        assert (
            self._rows is not None
            and self._cols is not None
            and self._region is not None
            and self._dataset is not None
        )
        data = self._dataset[self._region].astype(float)
        if self._autoscale:
            data -= data.min()
            data /= data.max()
        else:
            dtypeInfo = np.iinfo(self._dataset.dtype)
            data -= dtypeInfo.min
            data /= dtypeInfo.max
        data = (data * 255).T.copy(order="C").astype(np.uint8)
        assert data.shape == (self._cols, self._rows)
        return QtGui.QImage(
            data.tobytes(),
            self._cols,
            self._rows,
            self._cols,
            QtGui.QImage.Format_Grayscale8,
        )


def columnWidthRandomized(widget: QtWidgets.QTableView, column: int) -> float:
    model = widget.model()
    delegate = widget.itemDelegate()
    widths: List[float] = []
    for _ in range(10):
        index = model.index(random.randrange(model.rowCount()), column)
        style = QtWidgets.QStyleOptionViewItem()
        delegate.initStyleOption(style, index)
        sh = delegate.sizeHint(style, index)
        widths.append(sh.width())
    return max(widths) + 12


def columnWidthFromDtype(
    widget: QtWidgets.QTableView, dtype: np.dtype
) -> Optional[float]:
    if np.issubdtype(dtype, np.floating):
        info = np.finfo(dtype)
        digits = math.ceil(info.bits * math.log10(2))
        # Add sign, decimal point, and exponent
        digits += 4
    elif np.issubdtype(dtype, np.integer):
        info = np.iinfo(dtype)
        digits = math.ceil(info.bits * math.log10(2))
        if np.issubdtype(dtype, np.signedinteger):
            # Add sign
            digits += 1
    else:
        return None
    model = widget.model()
    delegate = widget.itemDelegate()
    index = model.index(0, 0)
    style = QtWidgets.QStyleOptionViewItem()
    delegate.initStyleOption(style, index)
    fontMetrics = QtGui.QFontMetrics(style.font)
    return float(fontMetrics.horizontalAdvance("8" * digits)) + 12


def formatAsStr(value: Any) -> str:
    if isinstance(value, h5py.Group):
        return f"Group {value.name!r} with {len(value.keys())} members"
    elif isinstance(value, h5py.Dataset):
        if value.shape == ():
            singlevalue = value[()]
            if isinstance(singlevalue, bytes):
                try:
                    singlevalue = singlevalue.decode()
                except ValueError:
                    pass
            return str(singlevalue)
        else:
            return (
                f"Dataset {value.name!r} {typeAndShapeAsStr(value.dtype, value.shape)}"
            )
    else:
        return str(value)


def typeAsStr(dtype: np.dtype) -> str:
    if h5py.check_string_dtype(dtype):
        return "string"
    elif h5py.check_vlen_dtype(dtype):
        return f"vlen array of {typeAsStr(h5py.check_vlen_dtype(dtype))}"
    elif h5py.check_enum_dtype(dtype):
        return "enum"
    elif dtype == h5py.ref_dtype:
        return "object reference"
    elif dtype == h5py.regionref_dtype:
        return "region reference"
    else:
        return str(dtype)


def typeAndShapeAsStr(dtype: np.dtype, shape: Tuple[int, ...]) -> str:
    if shape == ():
        return typeAsStr(dtype)
    else:
        return f"{typeAsStr(dtype)}{shape}"


class H5ViewWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent: Optional[QtWidgets.QWidget]) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        self._h5file: Optional[h5py.File] = None
        self._viewWidget: Optional[QtWidgets.QWidget] = None
        self._regionSpins: List[QtWidgets.QSpinBox] = []

        self.valueImageView = PixmapWidget(self)
        self.valueImageView.setAutoscale(self.actionAutoscale_Image.isChecked())
        self.viewWidgetContainer.layout().addWidget(self.valueImageView)
        # Hide view widgets
        for i in range(self.viewWidgetContainer.layout().count()):
            widget = self.viewWidgetContainer.layout().itemAt(i).widget()
            if widget is not self.valueTableView:
                widget.hide()
        self.spinContainer.hide()

        self.pathLabel.setText("No file loaded")
        self.typeLabel.setText("")

        self._connectSignals()

    def _connectSignals(self) -> None:
        self.actionOpen.triggered.connect(self._onOpen)
        self.actionShow_Image.triggered.connect(self._onUpdateShowIndex)
        self.actionAutoscale_Image.toggled.connect(self.valueImageView.setAutoscale)

    def _onOpen(self) -> None:
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            filter="H5 files (*.h5 *.mp *.mp.af);;All files (*)"
        )
        if fname:
            self.open(fname)

    def _onShowIndex(self, idx: QtCore.QModelIndex) -> None:
        self._showIndex(idx)

    def _onUpdateShowIndex(self) -> None:
        if self.treeView.selectionModel() is not None:
            self._showIndex(self.treeView.selectionModel().currentIndex())

    def open(self, fname: Union[str, bytes, os.PathLike]) -> None:
        self._h5file = h5py.File(fname)
        self._populateTreeView()

    def _populateTreeView(self) -> None:
        model = QtGui.QStandardItemModel()
        self._recursivePopulate(self._h5file, model.invisibleRootItem())
        self.treeView.setModel(model)
        self.treeView.selectionModel().currentChanged.connect(self._onShowIndex)

    def _recursivePopulate(
        self,
        group_or_dataset: Union[h5py.Group, h5py.Dataset],
        item: QtGui.QStandardItem,
    ) -> None:
        item.setData(group_or_dataset, QtCore.Qt.UserRole)
        if isinstance(group_or_dataset, h5py.Group):
            for name, sub_grp_or_ds in group_or_dataset.items():
                subitem = QtGui.QStandardItem(name)
                subitem.setFlags(subitem.flags() & ~QtCore.Qt.ItemIsEditable)
                self._recursivePopulate(sub_grp_or_ds, subitem)
                item.appendRow(subitem)
        elif isinstance(group_or_dataset, h5py.Dataset):
            pass
        else:
            raise RuntimeError()

    def _showIndex(self, idx: QtCore.QModelIndex) -> None:
        group_or_dataset = idx.data(QtCore.Qt.UserRole)
        self.pathLabel.setText(group_or_dataset.name)

        attrModel = QtGui.QStandardItemModel()
        for i, (name, value) in enumerate(group_or_dataset.attrs.items()):
            attrModel.setItem(i, 0, QtGui.QStandardItem(name))
            attrModel.setItem(i, 1, QtGui.QStandardItem(formatAsStr(value)))
        self.attrTableView.setModel(attrModel)
        self.attrTableView.resizeColumnsToContents()
        self.tabWidget.setTabText(1, f"Attributes ({len(group_or_dataset.attrs)})")

        viewWidget = None
        regionSpins = 0
        if isinstance(group_or_dataset, h5py.Group):
            self.typeLabel.setText("group")
            viewWidget = self.valueTableView
            model = QtGui.QStandardItemModel()
            for i, (name, value) in enumerate(group_or_dataset.items()):
                model.setItem(i, 0, QtGui.QStandardItem(name))
                model.setItem(i, 1, QtGui.QStandardItem(formatAsStr(value)))
            viewWidget.setModel(model)
            viewWidget.resizeColumnsToContents()

        elif isinstance(group_or_dataset, h5py.Dataset):
            self.typeLabel.setText(
                typeAndShapeAsStr(group_or_dataset.dtype, group_or_dataset.shape)
            )
            if group_or_dataset.shape == ():
                viewWidget = self.valueTextView
                viewWidget.setPlainText(formatAsStr(group_or_dataset))
            elif self.actionShow_Image.isChecked() and group_or_dataset.ndim >= 2:
                viewWidget = self.valueImageView
                self.valueImageView.setDataset(group_or_dataset)
                regionSpins = len(self.valueImageView.region())
            else:
                viewWidget = self.valueTableView
                viewWidget.setModel(DatasetModel(group_or_dataset))
                regionSpins = len(viewWidget.model().region())
                dtypeWidth = columnWidthFromDtype(viewWidget, group_or_dataset.dtype)
                for i in range(viewWidget.model().columnCount()):
                    viewWidget.setColumnWidth(
                        i, dtypeWidth or columnWidthRandomized(viewWidget, i)
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
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
            )
            label = QtWidgets.QLabel(f"Dim {len(self._regionSpins)}")
            label.setSizePolicy(sizePolicy)
            self.spinContainer.layout().insertWidget(len(self._regionSpins) * 2, label)

            spin = QtWidgets.QSpinBox(self)
            spin.setRange(0, group_or_dataset.shape[len(self._regionSpins)] - 1)
            spin.setSizePolicy(sizePolicy)
            spin.valueChanged.connect(self._onRegionChanged)
            self.spinContainer.layout().insertWidget(
                len(self._regionSpins) * 2 + 1, spin
            )
            self._regionSpins.append(spin)

        # Remember the spacer!
        self.spinContainer.setVisible(self.spinContainer.layout().count() != 1)
        self._setRegion()

    def _onRegionChanged(self) -> None:
        self._setRegion()

    def _setRegion(self) -> None:
        region = tuple(s.value() for s in self._regionSpins)
        if self._viewWidget is self.valueTableView and isinstance(
            self.valueTableView.model(), DatasetModel
        ):
            self.valueTableView.model().setRegion(region)
        elif self._viewWidget is self.valueImageView:
            self.valueImageView.setRegion(region)


if __name__ == "__main__":
    import sys

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    app = QtWidgets.QApplication(sys.argv)
    mw = H5ViewWindow(None)
    mw.show()
    if len(sys.argv) > 1:
        mw.open(sys.argv[1])
    app.exec_()

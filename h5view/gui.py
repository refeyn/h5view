import math
import random
from typing import Tuple, Any, Optional, List

import h5py
import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets

from h5view import utils


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
            return utils.formatAsStr(self._dataset[didx[: self._dataset.ndim]])


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
            self._cols, self._rows = dataset.shape[-2:]
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
        data: np.ndarray = self._dataset[self._region].astype(float)
        if self._autoscale:
            data -= data.min()
            data /= data.max()
        else:
            dtypeInfo = np.iinfo(self._dataset.dtype)
            data -= dtypeInfo.min
            data /= dtypeInfo.max
        data = (data * 255).copy(order="C").astype(np.uint8)
        assert data.shape == (self._cols, self._rows)
        return QtGui.QImage(
            data.tobytes(),
            self._rows,
            self._cols,
            self._rows,
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

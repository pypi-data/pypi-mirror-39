import logging

from PyQt5.QtCore import pyqtSignal, Qt
from .textlist import TextlistModel, TextlistView


logger = logging.getLogger(__name__)


class MyMusicItem(object):
    def __init__(self, name, on_click):
        self.name = name
        self.on_click = on_click


class MyMusicModel(TextlistModel):

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        item = self._items[row]
        if role == Qt.DisplayRole:
            return item.name
        return super().data(index, role)


class MyMusicView(TextlistView):

    def __init__(self, parent):
        super().__init__(parent)
        self.clicked.connect(
            lambda index: index.data(role=Qt.UserRole).on_click())

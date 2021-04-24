# This Python file uses the following encoding: utf-8
#
# Copyright 2021 LotrioLabs, <https://lotriolabs.github.io>.
#
# This file is part of Lotrio-QtPy, <https://github.com/lotriolabs/lotrio-qtpy>.
#
# Lotrio-QtPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Lotrio-QtPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Lotrio-QtPy.  If not, see <https://www.gnu.org/licenses/>.
#

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget


class PreferencesPageLotteries(QWidget):

    preferencesChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Title
        title = QLabel(self.tr("<strong style=\"font-size:large;\">{0}</strong>").format(self.title()))

        #
        # Content


        # Main layout
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(title)
        self._layout.addStretch(1)


    def setZeroMargins(self):

        self._layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr("Lotteries")


    def _onPreferencesChanged(self):

        self.preferencesChanged.emit()

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

from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QWidget

from preferences import Preferences


class Document(QWidget):

    _preferences = Preferences()

    documentClosed = Signal(str)


    def __init__(self, parent=None):
        super().__init__(parent)

        self._canonicalName = None

        self.setAttribute(Qt.WA_DeleteOnClose)


    def setPreferences(self, preferences):

        self._preferences = preferences


    def setCanonicalName(self, canonicalName):

        self._canonicalName = canonicalName


    def canonicalName(self):

        return self._canonicalName


    def load(self, canonicalName):

        self.setCanonicalName(canonicalName)

        return True


    def closeEvent(self, event):

        if True:
            # Document will be closed
            self.documentClosed.emit(self._canonicalName)

            event.accept()
        else:
            event.ignore()

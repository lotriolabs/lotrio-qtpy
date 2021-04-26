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

from PySide2.QtCore import QFileInfo, Qt, Signal
from PySide2.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from lottery_page_about import LotteryPageAbout
from preferences import Preferences


class Document(QWidget):

    aboutToClose = Signal(str)


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self._preferences = Preferences()
        self._canonicalName = None

        # Content
        self._tabBox = QTabWidget()
        self._tabBox.setTabPosition(QTabWidget.South)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self._tabBox)


    def setPreferences(self, preferences):

        self._preferences = preferences


    def setCanonicalName(self, canonicalName):

        self._canonicalName = canonicalName


    def canonicalName(self):

        return self._canonicalName


    def documentTitle(self):

        return self.windowTitle()


    def updateDocumentTitle(self):

        fileName = QFileInfo(self._canonicalName).fileName() if self._canonicalName else self.tr("Untitled")

        self.setWindowTitle(fileName)


    def setDocumentTabPosition(self, tabPosition):

        self._tabBox.setTabPosition(tabPosition)


    def documentTabPosition(self):

        return self._tabBox.tabPosition()


    def closeEvent(self, event):

        if True:
            # Document will be closed
            self.aboutToClose.emit(self._canonicalName)

            event.accept()
        else:
            event.ignore()


    def load(self, canonicalName):

        self.setCanonicalName(canonicalName)

        self._tabBox.setTabPosition(self._preferences.defaultTabPositionSheets())


        #
        # Pages

        pageAbout = LotteryPageAbout(self._canonicalName)

        self._tabBox.addTab(pageAbout, pageAbout.title())


        return True

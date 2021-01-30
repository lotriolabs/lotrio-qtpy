# This Python file uses the following encoding: utf-8
#
# Copyright 2021 LotrioLabs, <https://lotriolabs.github.io>.
#
# This file is part of Lotrio-QtPy.
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

from PySide2.QtCore import QByteArray, QSettings
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow

from settings import Settings

import resources


class MainWindow(QMainWindow):

    _settings = Settings()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon(':/icons/apps/512/lotrio.svg'))

        self.readSettings()


    def setApplicationState(self, state=QByteArray()):

        if state:
            self.restoreState(state)


    def applicationState(self):

        return self.saveState()


    def setApplicationGeometry(self, geometry=QByteArray()):

        if geometry:
            self.restoreGeometry(geometry)
        else:
            availableGeometry = self.screen().availableGeometry()
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)


    def applicationGeometry(self):

        return self.saveGeometry()


    def closeEvent(self, event):

        if True:
            self.writeSettings()
            event.accept()
        else:
            event.ignore()


    def readSettings(self):

        settings = QSettings()

        self._settings.load(settings)

        applicationState = settings.value('Application/State', QByteArray())
        applicationGeometry = settings.value('Application/Geometry', QByteArray())

        # Set application properties
        self.setApplicationState(applicationState)
        self.setApplicationGeometry(applicationGeometry)


    def writeSettings(self):

        settings = QSettings()

        self._settings.save(settings)

        settings.setValue('Application/State', self.applicationState())
        settings.setValue('Application/Geometry', self.applicationGeometry())

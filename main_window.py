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
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QMainWindow

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from preferences_dialog import PreferencesDialog
from settings import Settings

import lotrio_qtpy


class MainWindow(QMainWindow):

    _settings = Settings()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon(':/icons/apps/512/lotrio.svg'))

        self.createActions()
        self.createMenus()

        self.readSettings()


    def createActions(self):

        # Actions: Application
        self.actionAbout = QAction(self.tr(f'About {QApplication.applicationName()}'), self)
        self.actionAbout.setObjectName('actionAbout')
        self.actionAbout.setIcon(QIcon(':/icons/apps/512/lotrio.svg'))
        self.actionAbout.setIconText(self.tr('About'))
        self.actionAbout.setToolTip(self.tr('Brief description of the application'))
        self.actionAbout.triggered.connect(self.onActionAboutTriggered)

        self.actionColophon = QAction(self.tr('Colophon'), self)
        self.actionColophon.setObjectName('actionColophon')
        self.actionColophon.setToolTip(self.tr('Lengthy description of the application'))
        self.actionColophon.triggered.connect(self.onActionColophonTriggered)

        self.actionPreferences = QAction(self.tr('Preferences…'), self)
        self.actionPreferences.setObjectName('actionPreferences')
        self.actionPreferences.setIcon(QIcon.fromTheme('configure', QIcon(':/icons/actions/16/application-configure.svg')))
        self.actionPreferences.setIconText(self.tr('Preferences'))
        self.actionPreferences.setToolTip(self.tr('Customize the appearance and behavior of the application'))
        self.actionPreferences.triggered.connect(self.onActionPreferencesTriggered)

        self.actionQuit = QAction(self.tr('Quit'), self)
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.setIcon(QIcon.fromTheme('application-exit', QIcon(':/icons/actions/16/application-exit.svg')))
        self.actionQuit.setIconText(self.tr('Quit'))
        self.actionQuit.setShortcut(QKeySequence.Quit)
        self.actionQuit.setToolTip(self.tr(f'Quit the application [{self.actionQuit.shortcut().toString(QKeySequence.NativeText)}]'))
        self.actionQuit.triggered.connect(self.close)


    def createMenus(self):

        # Menu: Application
        menuApplication = self.menuBar().addMenu(self.tr('Application'))
        menuApplication.setObjectName('menuApplication')
        menuApplication.addAction(self.actionAbout)
        menuApplication.addAction(self.actionColophon)
        menuApplication.addSeparator()
        menuApplication.addAction(self.actionPreferences)
        menuApplication.addSeparator()
        menuApplication.addAction(self.actionQuit)

        # Menu: View
        menuView = self.menuBar().addMenu(self.tr('View'))
        menuView.setObjectName('menuView')


    def setApplicationState(self, state=QByteArray()):

        if not state.isEmpty():
            self.restoreState(state)


    def applicationState(self):

        return self.saveState()


    def setApplicationGeometry(self, geometry=QByteArray()):

        if not geometry.isEmpty():
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

        # Application properties
        state = settings.value('Application/State', QByteArray()) if self._settings.restoreApplicationState() else QByteArray()
        geometry = settings.value('Application/Geometry', QByteArray()) if self._settings.restoreApplicationState() else QByteArray()
        self.aboutDialogGeometry = settings.value('AboutDialog/Geometry', QByteArray())
        self.colophonDialogGeometry = settings.value('ColophonDialog/Geometry', QByteArray())
        self.preferencesDialogGeometry = settings.value('PreferencesDialog/Geometry', QByteArray())

        self.setApplicationState(state)
        self.setApplicationGeometry(geometry)


    def writeSettings(self):

        settings = QSettings()

        self._settings.save(settings)

        # Application properties
        state = self.applicationState() if self._settings.restoreApplicationState() else QByteArray()
        geometry = self.applicationGeometry() if self._settings.restoreApplicationGeometry() else QByteArray()

        settings.setValue('Application/State', state)
        settings.setValue('Application/Geometry', geometry)
        settings.setValue('AboutDialog/Geometry', self.aboutDialogGeometry)
        settings.setValue('ColophonDialog/Geometry', self.colophonDialogGeometry)
        settings.setValue('PreferencesDialog/Geometry', self.preferencesDialogGeometry)


    def onActionAboutTriggered(self):

        geometry = self.aboutDialogGeometry if self._settings.restoreDialogGeometry() else QByteArray()

        dialog = AboutDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()

        self.aboutDialogGeometry = dialog.dialogGeometry() if self._settings.restoreDialogGeometry() else QByteArray()


    def onActionColophonTriggered(self):

        geometry = self.colophonDialogGeometry if self._settings.restoreDialogGeometry() else QByteArray()

        dialog = ColophonDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()

        self.colophonDialogGeometry = dialog.dialogGeometry() if self._settings.restoreDialogGeometry() else QByteArray()


    def onActionPreferencesTriggered(self):

        geometry = self.preferencesDialogGeometry if self._settings.restoreDialogGeometry() else QByteArray()

        dialog = PreferencesDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.setSettings(self._settings)
        dialog.exec_()

        self._settings = dialog.settings()
        self.preferencesDialogGeometry = dialog.dialogGeometry() if self._settings.restoreDialogGeometry() else QByteArray()

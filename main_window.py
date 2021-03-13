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

from PySide2.QtCore import QByteArray, QSettings, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QMainWindow, QMdiArea

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from document import Document
from preferences import Preferences
from preferences_dialog import PreferencesDialog

import icons


class MainWindow(QMainWindow):

    _preferences = Preferences()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon(':/icons/apps/512/lotrio.svg'))

        self.readSettings()

        self.createLotteries()

        self.createActions()
        self.createMenus()
        self.createToolBars()

        # Application properties
        self.setApplicationState(self._applicationState)
        self.setApplicationGeometry(self._applicationGeometry)

        self.updateActionFullScreen()

        # Central widget
        self._documentArea = QMdiArea()
        self._documentArea.setViewMode(QMdiArea.TabbedView)
        self._documentArea.setTabsMovable(True)
        self._documentArea.setTabsClosable(True)
        self.setCentralWidget(self._documentArea)
        self._documentArea.subWindowActivated.connect(self.onDocumentActivated)


    def setApplicationState(self, state=QByteArray()):

        if not state.isEmpty():
            self.restoreState(state)
        else:
            self.toolbarApplication.setVisible(True)
            self.toolbarLotteries.setVisible(True)
            self.toolbarView.setVisible(False)
            self.toolbarHelp.setVisible(False)


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
            self._applicationState = self.applicationState() if self._preferences.restoreApplicationState() else QByteArray()
            self._applicationGeometry = self.applicationGeometry() if self._preferences.restoreApplicationGeometry() else QByteArray()

            self.writeSettings()
            event.accept()
        else:
            event.ignore()


    def readSettings(self):

        settings = QSettings()

        self._preferences.load(settings)

        # Application properties
        self._applicationState = settings.value('Application/State', QByteArray()) if self._preferences.restoreApplicationState() else QByteArray()
        self._applicationGeometry = settings.value('Application/Geometry', QByteArray()) if self._preferences.restoreApplicationGeometry() else QByteArray()
        self.aboutDialogGeometry = settings.value('AboutDialog/Geometry', QByteArray())
        self.colophonDialogGeometry = settings.value('ColophonDialog/Geometry', QByteArray())
        self.preferencesDialogGeometry = settings.value('PreferencesDialog/Geometry', QByteArray())


    def writeSettings(self):

        settings = QSettings()

        self._preferences.save(settings)

        # Application properties
        settings.setValue('Application/State', self._applicationState)
        settings.setValue('Application/Geometry', self._applicationGeometry)
        settings.setValue('AboutDialog/Geometry', self.aboutDialogGeometry)
        settings.setValue('ColophonDialog/Geometry', self.colophonDialogGeometry)
        settings.setValue('PreferencesDialog/Geometry', self.preferencesDialogGeometry)


    def createLotteries(self):

        self.listLotteries = {
            'eurojackpot': ['euEurojackpot', self.tr('Eurojackpot'), self.tr('Eurojackpot is a transnational European lottery')],
            'euromillions': ['euEuroMillions', self.tr('EuroMillions'), self.tr('EuroMillions is a transnational European lottery')],
            'vikinglotto': ['euVikinglotto', self.tr('Vikinglotto'), self.tr('Vikinglotto is a transnational European lottery')],
        }


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

        # Actions: Lotteries
        self.actionLotteries = []
        for key, value in sorted(self.listLotteries.items()):

            lottery = QAction(value[1], self)
            lottery.setObjectName(f'actionLottery_{value[0]}')
            lottery.setIconText(value[1])
            lottery.setCheckable(True)
            lottery.setToolTip(value[2])
            lottery.setData(key)
            lottery.toggled.connect(lambda checked, lottery=key: self.onActionLotteriesToggled(lottery, checked))

            self.actionLotteries.append(lottery)

        # Actions: View
        self.actionFullScreen = QAction(self)
        self.actionFullScreen.setObjectName('actionFullScreen')
        self.actionFullScreen.setIconText(self.tr('Full Screen'))
        self.actionFullScreen.setCheckable(True)
        self.actionFullScreen.setShortcuts([QKeySequence(Qt.Key_F11), QKeySequence.FullScreen])
        self.actionFullScreen.triggered.connect(self.onActionFullScreenTriggered)

        self.actionToolbarApplication = QAction(self.tr('Show Application Toolbar'), self)
        self.actionToolbarApplication.setObjectName('actionToolbarApplication')
        self.actionToolbarApplication.setCheckable(True)
        self.actionToolbarApplication.setToolTip(self.tr('Display the Application toolbar'))
        self.actionToolbarApplication.toggled.connect(lambda checked: self.toolbarApplication.setVisible(checked))

        self.actionToolbarLotteries = QAction(self.tr('Show Lotteries Toolbar'), self)
        self.actionToolbarLotteries.setObjectName('actionToolbarLotteries')
        self.actionToolbarLotteries.setCheckable(True)
        self.actionToolbarLotteries.setToolTip(self.tr('Display the Lotteries toolbar'))
        self.actionToolbarLotteries.toggled.connect(lambda checked: self.toolbarLotteries.setVisible(checked))

        self.actionToolbarView = QAction(self.tr('Show View Toolbar'), self)
        self.actionToolbarView.setObjectName('actionToolbarView')
        self.actionToolbarView.setCheckable(True)
        self.actionToolbarView.setToolTip(self.tr('Display the View toolbar'))
        self.actionToolbarView.toggled.connect(lambda checked: self.toolbarView.setVisible(checked))

        self.actionToolbarHelp = QAction(self.tr('Show Help Toolbar'), self)
        self.actionToolbarHelp.setObjectName('actionToolbarHelp')
        self.actionToolbarHelp.setCheckable(True)
        self.actionToolbarHelp.setToolTip(self.tr('Display the Help toolbar'))
        self.actionToolbarHelp.toggled.connect(lambda checked: self.toolbarHelp.setVisible(checked))


    def updateActionFullScreen(self):

        if not self.isFullScreen():
            self.actionFullScreen.setText(self.tr('Full Screen Mode'))
            self.actionFullScreen.setIcon(QIcon.fromTheme('view-fullscreen', QIcon(':/icons/actions/16/view-fullscreen.svg')))
            self.actionFullScreen.setChecked(False)
            self.actionFullScreen.setToolTip(self.tr(f'Display the window in full screen [{self.actionFullScreen.shortcut().toString(QKeySequence.NativeText)}]'))
        else:
            self.actionFullScreen.setText(self.tr('Exit Full Screen Mode'))
            self.actionFullScreen.setIcon(QIcon.fromTheme('view-restore', QIcon(':/icons/actions/16/view-restore.svg')))
            self.actionFullScreen.setChecked(True)
            self.actionFullScreen.setToolTip(self.tr(f'Exit the full screen mode [{self.actionFullScreen.shortcut().toString(QKeySequence.NativeText)}]'))


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

        # Menu: Lotteries
        menuLotteries = self.menuBar().addMenu(self.tr('Lotteries'))
        menuLotteries.setObjectName('menuLotteries')
        menuLotteries.addActions(self.actionLotteries)

        # Menu: View
        menuView = self.menuBar().addMenu(self.tr('View'))
        menuView.setObjectName('menuView')
        menuView.addAction(self.actionFullScreen)
        menuView.addSeparator()
        menuView.addAction(self.actionToolbarApplication)
        menuView.addAction(self.actionToolbarLotteries)
        menuView.addAction(self.actionToolbarView)
        menuView.addAction(self.actionToolbarHelp)

        # Menu: Help
        menuHelp = self.menuBar().addMenu(self.tr('Help'))
        menuHelp.setObjectName('menuHelp')


    def createToolBars(self):

        # Toolbar: Application
        self.toolbarApplication = self.addToolBar(self.tr('Application Toolbar'))
        self.toolbarApplication.setObjectName('toolbarApplication')
        self.toolbarApplication.addAction(self.actionAbout)
        self.toolbarApplication.addAction(self.actionPreferences)
        self.toolbarApplication.addSeparator()
        self.toolbarApplication.addAction(self.actionQuit)
        self.toolbarApplication.visibilityChanged.connect(lambda visible: self.actionToolbarApplication.setChecked(visible))

        # Toolbar: Lotteries
        self.toolbarLotteries = self.addToolBar(self.tr('Lotteries Toolbar'))
        self.toolbarLotteries.setObjectName('toolbarLotteries')
        self.toolbarLotteries.addActions(self.actionLotteries)
        self.toolbarLotteries.visibilityChanged.connect(lambda visible: self.actionToolbarLotteries.setChecked(visible))

        # Toolbar: View
        self.toolbarView = self.addToolBar(self.tr('View Toolbar'))
        self.toolbarView.setObjectName('toolbarView')
        self.toolbarView.addAction(self.actionFullScreen)
        self.toolbarView.visibilityChanged.connect(lambda visible: self.actionToolbarView.setChecked(visible))

        # Toolbar: Help
        self.toolbarHelp = self.addToolBar(self.tr('Help Toolbar'))
        self.toolbarHelp.setObjectName('toolbarHelp')
        self.toolbarHelp.visibilityChanged.connect(lambda visible: self.actionToolbarHelp.setChecked(visible))


    def onActionAboutTriggered(self):

        geometry = self.aboutDialogGeometry if self._preferences.restoreDialogGeometry() else QByteArray()

        dialog = AboutDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()

        self.aboutDialogGeometry = dialog.dialogGeometry() if self._preferences.restoreDialogGeometry() else QByteArray()


    def onActionColophonTriggered(self):

        geometry = self.colophonDialogGeometry if self._preferences.restoreDialogGeometry() else QByteArray()

        dialog = ColophonDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()

        self.colophonDialogGeometry = dialog.dialogGeometry() if self._preferences.restoreDialogGeometry() else QByteArray()


    def onActionPreferencesTriggered(self):

        geometry = self.preferencesDialogGeometry if self._preferences.restoreDialogGeometry() else QByteArray()

        dialog = PreferencesDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.setPreferences(self._preferences)
        dialog.exec_()

        self._preferences = dialog.preferences()
        self.preferencesDialogGeometry = dialog.dialogGeometry() if self._preferences.restoreDialogGeometry() else QByteArray()


    def onActionLotteriesToggled(self, lottery, checked):

        if checked:
            self.openDocument(lottery)
        else:
            self.closeDocument(lottery)


    def onActionFullScreenTriggered(self):

        if not self.isFullScreen():
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self.updateActionFullScreen()


    def onDocumentActivated(self):
        pass


    def onDocumentAboutToClose(self, canonicalName):

        for actionLottery in self.actionLotteries:
            if actionLottery.objectName() == f"actionLottery_{self.listLotteries[canonicalName][0]}":
                actionLottery.setChecked(False)
                return


    def createDocument(self):

        document = Document(self)
        document.setPreferences(self._preferences)
        document.aboutToClose.connect(self.onDocumentAboutToClose)

        self._documentArea.addSubWindow(document)

        return document


    def findDocument(self, documentName):

        for window in self._documentArea.subWindowList():
            if window.widget().canonicalName() == documentName:
                return window

        return None


    def openDocument(self, documentName):

        # Checks whether the given document is already open.
        window = self.findDocument(documentName)
        if window:
            self._documentArea.setActiveSubWindow(window)
            return True

        return self.loadDocument(documentName)


    def loadDocument(self, documentName):

        document = self.createDocument()

        succeeded = document.load(documentName)
        if succeeded:
            document.updateDocumentTitle()
            document.show()
        else:
            document.close()

        return succeeded


    def closeDocument(self, documentName):

        succeeded = False

        window = self.findDocument(documentName)
        if window:
            succeeded = window.close()

        return succeeded

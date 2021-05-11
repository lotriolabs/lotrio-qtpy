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
from PySide2.QtWidgets import QAction, QActionGroup, QApplication, QMainWindow, QMdiArea, QMenu, QStatusBar, QTabWidget

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from document import Document
from keyboard_shortcuts_dialog import KeyboardShortcutsDialog
from preferences import Preferences
from preferences_dialog import PreferencesDialog

import icons_rc


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon(":/icons/apps/512/lotrio.svg"))

        self._keyboardShortcutsDialog = None

        self._preferences = Preferences()
        self._preferences.loadSettings()

        self._createLotteries()

        self._createActions()
        self._createMenus()
        self._createToolBars()
        self._createStatusBar()

        self._loadSettings()

        self._updateActionFullScreen()
        self._updateActionTabbarLotteriesPosition()
        self._updateActionTabbarSheetsPosition(self._preferences.defaultTabbarSheetsPosition())

        self._enableUiElements()

        # Central widget
        self._documentArea = QMdiArea()
        self._documentArea.setViewMode(QMdiArea.TabbedView)
        self._documentArea.setTabsMovable(True)
        self._documentArea.setTabsClosable(True)
        self._documentArea.setTabPosition(self._preferences.defaultTabbarLotteriesPosition())
        self.setCentralWidget(self._documentArea)
        self._documentArea.subWindowActivated.connect(self._onDocumentWindowActivated)


    def closeEvent(self, event):

        if True:
            # Store application properties and preferences
            self._saveSettings()
            self._preferences.saveSettings()

            event.accept()
        else:
            event.ignore()


    def _loadSettings(self):

        settings = QSettings()

        # Application properties: Geometry
        geometry = settings.value("Application/Geometry", QByteArray()) if self._preferences.restoreApplicationGeometry() else QByteArray()
        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            availableGeometry = self.screen().availableGeometry()
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)

        # Application properties: State
        state = settings.value("Application/State", QByteArray()) if self._preferences.restoreApplicationState() else QByteArray()
        if not state.isEmpty():
            self.restoreState(state)
        else:
            self._toolbarApplication.setVisible(True)
            self._toolbarLotteries.setVisible(True)
            self._toolbarTools.setVisible(True)
            self._toolbarView.setVisible(False)
            self._toolbarHelp.setVisible(False)


    def _saveSettings(self):

        settings = QSettings()

        # Application properties: Geometry
        geometry = self.saveGeometry() if self._preferences.restoreApplicationGeometry() else QByteArray()
        settings.setValue("Application/Geometry", geometry)

        # Application properties: State
        state = self.saveState() if self._preferences.restoreApplicationState() else QByteArray()
        settings.setValue("Application/State", state)


    def _createLotteries(self):

        self._listLotteries = {
            "eurojackpot": ["euEurojackpot", self.tr("Eurojackpot"), self.tr("Eurojackpot is a transnational European lottery")],
            "euromillions": ["euEuroMillions", self.tr("EuroMillions"), self.tr("EuroMillions is a transnational European lottery")],
            "vikinglotto": ["euVikinglotto", self.tr("Vikinglotto"), self.tr("Vikinglotto is a transnational European lottery")],
        }


    def _createActions(self):

        #
        # Actions: Application

        self._actionAbout = QAction(self.tr("About {0}").format(QApplication.applicationName()), self)
        self._actionAbout.setObjectName("actionAbout")
        self._actionAbout.setIcon(QIcon(":/icons/apps/512/lotrio.svg"))
        self._actionAbout.setIconText(self.tr("About"))
        self._actionAbout.setToolTip(self.tr("Brief description of the application"))
        self._actionAbout.triggered.connect(self._onActionAboutTriggered)

        self._actionColophon = QAction(self.tr("Colophon"), self)
        self._actionColophon.setObjectName("actionColophon")
        self._actionColophon.setToolTip(self.tr("Lengthy description of the application"))
        self._actionColophon.triggered.connect(self._onActionColophonTriggered)

        self._actionPreferences = QAction(self.tr("Preferences…"), self)
        self._actionPreferences.setObjectName("actionPreferences")
        self._actionPreferences.setIcon(QIcon.fromTheme("configure", QIcon(":/icons/actions/16/application-configure.svg")))
        self._actionPreferences.setToolTip(self.tr("Customize the appearance and behavior of the application"))
        self._actionPreferences.triggered.connect(self._onActionPreferencesTriggered)

        self._actionQuit = QAction(self.tr("Quit"), self)
        self._actionQuit.setObjectName("actionQuit")
        self._actionQuit.setIcon(QIcon.fromTheme("application-exit", QIcon(":/icons/actions/16/application-exit.svg")))
        self._actionQuit.setShortcut(QKeySequence.Quit)
        self._actionQuit.setToolTip(self.tr("Quit the application"))
        self._actionQuit.triggered.connect(self.close)


        #
        # Actions: Lotteries

        self._actionLotteries = []
        for key, value in sorted(self._listLotteries.items()):

            actionLottery = QAction(value[1], self)
            actionLottery.setObjectName(f"actionLottery_{value[0]}")
            actionLottery.setIconText(value[1])
            actionLottery.setCheckable(True)
            actionLottery.setToolTip(value[2])
            actionLottery.setData(f"{key}/{value[1]}")
            actionLottery.toggled.connect(lambda checked, lottery=actionLottery.data(): self._onActionLotteriesToggled(checked, lottery))

            self._actionLotteries.append(actionLottery)

        self._actionClose = QAction(self.tr("Close"), self)
        self._actionClose.setObjectName("actionClose")
        self._actionClose.setIcon(QIcon.fromTheme("document-close", QIcon(":/icons/actions/16/document-close.svg")))
        self._actionClose.setShortcut(QKeySequence.Close)
        self._actionClose.setToolTip(self.tr("Close lottery"))
        self._actionClose.triggered.connect(self._onActionCloseTriggered)

        self._actionCloseOther = QAction(self.tr("Close Other"), self)
        self._actionCloseOther.setObjectName("actionCloseOther")
        self._actionCloseOther.setToolTip(self.tr("Close all other lotteries"))
        self._actionCloseOther.triggered.connect(self._onActionCloseOtherTriggered)

        self._actionCloseAll = QAction(self.tr("Close All"), self)
        self._actionCloseAll.setObjectName("actionCloseAll")
        self._actionCloseAll.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_W))
        self._actionCloseAll.setToolTip(self.tr("Close all lotteries"))
        self._actionCloseAll.triggered.connect(self._onActionCloseAllTriggered)


        #
        # Actions: View

        self._actionFullScreen = QAction(self)
        self._actionFullScreen.setObjectName("actionFullScreen")
        self._actionFullScreen.setIconText(self.tr("Full Screen"))
        self._actionFullScreen.setCheckable(True)
        self._actionFullScreen.setShortcuts([QKeySequence(Qt.Key_F11), QKeySequence.FullScreen])
        self._actionFullScreen.triggered.connect(self._onActionFullScreenTriggered)

        actionTabbarLotteriesPositionTop = QAction(self.tr("Top"), self)
        actionTabbarLotteriesPositionTop.setObjectName("actionTabbarLotteriesPositionTop")
        actionTabbarLotteriesPositionTop.setCheckable(True)
        actionTabbarLotteriesPositionTop.setToolTip(self.tr("The lottery tabs are displayed above the pages"))
        actionTabbarLotteriesPositionTop.setData(QTabWidget.North)

        actionTabbarLotteriesPositionBottom = QAction(self.tr("Bottom"), self)
        actionTabbarLotteriesPositionBottom.setObjectName("actionTabbarLotteriesPositionBottom")
        actionTabbarLotteriesPositionBottom.setCheckable(True)
        actionTabbarLotteriesPositionBottom.setToolTip(self.tr("The lottery tabs are displayed below the pages"))
        actionTabbarLotteriesPositionBottom.setData(QTabWidget.South)

        self._actionTabbarLotteriesPosition = QActionGroup(self)
        self._actionTabbarLotteriesPosition.setObjectName("actionTabbarLotteriesPosition")
        self._actionTabbarLotteriesPosition.addAction(actionTabbarLotteriesPositionTop)
        self._actionTabbarLotteriesPosition.addAction(actionTabbarLotteriesPositionBottom)
        self._actionTabbarLotteriesPosition.triggered.connect(self._onActionTabbarLotteriesPositionTriggered)

        actionTabbarSheetsPositionTop = QAction(self.tr("Top"), self)
        actionTabbarSheetsPositionTop.setObjectName("actionTabbarSheetsPositionTop")
        actionTabbarSheetsPositionTop.setCheckable(True)
        actionTabbarSheetsPositionTop.setToolTip(self.tr("The sheet tabs are displayed above the pages"))
        actionTabbarSheetsPositionTop.setData(QTabWidget.North)

        actionTabbarSheetsPositionBottom = QAction(self.tr("Bottom"), self)
        actionTabbarSheetsPositionBottom.setObjectName("actionTabbarSheetsPositionBottom")
        actionTabbarSheetsPositionBottom.setCheckable(True)
        actionTabbarSheetsPositionBottom.setToolTip(self.tr("The sheet tabs are displayed below the pages"))
        actionTabbarSheetsPositionBottom.setData(QTabWidget.South)

        self._actionTabbarSheetsPosition = QActionGroup(self)
        self._actionTabbarSheetsPosition.setObjectName("actionTabbarSheetsPosition")
        self._actionTabbarSheetsPosition.addAction(actionTabbarSheetsPositionTop)
        self._actionTabbarSheetsPosition.addAction(actionTabbarSheetsPositionBottom)
        self._actionTabbarSheetsPosition.triggered.connect(self._onActionTabbarSheetsPositionTriggered)

        self._actionToolbarApplication = QAction(self.tr("Show Application Toolbar"), self)
        self._actionToolbarApplication.setObjectName("actionToolbarApplication")
        self._actionToolbarApplication.setCheckable(True)
        self._actionToolbarApplication.setToolTip(self.tr("Display the Application toolbar"))
        self._actionToolbarApplication.toggled.connect(lambda checked: self._toolbarApplication.setVisible(checked))

        self._actionToolbarLotteries = QAction(self.tr("Show Lotteries Toolbar"), self)
        self._actionToolbarLotteries.setObjectName("actionToolbarLotteries")
        self._actionToolbarLotteries.setCheckable(True)
        self._actionToolbarLotteries.setToolTip(self.tr("Display the Lotteries toolbar"))
        self._actionToolbarLotteries.toggled.connect(lambda checked: self._toolbarLotteries.setVisible(checked))

        self._actionToolbarTools = QAction(self.tr("Show Tools Toolbar"), self)
        self._actionToolbarTools.setObjectName("actionToolbarTools")
        self._actionToolbarTools.setCheckable(True)
        self._actionToolbarTools.setToolTip(self.tr("Display the Tools toolbar"))
        self._actionToolbarTools.toggled.connect(lambda checked: self._toolbarTools.setVisible(checked))

        self._actionToolbarView = QAction(self.tr("Show View Toolbar"), self)
        self._actionToolbarView.setObjectName("actionToolbarView")
        self._actionToolbarView.setCheckable(True)
        self._actionToolbarView.setToolTip(self.tr("Display the View toolbar"))
        self._actionToolbarView.toggled.connect(lambda checked: self._toolbarView.setVisible(checked))

        self._actionToolbarHelp = QAction(self.tr("Show Help Toolbar"), self)
        self._actionToolbarHelp.setObjectName("actionToolbarHelp")
        self._actionToolbarHelp.setCheckable(True)
        self._actionToolbarHelp.setToolTip(self.tr("Display the Help toolbar"))
        self._actionToolbarHelp.toggled.connect(lambda checked: self._toolbarHelp.setVisible(checked))

        self._actionStatusbar = QAction(self.tr("Show Statusbar"), self)
        self._actionStatusbar.setObjectName("actionStatusbar")
        self._actionStatusbar.setCheckable(True)
        self._actionStatusbar.setChecked(True)
        self._actionStatusbar.setToolTip(self.tr("Display the statusbar"))
        self._actionStatusbar.toggled.connect(lambda checked: self._statusbar.setVisible(checked))


        #
        # Actions: Help

        self._actionKeyboardShortcuts = QAction(self.tr("Keyboard Shortcuts"), self)
        self._actionKeyboardShortcuts.setObjectName("actionKeyboardShortcuts")
        self._actionKeyboardShortcuts.setIcon(QIcon.fromTheme("help-keyboard-shortcuts", QIcon(":/icons/actions/16/help-keyboard-shortcuts.svg")))
        self._actionKeyboardShortcuts.setIconText(self.tr("Shortcuts"))
        self._actionKeyboardShortcuts.setToolTip(self.tr("List of all keyboard shortcuts"))
        self._actionKeyboardShortcuts.triggered.connect(self._onActionKeyboardShortcutsTriggered)


    def _createMenus(self):

        # Menu: Application
        menuApplication = self.menuBar().addMenu(self.tr("Application"))
        menuApplication.setObjectName("menuApplication")
        menuApplication.addAction(self._actionAbout)
        menuApplication.addAction(self._actionColophon)
        menuApplication.addSeparator()
        menuApplication.addAction(self._actionPreferences)
        menuApplication.addSeparator()
        menuApplication.addAction(self._actionQuit)

        # Menu: Lotteries
        menuLotteries = self.menuBar().addMenu(self.tr("Lotteries"))
        menuLotteries.setObjectName("menuLotteries")
        menuLotteries.addActions(self._actionLotteries)
        menuLotteries.addSeparator()
        menuLotteries.addAction(self._actionClose)
        menuLotteries.addAction(self._actionCloseOther)
        menuLotteries.addAction(self._actionCloseAll)

        # Menu: Tools
        menuTools = self.menuBar().addMenu(self.tr("Tools"))
        menuTools.setObjectName("menuTools")


        #
        # Menu: View

        menuLotteryTabs = QMenu(self.tr("Show Lottery Tabs…"), self)
        menuLotteryTabs.setObjectName("menuLotteryTabs")
        menuLotteryTabs.addActions(self._actionTabbarLotteriesPosition.actions())

        self._menuSheetTabs = QMenu(self.tr("Show Sheet Tabs…"), self)
        self._menuSheetTabs.setObjectName("menuSheetTabs")
        self._menuSheetTabs.addActions(self._actionTabbarSheetsPosition.actions())

        menuView = self.menuBar().addMenu(self.tr("View"))
        menuView.setObjectName("menuView")
        menuView.addAction(self._actionFullScreen)
        menuView.addSeparator()
        menuView.addMenu(menuLotteryTabs)
        menuView.addMenu(self._menuSheetTabs)
        menuView.addSeparator()
        menuView.addAction(self._actionToolbarApplication)
        menuView.addAction(self._actionToolbarLotteries)
        menuView.addAction(self._actionToolbarTools)
        menuView.addAction(self._actionToolbarView)
        menuView.addAction(self._actionToolbarHelp)
        menuView.addSeparator()
        menuView.addAction(self._actionStatusbar)


        # Menu: Help
        menuHelp = self.menuBar().addMenu(self.tr("Help"))
        menuHelp.setObjectName("menuHelp")
        menuHelp.addAction(self._actionKeyboardShortcuts)


    def _createToolBars(self):

        # Toolbar: Application
        self._toolbarApplication = self.addToolBar(self.tr("Application Toolbar"))
        self._toolbarApplication.setObjectName("toolbarApplication")
        self._toolbarApplication.addAction(self._actionAbout)
        self._toolbarApplication.addAction(self._actionPreferences)
        self._toolbarApplication.addSeparator()
        self._toolbarApplication.addAction(self._actionQuit)
        self._toolbarApplication.visibilityChanged.connect(lambda visible: self._actionToolbarApplication.setChecked(visible))

        # Toolbar: Lotteries
        self._toolbarLotteries = self.addToolBar(self.tr("Lotteries Toolbar"))
        self._toolbarLotteries.setObjectName("toolbarLotteries")
        self._toolbarLotteries.addActions(self._actionLotteries)
        self._toolbarLotteries.visibilityChanged.connect(lambda visible: self._actionToolbarLotteries.setChecked(visible))

        # Toolbar: Tools
        self._toolbarTools = self.addToolBar(self.tr("Tools Toolbar"))
        self._toolbarTools.setObjectName("toolbarTools")
        self._toolbarTools.visibilityChanged.connect(lambda visible: self._actionToolbarTools.setChecked(visible))

        # Toolbar: View
        self._toolbarView = self.addToolBar(self.tr("View Toolbar"))
        self._toolbarView.setObjectName("toolbarView")
        self._toolbarView.addAction(self._actionFullScreen)
        self._toolbarView.visibilityChanged.connect(lambda visible: self._actionToolbarView.setChecked(visible))

        # Toolbar: Help
        self._toolbarHelp = self.addToolBar(self.tr("Help Toolbar"))
        self._toolbarHelp.setObjectName("toolbarHelp")
        self._toolbarHelp.addAction(self._actionKeyboardShortcuts)
        self._toolbarHelp.visibilityChanged.connect(lambda visible: self._actionToolbarHelp.setChecked(visible))


    def _createStatusBar(self):

        self._statusbar = self.statusBar()


    def _updateActionFullScreen(self):

        if not self.isFullScreen():
            self._actionFullScreen.setText(self.tr("Full Screen Mode"))
            self._actionFullScreen.setIcon(QIcon.fromTheme("view-fullscreen", QIcon(":/icons/actions/16/view-fullscreen.svg")))
            self._actionFullScreen.setChecked(False)
            self._actionFullScreen.setToolTip(self.tr("Display the window in full screen"))
        else:
            self._actionFullScreen.setText(self.tr("Exit Full Screen Mode"))
            self._actionFullScreen.setIcon(QIcon.fromTheme("view-restore", QIcon(":/icons/actions/16/view-restore.svg")))
            self._actionFullScreen.setChecked(True)
            self._actionFullScreen.setToolTip(self.tr("Exit the full screen mode"))


    def _updateActionTabbarLotteriesPosition(self):

        for action in self._actionTabbarLotteriesPosition.actions():
            if action.data() == self._preferences.defaultTabbarLotteriesPosition():
                action.setChecked(True)
                break


    def _updateActionTabbarSheetsPosition(self, tabPosition):

        for action in self._actionTabbarSheetsPosition.actions():
            if action.data() == tabPosition:
                action.setChecked(True)
                break


    def _updateTitleBar(self):

        title = None

        document = self._activeDocument()
        if document:
            title = document.documentTitle()

        self.setWindowTitle(title)


    def _enableUiElements(self, subWindowCount=0):

        hasDocument = subWindowCount >= 1
        hasDocuments = subWindowCount >= 2

        # Actions: Lotteries
        self._actionClose.setEnabled(hasDocument)
        self._actionCloseOther.setEnabled(hasDocuments)
        self._actionCloseAll.setEnabled(hasDocument)

        # Menu: View
        self._menuSheetTabs.setEnabled(hasDocument)


    def _onActionAboutTriggered(self):

        dialog = AboutDialog(self)
        dialog.exec_()


    def _onActionColophonTriggered(self):

        dialog = ColophonDialog(self)
        dialog.exec_()


    def _onActionPreferencesTriggered(self):

        dialog = PreferencesDialog(self)
        dialog.setPreferences(self._preferences)
        dialog.exec_()

        self._preferences = dialog.preferences()


    def _onActionLotteriesToggled(self, checked, lottery):

        if checked:
            self._openDocument(lottery)
        else:
            self._closeDocument(lottery)


    def _onActionCloseTriggered(self):

        self._documentArea.closeActiveSubWindow()


    def _onActionCloseOtherTriggered(self):

        for subWindow in self._documentArea.subWindowList():
            if subWindow != self._documentArea.activeSubWindow():
                subWindow.close()


    def _onActionCloseAllTriggered(self):

        self._documentArea.closeAllSubWindows()


    def _onActionFullScreenTriggered(self):

        if not self.isFullScreen():
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self._updateActionFullScreen()


    def _onActionTabbarLotteriesPositionTriggered(self, actionTabbarLotteriesPosition):

        tabPosition = QTabWidget.TabPosition(actionTabbarLotteriesPosition.data())

        self._documentArea.setTabPosition(tabPosition)


    def _onActionTabbarSheetsPositionTriggered(self, actionTabbarSheetsPosition):

        tabPosition = QTabWidget.TabPosition(actionTabbarSheetsPosition.data())

        document = self._activeDocument()
        if document:
            document.setDocumentTabPosition(tabPosition)


    def _onActionKeyboardShortcutsTriggered(self):

        if not self._keyboardShortcutsDialog:
            self._keyboardShortcutsDialog = KeyboardShortcutsDialog(self)

        self._keyboardShortcutsDialog.show()
        self._keyboardShortcutsDialog.raise_()
        self._keyboardShortcutsDialog.activateWindow()


    def _onDocumentWindowActivated(self, subWindow):

        # Update application window and UI elements
        self._updateTitleBar()
        self._enableUiElements(len(self._documentArea.subWindowList()))

        if not subWindow:
            return

        document = subWindow.widget()

        self._updateActionTabbarSheetsPosition(document.documentTabPosition())


    def _onDocumentAboutToClose(self, canonicalName):

        # Workaround to show subwindows always maximized
        for subWindow in self._documentArea.subWindowList():
            if not subWindow.isMaximized():
                subWindow.showMaximized()

        # Update UI elements without the emitter
        self._enableUiElements(len(self._documentArea.subWindowList()) - 1)

        # Disable the Lottery action
        for actionLottery in self._actionLotteries:
            if actionLottery.data() == canonicalName:
                actionLottery.setChecked(False)
                return


    def _createDocument(self):

        document = Document()
        document.setPreferences(self._preferences)
        document.aboutToClose.connect(self._onDocumentAboutToClose)

        subWindow = self._documentArea.addSubWindow(document)
        subWindow.setWindowIcon(QIcon())
        subWindow.showMaximized()

        return document


    def _findDocumentWindow(self, canonicalName):

        for subWindow in self._documentArea.subWindowList():
            if subWindow.widget().canonicalName() == canonicalName:
                return subWindow

        return None


    def _activeDocument(self):

        subWindow = self._documentArea.activeSubWindow()

        return subWindow.widget() if subWindow else None


    def _openDocument(self, canonicalName):

        subWindow = self._findDocumentWindow(canonicalName)
        if subWindow:
            # Given document is already loaded; activate the subwindow
            self._documentArea.setActiveSubWindow(subWindow)
            return True

        return self._loadDocument(canonicalName)


    def _loadDocument(self, canonicalName):

        document = self._createDocument()

        succeeded = document.load(canonicalName)
        if succeeded:
            document.updateDocumentTitle()
            document.show()

            # Update the application window
            self._updateActionTabbarSheetsPosition(document.documentTabPosition())
            self._updateTitleBar()
        else:
            document.close()

        return succeeded


    def _closeDocument(self, canonicalName):

        succeeded = False

        subWindow = self._findDocumentWindow(canonicalName)
        if subWindow:
            succeeded = subWindow.close()

        return succeeded

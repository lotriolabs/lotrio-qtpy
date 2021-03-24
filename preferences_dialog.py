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

from PySide2.QtCore import QByteArray
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout

from preferences import Preferences
from preferences_draws_page import PreferencesDrawsPage
from preferences_general_page import PreferencesGeneralPage
from preferences_lotteries_page import PreferencesLotteriesPage
from preferences_plays_page import PreferencesPlaysPage


class PreferencesDialog(QDialog):

    _preferences = Preferences()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr('Preferences'))

        self.resize(800, 600)

        # Preferences box
        self.generalPage = PreferencesGeneralPage(self)
        self.generalPage.setZeroMargins()
        self.generalPage.preferencesChanged.connect(self.onPreferencesChanged)

        self.lotteriesPage = PreferencesLotteriesPage(self)
        self.lotteriesPage.setZeroMargins()
        self.lotteriesPage.preferencesChanged.connect(self.onPreferencesChanged)

        self.drawsPage = PreferencesDrawsPage(self)
        self.drawsPage.setZeroMargins()
        self.drawsPage.preferencesChanged.connect(self.onPreferencesChanged)

        self.playsPage = PreferencesPlaysPage(self)
        self.playsPage.setZeroMargins()
        self.playsPage.preferencesChanged.connect(self.onPreferencesChanged)

        stackedBox = QStackedWidget()
        stackedBox.addWidget(self.generalPage)
        stackedBox.addWidget(self.lotteriesPage)
        stackedBox.addWidget(self.drawsPage)
        stackedBox.addWidget(self.playsPage)
        stackedBox.setCurrentIndex(0)

        listBox = QListWidget()
        listBox.addItem(self.generalPage.title())
        listBox.addItem(self.lotteriesPage.title())
        listBox.addItem(self.drawsPage.title())
        listBox.addItem(self.playsPage.title())
        listBox.setCurrentRow(stackedBox.currentIndex())
        listBox.currentRowChanged.connect(stackedBox.setCurrentIndex)

        preferencesBox = QHBoxLayout()
        preferencesBox.addWidget(listBox, 1)
        preferencesBox.addWidget(stackedBox, 3)

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Ok | QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self.buttonApply = buttonBox.button(QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.onButtonDefaultsClicked)
        buttonBox.accepted.connect(self.onButtonOkClicked)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.onButtonApplyClicked)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addLayout(preferencesBox)
        layout.addWidget(buttonBox)

        self.updatePreferences()
        self.buttonApply.setEnabled(False)


    def setPreferences(self, preferences):

        self._preferences = preferences

        self.updatePreferences()
        self.buttonApply.setEnabled(False)


    def preferences(self):

        return self._preferences


    def onPreferencesChanged(self):

        self.buttonApply.setEnabled(True)


    def onButtonDefaultsClicked(self):

        self.updatePreferences(True)


    def onButtonOkClicked(self):

        self.savePreferences()
        self.close()


    def onButtonApplyClicked(self):

        self.savePreferences()
        self.buttonApply.setEnabled(False)


    def updatePreferences(self, isDefault=False):

        # General: Geometry & State
        self.generalPage.setRestoreApplicationGeometry(self._preferences.restoreApplicationGeometry(isDefault))
        self.generalPage.setRestoreApplicationState(self._preferences.restoreApplicationState(isDefault))


    def savePreferences(self):

        # General: Geometry & State
        self._preferences.setRestoreApplicationGeometry(self.generalPage.restoreApplicationGeometry())
        self._preferences.setRestoreApplicationState(self.generalPage.restoreApplicationState())

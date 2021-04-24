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

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout

from preferences import Preferences
from preferences_page_draws import PreferencesPageDraws
from preferences_page_general import PreferencesPageGeneral
from preferences_page_lotteries import PreferencesPageLotteries
from preferences_page_plays import PreferencesPagePlays


class PreferencesDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(800, 600)
        self.setWindowTitle(self.tr("Preferences"))

        self._preferences = Preferences()

        #
        # Content

        self._pageGeneral = PreferencesPageGeneral()
        self._pageGeneral.setZeroMargins()
        self._pageGeneral.preferencesChanged.connect(self._onPreferencesChanged)

        self._pageLotteries = PreferencesPageLotteries()
        self._pageLotteries.setZeroMargins()
        self._pageLotteries.preferencesChanged.connect(self._onPreferencesChanged)

        self._pageDraws = PreferencesPageDraws()
        self._pageDraws.setZeroMargins()
        self._pageDraws.preferencesChanged.connect(self._onPreferencesChanged)

        self._pagePlays = PreferencesPagePlays()
        self._pagePlays.setZeroMargins()
        self._pagePlays.preferencesChanged.connect(self._onPreferencesChanged)

        stackedBox = QStackedWidget()
        stackedBox.addWidget(self._pageGeneral)
        stackedBox.addWidget(self._pageLotteries)
        stackedBox.addWidget(self._pageDraws)
        stackedBox.addWidget(self._pagePlays)
        stackedBox.setCurrentIndex(0)

        listBox = QListWidget()
        listBox.addItem(self._pageGeneral.title())
        listBox.addItem(self._pageLotteries.title())
        listBox.addItem(self._pageDraws.title())
        listBox.addItem(self._pagePlays.title())
        listBox.setCurrentRow(stackedBox.currentIndex())
        listBox.currentRowChanged.connect(stackedBox.setCurrentIndex)

        preferencesBox = QHBoxLayout()
        preferencesBox.addWidget(listBox, 1)
        preferencesBox.addWidget(stackedBox, 3)

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Ok | QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self._buttonApply = buttonBox.button(QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self._onButtonDefaultsClicked)
        buttonBox.accepted.connect(self._onButtonOkClicked)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self._onButtonApplyClicked)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addLayout(preferencesBox)
        layout.addWidget(buttonBox)

        self._updatePreferences()
        self._buttonApply.setEnabled(False)


    def setPreferences(self, preferences):

        self._preferences = preferences

        self._updatePreferences()
        self._buttonApply.setEnabled(False)


    def preferences(self):

        return self._preferences


    def _onPreferencesChanged(self):

        self._buttonApply.setEnabled(True)


    def _onButtonDefaultsClicked(self):

        self._updatePreferences(True)


    def _onButtonOkClicked(self):

        self._savePreferences()
        self.close()


    def _onButtonApplyClicked(self):

        self._savePreferences()
        self._buttonApply.setEnabled(False)


    def _updatePreferences(self, isDefault=False):

        # General: Geometry & State
        self._pageGeneral.setRestoreApplicationGeometry(self._preferences.restoreApplicationGeometry(isDefault))
        self._pageGeneral.setRestoreApplicationState(self._preferences.restoreApplicationState(isDefault))


    def _savePreferences(self):

        # General: Geometry & State
        self._preferences.setRestoreApplicationGeometry(self._pageGeneral.restoreApplicationGeometry())
        self._preferences.setRestoreApplicationState(self._pageGeneral.restoreApplicationState())

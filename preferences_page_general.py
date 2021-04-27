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
from PySide2.QtWidgets import QButtonGroup, QCheckBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QRadioButton, QTabWidget, QVBoxLayout, QWidget


class PreferencesPageGeneral(QWidget):

    preferencesChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Title
        title = QLabel(self.tr("<strong style=\"font-size:large;\">{0}</strong>").format(self.title()))


        #
        # Content: Geometry & State

        self._chkRestoreApplicationGeometry = QCheckBox(self.tr("Save and restore the application geometry"))
        self._chkRestoreApplicationGeometry.stateChanged.connect(self._onPreferencesChanged)

        self._chkRestoreApplicationState = QCheckBox(self.tr("Save and restore the application state"))
        self._chkRestoreApplicationState.stateChanged.connect(self._onPreferencesChanged)

        geometryStateLayout = QVBoxLayout()
        geometryStateLayout.addWidget(self._chkRestoreApplicationGeometry)
        geometryStateLayout.addWidget(self._chkRestoreApplicationState)

        geometryStateGroup = QGroupBox(self.tr("Geometry && State"))
        geometryStateGroup.setLayout(geometryStateLayout)


        #
        # Content: Tab Bars

        rdbDefaultTabbarLotteriesPositionTop = QRadioButton(self.tr("Top"))
        rdbDefaultTabbarLotteriesPositionTop.setToolTip(self.tr("The lottery tabs are displayed above the pages"))

        rdbDefaultTabbarLotteriesPositionBottom = QRadioButton(self.tr("Bottom"))
        rdbDefaultTabbarLotteriesPositionBottom.setToolTip(self.tr("The lottery tabs are displayed below the pages"))

        self._grpDefaultTabbarLotteriesPosition = QButtonGroup(self)
        self._grpDefaultTabbarLotteriesPosition.addButton(rdbDefaultTabbarLotteriesPositionTop, QTabWidget.North)
        self._grpDefaultTabbarLotteriesPosition.addButton(rdbDefaultTabbarLotteriesPositionBottom, QTabWidget.South)
        self._grpDefaultTabbarLotteriesPosition.buttonClicked.connect(self._onPreferencesChanged)

        rdbDefaultTabbarSheetsPositionTop = QRadioButton(self.tr("Top"))
        rdbDefaultTabbarSheetsPositionTop.setToolTip(self.tr("The sheet tabs are displayed above the pages"))

        rdbDefaultTabbarSheetsPositionBottom = QRadioButton(self.tr("Bottom"))
        rdbDefaultTabbarSheetsPositionBottom.setToolTip(self.tr("The sheet tabs are displayed below the pages"))

        self._grpDefaultTabbarSheetsPosition = QButtonGroup(self)
        self._grpDefaultTabbarSheetsPosition.addButton(rdbDefaultTabbarSheetsPositionTop, QTabWidget.North)
        self._grpDefaultTabbarSheetsPosition.addButton(rdbDefaultTabbarSheetsPositionBottom, QTabWidget.South)
        self._grpDefaultTabbarSheetsPosition.buttonClicked.connect(self._onPreferencesChanged)

        defaultTabbarLotteriesPositionBox = QHBoxLayout()
        defaultTabbarLotteriesPositionBox.addWidget(rdbDefaultTabbarLotteriesPositionTop)
        defaultTabbarLotteriesPositionBox.addWidget(rdbDefaultTabbarLotteriesPositionBottom)

        defaultTabbarSheetsPositionBox = QHBoxLayout()
        defaultTabbarSheetsPositionBox.addWidget(rdbDefaultTabbarSheetsPositionTop)
        defaultTabbarSheetsPositionBox.addWidget(rdbDefaultTabbarSheetsPositionBottom)

        defaultTabbarPositionLayout = QFormLayout()
        defaultTabbarPositionLayout.addRow(self.tr("Position of the lottery tabs"), defaultTabbarLotteriesPositionBox)
        defaultTabbarPositionLayout.addRow(self.tr("Position of the sheet tabs"), defaultTabbarSheetsPositionBox)

        tabBarsGroup = QGroupBox(self.tr("Tab Bars"))
        tabBarsGroup.setLayout(defaultTabbarPositionLayout)


        # Main layout
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(title)
        self._layout.addWidget(geometryStateGroup)
        self._layout.addWidget(tabBarsGroup)
        self._layout.addStretch(1)


    def setZeroMargins(self):

        self._layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr("General")


    def _onPreferencesChanged(self):

        self.preferencesChanged.emit()


    def setRestoreApplicationGeometry(self, checked):

        self._chkRestoreApplicationGeometry.setChecked(checked)


    def restoreApplicationGeometry(self):

        return self._chkRestoreApplicationGeometry.isChecked()


    def setRestoreApplicationState(self, checked):

        self._chkRestoreApplicationState.setChecked(checked)


    def restoreApplicationState(self):

        return self._chkRestoreApplicationState.isChecked()


    def setDefaultTabbarLotteriesPosition(self, tabPosition):

        if tabPosition != self.defaultTabbarLotteriesPosition():
            self._onPreferencesChanged()

        for button in self._grpDefaultTabbarLotteriesPosition.buttons():
            if self._grpDefaultTabbarLotteriesPosition.id(button) == tabPosition:
                button.setChecked(True)
                break


    def defaultTabbarLotteriesPosition(self):

        return QTabWidget.TabPosition(self._grpDefaultTabbarLotteriesPosition.checkedId())


    def setDefaultTabbarSheetsPosition(self, tabPosition):

        if tabPosition != self.defaultTabbarSheetsPosition():
            self._onPreferencesChanged()

        for button in self._grpDefaultTabbarSheetsPosition.buttons():
            if self._grpDefaultTabbarSheetsPosition.id(button) == tabPosition:
                button.setChecked(True)
                break


    def defaultTabbarSheetsPosition(self):

        return QTabWidget.TabPosition(self._grpDefaultTabbarSheetsPosition.checkedId())

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

from PySide2.QtCore import QByteArray
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout


class PreferencesDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr('Preferences'))


        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(buttonBox)


    def setDialogGeometry(self, geometry=QByteArray()):

        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.resize(800, 600)


    def dialogGeometry(self):

        return self.saveGeometry()

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

from PySide2.QtCore import QByteArray, Qt
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QTabWidget, QVBoxLayout

from colophon_about_page import ColophonAboutPage
from colophon_authors_page import ColophonAuthorsPage
from colophon_credits_page import ColophonCreditsPage
from colophon_environment_page import ColophonEnvironmentPage
from colophon_license_page import ColophonLicensePage
from dialog_title_box import DialogTitleBox


class ColophonDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(self.tr('Colophon'))

        # Title box
        titleBox = DialogTitleBox()

        # Content
        aboutPage = ColophonAboutPage()
        environmentPage = ColophonEnvironmentPage()
        licensePage = ColophonLicensePage()
        authorsPage = ColophonAuthorsPage()
        creditsPage = ColophonCreditsPage()

        tabBox = QTabWidget()
        tabBox.addTab(aboutPage, aboutPage.title())
        tabBox.addTab(environmentPage, environmentPage.title())
        tabBox.addTab(licensePage, licensePage.title())
        tabBox.addTab(authorsPage, authorsPage.title())
        tabBox.addTab(creditsPage, creditsPage.title())

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(titleBox)
        layout.addWidget(tabBox)
        layout.addWidget(buttonBox)


    def setDialogGeometry(self, geometry=QByteArray()):

        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            self.resize(640, 480)


    def dialogGeometry(self):

        return self.saveGeometry()

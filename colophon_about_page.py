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

from PySide2.QtWidgets import QApplication, QFrame, QTextBrowser, QVBoxLayout, QWidget


class ColophonAboutPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(self.tr(f'''<html><body>
            <p>{QApplication.applicationName()} is an open source visualization tool written in Qt for Python and designed for easy creation and graphical representation of lottery data.</p>
            <p>Copyright &copy; 2021 <a href="{QApplication.organizationDomain()}">{QApplication.organizationName()}</a>.</p>
            <p>This application is licensed under the terms of the <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">GNU General Public License, version 3</a>.</p>
            </body></html>'''))

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(textBox)


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('About')

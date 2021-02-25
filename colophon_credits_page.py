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

from PySide2.QtWidgets import QFrame, QTextBrowser, QVBoxLayout, QWidget


class ColophonCreditsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(self.tr('''<html><body>
            <dl><dt><strong>Freepik</strong></dt>
                <dd>Application logo made by <a href="https://www.flaticon.com/authors/freepik/" title="Visit author's homepage">Freepik</a>
                    from <a href="https://www.flaticon.com" title="Visit organization's homepage">www.flaticon.com</a>
                    is licensed under <a href="https://file000.flaticon.com/downloads/license/license.pdf" title="Visit license's homepage">Free License (with attribution)</a>.</dd></dl>
            <dl><dt><strong>BreezeIcons project</strong></dt>
                <dd>Application icons made by <a href="https://api.kde.org/frameworks/breeze-icons/html/" title="Visit project's homepage">BreezeIcons project</a>
                    from <a href="https://kde.org" title="Visit organization's homepage">KDE</a>
                    are licensed under <a href="https://www.gnu.org/licenses/lgpl-3.0.en.html" title="Visit license's homepage">LGPLv3</a>.</dd></dl>
            </body></html>'''))

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(textBox)


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('Credits')

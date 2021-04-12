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

import sys
import PySide2.QtCore

from PySide2.QtCore import QSysInfo
from PySide2.QtWidgets import QApplication, QFrame, QTextBrowser, QVBoxLayout, QWidget


#
# Colophon page: About
#

class ColophonAboutPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(self.tr(f'''<html><body>
            <p>{QApplication.applicationName()} is an open source visualization tool written in Qt for Python and designed for easy creation and graphical representation of lottery data.</p>
            <p>Copyright &copy; 2021 <a href="{QApplication.organizationDomain()}" title="Visit organization's homepage">{QApplication.organizationName()}</a>.</p>
            <p>This application is licensed under the terms of the <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" title="Visit license's homepage">GNU General Public License, version 3</a>.</p>
            </body></html>'''))

        # Main layout
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(textBox)


    def setZeroMargins(self):

        self._layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('About')


#
# Colophon page: Authors
#

class ColophonAuthorsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(self.tr('''<html><body>
            <dl><dt><strong>NotNypical</strong></dt>
                <dd>Created and developed by <a href="https://notnypical.github.io" title="Visit author's homepage">NotNypical</a>.</dd></dl>
            </body></html>'''))

        # Main layout
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(textBox)


    def setZeroMargins(self):

        self._layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('Authors')


#
# Colophon page: Credits
#

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
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(textBox)


    def setZeroMargins(self):

        self._layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('Credits')


#
# Colophon page: Environment
#

class ColophonEnvironmentPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        pythonVersion = sys.version
        pysideVersion = PySide2.__version__
        qtVersion = PySide2.QtCore.qVersion()  # Qt version used to run Qt for Python
        qtBuildVersion = PySide2.QtCore.__version__  # Qt version used to compile PySide2
        osName = QSysInfo.prettyProductName()
        osKernelVersion = QSysInfo.kernelVersion()
        osCpuArchitecture = QSysInfo.currentCpuArchitecture()

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(self.tr(f'''<html><body>
            <dl><dt><strong>Application version</strong></dt>
                <dd>{QApplication.applicationVersion()}</dd></dl>
            <dl><dt><strong>Qt for Python version</strong></dt>
                <dd>{pysideVersion} runs on Qt {qtVersion} (Built against {qtBuildVersion})</dd></dl>
            <dl><dt><strong>Python version</strong></dt>
                <dd>{pythonVersion}</dd></dl>
            <dl><dt><strong>Operation System</strong></dt>
                <dd>{osName} (Kernel {osKernelVersion} on {osCpuArchitecture})</dd></dl>
            </body></html>'''))

        # Main layout
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(textBox)


    def setZeroMargins(self):

        self._layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('Environment')


#
# Colophon page: License
#

class ColophonLicensePage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(self.tr(f'''<html><body>
            <p>{QApplication.applicationName()} is free software: you can redistribute it and/or modify it under the terms of the
                GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
                or (at your option) any later version.</p>
            <p>{QApplication.applicationName()} is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
                without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
                See the GNU General Public License for more details.</p>
            <p>You should have received a copy of the GNU General Public License along with {QApplication.applicationName()}.
                If not, see <a href="https://www.gnu.org/licenses/" title="Visit license's homepage">https://www.gnu.org/licenses/</a>.</p>
            </body></html>'''))

        # Main layout
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(textBox)


    def setZeroMargins(self):

        self._layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('License')

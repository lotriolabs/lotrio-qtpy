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

import sys
import PySide2.QtCore

from PySide2.QtCore import QSysInfo
from PySide2.QtWidgets import QApplication, QFrame, QTextBrowser, QVBoxLayout, QWidget


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
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(textBox)


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('Environment')

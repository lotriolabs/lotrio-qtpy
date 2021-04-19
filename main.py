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

from PySide2.QtCore import QCommandLineOption, QCommandLineParser, QCoreApplication
from PySide2.QtWidgets import QApplication

from main_window import MainWindow


def showLanguageList():

    usage = QCoreApplication.instance().arguments()[0]
    usage += " " + "--language"
    usage += " " + QCoreApplication.translate("main", "[Language code]")

    print(QCoreApplication.translate("main", "Usage: {0}").format(usage) + "\n")


    return 0


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setOrganizationName("LotrioLabs")
    app.setOrganizationDomain("https://lotriolabs.github.io")
    app.setApplicationName("Lotrio-QtPy")
    app.setApplicationDisplayName("Lotrio-QtPy")
    app.setApplicationVersion("0.1.0")

    languageListOption = QCommandLineOption(["language-list"], QCoreApplication.translate("main", "Lists available application languages."))

    parser = QCommandLineParser()
    parser.setApplicationDescription(QCoreApplication.translate("main", "{0} - A visualization tool for lottery data").format(app.applicationName()))
    parser.addHelpOption()
    parser.addVersionOption()
    parser.addOption(languageListOption)
    parser.process(app)

    if parser.isSet(languageListOption):
        sys.exit(showLanguageList())

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

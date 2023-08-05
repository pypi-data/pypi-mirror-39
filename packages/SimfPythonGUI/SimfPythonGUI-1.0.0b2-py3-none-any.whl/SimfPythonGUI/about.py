import pkg_resources
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
import os


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__(flags=Qt.WindowStaysOnTopHint)
        version_file = open(pkg_resources.resource_filename(__name__,
                                                            "VERSION"))
        version = version_file.read().strip()
        ui_file = pkg_resources.resource_filename(__name__, "AboutDialog.ui")
        uic.loadUi(ui_file, self)
        self.show()
        self.versionLabel.setText("Version: " + version)

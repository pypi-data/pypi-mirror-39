#!/usr/bin/env python
import sys
import webbrowser
from PyQt5 import uic
import pkg_resources
from PyQt5.QtCore import QProcess, QProcessEnvironment, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene
from .filehandlers import ImageThread
from .sudo import PasswordWindow
from .about import AboutDialog
from .config import Config, ConfigEditor


class MainWindow(QMainWindow):
    simfProcess = QProcess()

    def __init__(self):
        super().__init__(flags=Qt.Window)

        ui_file = pkg_resources.resource_filename(__name__, "MainWindow.ui")
        uic.loadUi(ui_file, self)

        self.passprompt = None
        self.configdialog = None
        self.aboutdialog = None

        self.png_watcher = ImageThread()
        self.png_watcher.new_image.connect(self.update_image)

        # Register Events
        self.startCapButton.clicked.connect(self.start_capture)
        self.stopCapButton.clicked.connect(self.stop_capture)
        self.actionSourceCode.triggered.connect(
            lambda:
            MainWindow.open_link("https://git.nclf.net/SIMF/simf-python-gui")
        )
        self.actionLicense.triggered.connect(
            lambda:
            MainWindow.open_link("https://git.nclf.net/SIMF/simf-python-gui/"
                                 "blob/master/LICENSE.md")
        )
        self.actionExit.triggered.connect(self.close)
        self.actionSettings.triggered.connect(self.show_settings)
        self.actionAbout.triggered.connect(self.show_about)

        # Process setup
        self.simfProcess.readyRead.connect(self.console_write)
        self.simfProcess.started.connect(self.process_started)
        self.simfProcess.finished.connect(self.process_finished)

        # Ready to show the UI!
        self.show()

        self.cameraCount.display("OFF")
        self.solarIrradiance.display("OFF")

        # Init the scenes for the graphics displays
        self.sceneN = QGraphicsScene()
        self.imgN.setScene(self.sceneN)
        self.sceneNE = QGraphicsScene()
        self.imgNE.setScene(self.sceneNE)
        self.sceneE = QGraphicsScene()
        self.imgE.setScene(self.sceneE)
        self.sceneSE = QGraphicsScene()
        self.imgSE.setScene(self.sceneSE)
        self.sceneS = QGraphicsScene()
        self.imgS.setScene(self.sceneS)
        self.sceneSW = QGraphicsScene()
        self.imgSW.setScene(self.sceneSW)
        self.sceneW = QGraphicsScene()
        self.imgW.setScene(self.sceneW)
        self.sceneNW = QGraphicsScene()
        self.imgNW.setScene(self.sceneNW)
        self.sceneCenter = QGraphicsScene()
        self.imgCenter.setScene(self.sceneCenter)
        self.current = 0

    # Updates the image and determines the capture progress
    def update_image(self, path):
        pix = QPixmap(path)

        if self.current == 0:
            self.sceneNW.addPixmap(pix)
        elif self.current == 1:
            self.sceneN.addPixmap(pix)
        elif self.current == 2:
            self.sceneNE.addPixmap(pix)
        elif self.current == 3:
            self.sceneW.addPixmap(pix)
        elif self.current == 4:
            self.sceneCenter.addPixmap(pix)
        elif self.current == 5:
            self.sceneE.addPixmap(pix)
        elif self.current == 6:
            self.sceneSW.addPixmap(pix)
        elif self.current == 7:
            self.sceneS.addPixmap(pix)
        elif self.current == 8:
            self.sceneSE.addPixmap(pix)

        # TODO: Capture progress
        self.current = (self.current + 1) % Config.dbg_lepton_set

    # Opens a link
    @staticmethod
    def open_link(link):
        webbrowser.open(link)

    # Triggered when window closes, I know it isn't PEP8 compliant but thats
    # the way pyqt5 is
    def closeEvent(self, QCloseEvent):
        self.simfProcess.kill()  # Cleanly kill the simfprocess
        self.close()

    def show_about(self):
        self.aboutdialog = AboutDialog()

    def show_settings(self):
        self.configdialog = ConfigEditor()

    # Toggle all the enable/disable options
    # status=true lepton-grabber process running
    # status=false lepton-grabber process stopped
    # sorry
    def button_toggle(self, status):
        self.capProgress.setEnabled(status)
        self.cameraCount.setEnabled(status)
        self.solarIrradiance.setEnabled(status)
        self.startCapButton.setDisabled(status)
        self.stopCapButton.setEnabled(status)
        self.capProgressLabel.setEnabled(status)
        self.cameraCountLabel.setEnabled(status)
        self.solarIrradianceLabel.setEnabled(status)
        self.imgN.setEnabled(status)
        self.imgNE.setEnabled(status)
        self.imgE.setEnabled(status)
        self.imgSE.setEnabled(status)
        self.imgS.setEnabled(status)
        self.imgSW.setEnabled(status)
        self.imgW.setEnabled(status)
        self.imgNW.setEnabled(status)
        self.imgCenter.setEnabled(status)
        self.actionSettings.setDisabled(status)

        if status:
            self.cameraCount.display(Config.dbg_lepton_set)
            self.statusLabel.setText("Status: Capturing")
        else:
            self.cameraCount.display("OFF")
            self.solarIrradiance.display("OFF")
            self.statusLabel.setText("Status: Stopped")

    # Triggered when the QProcess that runs the lepton-grabber runs
    def process_started(self):
        self.button_toggle(True)
        self.current = 0
        self.png_watcher.start()

    # Triggered when the QProcess that runs the lepton-grabber dies for any
    # reason
    def process_finished(self):
        self.button_toggle(False)

        self.console_write()
        self.console_write_line("Capture Ended")

        self.png_watcher.terminate()

    # Fired when the observer started in process_started
    # detects a new image from the lepton grabbers
    def update_images(self):
        self.console_write_line("New images!\n")

    # Allows the console to handle \n newlines
    def console_write_line(self, output):
        # the QPlainTextEdit widget doesn't like newlines
        # So I use appendhtml and <br /> instead
        output = output.replace('\\n', '<br />')
        self.consoleWidget.appendHtml(output)

    # Event handle fired when there is new stdout or stderr from SIMF
    def console_write(self):
        output = str(self.simfProcess.readAll(), encoding='utf-8')
        self.console_write_line(output)

    # Fired by the OK button on the sudo dialog
    def start_capture(self):
        # Retrieves the password via a QDialog
        self.passprompt = PasswordWindow()
        self.passprompt.exec_()  # Wait for the password dialog to finish
        if self.passprompt.rejectstat:  # Cancel was pressed
            return
        password = self.passprompt.passLine.text()  # Grab the password

        env = QProcessEnvironment.systemEnvironment()
        self.simfProcess.setProcessEnvironment(env)
        self.simfProcess.setWorkingDirectory(Config.lepton_grabber_working_dir)
        self.simfProcess.setProcessChannelMode(QProcess.MergedChannels)
        # Note this is a kinda hacky way to get the script to execute
        # with sudo permissions, likely a better way to do this at the system
        # level
        self.simfProcess.start(Config.bash_path)
        self.simfProcess.writeData(("printf -v pw \"%q\\n\" \""
                                    + password + "\"\n").encode('utf-8'))
        self.simfProcess.writeData(("echo $pw | " + "\"" + Config.sudo_path +
                                    "\" -S "
                                    + "\"" + Config.python_path + "\"" +
                                    " frame_grabber.py"
                                    " --dbg_interval "
                                    + str(Config.dbg_interval) + ""
                                    + (" --dbg_png" if Config.dbg_png
                                       else "") +
                                    " --dbg_ffc_interval "
                                    + str(Config.dbg_ffc_interval) +
                                    " --dbg_capture_count "
                                    + str(Config.dbg_capture_count) +
                                    " --dbg_serial_csv "
                                    + str(int(Config.dbg_serial_csv)) +
                                    " --dbg_lepton_set "
                                    + str(Config.dbg_lepton_set)
                                    + (" --dbg_testmode1"
                                       if Config.dbg_testmode1
                                       else "")
                                    + (" --dbg_print" if Config.dbg_print
                                       else "")
                                    + (" --dbg_ser_noavg"
                                       if Config.dbg_ser_noavg
                                       else "")
                                    + (" --dbg_no_serial"
                                       if Config.dbg_no_serial
                                       else "")
                                    + "\n")
                                   .encode('utf-8'))

        self.simfProcess.writeData("exit\n".encode('utf-8'))

    # Fired when the stop capture button is hit
    def stop_capture(self):
        self.console_write_line("Capture terminated!")
        self.simfProcess.kill()  # Kill the capture subprocess


# Main Function for the whole thing
def main():
    config = Config()
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

import os
from configparser import SafeConfigParser
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog


class Config:
    # TODO: Comment generated config file
    config_name = 'config.ini'

    """  READ ME BEFORE EDITING BELOW
    These are the **default** values, if you want to change
    configuration values use the GUI or modify the config file named
    in the variable above and relaunch the program!
    
    If you don't have a config file, just run the program for the first
    time to generate the default file.
    """

    # paths
    lepton_grabber_working_dir = "lepton-grabber"
    python_path = "/usr/bin/python3"
    sudo_path = "sudo"
    # Note that bash can be replaced by other compatible shells
    # All I use is echo, quit, printf, and the piping command "|"
    bash_path = "bash"

    # lepton-grabber launch options
    dbg_interval = 10
    dbg_png = True
    dbg_ffc_interval = -180
    dbg_capture_count = 720
    dbg_serial_csv = True

    def read_config(self, parser):
        parser.read(self.config_name)

        # Get Paths
        self.lepton_grabber_working_dir = parser.get(
            'Paths', 'lepton_grabber_working_dir')
        self.python_path = parser.get('Paths', 'python_path')
        self.sudo_path = parser.get('Paths', 'sudo_path')
        self.bash_path = parser.get('Paths', 'bash_path')

        # Get lepton config
        self.dbg_interval = parser.getint('LeptonGrabberLaunchOptions',
                                          'dbg_interval')
        self.dbg_png = parser.getboolean('LeptonGrabberLaunchOptions',
                                         'dbg_png')
        self.dbg_ffc_interval = parser.getint('LeptonGrabberLaunchOptions',
                                              'dbg_ffc_interval')
        self.dbg_capture_count = parser.getint('LeptonGrabberLaunchOptions',
                                               'dbg_capture_count')
        self.dbg_serial_csv = parser.getboolean('LeptonGrabberLaunchOptions',
                                                'dbg_serial_csv')

    @staticmethod
    def write_config(parser):
        parser.add_section('Paths')
        parser.set('Paths', 'lepton_grabber_working_dir',
                   Config.lepton_grabber_working_dir)
        parser.set('Paths', 'python_path', Config.python_path)
        parser.set('Paths', 'sudo_path', Config.sudo_path)
        parser.set('Paths', 'bash_path', Config.bash_path)

        parser.add_section('LeptonGrabberLaunchOptions')
        parser.set('LeptonGrabberLaunchOptions', 'dbg_interval',
                   str(Config.dbg_interval))
        parser.set('LeptonGrabberLaunchOptions', 'dbg_png',
                   str(Config.dbg_png))
        parser.set('LeptonGrabberLaunchOptions', 'dbg_ffc_interval',
                   str(Config.dbg_ffc_interval))
        parser.set('LeptonGrabberLaunchOptions', 'dbg_capture_count',
                   str(Config.dbg_capture_count))
        parser.set('LeptonGrabberLaunchOptions', 'dbg_serial_csv',
                   str(Config.dbg_serial_csv))

        with open(Config.config_name, 'w') as file:
            parser.write(file)

    def __init__(self):
        parser = SafeConfigParser(allow_no_value=True)

        if os.path.isfile(self.config_name):
            self.read_config(parser)
        else:
            # Generate new config
            self.write_config(parser)


class ConfigEditor(QDialog):
    def __init__(self):
        super().__init__(flags=Qt.WindowStaysOnTopHint)
        uic.loadUi('SettingsDialog.ui', self)
        self.show()

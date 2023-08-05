import os
from PyQt5.QtCore import QThread, pyqtSignal
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
from .config import Config
from watchdog.observers import Observer


# Computes where the lepton grabber is currently dumping output
class FileHandlerUtils:
    @staticmethod
    def compute_current_data_dir():
        today = datetime.utcnow()

        return Config.lepton_grabber_working_dir + "/" \
            + today.strftime("%y-%m-%d")


class ImageThread(QThread):
    new_image = pyqtSignal(str)

    class ImageHandler(PatternMatchingEventHandler):
        patterns = ["*.png"]

        def __init__(self, event_thread):
            super().__init__()
            self.event_thread = event_thread

        def on_created(self, event):
            self.event_thread.new_image.emit(event.src_path)

    def run(self):
        datadir = FileHandlerUtils.compute_current_data_dir()

        if not os.path.exists(datadir):
            # Wait for lepton-grabber to make the directory rather than failing
            # here or waiting for the data directory to be created just create
            # it ourselves
            os.mkdir(datadir)

        observer = Observer()
        # FIXME: When this ticks over to the next day it fails to update
        observer.schedule(self.ImageHandler(self), path=datadir)

        observer.start()
        observer.join()


class LicorThread(QThread):
    new_licor = pyqtSignal(float)

    class LicorHandler(PatternMatchingEventHandler):
        patterns = ["*.txt"]

        def __init__(self, event_thread):
            super().__init__()
            self.event_thread = event_thread

        def on_created(self, event):
            # TODO: Read licor file, convert to float, send to event
            self.event_thread.new_licor.emit(event.src_path)

    def run(self):
        datadir = FileHandlerUtils.compute_current_data_dir()

        if not os.path.exists(datadir):
            # Wait for lepton-grabber to make the directory rather than failing
            # here or waiting for the data directory to be created just create
            # it ourselves
            os.mkdir(datadir)

        observer = Observer()
        # FIXME: When this ticks over to the next day it fails to update
        observer.schedule(self.LicorHandler(self), path=datadir)

        observer.start()
        observer.join()

from watchdog.events import PatternMatchingEventHandler
from datetime import date


# Computes where the lepton grabber is currently dumping output
class FileHandlerUtils:
    @staticmethod
    def compute_current_data_dir():
        today = date.today()

        return "lepton-grabber/" + today.strftime("%y-%m-%d")


class ImageHandler(PatternMatchingEventHandler):
    patterns = ["*.png"]
    main = None

    # Holders for the images
    pngN = None
    pngNE = None
    pngE = None
    pngSE = None
    pngS = None
    pngSW = None
    pngW = None
    pngNW = None
    pngCenter = None

    def __init__(self, mainwindow):
        self.main = mainwindow

    def on_created(self, event):
        # TODO: Update image views
        print("Update image")

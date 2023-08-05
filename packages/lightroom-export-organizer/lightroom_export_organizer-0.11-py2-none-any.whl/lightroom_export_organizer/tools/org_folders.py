"""
Organizes exported Lightroom photos into directories, according to a key-value pair in
a side-car text file for each image. The value of this key-value pair is the name of the
directory that the photo should be put into.

UI code is a liberal adaptation of https://pythonspot.com/pyqt5-file-dialog/
"""
import os
import sys
import structlog
from os import path
from argparse import ArgumentParser
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

from lightroom_export_organizer.org_folders import do2

log = structlog.getLogger()


class UI(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Lightroom Export Organizer"
        self.init_ui()

    def get_directory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        return QFileDialog.getExistingDirectory(
            self,
            "Select the directory where the photos are.",
            path.join(path.expanduser("~"), "Desktop"),
            options=options
        )

    def init_ui(self):
        self.setWindowTitle(self.title)


def get_clargs():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input-directory", required=False, default=None,
                        help="Path to directory")
    return parser.parse_args()


def main():
    args = get_clargs()
    os.environ["DISPLAY"] = ":0.0"
    while args.input_directory is None:
        app = QApplication(sys.argv)
        args.input_directory = UI().get_directory()

    return do2(args.input_directory)


if __name__ == '__main__':
    sys.exit(main())

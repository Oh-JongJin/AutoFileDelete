import os
import shutil
import psutil

from PyQt5.QtWidgets import QWidget, QApplication, QMenuBar, \
    QAction, QFileDialog, qApp
from PyQt5.QtCore import QSettings, Qt
from PyQt5 import uic

form = uic.loadUiType("auto_file_delete.ui")[0]


def byte_transform(bytes, to, bsize=1024):
    """Unit conversion of byte received from shutil

    :return: Capacity of the selected unit (int)
    """
    unit = {'KB': 1, 'MB': 2, 'GB': 3, 'TB': 4}
    r = float(bytes)
    for i in range(unit[to]):
        r = r / bsize
    return int(r)


class FileAutoDelete(QWidget, form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        drive = []
        for i in range(len(psutil.disk_partitions())):
            drive.append(str(psutil.disk_partitions()[i])[18:19])
        self.comboBox.addItems(drive)

        self.comboBox.setCurrentText(Settings.get('drive'))
        self.spinBox.setValue(Settings.get('storage'))

        self.comboBox.currentTextChanged.connect(self.change_combo)

        self.diskLabel = f'{self.comboBox.currentText()}:\\'
        self.total, self.used, self.free = shutil.disk_usage(self.diskLabel)

        self.label.setText(f"{self.comboBox.currentText()}: {byte_transform(self.free, 'GB')} GB")

        self.value = None
        self.path = None
        self.oldPos = None

        # self.menuBar = QMenuBar(self)
        # exitMenu = self.menuBar.addMenu('&File')
        # exitAction = QAction('Exit', self)
        # exitAction.setShortcut("Ctrl+W")
        # exitAction.triggered.connect(qApp.quit)
        # exitMenu.addAction(exitAction)

        self.pushButton.clicked.connect(self.btn_click)

    def change_combo(self, value):
        self.total, self.used, self.free = shutil.disk_usage(f'{value}:\\')
        self.label.setText(f"{value}: {byte_transform(self.free, 'GB')} GB")

    def delete_oldest_files(self, path, minimum_storage_GB: int):
        """
        The main function of this Program
        Find oldest file and proceed with deletion

        :param path: Path to proceed with a auto-delete
        :param minimum_storage_GB: Minimum storage space desired by the user
        """
        is_old = {}

        if minimum_storage_GB >= byte_transform(self.free, 'GB'):

            for f in os.listdir(path):

                i = os.path.join(path, f)
                is_old[f'{i}'] = int(os.path.getctime(i))

            value = list(is_old.values())
            key = {v: k for k, v in is_old.items()}
            old_folder = key.get(min(value))
            old_folder = os.path.dirname(os.path.abspath(old_folder))
            print(old_folder)
            # sys.exit()

            try:
                shutil.rmtree(old_folder)
                self.progressBar.setValue(self.progressBar.value() + 1)
            except IndexError:
                self.complete_lbl.setText('Complete')

            self.complete_lbl.setText('Complete')
            self.progressBar.setValue(100)

        else:
            print('Already you have enough storage.')
            self.complete_lbl.setText('Enough Storage')

    def btn_click(self):
        if self.spinBox.value() >= byte_transform(self.free, 'GB'):
            self.progressBar.setValue(0)
            self.complete_lbl.clear()
            self.path = QFileDialog.getExistingDirectory(self, 'Select directory',
                                                         directory=f'{self.comboBox.currentText()}:\\')
            if self.path:
                self.delete_oldest_files(self.path, self.spinBox.value())

            Settings.set('drive', self.comboBox.currentText())
            Settings.set('storage', self.spinBox.value())
        else:
            self.complete_lbl.setText('Input storage again')

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_W:
                self.close()
                sys.exit()


class Settings:
    settings = QSettings('sijung', 'js08')
    defaults = {
        'drive': 'C',
        'storage': 0
    }

    @classmethod
    def set(cls, key, value):
        cls.settings.setValue(key, value)

    @classmethod
    def get(cls, key):
        return cls.settings.value(
            key,
            cls.defaults[key],
            type(cls.defaults[key])
        )


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    window = FileAutoDelete()
    window.show()
    sys.exit(app.exec_())

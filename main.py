# -*- coding: utf-8 -*-
"""GUI labeling tool

Notic
    Please modify AppWindow attribute dir to your dataset dir

"""
import sys
import os

from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QSizePolicy, QMenu, QMessageBox
from PySide2.QtCore import Slot, Qt, QPoint, Signal, QEvent
from layout import Ui_MainWindow

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setting = {}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.dir = '../../captcha'
        self.png_dict = self.load_csv()
        for name in self.list_png():
            if not name in self.png_dict:
                self.png_dict[name] = ""
        self.png_list = list(self.png_dict.keys())
        self.png_list.sort()
        self.idx = 0
        self.update_img()

        self.ui.lableLineEdit.installEventFilter(self)

    def list_png(self):
        files = os.listdir(self.dir)
        png_files = list(filter(lambda name: '.png' in name, files))
        png_files.sort()
        return png_files

    def load_csv(self, name='label.csv'):
        png_dict = {}
        if os.path.isfile(os.path.join(self.dir, name)):
            with open(os.path.join(self.dir, name), 'r') as f:
                for name, lable in map(lambda line: line.split(','), f.readlines()):
                    png_dict[name] = lable.strip()
        return png_dict

    def save_csv(self, name='label.csv'):
        with open(os.path.join(self.dir, name), 'w') as f:
            for name in self.png_list:
                f.write(name + ',' + self.png_dict[name] + '\n')
        
        print('saved csv')

    def update_img(self):
        label = self.png_dict[self.png_list[self.idx]]
        self.ui.lableLineEdit.setStyleSheet("color: black;")
        self.ui.lableLineEdit.setText(label)
        print('show', self.idx)
        self.ui.imgLabel.setText(self.png_list[self.idx])
        self.ui.groupBox.setTitle(self.png_list[self.idx])
        pixmap = QPixmap(os.path.join(self.dir, self.png_list[self.idx]))
        self.ui.imgLabel.setPixmap(pixmap)
        

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and source is self.ui.lableLineEdit:
            if event.key() == Qt.Key_Up:
                self.on_preBtn_clicked()
            if event.key() == Qt.Key_Down:
                self.on_nextBtn_clicked()
            # print('key press:', (event.key(), event.text()))
        return super(AppWindow, self).eventFilter(source, event)

    @Slot()
    def on_preBtn_clicked(self):
        skip = self.ui.skipCheckBox.isChecked()
        self.idx -= 1
        if self.idx < 0:
            self.idx = 0
            return
        while skip and len(self.png_dict[self.png_list[self.idx]]) == 4:
            self.idx -= 1
            if self.idx < 0:
                self.idx = 0
                return
        self.update_img()
        print("上一個")

    @Slot()
    def on_nextBtn_clicked(self):
        skip = self.ui.skipCheckBox.isChecked()
        self.idx += 1
        if self.idx >= len(self.png_list):
            self.idx = len(self.png_list)-1
            return
        while skip and len(self.png_dict[self.png_list[self.idx]]) == 4:
            self.idx += 1
            if self.idx >= len(self.png_list):
                self.idx = len(self.png_list)-1
                return
        self.update_img()
        print("下一個")

    @Slot()
    def on_lableLineEdit_returnPressed(self):
        self.png_dict[self.png_list[self.idx]] = self.ui.lableLineEdit.text().strip().upper()
        self.on_nextBtn_clicked()
        print('enter')

    @Slot()
    def on_enterBtn_clicked(self):
        self.on_lableLineEdit_returnPressed()

    @Slot()
    def on_saveBtn_clicked(self):
        self.save_csv()

    def closeEvent(self, event):
        self.save_csv()
        event.accept()

def main():
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
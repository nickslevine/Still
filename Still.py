"""
To build:
    pyinstaller --onefile --windowed --icon=still_icon.icns --add-data="siteslist:." Still.py
To make icon:
    sips -s format icns still_icon.png --out still_icon.icns
"""

import sys
import os
import pickle
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QListWidget, QLineEdit)

class Still(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        try:
            with open('siteslist', 'rb') as data:
                self.sites = pickle.load(data)
        except:
            self.sites = []

        grid = QGridLayout()
        self.setLayout(grid)

        add = QPushButton('Add Site')
        add.clicked.connect(self.add_site)
        grid.addWidget(add, 0, 1)

        remove = QPushButton('Remove Site')
        remove.clicked.connect(self.remove_site)
        grid.addWidget(remove, 1, 1)

        block = QPushButton('Block Sites')
        block.clicked.connect(self.update_hosts)
        grid.addWidget(block, 2, 1)

        unblock = QPushButton('Unblock Sites')
        unblock.clicked.connect(self.clear_hosts)
        grid.addWidget(unblock, 3, 1)

        self.listbox = QListWidget()
        grid.addWidget(self.listbox, 1, 0)
        for item in self.sites:
            self.listbox.addItem(item)

        self.entry = QLineEdit()
        grid.addWidget(self.entry, 0, 0)

        self.move(300, 150)
        self.setWindowTitle('Still')
        self.show()

    def add_site(self):
        s = self.entry.text()
        self.entry.clear()
        self.listbox.addItem(s)
        self.sites.append(s)
        self.update_siteslist
        print(self.sites)

    def remove_site(self):
        s = self.listbox.currentItem().text()
        self.listbox.takeItem(self.listbox.currentRow())
        self.sites.remove(s)
        update_siteslist(self)

    def update_hosts(self):
        command = """
        pw="$(osascript -e 'Tell application "System Events" to display dialog "Password:" default answer "" with hidden answer' -e 'text returned of result' 2>/dev/null)" && echo $pw | sudo -S echo "
# Host Database !
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1   localhost
255.255.255.255 broadcasthost
::1             localhost
fe80::1%lo0 localhost
"""
        for item in self.sites:
            command += "127.0.0.1 " + item + "\n"
        command += "\" | sudo tee /etc/hosts > /dev/null"

        os.system(command)

    def clear_hosts(self):
        command = """
        pw="$(osascript -e 'Tell application "System Events" to display dialog "Password:" default answer "" with hidden answer' -e 'text returned of result' 2>/dev/null)" && echo $pw | sudo -S echo "
# Host Database !
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1   localhost
255.255.255.255 broadcasthost
::1             localhost
fe80::1%lo0 localhost
"""
        command += "\" | sudo tee /etc/hosts > /dev/null"
        os.system(command)

    def update_siteslist(self):
        with open('siteslist', 'wb') as data:
            pickle.dump(self.sites, data)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Still()
    sys.exit(app.exec_())

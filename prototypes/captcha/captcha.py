#  http://www.titulky.com/idown.php?R=1342961604&titulky=0000170819&zip=&histstamp=
#  http://www.titulky.com/captcha/captcha.php

import sys
from PyQt4 import QtGui, QtCore, QtNetwork

class CaptchaDialog(QtGui.QDialog):

    def __init__(self, parent = None, flags = 0):
        super(CaptchaDialog, self).__init__(parent)

        layout = QtGui.QGridLayout()

        #btn = QtGui.QPushButton('ahoj')
        #layout.addWidget(btn)
        lblCaptcha = QtGui.QLabel('a', self)

        self.setLayout(layout)


        manager = QtNetwork.QNetworkAccessManager(self)
        #QObject.connect(manager, SIGNAL("finished(reply)"

















def main():
    app = QtGui.QApplication(sys.argv)
    sys.exit(CaptchaDialog().exec_())


if __name__ == '__main__':
    main()

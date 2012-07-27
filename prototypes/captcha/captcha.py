#  http://www.titulky.com/idown.php?R=1342961604&titulky=0000170819&zip=&histstamp=
#  http://www.titulky.com/captcha/captcha.php

import sys
from PyQt4 import QtGui, QtCore, QtNetwork

from PyQt4.QtCore import SLOT, SIGNAL

class CaptchaDialog(QtGui.QDialog):

    def __init__(self, parent = None, flags = 0):
        super(CaptchaDialog, self).__init__(parent)

        self.layout = QtGui.QGridLayout()

        #layout.addWidget(btn)
        self.lblCaptcha = QtGui.QLabel('a', self)



        manager = QtNetwork.QNetworkAccessManager(self)
        self.connect(manager, SIGNAL("finished(reply)"), self, SLOT('managerFinished(self, reply)'))

        #url = QtNetwork.QUrl('http://www.titulky.com/captcha/captcha.php')
        url = QtCore.QUrl('http://www.titulky.com/captcha/captcha.php')
        request = QtNetwork.QNetworkRequest(url)

        manager.get(request)



    def managerFinished(self, reply):
        print('ahoj')

        if reply.error() != QtNetwork.QNetworkReply.NoError:
            print('nastala chyba')
            print(reply.errorString())

        data = reply.readAll()
        pixmap = QtCore.QPixmap()
        pixmap.loadFromData(data)

        self.lblCaptcha.setPixmap(pixmap)




def main():
    app = QtGui.QApplication(sys.argv)
    sys.exit(CaptchaDialog().exec_())


if __name__ == '__main__':
    main()

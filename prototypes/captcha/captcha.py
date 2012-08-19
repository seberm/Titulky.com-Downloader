import sys
from PyQt4 import QtGui, QtCore, QtNetwork

from PyQt4.QtCore import SLOT, SIGNAL

CAPTCHA_URL = 'http://www.titulky.com/captcha/captcha.php'


class CaptchaDialog(QtGui.QDialog):

    def __init__(self, parent = None, flags = 0):
        super(CaptchaDialog, self).__init__(parent)

        # Dialog settings
        self.setWindowTitle('Re-type captcha')

        # Widgets
        self.lblCaptcha = QtGui.QLabel('No captcha loaded', self)
        self.lblCaptcha.setFixedSize(200, 70)

        self.btnReload = QtGui.QPushButton('Reload', self)
        self.connect(self.btnReload, SIGNAL("clicked()"), self.reloadCaptcha)
        self.btnSend = QtGui.QPushButton('Send', self)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.lblCaptcha)
        layout.addWidget(self.btnReload)
        layout.addWidget(self.btnSend)

        self.setLayout(layout)
        

        # Load captcha into label
        self.manager = QtNetwork.QNetworkAccessManager(self)
        self.connect(self.manager, SIGNAL("finished(QNetworkReply*)"), self.managerFinished)

        self.reloadCaptcha()



    def managerFinished(self, reply):

        if reply.error() != QtNetwork.QNetworkReply.NoError:
            print('Error in loading captcha...')
            print(reply.errorString())

        data = reply.readAll()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)

        self.lblCaptcha.setPixmap(pixmap)


    def reloadCaptcha(self):

        url = QtCore.QUrl(CAPTCHA_URL)
        request = QtNetwork.QNetworkRequest(url)

        self.manager.get(request)




def main():
    app = QtGui.QApplication(sys.argv)
    sys.exit(CaptchaDialog().exec_())


if __name__ == '__main__':
    main()

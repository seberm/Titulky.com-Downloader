import sys
from PyQt4 import QtGui, QtCore, QtNetwork

from PyQt4.QtCore import SLOT, SIGNAL

CAPTCHA_URL = 'http://www.titulky.com/captcha/captcha.php'
MAX_CAPTCHA_LEN = 8


class CaptchaDialog(QtGui.QDialog):


    # Signal is emmited if captcha code is sucessfuly re-typed
    codeRead = QtCore.pyqtSignal()


    def __init__(self, parent = None, flags = 0):
        super(CaptchaDialog, self).__init__(parent)

        self.setWindowTitle('Re-type captcha')

        # Widgets
        self.lblCaptcha = QtGui.QLabel('Loading captcha image ...', self)
        self.lblCaptcha.setFixedSize(200, 70)

        self.btnReload = QtGui.QPushButton('Reload', self)
        self.connect(self.btnReload, SIGNAL("clicked()"), self.reloadCaptcha)
        self.btnSend = QtGui.QPushButton('Send', self)
        self.connect(self.btnSend, SIGNAL("clicked()"), self.sendCode)

        self.leCode = QtGui.QLineEdit(self)
        self.leCode.setFocus()
        self.leCode.setMaxLength(MAX_CAPTCHA_LEN)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.lblCaptcha)
        layout.addWidget(self.btnReload)
        layout.addWidget(self.leCode)
        layout.addWidget(self.btnSend)

        self.setLayout(layout)
        

        # Load captcha into label
        self.manager = QtNetwork.QNetworkAccessManager(self)
        self.connect(self.manager, SIGNAL("finished(QNetworkReply*)"), self.managerFinished)

        self.reloadCaptcha()



    def managerFinished(self, reply):

        if reply.error() != QtNetwork.QNetworkReply.NoError:
            self.lblCaptcha.setText('Error in loading captcha image')
            print(reply.errorString())
            return

        data = reply.readAll()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)

        self.lblCaptcha.setPixmap(pixmap)


    def reloadCaptcha(self):

        url = QtCore.QUrl(CAPTCHA_URL)
        request = QtNetwork.QNetworkRequest(url)

        self.manager.get(request)


    def sendCode(self):

        self.leCode.setDisabled(True)
        self.captchaCode = self.leCode.text()

        # We just emit a signal
        self.codeRead.emit()
        #self.close()



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    sys.exit(CaptchaDialog().exec_())

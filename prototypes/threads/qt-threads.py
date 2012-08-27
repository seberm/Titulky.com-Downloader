#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import sys
import time

titlesLinks = []


class Foo (QtCore.QThread):

    def __init__(self,x):
        self.__x = x
        QtCore.QThread.__init__(self)

    def run (self):
          #print(str(self.__x), end=", ")
          time.sleep(0.20)
          self.emit(QtCore.SIGNAL("newNumber(int)"), self.__x)
          msg = QtGui.QMessageBox()
          msg.setText('ahoj')
          msg.exec_()


    def __del__(self):
        self.exiting = True
        self.wait()


def main():
    threds = []
    for x in range(20):
        threds.append(Foo(x))
    
    # Start all threds
    for t in threds:
        QtCore.QObject.connect(t, QtCore.SIGNAL('newNumber(int)'), append)
        t.start()

    print('all threads started')


def append(i):
    global titlesLinks
    titlesLinks.append('cislo: %d' % i)

def tisk():
    print(list(titlesLinks))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main()



#!/usr/bin/python

import threading
import time

titlesLinks = []


class Foo (threading.Thread):
    def __init__(self,x):
        self.__x = x
        self.__end = False
        threading.Thread.__init__(self)

    def run (self):
          print(str(self.__x), end=", ")
          print('putting to list ')
          #sleep(
          global titlesLinks
          titlesLinks.append('cislo: %d' % self.__x)

threds = []
for x in range(20):
    threds.append(Foo(x))

for t in threds:
    t.start()

print('all threads started')

print(list(titlesLinks))

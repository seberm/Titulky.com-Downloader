# -*- coding: utf-8 -*-

from urllib import request
from urllib import parse
from http import cookiejar
import sys

login = sys.argv[1]
password = sys.argv[2]
remember = 1

cj = cookiejar.CookieJar()
opener = request.build_opener(request.HTTPCookieProcessor(cj))
loginData = parse.urlencode({'Login' : login, 'Password' : password, 'foreverlog' : remember})

opener.open('http://www.titulky.com/index.php', loginData.encode('ascii'))

print(opener.open('http://www.titulky.com/').read())

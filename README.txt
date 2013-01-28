Titulky.com Subtitles Downloader
--------------------------------

- Author: Šabart Otto <seberm[at]gmail[dot]com>
- Jabber: seberm[at]jabber[dot]cz
- Web: http://www.seberm.com
- Bugzilla: http://bugs.seberm.com

Copyright © 2012 Sabart Otto <seberm[at]gmail[dot]com>


About
=====
Downloads subtitles from Titulky.com. First five subtitles is possible
to download. After it's necessary to re-type the captcha security
image (captcha is under development).

If you want download subtitles which are newer than 2 weeks it's necessary
to provide your credentials to the netusers.cz server.

It should work VIP download If you're a user with a VIP account.
(Still looking for somebody who can test it)

For installation read an INSTALL.txt file.


Usage
=====
For program options run:
$ run.sh --help


Downloading titles
==================
For download of subtitles it's necessary to provide their link(s).
$ run.sh --download http://www.titulky.com/Batman-99294.htm

If you just want to get download link, run:
$ run.sh --link http://www.titulky.com/The-Animatrix-144275.htm

In the future will be possible to download titles with direct link:
$ run.sh --direct-link http://www.titulky.com/idown.php?R=1343462842&titulky=0000144275&zip=&histstamp=

For subtitles which are newer than 2 weeks it's necessary to be registered
and provide your login and password to netusers.cz
$ run.sh --login http://www.titulky.com/Cougar-Town-S01E17-202766.htm


Development info
================
- Optional dependencies for program testing:
    - nosetests - http://nose.readthedocs.org/

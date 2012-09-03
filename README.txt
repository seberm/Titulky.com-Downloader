Titulky.com Subtitles Downloader
--------------------------------

- Author: Šabart Otto <seberm[at]gmail[dot]com>
- Jabber: seberm[at]jabber[dot]cz
- Web: http://www.seberm.com
- Bugzilla: http://bugs.seberm.com

Copyright © 2012 Sabart Otto <seberm[at]gmail[dot]com>


About
=====
Downloads subtitles from Titulky.com. First three subtitles is possible to download without waiting. After it it's necessary to retype the captcha security image (captcha is under development).

If you want download subtitles which are newer than 2 weeks it's necessary to provide your credentials to server netusers.cz.

It should work VIP download If you're a user with VIP account.

For installation read file INSTALL.txt


Usage
=====
For program options run:
$ run.sh --help


Downloading titles
==================
For download of titles it's necessary to provide their link(s).
$ run.sh --download http://www.titulky.com/Batman-99294.htm
Sometimes download option is not working and program downloads file which contents text '<h2>Odkaz jetì není funkèní</h2>Pokraèujte tudy na <a href="http://www.titulky.com">titulky</a>'.
So, maybe is better to use following command for now.
$ wget `./run.sh --link http://www.titulky.com/Batman-99294.htm`

If you just want to get download link, run:
$ run.sh --link http://www.titulky.com/The-Animatrix-144275.htm

In the future will be possible to download titles with direct link:
$ run.sh --direct-link http://www.titulky.com/idown.php?R=1343462842&titulky=0000144275&zip=&histstamp=

For subtitles which are newer than 2 weeks it's necessary to be registered and provide your login and password to netusers.cz
$ run.sh --login http://www.titulky.com/Cougar-Town-S01E17-202766.htm

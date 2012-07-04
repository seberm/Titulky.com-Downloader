#!/usr/bin/python

from optparse import OptionParser, OptionGroup

# Globals
NAME = 'titulky_com_downloader'

def main():
    parser = OptionParser(description = '%prog Download subtitles from titulky.com',
                          usage = '%prog [options]',
                          epilog = 'Support: Otto Sabart (www.seberm.com / seberm@gmail.com)')

    options = OptionGroup(parser, "Program Options", "Options specific to titulky_com_downloader.")
    
    #options.add_option("--hel", action="callback", callback=hel, help='Show usage information.')
    options.add_option('-l', '--link', dest='link', action='store_true')
    options.add_option('-e', '--encoding', dest='encoding', action='store')

    parser.add_option_group(options)

    (opt, args) = parser.parse_args()
    print(args)
    if opt.link:
        print('link....')

def hel(*args):
    print('''some func name: {Name}'''.format(Name=NAME))


if __name__ == '__main__':
    main()

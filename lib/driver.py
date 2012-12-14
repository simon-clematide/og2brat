#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import xml_to_brat

"""
Erwartet wird einer der OptionParsers und ein Argument:
als erstes Argument den Ordner zu den .xml Dateien
als zweites Argument den Ordner und Dateiname (ohne Endung)
    bei -f wird es arg[0].txt
    bei -t, -c und -s wird es arg[0].ann
"""

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file",
                     help="write text from FILE to [arg0].txt", metavar="FILE")
    parser.add_option("-t", "--term", dest="term",
                     help="create termannotation from FILE to [arg0].txt", metavar="FILE")
    parser.add_option("-c", "--chunk", dest="chunk",
                     help="create chunkannotation from FILE to [arg0].txt", metavar="FILE")
    parser.add_option("-s", "--syntax", dest="syntax",
                     help="create syntaxannotation from FILE to [arg0].txt", metavar="FILE")

    (options, args) = parser.parse_args()

    if options.file or options.term or options.chunk or options.syntax:
        if options.file:
            xml_to_brat.to_txt(options.file.replace("=",""), args)

        if options.term:
            xml_to_brat.term(options.term.replace("=",""), args)

        if options.chunk:
            xml_to_brat.chunk(options.chunk.replace("=",""), args)

        if options.syntax:
            xml_to_brat.syntax(options.syntax.replace("=",""), args)

    else:
        print 'ERROR -- Necessary command line options not given!'
        print parser.print_help()

if __name__ == '__main__':
    main()



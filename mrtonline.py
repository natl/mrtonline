#!/bin/python
# -*- coding: UTF-8 -*-
###############################################################################
###
###  Main executable for mrtonline
###  Author: Nathanael Lampe
###  Created: June 2015
###  Last Modified: June 16, 2015
###
###  Brief summary:
###  MRT tables are a well defined standard used in astrophysics publications
###  The classes contained here provide containers for each column of an MRT
###  table.
###
###############################################################################

from __future__ import division, unicode_literals, print_function
from webtable import WebTable
import sys

helpStrings = ['-h', '--help']
usage = '''Usage: mrtonline.py FILENAME ERROR_PREFIX'''

def main(filename, errorPrefix):
    """
    """
    webtable = WebTable(filename, errorPrefix)

    outfile = open("resources/index.htm", 'w')
    
   
    headpage =  file2string("resources/html/head.htm")
    headmap = webtable.getUnitsMap()
    headpage = headpage.replace(r'/*INSERT_UNITS_MAP*/', headmap)
    outfile.write(headpage)
 
    outfile.write(file2string("resources/html/prenavbar.htm"))
    
    nbpage = file2string("resources/html/navbar.htm")
    nblist = webtable.getDropdownListAsHTML()
    nbpage = nbpage.replace(r'<!--INSERT_DROPDOWN-->', nblist)
    outfile.write(nbpage)

    outfile.write(file2string("resources/html/home-jumbotron.htm"))

    tbpage = file2string("resources/html/table-jumbotron.htm")
    table = webtable.getTableAsHTML()
    tbpage = tbpage.replace(r'<!--INSERT_TABLE-->', table)
    outfile.write(tbpage)
    
    plotPage = file2string("resources/html/plotting-jumbotron.htm")
    xselector = webtable.getPlottingDropDownList('xdataselector')
    yselector = webtable.getPlottingDropDownList('ydataselector')
    plotPage = plotPage.replace(r'<!--INSERT_XSELECTOR-->', xselector)
    plotPage = plotPage.replace(r'<!--INSERT_YSELECTOR-->', yselector)
    outfile.write(plotPage)

    outfile.write(file2string("resources/html/footer.htm"))


def file2string(filename):
    """
    """
    f = open(filename, 'r')
    out = f.read()
    f.close()
    return unicode(out)



if __name__ == "__main__":
    if sys.argv[1] in helpStrings:
        print(usage)
        sys.exit()

    assert sys.argv[1], usage
    filename = sys.argv[1]
    try:
        errorPrefix = sys.argv[2]
    except IndexError:
        errorPrefix = ''

    main(filename, errorPrefix)


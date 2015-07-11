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
import os
import shutil

cssDir = r'resources/css'
jsDir = r'resources/js'
helpStrings = ['-h', '--help']
usage = '''Usage: mrtonline.py FILENAME OUTPUT_DIR [-e ERROR_PREFIX] [-r]\n
-r enables overwrite of output directory'''

def main(filename, outputDir, errorPrefix, overwrite):
    """
    """

    webtable = WebTable(filename, errorPrefix)
    
    outfile = open(outputDir+"/index.htm", 'w')
    
   
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

    #copy resources to output directory:
    try:
        shutil.copytree(cssDir, outputDir+"/css")
        shutil.copytree(jsDir, outputDir+"/js")
    except OSError:
        print("CSS and js directories seem to already exist, they have not "+
            "had new code added to them")

def file2string(filename):
    """
    """
    f = open(filename, 'r')
    out = f.read()
    f.close()
    return unicode(out)



if __name__ == "__main__":

    if len(set(sys.argv) & set(helpStrings)) !=0 :
        print(usage)
        sys.exit()


    assert sys.argv[1], usage
    filename = sys.argv[1]
    #Check filename is valid
    assert os.path.exists(filename), '''Error: input does not exist'''

    assert sys.argv[2], usage
    outputDir = sys.argv[2]
    #remove any trailing slash
    if outputDir[-1] == r"/": outputDir = outputDir[:(len(outputDir)-1)]

    #The rest of the verifaction for the output dir is done later
    
    #options
    #error prefix
    errorPrefix = ""
    if '-e' in sys.argv:
        errorPrefix = sys.argv[ sys.argv.index('-e')+1 ]

    #overwrite
    overwrite = False
    if '-r' in sys.argv:
        overwrite = True

    if os.path.exists(outputDir):
        if overwrite == False: sys.exit('Output directory exists, use -r to '+
            'allow it to be overwritten')
        if not os.path.isdir(outputDir): sys.exit('Output is not a directory')
    else:
        os.mkdir(outputDir)

    main(filename, outputDir, errorPrefix, overwrite)


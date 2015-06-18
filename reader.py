###############################################################################
###
###  Data container class definitions for the MRTOnline script
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
from dataclasses import *
from astropy.io.ascii import read as asciiread

class MRTTableLoader(object):
    """
    """
    def __init__(self, tableFileName):
        """
        """
        self.columns = []
        #open file
        table = asciiread(tableFileName)
        colnames = table.colnames
        
        #load columns
        for name in colnames:
            #are there errors?
            #TODO add asymmetric errors
            if 'e'+name in colnames:
                colnames.remove('e'+name)
                errors = 1
            else:
                errors = 0
            
            #create a column
            col = DataColumn(t.name, t.unit, t.description, dt = t.dtype,
                errors = errors)
            self.columns.append(col)

        #put string data into column members
        for col in self.columns:
            if col.errors == 0:
                #get the right column from astropy
                vals = table.columns[col.label]
                for val in vals:
                    #delegate the formatting of the string to astropy
                    col.append(val.__str__().strip())

            elif col.errors == 1:
                #get the right column from astropy
                vals = table.columns[col.label]
                errvals = table.columns['e'+col.label]
                for (val,errval) in zip(vals, errvals):
                    #delegate the formatting of the string to astropy
                    col.append(val.__str__().strip(),
                        errval.__str__().strip())

            elif col.errors == 2:
                raise NotImplementedError('Asymmetric errors are not '+
                    'yet implemented')

            else:
                #This case *should* be impossible, diagnostic test
                raise RuntimeError('The error value for ' + col.label +
                    ' is defined outside the acceptable range')

    def getDropdownListAsHTML(self):
        """
        """
        toggleMenu = ''
        for col in self.columns:
            toggleMenu += r'<li><label class="checkbox">'
            toggleMenu += r'<input name="{0.label}" type="checkbox"/>'.format(
                col)
            toggleMenu += r'{0.label}'.format(col)
            toggleMenu += r'</label></li>'

        return toggleMenu

    def getTableAsHTML(self):
        """
        """
        tableString = ''
        key = self.columns[0]
        n_entries = len(key)
        n_cols = len(self.columns)
        for ii in xrange(0, n_entries):

            tableString += r'<tr class="{0}">'.format(key[ii])
            tableString += r'<td class="{0.name}"

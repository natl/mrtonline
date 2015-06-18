#!/bin/python
# -*- coding: UTF-8 -*-
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

import sys

from astropy.io.ascii import read as asciiread

class WebTable(object):
    """
    """
    def __init__(self, tableFileName, uncertainty_str = None):
        """
        """
        #open file
        self.table = asciiread(tableFileName)
        self.uncertainty_str = uncertainty_str
        
        for colname in self.table.colnames:
            self.table.columns[colname].hasUncertaintyWT = False
            self.table.columns[colname].isUncertaintyWT  = False

        if uncertainty_str != None:
            assert type(uncertainty_str) == str, ('uncertainty_str should' +
                ' be a string that preceeds a parameter label to flag errors')
            for colname in self.table.colnames:
                ucolname = self.getUColName(colname)
                if ucolname != False:
                    #Here, we add flags to each column to indicate uncertainty
                    self.table.columns[colname].hasUncertaintyWT = True
                    self.table.columns[colname].isUncertaintyWT  = False
                    self.table.columns[ucolname].hasUncertaintyWT = False
                    self.table.columns[ucolname].isUncertaintyWT  = True


    def getUColName(self, colname):
        """
        """
        colnames_lower = [x.lower() for x in self.table.colnames]
        ucolname_lower = (self.uncertainty_str+colname).lower()
        try:
           idx = colnames_lower.index(ucolname_lower)
           return self.table.colnames[idx]
        except ValueError:
            return False
    
        

    def getDropdownListAsHTML(self):
        """
        Return the HTML code for the dropdown list
        Will not yield checkboxes for uncertainty quantities
        """
        toggleMenu = ''
        for colname in self.table.colnames:
            if self.table.columns[colname].isUncertaintyWT == False:
                toggleMenu += (r'<li><label class="checkbox">' + 
                    r'<input name="{0.name}" type="checkbox"/>' + 
                    r'{0.name}</label></li>').format(
                    self.table.columns[colname])

        return toggleMenu

    def getTableAsHTML(self):
        """
        """
        tableString = ''
        key = self.table.columns[0]
        n_entries = len(key)
        n_cols = len(self.table.columns)
        #make the table start code
        tableString += (r'<table class="table table-hover table-condensed '+
            r'tablesorter table-striped">')

        #add the header
        tableString += r'<thead>'+'\n'
        headerrow = r'<tr>'
        unitsrow  = r'<tr>'
        for colname in self.table.colnames:
            hasUnit = True if self.table.columns[colname].unit != '' else False
            hasUncertainty = self.table.columns[colname].hasUncertaintyWT
            if self.table.columns[colname].isUncertaintyWT == False:
                if hasUnit and hasUncertainty:
                    #uncertainty+units
                    headerrow += (r'<th class="{0.name}" ' +
                        r'title="{0.description}">{0.name}</th>' + 
                        r'<th class="{0.name}" ' +
                        r'title="{0.description}">±ẟ</th>').format(
                        self.table.columns[colname])
                    unitsrow += (r'<td class="{0.name}" colspan=2 ' + 
                        r'title="{0.description}">{0.unit}</td>').format(
                        self.table.columns[colname])

                if (not hasUnit) and hasUncertainty:
                    #uncertainty only
                    headerrow += (r'<th class="{0.name}" rowspan=2 ' +
                        r'title="{0.description}">{0.name}</th>' + 
                        r'<th class="{0.name}" rowspan=2 ' +
                        r'title="{0.description}">±ẟ</th>').format(
                        self.table.columns[colname])

                if hasUnit and (not hasUncertainty):
                    #no uncertainty with units
                    headerrow += (r'<th class="{0.name}" ' +
                        r'title="{0.description}">{0.name}</th>').format(
                        self.table.columns[colname])
                    unitsrow += (r'<th class="{0.name}" ' + 
                        r'title="{0.description}">{0.unit}</td>').format(
                        self.table.columns[colname])
                if (not hasUnit) and (not hasUncertainty):
                    #no uncertainty no units
                    headerrow += (r'<th class="{0.name}" rowspan=2 ' +
                        r'title="{0.description}">{0.name}</th>').format(
                        self.table.columns[colname])
        headerrow += r'</tr>'+'\n'
        unitsrow += r'</tr></thead>'+'\n'
        tableString += headerrow
        tableString += unitsrow
        
        tableString += r'<tbody>'
        #make the data bits
        for ii in xrange(0, n_entries):
            tableString += r'<tr class="{0}">'.format(key[ii])
            for colname in self.table.colnames:
                if self.table.columns[colname].isUncertaintyWT == False:
                    #check this isn't an uncertainty column
                    tableString += r'<td class="{0.name}">{1}</td>'.format(
                        self.table.columns[colname],
                        self.table.columns[colname][ii].__str__().strip())
                    if self.table.columns[colname].hasUncertaintyWT == True:
                        #print the associated uncertainty column if it exists
                        ucolname = self.getUColName(colname)
                        tableString += r'<td class="{0.name}">{1}</td>'.format(
                            self.table.columns[colname],
                            self.table.columns[ucolname][ii].__str__().strip())
            tableString += r'</tr>'+'\n'
        tableString += r'</tbody></table>'

        return tableString




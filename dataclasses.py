###############################################################################
###
###
###
###
###
###############################################################################

from __future__ import division, unicode_literals, print_statement


class DataColumn():
    def __init__(self):
        """
        """
        #Initialise member variables
        self.values = []

        #strings
        self.label    = ''
        self.fmt      = ''
        self.unit     = ''
        self.desc     = ''


        #ints
        self.firstbyte = 0 
        self.lastbyte  = 0

        #switch paramaters
        #Describes whether errors exist
        # 0 : no uncertainty
        # 1 : symmetric uncertainties
        # 2 : asymmetric uncertainties
        self.errors = 0

        return True

    def __str__(self):
        """
        """
        return True

    def printHeader(self):
        """
        """
        return True

    def printSortFunction(self):
        """
        """
        return True

    def printValue(self):
        """
        """
        return True

    def addItem(self, value):
        """
        """
        self.values.append(value)
        return True


class StringColumn(DataColumn):
    def __init__(self, label, fmt, unit, desc, firstbyte, lastbyte):
        """

        """
        #initialise member variables
        self.values = []
        
        self.label = label
        self.fmt = fmt
        self.unit = unit
        self.desc = desc

        self.firstbyte = firstbyte
        self.lastbyte  = lastbyte

        self.errors = 0

        return True




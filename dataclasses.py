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


class DataColumn(object):
    """
    Represents a column of string values
    """
    def __init__(self, label, unit, desc, errors = 0):
        """
        """
        #Initialise member variables
        self.values = []

        #strings
        self.label    = label
        self.dtype    = str
        self.unit     = unit
        self.desc     = desc
        
        '''
        Use a dtype instead of fmt tags
        #process the fmt tag
        self.letter = fmt[0]
        sp = fmt.split('.')
        self.width = sp[0][1:]
        self.precision = sp[1] if len(split) == 2 else '0'
        '''

        #ints
        self.firstbyte = firstbyte
        self.lastbyte  = lastbyte

        #set column errors
        self.setColumnErrors(errors)

        return True


    def __len__(self):
        """
        """
        return self.values.__len__()

    def __getitem__(self, key):
        """
        """
        return self.values[key]

    def __setitem__(self, key, val):
        """
        """
        self.values[key] = val
        return None

    def __delitem__(self, key):
        del self.values[key]
        return None

    def __str__(self):
        """
        """
        return (super(DataColumn, self).__str__() + '\n' +
                'Column label  : {0.label}\n' +
                'Column dtype  : {0.dtype}\n'   +
                'Column unit   : {0.unit}\n'  +
                'Column desc   : {0.desc}\n'  +
                'Entries       : {0.__len__()}'.format(self))

    def value2string(self, idx):
        """
        """
        return str(self.values[idx])

    def setColumnErrors(self, errorcode):
        """
        """
        #defensive assertions. Aim to prevent any errors from slipping through
        assert errorcode in [0,1,2], ('Only error codes 0 (no errors),' + 
            ' 1 (symmetric errors) and 2 (asymmetric errors) are currently' + 
            ' supported')
        assert len(self.values) == 0, ('It is necessary to set column errors' +
            'before adding any entried to the column')

        if errorcode == 0:
            self.errors = 0
        elif errorcode == 1:
            self.errors = 1
            self.errorvaluesupper = []
        elif errorcode == 2:
            self.errors = 2
            self.errorvaluesupper = []
            self.errorvalueslower = []
        else:
            return False
        return True

    def printTableHeader(self, idx):
        """
        """
        fst = r'<th class="{0.label}" title="{0.desc}">'.format(self)
        mid = self.label
        lst = r'</th>'
        return fst + mid + lst

    def printSortFunction(self):
        """
        """
        return True

    def printTableData(self, idx):
        """
        """
        fst = r'<td class="{0.label}">'.format(self)
        mid = self.value2string(idx)
        lst = r'</td>'
        return fst + mid + lst

    def append(self, value):
        """
        """

        self.values.append(value)
        return True

    def value2string(self, idx):
        """
        """
        if errorcode == 0:
            return '{0}'.format(self.values[idx]))
        if errorcode == 1:
            return '{0}±{1}'.format(self.values[idx], self.errupper[idx])
        if errorcode == 2:
            raise NotImplementedError('Asymmetric Errors Are Not Implemented')


class StrColumn(DataColumn):
    """
    """
    pass


class FloatColumn(DataColumn):
    """
    """
    def value2string(self, idx):
        """
        """
        if errorcode == 0:
            return '{0:{w}.{p}f}'.format(self.values[idx], w = self.width,
                p = self.precision)
        #TODO Implement printing of errorbars
        if errorcode == 1:
            return '{0:{w}.{p}f}'.format(self.values[idx], w = self.width,
                p = self.precision)

        if errorcode == 2:
            return '{0:{w}.{p}f}'.format(self.values[idx], w = self.width,
                p = self.precision)


    def append(self, value, errupper = None, errlower = None ):
        """
        """
        #cases with defensive assertions
        if self.errors == 0:
            assert (errupper == None) and (errlower == None), ('No error ' +
                'values have been set, so only the column value may be ' +
                'appended')
            self.values.append(float(value))

        elif self.errors == 1:
            assert (errupper != None) and (errlower == None), ('Asymptotic ' +
                'error values have been set, so a value and uncertainty ' +
                'need to be appended together')
            self.values.append(float(value))
            self.errorvaluesupper.append(float(errupper))


        elif self.errors == 2:
            assert (errupper != None) and (errlower != None), ('Asymmetric' +
                'error values have been set, so the value must be accompanied' +
                ' by its associated two errors')
            self.values.append(float(value))
            self.errorvaluesupper.append(float(errupper))
            self.errorvalueslower.append(float(errlower))
        else:
            return False
        return True

class IntColumn(DataColumn):
    """
    """

    def value2string(self, idx):
        """
        """
        return '{0:i}'.format(self.values[idx])

    def append(self, value):
        """
        """
        self.values.append(int(value))


'''
Created on 23 Nov 2013

Tools for processing text files into a variety of objects

Generic reader has function:
make_parser : creates the correct parser for that filetype
which is called in init and sets up the correct parser object

genericreader.read calls the read function of the parser object

Parser: on init, gets the file handle (i.e opens the file)


@author: james
'''
import csv

_parser_defaults = {
    'delimiter' : None,
    'nrows' : None,
    'chunksize' : None,
    'header' : None,
    'na_value' : 'NaN',
    'skip_rows' : None,
    'filetype' : 'infer'}

def _read(path):
    parser = GenericReader(path) # add kwds
    
    parser.read()

class GenericReader(object):
    '''
    classdocs
    '''


    def __init__(self, path, **kwds):
        '''
        Constructor
        '''
        
        self.parser = None
        self.f = path
        
        # The reader should be in keyword arguments. If not, default to...?
        
        self._make_parser(path)
        
        
    def _get_options(self):    
        pass
        
    def _make_parser(self, path):
        '''
        Creates the correct parser for this file type
        '''
        
        
        
    def read(self):
        
        self.parser.read()
        
        ## If read_protocol, must return only a profile class (with quadrapoles)
        ## If read electrodes, returns a polyline class (a line of electrodes)
        
    def __iter__(self):
        
        try:
            if self.chunksize:
                while True:
                    yield self.read(self.chunksize)
            else:
                yield self.read()
        except StopIteration:
            pass
        
    
    
    
class R2Parser():
    """ Parser for R2 files """
    
    def __init__(self, f):
        pass
        
        
    def read(self):
        pass
    
    
    def _make_reader(self, f):
        """ This function should create a csv.reader instance with the appropriate dialect """
        
        self.data = csv.reader(f) #Need to add dialect


class R2Protocol(R2Parser):
    
    def __init__(self, f):
        R2Parser.__init__(self, f)
        
    
    
class R2In(R2Parser):
    
    def __init__(self):
        pass        
    
def _get_handle(path, mode):
    
    f = open(path, mode)
    return f
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

class GenericReader(object):
    '''
    classdocs
    '''


    def __init__(self, path):
        '''
        Constructor
        '''
        self.parser = None
        
        self._make_parser(path)
        
        
    def _make_parser(self, path):
        '''
        Creates the correct parser for this file type
        '''
        
        
        
    def read(self):
        
        self.parser.read()
        
        
        
    
    
    
class R2Parser():
    """ Parser for R2 files """
    
    def __init__(self, f):
        pass
        
        
    def read(self):
        pass
    
    
    def _make_reader(self):
        """ This function should create a csv.reader instance with the appropriate dialect """


class R2Protocol(R2Parser):
    
    def __init__(self):
        pass
    
class R2In(R2Parser):
    
    def __init__(self):
        pass        
    
def _get_handle(path, mode):
    
    f = open(path, mode)
    return f
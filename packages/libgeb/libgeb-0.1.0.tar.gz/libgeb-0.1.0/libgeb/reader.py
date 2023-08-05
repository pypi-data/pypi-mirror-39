import libgeb
import libgenomic
import os
#import mmap
import libdna
import struct
import sys
import json


class BufferedReader(object):
    BUFFER_SIZE = 8192
    
    """
    Memory mapped file wrapper.
    
    Parameters
    ----------
    file : str
        Path to file.
    """
    def __init__(self, file):
        self.__file = file
        self.__reader = None
        # memory-map the file, size 0 means whole file
        #self.__reader = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    
    @property
    def file(self):
        return self.__file
    
    @property
    def reader(self):
        if self.__reader is None:
            self.__reader = open(self.file, 'rb', buffering=BufferedReader.BUFFER_SIZE)
        return self.__reader
    
    def seek(self, address):
        return self.reader.seek(address)
    
    def read(self, n=1):
        return self.reader.read(n)
    
    def read_int(self):
        return struct.unpack('>I', self.read(4))[0]
    
    def read_short(self):
        return struct.unpack('>H', self.read(2))[0]
    
    def read_double(self):
        return struct.unpack('>d', self.read(8))[0]
        
    def read_byte(self):
        return struct.unpack('>B', self.read())[0]
       
    def read_char(self):
        return self.read().decode('utf-8')
    
    def read_string(self, n):
        return self.read(n).decode('utf-8')
    
    def read_varchar(self):
        return self.read_string(self.read_byte())
    
    @property
    def tell(self):
        return self.reader.tell()
    
    def close(self):
        self.reader.close()
    

class BinaryReader(object):
    """
    Base class binary reader.
    
    Parameters
    ----------
    dir : str
        Directory where geb files are located.
    genome : str
        Genome
    chr : str, optional
        If reader is chromosome specific, supply chr, e.g. 'chr1'.
    window : int, optional
        Size of bins in bp.
    """
    
    def __init__(self, dir, prefix, genome, chr=None, window=libgeb.DEFAULT_WINDOW):
        self.__dir = dir
        self.__prefix = prefix
        self.__genome = genome
        self.__chr = chr
        self.__window = window
        self.__reader = None
    
    @property
    def reader(self):
        """
        Return the reader
        """
        
        if self.__reader is None:
            file = os.path.join(self.__dir, self.get_file_name())
            self.__reader = BufferedReader(file)

        return self.__reader
    
    def close(self):
        self.reader.close()
    
    @property
    def dir(self):
        return self.__dir
    
    @property
    def file(self):
        return self.reader.file
    
    @property
    def prefix(self):
        return self.__prefix

    @property
    def chr(self):
        return self.__chr

    @property
    def window(self):
        return self.__window

    @property
    def genome(self):
        return self.__genome

    def get_file_name(self, chr):
        return ''

    def seek(self, address):
        self.reader.seek(address)
    
    @property
    def tell(self):
        return self.reader.tell

    def read(self, n=1, address=-1):
        if address > 0:
            self.seek(address)
            
        return self.reader.read(n)

    def read_byte(self, address=-1):
        if address > 0:
            self.seek(address)
            
        return self.reader.read_byte()

    def read_int(self, address=-1):
        if address > 0:
            self.seek(address)
        
        return self.reader.read_int()
    
    def read_short(self, address=-1):
        if address > 0:
            self.seek(address)
        
        return self.reader.read_short()
  
    def read_double(self, address=-1):
        if address > 0:
            self.seek(address)
            
        return self.reader.read_double()
    
    def read_varchar(self, address=-1):
        if address > 0:
            self.seek(address)
            
        return self.reader.read_varchar()
    
    def read_char(self, address=-1):
        if address > 0:
            self.seek(address)
            
        return self.reader.read_char()


class BinReader(BinaryReader):
    N_BYTES_OFFSET = libgeb.WINDOW_BYTE_OFFSET + libgeb.INT_BYTES

    HEADER_BYTES_OFFSET = N_BYTES_OFFSET + libgeb.INT_BYTES


    """
    Create a new bin reader for scanning chromosome bins
    
    Parameters
    ----------
    dir : str
        Directory of geb files.
    genome : str
        Genome of interest, e.g. 'hg19'
    chr : str
        Chromosome of interest, e.g. 'chr1'.
    window : int
        Bin size.
    """
    def __init__(self, dir, prefix, genome, chr, window=libgeb.DEFAULT_WINDOW):
        super().__init__(dir, prefix, genome, chr=chr, window=window)

    def _read_bin_address(self, bin):
        self.seek(BinReader.HEADER_BYTES_OFFSET + bin * libgeb.INT_BYTES)
        return self.reader.read_int()
        
    
    def _bin_addresses_from_bins(self, bins):
        """
        Return the addresses of bins given a set of bins of interest.
        
        Parameters
        ----------
        bins: list
            Integer list of bins
            
        Returns
        -------
        list
            Integer list of bin addresses in file.
        """
        
        n = len(bins)
    
        ret = []
    
        for i in range(0, n):
          ret.append(self._read_bin_address(bins[i]))
          
        return ret
    
    
    def _element_addresses_from_bins(self, bin_addresses):
        ret = []

        for ba in bin_addresses:
            self.seek(ba)

            size = self.reader.read_int()
            
            used = set()
            
            for i in range(0, size):
                ga = self.reader.read_int()
    
                if ga not in used:
                    ret.append(ga)
                    used.add(ga)
            
        return ret
    
    def element_addresses(self, loc):
         sb = loc.start // self.window
         eb = loc.end // self.window
         bins = [i for i in range(sb, eb + 1)]
         bin_addresses = self._bin_addresses_from_bins(bins)
         ret = self._element_addresses_from_bins(bin_addresses)
         return ret
     
     
    def get_file_name(self):
        return libgeb.get_bins_file_name(self.prefix, self.chr)
    

class BTreeReader(BinaryReader):
    BINS_BYTES_OFFSET = libgeb.WINDOW_BYTE_OFFSET + libgeb.INT_BYTES
    HEADER_BYTES_OFFSET = BINS_BYTES_OFFSET + libgeb.INT_BYTES
    BTREE_CHILD_ADDRESSES_BYTES = 2 * libgeb.INT_BYTES

  
    def __init__(self, dir, prefix, genome, chr, window=libgeb.DEFAULT_WINDOW):
        super().__init__(dir, prefix, genome, chr=chr, window=window)
   
    def _bin_address_from_bin(self, bin):
        self.seek(BTreeReader.HEADER_BYTES_OFFSET);
    
        search = True

        while search:
            b = self.read_int()
            ba = self.read_int()
            la = self.read_int()
            ra = self.read_int()
            
            if bin < b:
                if la > 0:
                    self.seek(la)
                else:
                    # return closest bin
                    return ba #-1
            elif bin > b:
                if ra > 0:
                    self.seek(ra)
                else:
                    # return closest bin
                    return ba #-1
            else:
                # found the bin of interest
                return ba
        
        return -1
  
  
    def _bin_addresses_from_tree(self, address1, address2): #tree_bin_addresses):
        ret = []
        
        self.seek(address1)
        
        print(address1, address2, self.file)
        
        while self.tell <= address2:
            ret.append(self.read_int())
        
        #for address in tree_bin_addresses:
        #    self.seek(address)
        #    ret.append(self.read_int())

        return ret

    def _element_addresses_from_bins(self, bin_addresses):
        ret = []
        
        for ba in bin_addresses:
            self.seek(ba)
            
            n = self.read_int()
            
            for i in range(0, n):
                ret.append(self.read_int())

        return ret
    

    def element_addresses(self, loc):
        sb = loc.start // self.window
        eb = loc.end // self.window

        b1 = self._bin_address_from_bin(sb)
        b2 = self._bin_address_from_bin(eb)
    
        bin_addreses = self._bin_addresses_from_tree(b1, b2) #tree_bin_addresses)

        element_addresses = self._element_addresses_from_bins(bin_addreses)

        return element_addresses
    
    def get_file_name(self):
        return libgeb.get_btree_file_name(self.prefix, self.chr)
    

class DataReader(BinaryReader):
    def __init__(self, dir, prefix, genome, window=libgeb.DEFAULT_WINDOW):
        super().__init__(dir, prefix, genome, window)
    
    def get_file_name(self):
        return libgeb.get_data_file_name(self.prefix)
    

class ElementReader(BinaryReader):
    N_BYTES_OFFSET = libgeb.WINDOW_BYTE_OFFSET + libgeb.INT_BYTES
    HEADER_BYTES_OFFSET = N_BYTES_OFFSET + libgeb.INT_BYTES

    def __init__(self, data_reader, dir, prefix, genome, window=libgeb.DEFAULT_WINDOW):
        super().__init__(dir, prefix, genome, window)
        self.__data_reader = data_reader
    
    @property
    def data_reader(self):
        return self.__data_reader
    
    def read_tag(self):
        address = self.read_int()
        pos = self.reader.tell()
        ret = self.data_reader.read_varchar(address)
        self.reader.seek(pos)
        return ret
    
    
    def read_tags(self):
        n = self.read_byte()
        
        ret = [''] * n
        
        for i in range(0, n):
            ret[i] = self.read_tag()
            
        return ret
    
    
    def read_strand(self):
        s = self.read_byte()
        
        if s == 0:
            return '+'
        else:
            return '-'
        
    
    def _read_chr(self):
        return self.data_reader.read_varchar(self.read_int())
    
    def _read_location(self):
        c = self._read_chr()
        s = self.read_int()
        e = self.read_int()
        
        return libdna.Loc(c, s, e)
    
    
    def read_property(self, e):
        name_address = self.read_int()

        t = self.read_byte()
    
        value_address = self.read_int()

        name = self.data_reader.read_varchar(name_address)
 
        if t == 2:
            e.set_property(name, self.data_reader.read_double(value_address))
        elif t == 1:
            e.set_property(name, self.data_reader.read_int(value_address))
        else:
            e.set_property(name, self.data_reader.read_varchar(value_address))
    
    
    def read_properties(self, e):
        n = self.read_byte()

        for i in range(0, n):
            self.read_property(e)

        return n

    def _create_element(self):
        level = self.data_reader.read_varchar(self.read_int())

        loc = self._read_location()
        
        strand = self.read_strand()
        
        element = libgenomic.GenomicElement(loc.chr, loc.start, loc.end, level, strand)

        self.read_properties(element)

        return element
    
    
    def _read_element(self, ret, level='', depth=0, parent=None):
        element = self._create_element()

        correct = element.level == level or (depth == 0 and level == '')
        
        # number of children
        n = self.read_short()
        
        for i in range(0, n):
            self._read_element(level, ret, depth=(depth + 1), parent=(element if correct else None))

        if parent is not None:
            parent.add(element)
            
        if correct:
            ret.append(element)
            
            
    def read_elements(self, addresses, level=''):
        ret = []

        for address in addresses:
            self.seek(address)
            self._read_element(ret, level=level)

        return ret
    
    
    def _get_n(self):
        self.seek(ElementReader.N_BYTES_OFFSET)
        return self.read_int()
 
    
    def read_all(self, level=''):
        n = self._get_n()

        ret = []

        for i in range(0, n):
            self._read_element(ret, level=level)

        return ret
    
    
    def get_file_name(self):
        return libgeb.get_elements_file_name(self.prefix)
        
        
class RadixReader(BinaryReader):
    HEADER_BYTES_OFFSET = libgeb.WINDOW_BYTE_OFFSET + libgeb.INT_BYTES
  
    RADIX_TREE_PREFIX_BYTES = 1 + libgeb.INT_BYTES


    def __init__(self, dir, prefix, genome, window=libgeb.DEFAULT_WINDOW):
        super().__init__(dir, prefix, genome, window)
  
    def get_file_name(self):
        return libgeb.get_radix_file_name(self.prefix)

    def element_addresses(self, id, exact=False):
        self.seek(RadixReader.HEADER_BYTES_OFFSET)

        leafc = 0
        address = 0
        n = 0

        for c in id:
            n = self.read_byte()

            #assume we won't find a match
            found = False

            for i in range(0, n):
                leafc = self.read_char()
                address = self.read_int()
        
                if leafc == c:
                    # we did find a match so keep going
                    found = True
                    self.seek(address)
                    break
                
            if not found:
                break
    
        if not found:
            return []

        self.read(self.read_byte() * RadixReader.RADIX_TREE_PREFIX_BYTES)

        ret = []

        n = self.read_int()

        for i in range(0, n):
            ret.append(self.read_int())
    
        if exact:
            return ret
        
        n = self.read_int()

        for i in range(0, n):
            ret.append(self.read_int())
            
        return ret

     
class GEBReader(object):
    def __init__(self, dir, prefix, genome, window=libgeb.DEFAULT_WINDOW):
        self.__dir = dir
        self.__prefix = prefix
        self.__genome = genome
        self.__window = window
        self.__current_chr = None
        #self.__bin_reader = None
        self.__btree_reader = None
        self.__data_reader =  None
        self.__radix_reader = None
        self.__element_reader = None

    def close(self):
        """
        Close currently opened file handles.
        """
        
        self.data_reader.close()
        self.element_reader.close()
        
        #if self.__bin_reader is not None:
        #    self.__bin_reader.close()
            
        if self.__btree_reader is not None:
            self.__btree_reader.close()
    
    @property
    def dir(self):
        return self.__dir
    
    @property
    def prefix(self):
        return self.__prefix
    
    @property
    def genome(self):
        return self.__genome
    
    @property
    def window(self):
        return self.__window
           
#    def bin_reader(self, loc):
#        # Cache current chr
#        if loc.chr != self.__current_chr or self.__reader is None:
#            self.__bin_reader = BinReader(self.dir, self.prefix, self.genome, chr=loc.chr, window=self.window)
#            self.__current_chr = loc.chr
#            
#        return self.__bin_reader
    
    def btree_reader(self, loc):
        # Cache current chr
        if loc.chr != self.__current_chr or self.__reader is None:
            self.__btree_reader = BTreeReader(self.dir, self.prefix, self.genome, chr=loc.chr, window=self.window)
            self.__current_chr = loc.chr
            
        return self.__btree_reader

    @property
    def radix_reader(self):
        # Cache current chr
        if self.__radix_reader is None:
            self.__radix_reader = RadixReader(self.dir, self.prefix, self.genome, window=self.window)
            
        return self.__radix_reader
    
    @property
    def data_reader(self):
        # Cache current chr
        if self.__data_reader is None:
            self.__data_reader = DataReader(self.dir, self.prefix, self.genome, window=self.window)
            
        return self.__data_reader
    
    @property
    def element_reader(self):
        # Cache current chr
        if self.__element_reader is None:
            self.__element_reader = ElementReader(self.data_reader, self.dir, self.prefix, self.genome, self.window)
            
        return self.__element_reader
    

    @staticmethod
    def _find_closest(loc, genes, min_bp=1):
        ret = []
        
        for gene in genes:
            overlap = libgenomic.overlap(loc.chr, loc.start, loc.end, gene.chr, gene.start, gene.end)

            if overlap is not None and overlap.length >= min_bp:
                ret.append(gene)

        return ret
    
    @staticmethod
    def _overlapping(loc, elements, min_bp=1):
        ret = []
        
        for element in elements:
            overlap = libgenomic.overlap(loc.chr, loc.start, loc.end, element.chr, element.start, element.end)

            if overlap is not None and overlap.length >= min_bp:
                ret.append(element)

        return ret
    

    def _find(self, loc, level=''):
        loc = libdna.parse_loc(loc)

        addresses = self.btree_reader(loc).element_addresses(loc)
        
        ret = self.element_reader.read_elements(addresses, level=level)

        return ret
    
    
    def closest_elements(self, loc, level):
        genes = self._find(loc, level)

        mid = (loc.end + loc.start) // 2
        minD = sys.maxint

        for gene in genes:
            d = abs(mid - gene.start) # GenomicRegion.mid(gene))

            if d < minD:
                minD = d
        
        ret = []
        
        for gene in genes:
            d = abs(mid - gene.start)

            if d == minD:
                ret.append(gene)

        return ret
    
    
    def find(self, loc, level=''):
        loc = libdna.parse_loc(loc)
        
        elements = self._find(loc, level=level)
        
        return GEBReader._overlapping(loc, elements)
    
    def get_elements(self, id, level, exact=False):
        addresses = self.radix_reader.element_addresses(id, exact)

        ret = self.element_reader.read_elements(addresses, level=level)

        return ret
    
    
def from_gei(file):
    dir = os.path.dirname(file)
    
    with open(file) as f:
        data = json.loads(f.read())
    
    genome = data['genome']['name']
    
    return GEBReader(dir, data['name'], genome, int(data['window']));
    

if __name__ == '__main__':
    reader = GEBReader('/home/antony/Desktop/geb_test', 'test', 'hg19', 1000)
    
    genes = reader.find('chr10:87575-87801', 'bed')
    
    print('tada-------------------------------------------')
    
    for gene in genes:
        print(gene)

    genes = reader.get_elements('chr1', 'bed')
    
    print('presto-------------------------------------------')
    
    #for gene in genes:
    #    print(gene)

    reader.close()
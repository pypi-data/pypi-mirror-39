from struct import unpack_from
from .column_tile import ColumnTile 

class IntRangeColumnTile(ColumnTile):
    def __init__(self,params, type_, offset, length):
        ColumnTile.__init__(self, params, type_, offset, length)
        self.values_code = 'i'
        self.values_lower = params.range_data.values_lower
        self.values_upper = params.range_data.values_upper

    def get(self,i):
        j = i + self.length if i < 0 else i
        code = "%s%s" % (self.endian, self.values_code)
        size = ColumnTile.type_to_size(self.values_code)
        if self.exists(j):
            return ( unpack_from(code, self.values_lower, j*size)[0],
                     unpack_from(code, self.values_lower, j*size)[0] )
        else:
            return None        
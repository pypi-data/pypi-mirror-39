from struct import unpack_from
from datetime import datetime
from .column_tile import ColumnTile 

class DatetimeColumnTile(ColumnTile):
    def __init__(self,params, type_, offset, length):
        ColumnTile.__init__(self, params, type_, offset, length)
        self.values_code = 'd'
        self.values_lower = params.range_data.values_lower
        self.values_upper = params.range_data.values_upper
        self.ref_time = -62162035200000 # ms between unix epoch and 01-03-0000

    def get(self,i):
        j = i + self.length if i < 0 else i
        code = "%s%s" % (self.endian, self.values_code)
        size = ColumnTile.type_to_size(self.values_code)
        if self.exists(j):
            datetime_ms = unpack_from(code, self.values_lower, j*size)[0] + self.ref_time
            return datetime.fromtimestamp(datetime_ms/1000).date()
            # return (unpack_from(code, self.values_lower, j*size)[0] + self.ref_time,
            #         unpack_from(code, self.values_lower, j*size)[0] + self.ref_time)
        else:
            return None        

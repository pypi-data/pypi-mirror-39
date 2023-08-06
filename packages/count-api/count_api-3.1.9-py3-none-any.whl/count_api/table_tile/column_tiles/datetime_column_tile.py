from struct import unpack_from
from datetime import datetime, time
import math
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
            try:
                datetime_ms = unpack_from(code, self.values_lower, j*size)[0]
                if datetime_ms + self.ref_time > 0:
                    datetime_ms = datetime_ms + self.ref_time
                    return datetime.fromtimestamp(datetime_ms/1000).date()
                if datetime_ms < 24*60*60*1000:
                    hours = math.floor(datetime_ms/(60*60*1000))
                    datetime_ms = datetime_ms - hours*60*60*1000
                    mins = math.floor(datetime_ms/(60*1000))
                    datetime_ms = datetime_ms - mins*60*1000
                    seconds = math.floor(datetime_ms/1000)
                    miliseconds = datetime_ms - seconds*1000
                    return time(hour=hours, min=mins, second=seconds, microsecond = miliseconds*1000)
                raise "Unknown" 
                # return (unpack_from(code, self.values_lower, j*size)[0] + self.ref_time,
                #         unpack_from(code, self.values_lower, j*size)[0] + self.ref_time)
            except:
                datetime_ms = unpack_from(code, self.values_lower, j*size)[0]
                return unpack_from(code, self.values_lower, j*size)[0]
        else:
            return None        

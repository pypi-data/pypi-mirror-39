from struct import unpack_from
from .column_tile import ColumnTile 

class StringColumnTile(ColumnTile):
    def __init__(self,params, type_, offset, length):
        ColumnTile.__init__(self, params, type_, offset, length)
        self.breaks = params.string_data.breaks
        self.values = params.string_data.values
        self.breaks_code = 'i'
        self.values_code = 's'

    def get(self,i):
        j = i + self.length if i < 0 else i
        breaks_code = "%s%s" % (self.endian, self.breaks_code)
        breaks_size = ColumnTile.type_to_size(self.breaks_code)
        if self.exists(j):
            read_from = 0 if j == 0 else unpack_from(breaks_code, self.breaks, (j-1)*breaks_size)[0]
            read_to = unpack_from(breaks_code, self.breaks, j*breaks_size)[0]
            return self.read_utf8(read_from, read_to)
        else:
            return None 

    # Adapted from https://github.com/mapbox/pbf
    def read_utf8(self,begin, end):
        string = []
        i = begin
        buf = self.values
        while i < end:
            b0 = buf[i]
            if isinstance(b0,str):
                b0 = ord(b0)
            bytes_per_sequence = 1
            if b0 > 0xEF:
                bytes_per_sequence = 4
            elif b0 > 0xDF:
                bytes_per_sequence = 3
            elif b0 > 0xBF:
                bytes_per_sequence = 2

            if i + bytes_per_sequence > end:
                break
            
            c = None
            if bytes_per_sequence == 1:
                if b0 < 0x80:
                    c = b0
            elif bytes_per_sequence == 2:
                b1 = buf[i + 1]
                if (b1 & 0xC0) == 0x80:
                    c = (b0 & 0x1F) << 0x6 | (b1 & 0x3F)
                    if c <= 0x7F:
                        c = None
            elif bytes_per_sequence == 3:
                b1 = buf[i + 1]
                b2 = buf[i + 2]
                if ((b1 & 0xC0) == 0x80 and (b2 & 0xC0) == 0x80):
                    c = (b0 & 0xF) << 0xC | (b1 & 0x3F) << 0x6 | (b2 & 0x3F)
                    if (c <= 0x7FF or (c >= 0xD800 and c <= 0xDFFF)):
                        c = None
            elif bytes_per_sequence == 4:
                b1 = buf[i + 1]
                b2 = buf[i + 2]
                b3 = buf[i + 3]
                if ((b1 & 0xC0) == 0x80 and (b2 & 0xC0) == 0x80 and (b3 & 0xC0) == 0x80):
                    c = (b0 & 0xF) << 0x12 | (b1 & 0x3F) << 0xC | (b2 & 0x3F) << 0x6 | (b3 & 0x3F)
                    if (c <= 0xFFFF or c >= 0x110000):
                        c = None
            if not c:
                c = 0xFFFD
                bytes_per_sequence = 1
            elif (c > 0xFFFF):
                c = c - 0x10000
                string_char = (rshift(c,10) & 0x3FF | 0xD800)
                string.append(chr(string_char))
                c = 0xDC00 | c & 0x3FF
            string.append(chr(c))
            i += bytes_per_sequence
        return ''.join(string)

def rshift(val, n): return (val % 0x100000000) >> n
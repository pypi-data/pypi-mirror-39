from struct import unpack_from

TYPE_TO_SIZE = {
  'x' : 1,
  'c' : 1,
  'b' : 1,
  'B' : 1,
  '?' : 1,
  'h' : 2,
  'H' : 2,
  'i' : 4,
  'I' : 4,
  'l' : 4,
  'L' : 4,
  'q' : 8,
  'Q' : 8, 
  'f' : 4,
  'd' : 8 }

class ColumnTile:
    def __init__(self,params, type_, offset, length):
        self.key = params.key
        self.name = params.name
        self.type = type_
        self.offset = offset
        self.length = length
        self.endian = '<'
        self.present = params.present
        self.present_code = 'b'
        self.values = None
        self.values_code = None

    @staticmethod
    def type_to_size(type):
      return TYPE_TO_SIZE[type]

    def get(self,i):
        j = i + self.length if i < 0 else i
        code = "%s%s" % (self.endian, self.values_code)
        size = ColumnTile.type_to_size(self.values_code)
        return unpack_from(code, self.values, j*size)[0] if self.exists(j) else None

    def slice_(self, start=0, end=None):
        if not end:
            end = self.length
        clamped_end = min(self.length, end + self.length if end < 0 else end)
        clamped_start = max(0, min(clamped_end, start + self.length if start < 0 else start))
        ret = []
        i = clamped_start
        while i < clamped_end:
            ret.append(self.get(i))
            i = i + 1
        return ret

    def exists(self, i):
        j = i + self.length if i < 0 else i
        code = "%s%s" % (self.endian, self.present_code)
        size = ColumnTile.type_to_size(self.present_code)
        return unpack_from(code, self.present, j*size) if j >= 0 and j < self.length else False
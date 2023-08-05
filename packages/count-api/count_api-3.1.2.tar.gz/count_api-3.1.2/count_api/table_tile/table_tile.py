from .row_indices import RowIndices
from .column_tiles import StringColumnTile, IntColumnTile, DoubleColumnTile, IntRangeColumnTile, DoubleRangeColumnTile, DatetimeColumnTile, ColumnTile
from .pbf import Table

def create_column(params, offset, length):
  type = params.type
  if type == 0:
      return StringColumnTile(params, type_='string', offset=offset, length=length)
  elif type == 1:
      return IntColumnTile(params, type_='int', offset=offset, length=length)
  elif type == 2:
      return DoubleColumnTile(params, type_='double', offset=offset, length=length)
  elif type == 3:
      return IntRangeColumnTile(params, type_='int_range', offset=offset, length=length)
  elif type == 4:
      return DoubleRangeColumnTile(params, type_='double_range', offset=offset, length=length)
  elif type == 5:
      return DatetimeColumnTile(params, type_='datetime', offset=offset, length=length)
  else:
      return ColumnTile(params, type_=None, offset=offset, length=length)

class TableTile:

    @staticmethod
    def from_buffer(buffer):
        return TableTile(buffer)

    def __init__(self, buffer):
        self.headers = None
        if len(buffer) == 0:
            self.key = None
            self.name = None
            self.offset = 0
            self.length = 0
            self.sample = False
            self.row_indices = None
            self.columns = []
        else:
            table = Table()
            table.ParseFromString(buffer)
            self.key = table.key
            self.name = table.name
            self.offset = table.begin
            self.length = table.length
            self.sample = table.sample
            self.row_indices = RowIndices(table)
            self.columns = [create_column(c, self.offset, self.length) for c in table.columns]
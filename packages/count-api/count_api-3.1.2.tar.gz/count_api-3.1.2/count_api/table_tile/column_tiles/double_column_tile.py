from struct import unpack_from
from .column_tile import ColumnTile 

class DoubleColumnTile(ColumnTile):
    def __init__(self,params, type_, offset, length):
        ColumnTile.__init__(self, params, type_, offset, length)
        self.values_code = 'd'
        self.values = params.number_data.values


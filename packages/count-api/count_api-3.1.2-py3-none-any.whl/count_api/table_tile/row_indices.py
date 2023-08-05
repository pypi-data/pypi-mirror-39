from struct import unpack_from

class RowIndices:
    def __init__(self,table):
        indices = table.row_indices
        self.indices = unpack_from('<i', indices)
        self.length = table.length

    def get(self,i):
        j = i + self.length if i < 0 else i
        return self.indices[j]

    def slice_(self, start=0, end=None):
        if not end:
            end = self.length
        clamped_end = min(self.length, end + self.length if end < 0 else end)
        clamped_start = max(0, min(clamped_end, start + self.length if start < 0 else start))
        return self.indices[clamped_start:clamped_end]

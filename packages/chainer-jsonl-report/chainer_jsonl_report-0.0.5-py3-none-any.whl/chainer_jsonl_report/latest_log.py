class LatestLog:

    def __init__(self):
        self._record = {}
        self._size = 0

    def __len__(self):
        return self._size

    def __getitem__(self, idx):
        assert idx == self._size-1
        return self._record

    def update(self, record):
        self._record = record
        self._size += 1

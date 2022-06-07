class Disk:
    _name: str
    _total: int
    _used: int
    _free: int

    def __init__(self):
        pass

    def set_name(self, name: str):
        self._name = name

    def get_name(self):
        return self._name

    def set_total(self, total: int):
        self._total = total

    def get_total(self):
        return self._total

    def set_used(self, used: int):
        self._used = used

    def get_used(self):
        return self._used

    def set_free(self, free: int):
        self._free = free

    def get_free(self):
        return self._free

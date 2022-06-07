class Memory:
    _total: int
    _avaliable: int
    _used: int

    def __init__(self):
        pass

    def set_total(self, total: int):
        self._total = total

    def get_total(self):
        return self._total

    def set_available(self, available: int):
        self._avaliable = available

    def get_available(self):
        return self._avaliable

    def set_used(self, used: int):
        self._used = used

    def get_used(self):
        return self._used

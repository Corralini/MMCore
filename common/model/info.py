from common.model.memory import Memory


class Info:
    _cpu_usage: float
    _memory: str
    _disks: str

    def __init__(self):
        self._disks = []

    def set_cpu_usage(self, cpu_usage: float):
        self._cpu_usage = cpu_usage

    def get_cpu_usage(self):
        return self._cpu_usage

    def set_memory(self, memory: str):
        self._memory = memory

    def get_memory(self):
        return self._memory

    def get_disk(self):
        return self._disks

    def set_disk(self, disks: str):
        self._disks = disks

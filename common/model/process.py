class Process:
    _id: int = None
    _name: str = None
    _status: str = None
    _started_date: str = None

    def __init__(self):
        pass

    def set_id(self, id: int):
        self._id = id

    def get_id(self) -> int:
        return self._id

    def set_name(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def set_status(self, status: str):
        self._status = status

    def get_status(self) -> str:
        return self._status

    def set_started_date(self, started_date: str):
        self._started_date = started_date

    def get_started_date(self) -> str:
        return self._started_date

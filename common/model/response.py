class Response:
    _status: str
    _data: object

    def __init__(self):
        pass

    def set_status(self, status):
        self._status = status

    def get_status(self):
        return self._status

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data
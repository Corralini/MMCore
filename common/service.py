class Service:
    _id: int = None
    _name: str = None
    _status: str = None
    _start_type: str = None
    _description: str = None

    def __init__(self):
        pass

    def set_id(self, id: int):
        self._id = id

    def set_name(self, name: str):
        self._name = name

    def set_status(self, status: str):
        self._status = status

    def set_start_type(self, start_type: str):
        self._start_type = start_type

    def set_description(self, description: str):
        self._description = description

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_status(self):
        return self._status

    def get_start_type(self):
        return self._start_type

    def get_description(self):
        return self._description

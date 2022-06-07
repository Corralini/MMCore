class User:
    _id: int
    _user: str
    _psswd: str

    def __init__(self):
        pass

    def set_id(self, id: int):
        self._id = id

    def set_user(self, user: str):
        self._user = user

    def set_psswd(self, psswd: str):
        self._psswd = psswd

    def get_id(self):
        return self._id

    def get_user(self):
        return self._user

    def get_psswd(self):
        return self._psswd

from dataclasses import dataclass


@dataclass
class user:

    unique_id: str
    user_id: int
    name: str
    avatar: str

    def __init__(self):
        self.unique_id = ''
        self.user_id = 0
        self.name = ''
        self.avatar = ''



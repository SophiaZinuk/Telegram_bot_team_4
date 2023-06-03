

class UserState:

    def __init__(self, chat_id: int, user_id: int) -> None:
        self.chat_id = chat_id
        self.user_id = user_id
        self.authorized = False
        self.menu = dict()

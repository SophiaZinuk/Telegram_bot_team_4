from typing import Optional
from state.taxi_application_state import TaxiApplicationState


class UserState:

    chat_id: int
    user_id: int
    is_admin: bool
    db_id: int
    authorized: bool
    menu: dict
    taxi_application: Optional[TaxiApplicationState]

    def __init__(self, chat_id: int, user_id: int, db_id: int) -> None:
        self.chat_id = chat_id
        self.user_id = user_id
        self.is_admin = False
        self.db_id = db_id
        self.authorized = False
        self.menu = dict()
        self.taxi_application = None

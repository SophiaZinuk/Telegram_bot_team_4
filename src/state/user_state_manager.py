from typing import Optional
from state.user_state import UserState
import jsonpickle


class UserStateManager:

    def __init__(self) -> None:
        self.user_state = None

    def update_state(self, user_state: UserState) -> None:
        try:
            file_name = str(user_state.user_id) + '.json'
            file = open('data/' + file_name, mode='w')
            json_str = jsonpickle.encode(user_state)
            file.write(json_str)
            file.close()
        except Exception as e:
            raise e

    def get_state(self, user_id: int) -> Optional[UserState]:
        try:
            file_name = str(user_id) + '.json'
            file = open('data/' + file_name, mode='r')
            data = file.read()
            user_state: UserState = jsonpickle.decode(data)
            file.close()
            return user_state
        except FileNotFoundError as e:
            print(e)
            return None

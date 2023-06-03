from typing import Optional
from state.user_state import UserState
import jsonpickle
import os
from menu.menu_type import MenuType


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

    def remove_state(self, user_id: int) -> None:
        try:
            file_path = 'data/' + str(user_id) + '.json'
            if os.path.isfile(file_path):
                os.remove(file_path)
        except FileNotFoundError as e:
            print(e)
            return None

    def update_menu(self, user_id: int, msg_id: int, menu: MenuType):
        state: UserState = self.get_state(user_id)
        if state is not None:
            state.menu[msg_id] = menu
        self.update_state(state)

    def is_user_authorized(self, user_id: int) -> bool:
        user_state = self.get_state(user_id)
        if user_state is None:
            return False
        return user_state.authorized


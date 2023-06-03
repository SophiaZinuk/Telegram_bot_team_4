from telebot import TeleBot
from telebot import types

from localization.localization import Localization
from menu.menu_manager import MenuManager
from state.user_state_manager import UserStateManager


class TaxiConversation:

    def __init__(
            self,
            bot: TeleBot,
            localization: Localization,
            menu_manager: MenuManager,
            user_state_manager: UserStateManager
    ):
        self.bot = bot
        self.localization = localization
        self.menu_manager = menu_manager
        self.user_state_manager = user_state_manager

    def start_conversation(self, callback: types.CallbackQuery):
        try:
            msg = self.bot.send_message(callback.message.chat.id, 'Введіть номер таксі:')
            self.bot.register_next_step_handler(msg, self._process_taxi_number)
        except Exception as e:
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['something_went_wrong'])
            self.bot.clear_step_handler_by_chat_id(callback.message.chat.id)

    def _process_taxi_number(self, message: types.Message):
        try:
            taxi_number: str = self._get_taxi_number(message)
            self.bot.clear_step_handler_by_chat_id(message.chat.id)

        except Exception as e:
            print(e)

    def _get_taxi_number(self, msg: types.Message) -> str:
        return msg.text

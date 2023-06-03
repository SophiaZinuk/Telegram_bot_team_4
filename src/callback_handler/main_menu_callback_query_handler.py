from telebot import TeleBot
from telebot import types

from callback_handler.callback_type import CallbackType
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler
from localization.localization import Localization
from menu.menu_manager import MenuManager
from state.user_state_manager import UserStateManager


class MainMenuCallbackQueryHandler(GeneralCallbackQueryHandler):

    def __init__(
            self,
            bot: TeleBot,
            localization: Localization,
            menu_manager: MenuManager,
            user_state_manager: UserStateManager,
    ):
        self.bot = bot
        self.localization = localization
        self.menu_manager = menu_manager
        self.user_state_manager = user_state_manager

    def handle(self, callback: types.CallbackQuery):
        if callback.data == CallbackType.LOGOUT:
            self._handle_logout(callback)

    def _handle_logout(self, callback: types.CallbackQuery):
        try:
            user_id: int = callback.from_user.id
            is_authorized: bool = self._is_user_authorized(user_id)
            if is_authorized:
                self._logout(user_id)
                self.bot.answer_callback_query(callback_query_id=callback.id)
                self.bot.send_message(
                    callback.message.chat.id,
                    self.localization.lang['logged_out_successfully'])
            else:
                self.bot.answer_callback_query(callback_query_id=callback.id)
                self.bot.send_message(
                    callback.message.chat.id,
                    self.localization.lang['you_have_already_logged_out'])
        except Exception as e:
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['something_went_wrong'])

    def _logout(self, user_id: int):
        user_state = self.user_state_manager.get_state(user_id)
        user_state.authorized = False
        self.user_state_manager.update_state(user_state)

    def _is_user_authorized(self, user_id: int) -> bool:
        user_state = self.user_state_manager.get_state(user_id)
        if user_state is None:
            return False
        return user_state.authorized

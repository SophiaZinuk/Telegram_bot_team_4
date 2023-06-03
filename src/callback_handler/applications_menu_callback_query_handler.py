from telebot import TeleBot
from telebot import types

from callback_handler.callback_type import CallbackType
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler
from conversation.taxi_conversation import TaxiConversation
from localization.localization import Localization
from menu.menu_manager import MenuManager
from menu.menu_type import MenuType
from state.user_state_manager import UserStateManager


class ApplicationsMenuCallbackQueryHandler(GeneralCallbackQueryHandler):

    def __init__(
            self,
            bot: TeleBot,
            localization: Localization,
            menu_manager: MenuManager,
            user_state_manager: UserStateManager,
            taxi_conversation: TaxiConversation
    ):
        self.bot = bot
        self.localization = localization
        self.menu_manager = menu_manager
        self.user_state_manager = user_state_manager
        self.taxi_conversation = taxi_conversation

    def handle(self, callback: types.CallbackQuery):
        is_authorized: bool = self.user_state_manager.is_user_authorized(callback.from_user.id)
        if is_authorized:
            if callback.data == CallbackType.APPLICATIONS_BACK:
                self._handle_applications_back(callback)
            if callback.data == CallbackType.TAXI:
                self._handle_taxi_application(callback)
        else:
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['authorize_first'])

    def _handle_applications_back(self, callback: types.CallbackQuery):
        self.bot.answer_callback_query(callback_query_id=callback.id)
        previous_menu_type: MenuType = self.menu_manager.get_previous_menu(MenuType.APPLICATIONS)
        self.bot.edit_message_text(self.localization.lang['choose_option'],
                                   callback.message.chat.id,
                                   callback.message.message_id,
                                   reply_markup=self.menu_manager.get_menu(previous_menu_type))
        self.user_state_manager.update_menu(callback.from_user.id, callback.message.message_id, previous_menu_type)

    def _handle_taxi_application(self, callback: types.CallbackQuery):
        self.bot.answer_callback_query(callback_query_id=callback.id)
        self.taxi_conversation.start_conversation(callback)

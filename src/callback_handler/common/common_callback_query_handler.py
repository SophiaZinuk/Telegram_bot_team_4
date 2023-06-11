from telebot import TeleBot
from telebot.types import CallbackQuery
from callback_handler.callback_type import CallbackType
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler
from db.service.application_service import ApplicationService
from localization.localization import Localization
from menu.menu_manager import MenuManager
from state.user_state_manager import UserStateManager


class CommonCallbackQueryHandler(GeneralCallbackQueryHandler):

    def __init__(
            self,
            bot: TeleBot,
            localization: Localization,
            menu_manager: MenuManager,
            user_state_manager: UserStateManager,
            application_service: ApplicationService
    ):
        self.bot = bot
        self.localization = localization
        self.menu_manager = menu_manager
        self.user_state_manager = user_state_manager
        self.application_service = application_service
        self._init_handler_mapper()

    def is_handled(self, callback: CallbackQuery) -> bool:
        callback_data: str = callback.data
        handler = self.handler_mapper.get(callback_data)
        return handler is not None

    def handle(self, callback: CallbackQuery):
        if callback.data == CallbackType.LOGOUT:
            self._handle_logout(callback)

    def _init_handler_mapper(self):
        self.handler_mapper = dict()
        self.handler_mapper[CallbackType.LOGOUT] = self._handle_logout


    def _handle_logout(self, callback: CallbackQuery):
        user_id: int = callback.from_user.id
        is_authorized: bool = self.user_state_manager.is_user_authorized(user_id)
        if is_authorized:
            self._logout(user_id)
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.delete_message(callback.message.chat.id, callback.message.message_id)
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['logged_out_successfully'])
        else:
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.delete_message(callback.message.chat.id, callback.message.message_id)
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['you_have_already_logged_out'])

    def _logout(self, user_id: int):
        self.user_state_manager.remove_state(user_id)

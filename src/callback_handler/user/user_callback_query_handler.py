from typing import Optional
import telebot
from telebot.types import CallbackQuery
from callback_handler.callback_type import CallbackType
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler
from localization.localization import Localization
from state.user_state import UserState
from state.user_state_manager import UserStateManager


class UserCallbackQueryHandler(GeneralCallbackQueryHandler):

    def __init__(
            self,
            bot: telebot.TeleBot,
            localization: Localization,
            user_state_manager: UserStateManager,
            main_menu_handler: GeneralCallbackQueryHandler,
            applications_menu_callback_query_handler: GeneralCallbackQueryHandler,
            applications_pagination_menu_callback_query_handler: GeneralCallbackQueryHandler,
            single_application_callback_query_handler: GeneralCallbackQueryHandler,
    ):
        self.bot = bot
        self.localization = localization
        self.user_state_manager = user_state_manager
        self.main_menu_handler = main_menu_handler
        self.applications_menu_callback_query_handler = applications_menu_callback_query_handler
        self.applications_pagination_menu_callback_query_handler = applications_pagination_menu_callback_query_handler
        self.single_application_callback_query_handler = single_application_callback_query_handler
        self._init_handler_mapper()

    def is_handled(self, callback: CallbackQuery) -> bool:
        callback_data: str = callback.data
        if callback_data.startswith(CallbackType.APPLICATION_PAGINATION_APP):
            self.applications_pagination_menu_callback_query_handler.handle(callback)
        handler = self.handler_mapper.get(callback_data)
        return handler is not None

    def handle(self, callback: CallbackQuery):
        user_state: UserState = self.user_state_manager.get_state(callback.from_user.id)
        is_authorized: bool = self._is_auth(user_state)
        is_admin: bool = self._is_admin(user_state)
        if is_authorized and not is_admin:
            self._handle(callback)
        else:
            text: str = self.localization.lang['authorize_first'] if not is_authorized \
                else self.localization.lang['you_are_admin_auth_as_user']
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.send_message(
                callback.message.chat.id,
                text)

    def _handle(self, callback: CallbackQuery):
        callback_data: str = callback.data
        if callback_data.startswith(CallbackType.APPLICATION_PAGINATION_APP):
            self.applications_pagination_menu_callback_query_handler.handle(callback)
            return
        handler = self.handler_mapper.get(callback_data)
        handler.handle(callback)


    def _init_handler_mapper(self):
        self.handler_mapper = dict()
        self.handler_mapper[CallbackType.CREATE_APPLICATION] = self.main_menu_handler
        self.handler_mapper[CallbackType.APPLICATIONS_STATUS] = self.main_menu_handler
        self.handler_mapper[CallbackType.SECURITY_CONTACTS] = self.main_menu_handler

        self.handler_mapper[CallbackType.TAXI] = self.applications_menu_callback_query_handler
        self.handler_mapper[CallbackType.CARRIER] = self.applications_menu_callback_query_handler
        self.handler_mapper[CallbackType.GUESTS] = self.applications_menu_callback_query_handler
        self.handler_mapper[CallbackType.PARKING_PROBLEMS] = self.applications_menu_callback_query_handler
        self.handler_mapper[CallbackType.OTHER] = self.applications_menu_callback_query_handler
        self.handler_mapper[CallbackType.APPLICATIONS_BACK] = self.applications_menu_callback_query_handler

        self.handler_mapper[
            CallbackType.APPLICATIONS_PAGINATION_BACK] = self.applications_pagination_menu_callback_query_handler
        self.handler_mapper[
            CallbackType.APPLICATIONS_PAGINATION_BACKWARD] = self.applications_pagination_menu_callback_query_handler
        self.handler_mapper[
            CallbackType.APPLICATIONS_PAGINATION_FORWARD] = self.applications_pagination_menu_callback_query_handler

        self.handler_mapper[CallbackType.SINGLE_APPLICATION_TO_MAIN] = self.single_application_callback_query_handler
        self.handler_mapper[CallbackType.SINGLE_APPLICATION_BACK] = self.single_application_callback_query_handler

    def _is_auth(self, user_state: Optional[UserState]) -> bool:
        if user_state is None:
            return False
        return user_state.authorized

    def _is_admin(self,  user_state: Optional[UserState]) -> bool:
        authorized: bool = self._is_auth(user_state)
        if not authorized:
            return False
        return user_state.is_admin

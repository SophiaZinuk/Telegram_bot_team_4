from typing import Optional
import telebot
from telebot.types import CallbackQuery
from callback_handler.callback_type import CallbackType
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler
from localization.localization import Localization
from state.user_state import UserState
from state.user_state_manager import UserStateManager


class AdminCallbackQueryHandler(GeneralCallbackQueryHandler):

    def __init__(
            self,
            bot: telebot.TeleBot,
            localization: Localization,
            user_state_manager: UserStateManager,
            main_admin_menu_callback_query_handler: GeneralCallbackQueryHandler,
            admin_applications_pagination_menu_callback_query_handler: GeneralCallbackQueryHandler,
            admin_single_application_callback_query_handler: GeneralCallbackQueryHandler,
    ):
        self.bot = bot
        self.localization = localization
        self.user_state_manager = user_state_manager
        self.main_admin_menu_callback_query_handler = main_admin_menu_callback_query_handler
        self.admin_applications_pagination_menu_callback_query_handler = \
            admin_applications_pagination_menu_callback_query_handler
        self.admin_single_application_callback_query_handler = admin_single_application_callback_query_handler
        self._init_handler_mapper()

    def is_handled(self, callback: CallbackQuery) -> bool:
        callback_data: str = callback.data
        if callback_data.startswith(CallbackType.ADMIN_APPLICATION_PAGINATION_APP):
            return True
        handler = self.handler_mapper.get(callback_data)
        return handler is not None

    def handle(self, callback: CallbackQuery):
        user_state: UserState = self.user_state_manager.get_state(callback.from_user.id)
        is_authorized: bool = self._is_auth(user_state)
        is_admin: bool = self._is_admin(user_state)
        if is_authorized and is_admin:
            self._handle(callback)
        else:
            text: str = self.localization.lang['authorize_first'] if not is_authorized \
                else self.localization.lang['you_are_user_auth_as_admin']
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.send_message(
                callback.message.chat.id,
                text)

    def _handle(self, callback: CallbackQuery):
        callback_data: str = callback.data
        if callback_data.startswith(CallbackType.ADMIN_APPLICATION_PAGINATION_APP):
            self.admin_applications_pagination_menu_callback_query_handler.handle(callback)
            return
        handler = self.handler_mapper.get(callback_data)
        handler.handle(callback)

    def _init_handler_mapper(self):
        self.handler_mapper = dict()
        self.handler_mapper[CallbackType.ADMIN_APPLICATIONS_STATUS] = self.main_admin_menu_callback_query_handler
        self.handler_mapper[
            CallbackType.ADMIN_APPLICATIONS_PAGINATION_BACK] = \
            self.admin_applications_pagination_menu_callback_query_handler
        self.handler_mapper[
            CallbackType.ADMIN_APPLICATIONS_PAGINATION_BACKWARD] = \
            self.admin_applications_pagination_menu_callback_query_handler
        self.handler_mapper[
            CallbackType.ADMIN_APPLICATIONS_PAGINATION_FORWARD] = \
            self.admin_applications_pagination_menu_callback_query_handler
        self.handler_mapper[CallbackType.ADMIN_SINGLE_APPLICATION_TO_MAIN] = \
            self.admin_single_application_callback_query_handler
        self.handler_mapper[CallbackType.ADMIN_SINGLE_APPLICATION_BACK] = \
            self.admin_single_application_callback_query_handler
        self.handler_mapper[CallbackType.ADMIN_SINGLE_APPLICATION_APPROVE] = \
            self.admin_single_application_callback_query_handler
        self.handler_mapper[CallbackType.ADMIN_SINGLE_APPLICATION_REJECT] = \
            self.admin_single_application_callback_query_handler

    def _is_auth(self, user_state: Optional[UserState]) -> bool:
        if user_state is None:
            return False
        return user_state.authorized

    def _is_admin(self,  user_state: Optional[UserState]) -> bool:
        authorized: bool = self._is_auth(user_state)
        if not authorized:
            return False
        return user_state.is_admin

from typing import List

from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, \
    Message

from callback_handler.callback_type import CallbackType
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler
from db.model.model import Application
from db.service.application_service import ApplicationService
from localization.localization import Localization
from menu.applications_pagination_menu import ApplicationsPaginationMenu
from menu.menu_manager import MenuManager
from menu.menu_type import MenuType
from state.menu_state import MenuState
from state.user_state import UserState
from state.user_state_manager import UserStateManager


class MainMenuCallbackQueryHandler(GeneralCallbackQueryHandler):

    def __init__(self, bot: TeleBot, localization: Localization, menu_manager: MenuManager,
                 user_state_manager: UserStateManager, application_service: ApplicationService):
        self.bot = bot
        self.localization = localization
        self.menu_manager = menu_manager
        self.user_state_manager = user_state_manager
        self.application_service = application_service

    def handle(self, callback: CallbackQuery):
        super().handle(callback)
        if callback.data == CallbackType.CREATE_APPLICATION:
            self._handle_create_application(callback)
        if callback.data == CallbackType.APPLICATIONS_STATUS:
            self._handle_applications_status(callback)
        if callback.data == CallbackType.SECURITY_CONTACTS:
            self._handle_security_contacts(callback)

    def _handle_create_application(self, callback: CallbackQuery):
        user_id: int = callback.from_user.id
        is_authorized: bool = self.user_state_manager.is_user_authorized(
            user_id)
        if is_authorized:
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.edit_message_text(self.localization.lang['choose_application_type'],
                                       callback.message.chat.id,
                                       callback.message.message_id,
                                       reply_markup=self.menu_manager.get_menu_markup(MenuType.APPLICATIONS))
            self.user_state_manager.update_menu(callback.from_user.id, callback.message.message_id,
                                                MenuState(MenuType.APPLICATIONS))
        else:
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['authorize_first'])

    def _handle_applications_status(self, callback: CallbackQuery):
        self.bot.answer_callback_query(callback_query_id=callback.id)
        user_id: int = callback.from_user.id
        is_authorized: bool = self.user_state_manager.is_user_authorized(
            user_id)
        if is_authorized:
            self.bot.answer_callback_query(callback_query_id=callback.id)
            markup: InlineKeyboardMarkup = self._assemble_application_statuses_markup(
                callback)
            msg: Message = self.bot.edit_message_text(self.localization.lang['your_applications'],
                                                      callback.message.chat.id,
                                                      callback.message.message_id,
                                                      reply_markup=markup)
            menu: MenuState = MenuState(MenuType.APPLICATIONS_PAGINATION_MENU)
            self.user_state_manager.update_menu(
                callback.from_user.id, msg.id, menu)
        else:
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['authorize_first'])

    def _handle_security_contacts(self, callback: CallbackQuery):
        text: str = self._assemble_contacts_text()
        self.bot.send_message(callback.message.chat.id, text)

    def _assemble_application_statuses_markup(self, callback: CallbackQuery) -> InlineKeyboardMarkup:
        user_state: UserState = self.user_state_manager.get_state(
            callback.from_user.id)
        menu: ApplicationsPaginationMenu = self.menu_manager.get_menu(
            MenuType.APPLICATIONS_PAGINATION_MENU)
        applications: List[Application] = self.application_service.find_by_user_id_with_pagination(
            user_state.db_id, 4, 0)
        markup: InlineKeyboardMarkup = menu.create(applications, 0)
        return markup

    def _assemble_contacts_text(self) -> str:
        result = ''
        result += self.localization.lang['security_number_text']
        result += '\n\n'
        result += self.localization.lang['security_number_first']
        result += '\n'
        result += self.localization.lang['security_number_second']
        return result

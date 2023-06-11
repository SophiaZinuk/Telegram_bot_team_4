from typing import List

from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, Message

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


class SingleApplicationCallbackQueryHandler(GeneralCallbackQueryHandler):

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

    def handle(self, callback: CallbackQuery):
        self.bot.answer_callback_query(callback_query_id=callback.id)
        is_authorized: bool = self.user_state_manager.is_user_authorized(callback.from_user.id)
        if is_authorized:
            if callback.data == CallbackType.SINGLE_APPLICATION_BACK:
                self._handle_back(callback)
            if callback.data == CallbackType.SINGLE_APPLICATION_TO_MAIN:
                self._handle_main_menu(callback)
        else:
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['authorize_first'])

    def _handle_back(self, callback: CallbackQuery) -> None:
        self.bot.answer_callback_query(callback_query_id=callback.id)
        markup: InlineKeyboardMarkup = self._assemble_application_statuses_markup(callback)
        msg: Message = self.bot.edit_message_text(self.localization.lang['your_applications'],
                                                  callback.message.chat.id,
                                                  callback.message.message_id,
                                                  reply_markup=markup)
        menu: MenuState = MenuState(MenuType.APPLICATIONS_PAGINATION_MENU)
        self.user_state_manager.update_menu(callback.from_user.id, msg.id, menu)

    def _handle_main_menu(self, callback: CallbackQuery) -> None:
        markup: InlineKeyboardMarkup = self.menu_manager.get_menu_markup(MenuType.MAIN)
        msg: Message = self.bot.edit_message_text(self.localization.lang['choose_option'],
                                                  callback.message.chat.id,
                                                  callback.message.message_id,
                                                  reply_markup=markup)
        menu_state: MenuState = MenuState(MenuType.MAIN)
        self.user_state_manager.update_menu(callback.from_user.id, msg.message_id, menu_state)

    def _assemble_application_statuses_markup(self, callback: CallbackQuery) -> InlineKeyboardMarkup:
        user_state: UserState = self.user_state_manager.get_state(callback.from_user.id)
        menu: ApplicationsPaginationMenu = self.menu_manager.get_menu(MenuType.APPLICATIONS_PAGINATION_MENU)
        applications: List[Application] = self.application_service.find_by_user_id_with_pagination(
            user_state.db_id, 4, 0)
        markup: InlineKeyboardMarkup = menu.create(applications, 0)
        return markup

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
from state.user_state_manager import UserStateManager


class MainAdminMenuCallbackQueryHandler(GeneralCallbackQueryHandler):

    def __init__(self, bot: TeleBot, localization: Localization, menu_manager: MenuManager,
                 user_state_manager: UserStateManager, application_service: ApplicationService):
        self.bot = bot
        self.localization = localization
        self.menu_manager = menu_manager
        self.user_state_manager = user_state_manager
        self.application_service = application_service

    def handle(self, callback: CallbackQuery):
        super().handle(callback)
        if callback.data == CallbackType.ADMIN_APPLICATIONS_STATUS:
            self._handle_applications_status(callback)

    def _handle_applications_status(self, callback: CallbackQuery):
        self.bot.answer_callback_query(callback_query_id=callback.id)
        user_id: int = callback.from_user.id
        is_authorized: bool = self.user_state_manager.is_user_authorized(user_id)
        if is_authorized:
            self.bot.answer_callback_query(callback_query_id=callback.id)
            markup: InlineKeyboardMarkup = self._assemble_application_statuses_markup()
            msg: Message = self.bot.edit_message_text(self.localization.lang['all_applications'],
                                                      callback.message.chat.id,
                                                      callback.message.message_id,
                                                      reply_markup=markup)
            menu: MenuState = MenuState(MenuType.ADMIN_APPLICATIONS_PAGINATION_MENU)
            self.user_state_manager.update_menu(callback.from_user.id, msg.id, menu)
        else:
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['authorize_first'])

    def _assemble_application_statuses_markup(self) -> InlineKeyboardMarkup:
        menu: ApplicationsPaginationMenu = self.menu_manager.get_menu(MenuType.ADMIN_APPLICATIONS_PAGINATION_MENU)
        applications: List[Application] = self.application_service.find_all_with_pagination(4, 0)
        markup: InlineKeyboardMarkup = menu.create(applications, 0)
        return markup

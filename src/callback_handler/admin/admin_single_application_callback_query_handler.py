from typing import List

from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, Message

from callback_handler.callback_type import CallbackType
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler
from db.constant.application_status import ApplicationStatus
from db.exception.status_already_updated_exception import StatusAlreadyUpdatedException
from db.model.model import Application
from db.service.application_service import ApplicationService
from db.util.application_util import ApplicationUtil
from localization.localization import Localization
from menu.admin_single_application_menu import AdminSingleApplicationMenu
from menu.applications_pagination_menu import ApplicationsPaginationMenu
from menu.menu_manager import MenuManager
from menu.menu_type import MenuType
from state.menu_state import MenuState
from state.user_state_manager import UserStateManager


class AdminSingleApplicationCallbackQueryHandler(GeneralCallbackQueryHandler):

    def __init__(
            self,
            bot: TeleBot,
            localization: Localization,
            menu_manager: MenuManager,
            user_state_manager: UserStateManager,
            application_service: ApplicationService,
            application_util: ApplicationUtil
    ):
        self.bot = bot
        self.localization = localization
        self.menu_manager = menu_manager
        self.user_state_manager = user_state_manager
        self.application_service = application_service
        self.application_util = application_util

    def handle(self, callback: CallbackQuery):
        self.bot.answer_callback_query(callback_query_id=callback.id)
        is_authorized: bool = self.user_state_manager.is_user_authorized(callback.from_user.id)
        if is_authorized:
            if callback.data == CallbackType.ADMIN_SINGLE_APPLICATION_BACK:
                self._handle_back(callback)
            if callback.data == CallbackType.ADMIN_SINGLE_APPLICATION_TO_MAIN:
                self._handle_main_menu(callback)
            if callback.data == CallbackType.ADMIN_SINGLE_APPLICATION_APPROVE:
                self._handle_update_app_status(callback, ApplicationStatus.APPROVED)
            if callback.data == CallbackType.ADMIN_SINGLE_APPLICATION_REJECT:
                self._handle_update_app_status(callback, ApplicationStatus.REJECTED)
        else:
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['authorize_first'])

    def _handle_back(self, callback: CallbackQuery) -> None:
        self.bot.answer_callback_query(callback_query_id=callback.id)
        markup: InlineKeyboardMarkup = self._assemble_application_statuses_markup()
        msg: Message = self.bot.edit_message_text(self.localization.lang['your_applications'],
                                                  callback.message.chat.id,
                                                  callback.message.message_id,
                                                  reply_markup=markup)
        menu: MenuState = MenuState(MenuType.ADMIN_APPLICATIONS_PAGINATION_MENU)
        self.user_state_manager.update_menu(callback.from_user.id, msg.id, menu)

    def _handle_main_menu(self, callback: CallbackQuery) -> None:
        markup: InlineKeyboardMarkup = self.menu_manager.get_menu_markup(MenuType.MAIN_ADMIN)
        msg: Message = self.bot.edit_message_text(self.localization.lang['choose_option'],
                                                  callback.message.chat.id,
                                                  callback.message.message_id,
                                                  reply_markup=markup)
        menu_state: MenuState = MenuState(MenuType.MAIN_ADMIN)
        self.user_state_manager.update_menu(callback.from_user.id, msg.message_id, menu_state)

    def _handle_update_app_status(self, callback: CallbackQuery, status: str) -> None:
        menu_state: MenuState = self.user_state_manager.get_menu_state(callback.from_user.id,
                                                                       callback.message.message_id)
        app_id: int = menu_state.current_application_id
        try:
            app: Application = self.application_service.update_application_status(app_id, status)
            self._respond_with_updated_application(app, callback)
        except StatusAlreadyUpdatedException:
            self._handle_status_already_updated(app_id, callback)

    def _assemble_application_statuses_markup(self) -> InlineKeyboardMarkup:
        menu: ApplicationsPaginationMenu = self.menu_manager.get_menu(MenuType.ADMIN_APPLICATIONS_PAGINATION_MENU)
        applications: List[Application] = self.application_service.find_all_with_pagination(4, 0)
        markup: InlineKeyboardMarkup = menu.create(applications, 0)
        return markup

    def _assemble_single_application_menu_markup(self) -> InlineKeyboardMarkup:
        menu: AdminSingleApplicationMenu = self.menu_manager.get_menu(MenuType.ADMIN_SINGLE_APPLICATION_MENU)
        return menu.create(False)

    def _respond_with_updated_application(self, app: Application, callback: CallbackQuery):
        app_text: str = self.application_util.assemble_app_text(app)
        markup: InlineKeyboardMarkup = self._assemble_single_application_menu_markup()
        msg: Message = self.bot.edit_message_text(app_text,
                                                  callback.message.chat.id,
                                                  callback.message.message_id,
                                                  reply_markup=markup)
        menu_state: MenuState = MenuState(MenuType.ADMIN_SINGLE_APPLICATION_MENU)
        menu_state.current_application_id = app.id
        self.user_state_manager.update_menu(callback.from_user.id, msg.message_id, menu_state)

    def _handle_status_already_updated(self, app_id: int, callback: CallbackQuery):
        self.bot.send_message(callback.message.chat.id, self.localization.lang['application_status_already_updated'])
        app: Application = self.application_service.find_by_id(app_id)
        app_text: str = self.application_util.assemble_app_text(app)
        markup: InlineKeyboardMarkup = self._assemble_single_application_menu_markup()
        msg: Message = self.bot.edit_message_text(app_text,
                                                  callback.message.chat.id,
                                                  callback.message.message_id,
                                                  reply_markup=markup)
        menu_state: MenuState = MenuState(MenuType.ADMIN_SINGLE_APPLICATION_MENU)
        menu_state.current_application_id = app_id
        self.user_state_manager.update_menu(callback.from_user.id, msg.message_id, menu_state)

from typing import List
from telebot import TeleBot, types
from telebot.types import CallbackQuery, InlineKeyboardMarkup, Message
from callback_handler.callback_type import CallbackType
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler
from db.constant.application_status import ApplicationStatus
from db.model.model import Application
from db.service.application_service import ApplicationService
from db.util.application_util import ApplicationUtil
from localization.localization import Localization
from menu.admin_single_application_menu import AdminSingleApplicationMenu
from menu.applications_pagination_menu import ApplicationsPaginationMenu
from menu.menu_manager import MenuManager
from menu.menu_type import MenuType
from state.menu_pagination_state import MenuPaginationState
from state.menu_state import MenuState
from state.user_state import UserState
from state.user_state_manager import UserStateManager


class AdminApplicationsPaginationMenuCallbackQueryHandler(GeneralCallbackQueryHandler):

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
            if callback.data == CallbackType.ADMIN_APPLICATIONS_PAGINATION_BACK:
                self._handle_back(callback)
                return
            if callback.data == CallbackType.ADMIN_APPLICATIONS_PAGINATION_FORWARD:
                self._handle_forward(callback)
                return
            if callback.data == CallbackType.ADMIN_APPLICATIONS_PAGINATION_BACKWARD:
                self._handle_backward(callback)
                return
            self._handle_application(callback)
        else:
            self.bot.answer_callback_query(callback_query_id=callback.id)
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['authorize_first'])

    def _handle_back(self, callback: CallbackQuery):
        previous_menu_type: MenuType = MenuType.MAIN_ADMIN
        previous_menu: MenuState = MenuState(previous_menu_type)
        self.bot.edit_message_text(self.localization.lang['choose_option'],
                                   callback.message.chat.id,
                                   callback.message.message_id,
                                   reply_markup=self.menu_manager.get_menu_markup(previous_menu_type))
        self.user_state_manager.update_menu(callback.from_user.id, callback.message.message_id, previous_menu)

    def _handle_forward(self, callback: CallbackQuery) -> None:
        user_state: UserState = self.user_state_manager.get_state(callback.from_user.id)
        menu_state: MenuState = user_state.menu.get(str(callback.message.message_id))
        menu: ApplicationsPaginationMenu = self.menu_manager.get_menu(MenuType.ADMIN_APPLICATIONS_PAGINATION_MENU)
        pagination: MenuPaginationState = menu_state.pagination
        next_page: int = pagination.page + 1
        applications: List[Application] = self.application_service.find_all_with_pagination(4, next_page)
        markup: InlineKeyboardMarkup = menu.create(applications, next_page)
        msg: Message = self.bot.edit_message_text(self.localization.lang['your_applications'],
                                                  callback.message.chat.id,
                                                  callback.message.message_id,
                                                  reply_markup=markup)
        next_menu_state: MenuState = MenuState(MenuType.ADMIN_APPLICATIONS_PAGINATION_MENU)
        next_menu_state.pagination.page = next_page
        self.user_state_manager.update_menu(callback.from_user.id, msg.message_id, next_menu_state)

    def _handle_backward(self, callback: CallbackQuery) -> None:
        user_state: UserState = self.user_state_manager.get_state(callback.from_user.id)
        menu_state: MenuState = user_state.menu.get(str(callback.message.message_id))
        menu: ApplicationsPaginationMenu = self.menu_manager.get_menu(MenuType.ADMIN_APPLICATIONS_PAGINATION_MENU)
        pagination: MenuPaginationState = menu_state.pagination
        next_page: int = pagination.page - 1
        if next_page < 0:
            return
        applications: List[Application] = self.application_service.find_all_with_pagination(4, next_page)
        markup: InlineKeyboardMarkup = menu.create(applications, next_page)

        msg: Message = self.bot.edit_message_text(self.localization.lang['your_applications'],
                                                  callback.message.chat.id,
                                                  callback.message.message_id,
                                                  reply_markup=markup)
        next_menu_state: MenuState = MenuState(MenuType.ADMIN_APPLICATIONS_PAGINATION_MENU)
        next_menu_state.pagination.page = next_page
        self.user_state_manager.update_menu(callback.from_user.id, msg.message_id, next_menu_state)

    def _handle_application(self, callback: CallbackQuery):
        app_id: int = self._get_application_id(callback.data)
        application: Application = self.application_service.find_by_id(app_id)
        message_text: str = self.application_util.assemble_app_text(application)
        markup: InlineKeyboardMarkup = self._assemble_markup(application)
        msg: Message = self.bot.edit_message_text(message_text,
                                                  callback.message.chat.id,
                                                  callback.message.message_id,
                                                  reply_markup=markup)
        menu_state: MenuState = MenuState(MenuType.ADMIN_SINGLE_APPLICATION_MENU)
        menu_state.current_application_id = application.id
        self.user_state_manager.update_menu(callback.from_user.id, msg.message_id, menu_state)

    def _get_application_id(self, callback_data: str) -> int:
        arr: List[str] = callback_data.split('_')
        return int(arr[len(arr) - 1])

    def _assemble_markup(self, app: Application) -> InlineKeyboardMarkup:
        menu: AdminSingleApplicationMenu = self.menu_manager.get_menu(MenuType.ADMIN_SINGLE_APPLICATION_MENU)
        operational_buttons_enabled: bool = app.application_status == ApplicationStatus.PENDING
        return menu.create(operational_buttons_enabled)


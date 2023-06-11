from typing import Optional

from telebot import TeleBot
from telebot import types

from db.constant.user_type import UserType
from db.model.model import User
from localization.localization import Localization
from menu.menu_manager import MenuManager
from menu.menu_type import MenuType
from state.menu_state import MenuState
from state.user_state_manager import UserStateManager
from state.user_state import UserState
from db.service.user_service import UserService


class AuthConversation:

    def __init__(
            self,
            bot: TeleBot,
            localization: Localization,
            menu_manager: MenuManager,
            user_state_manager: UserStateManager,
            user_service: UserService
    ):
        self.bot = bot
        self.localization = localization
        self.menu_manager = menu_manager
        self.user_state_manager = user_state_manager
        self.user_service = user_service

    def start_conversation(self, message: types.Message):
        user_state: Optional[UserState] = self.user_state_manager.get_state(
            message.from_user.id)
        is_authorized: bool = False if user_state is None else user_state.authorized
        if is_authorized:
            menu_type: MenuType = MenuType.MAIN_ADMIN if user_state.is_admin else MenuType.MAIN
            msg = self.bot.send_message(
                message.chat.id,
                self.localization.lang['choose_option'],
                reply_markup=self.menu_manager.get_menu_markup(menu_type))
            self.user_state_manager.update_menu(
                message.from_user.id, msg.id, MenuState(menu_type))
        else:
            msg = self.bot.send_message(
                message.chat.id,
                self.localization.lang['send_number_or_share_contacts'],
                reply_markup=self.menu_manager.get_menu_markup(MenuType.START))
            self.bot.register_next_step_handler(
                msg, self._process_phone_number)

    def _process_phone_number(self, message: types.Message):
        try:
            phone_number = self._get_phone_number(message)
            formated_phone_number = self._modify_phone_number(phone_number)
            user: Optional[User] = self._auth_user(
                message, formated_phone_number)
            auth_successful: bool = user is not None
            if auth_successful:
                menu_type: MenuType = self._get_proper_menu_markup(user)
                self.bot.send_message(
                    message.chat.id,
                    self.localization.lang['login_successful'],
                    reply_markup=types.ReplyKeyboardRemove())
                msg = self.bot.send_message(
                    message.chat.id,
                    self.localization.lang['choose_option'],
                    reply_markup=self.menu_manager.get_menu_markup(menu_type))
                self.user_state_manager.update_menu(
                    message.from_user.id, msg.id, MenuState(menu_type))
            else:
                self.bot.send_message(
                    message.chat.id,
                    self.localization.lang['auth_failed'],
                    reply_markup=types.ReplyKeyboardRemove())
        except Exception as e:
            print(e)
            self.bot.send_message(
                message.chat.id,
                self.localization.lang['something_went_wrong'],
                reply_markup=types.ReplyKeyboardRemove())
        finally:
            self.bot.clear_step_handler_by_chat_id(message.chat.id)

    def _auth_user(self, msg: types.Message, phone_number: str) -> Optional[User]:
        if phone_number is None:
            return None

        user_by_phone_number: Optional[User] = self.user_service.find_user_by_phone_number(
            phone_number)
        if user_by_phone_number is None:
            return None
        user_state = UserState(
            msg.chat.id, msg.from_user.id, user_by_phone_number.id)
        user_state.authorized = True
        user_state.is_admin = user_by_phone_number.user_type == UserType.ADMIN
        self.user_state_manager.update_state(user_state)
        return user_by_phone_number

    def _get_phone_number(self, msg: types.Message):
        content_type = msg.content_type
        phone_number = None
        if content_type == 'contact':
            phone_number = msg.contact.phone_number
        if content_type == 'text':
            phone_number = msg.text
        return phone_number

    def _get_proper_menu_markup(self, user: User) -> MenuType:
        if user.user_type == UserType.ADMIN:
            return MenuType.MAIN_ADMIN
        return MenuType.MAIN

    def _modify_phone_number(self, phone_number: str) -> Optional[str]:
        if phone_number is None:
            return None
        result: str = phone_number
        firt_symbol: str = phone_number[0]
        if firt_symbol != '+':
            result = '+' + result
        return result

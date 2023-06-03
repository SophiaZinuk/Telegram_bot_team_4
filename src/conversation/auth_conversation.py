from typing import Optional

from telebot import TeleBot
from telebot import types

from db.model.user import User
from localization.localization import Localization
from menu.menu_manager import MenuManager
from menu.menu_type import MenuType
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
        is_authorized: bool = self.user_state_manager.is_user_authorized(message.from_user.id)
        if is_authorized:
            msg = self.bot.send_message(
                message.chat.id,
                self.localization.lang['choose_option'],
                reply_markup=self.menu_manager.get_menu(MenuType.MAIN))
            self.user_state_manager.update_menu(message.from_user.id, msg.id, MenuType.MAIN)
        else:
            msg = self.bot.send_message(
                message.chat.id,
                self.localization.lang['send_number_or_share_contacts'],
                reply_markup=self.menu_manager.get_menu(MenuType.START))
            self.bot.register_next_step_handler(msg, self._process_phone_number)

    def _process_phone_number(self, message: types.Message):
        try:
            phone_number = self._get_phone_number(message)
            auth_successful: bool = self._auth_user(message, phone_number)
            if auth_successful:
                self.bot.send_message(
                    message.chat.id,
                    self.localization.lang['login_successful'],
                    reply_markup=types.ReplyKeyboardRemove())
                msg = self.bot.send_message(
                    message.chat.id,
                    self.localization.lang['choose_option'],
                    reply_markup=self.menu_manager.get_menu(MenuType.MAIN))
                self.user_state_manager.update_menu(message.from_user.id, msg.id, MenuType.MAIN)
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

    def _auth_user(self, msg: types.Message, phone_number: str) -> bool:
        if phone_number is None:
            return False

        user_by_phone_number: Optional[User] = self.user_service.find_user_by_phone_number(phone_number)
        if user_by_phone_number is None:
            return False
        user_state = UserState(msg.chat.id, msg.from_user.id)
        user_state.authorized = True
        self.user_state_manager.update_state(user_state)
        return True

    def _get_phone_number(self, msg: types.Message):
        content_type = msg.content_type
        phone_number = None
        if content_type == 'contact':
            phone_number = msg.contact.phone_number
        if content_type == 'text':
            phone_number = msg.text
        return phone_number

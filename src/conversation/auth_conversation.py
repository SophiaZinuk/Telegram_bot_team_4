from telebot import TeleBot
from telebot import types
from localization.localization import Localization
from menu.menu_manager import MenuManager
from menu.menu_type import MenuType
from state.user_state_manager import UserStateManager
from state.user_state import UserState


class AuthConversation:

    def __init__(
            self,
            bot: TeleBot,
            localization: Localization,
            menu_manager: MenuManager,
            user_state_manager: UserStateManager
    ):
        self.bot = bot
        self.localization = localization
        self.menu_manager = menu_manager
        self.user_state_manager = user_state_manager

    def start_conversation(self, message: types.Message):
        is_authorized: bool = self._is_user_authorized(message)
        if is_authorized:
            self.bot.send_message(
                message.chat.id,
                self.localization.lang['choose_option'],
                reply_markup=self.menu_manager.get_menu(MenuType.MAIN))
        else:
            msg = self.bot.send_message(
                message.chat.id,
                self.localization.lang['send_number_or_share_contacts'],
                reply_markup=self.menu_manager.get_menu(MenuType.START))
            self.bot.register_next_step_handler(
                msg, self._process_phone_number)

    def _process_phone_number(self, message: types.Message):
        try:
            phone_number = self._get_phone_number(message)
            auth_successful: bool = self._auth_user(message, phone_number)
            if auth_successful:
                self.bot.send_message(
                    message.chat.id,
                    self.localization.lang['login_successful'],
                    reply_markup=types.ReplyKeyboardRemove())
                self.bot.send_message(
                    message.chat.id,
                    self.localization.lang['choose_option'],
                    reply_markup=self.menu_manager.get_menu(MenuType.MAIN))
            else:
                raise Exception(self.localization.lang['Auth failed'])
        except Exception as e:
            self.bot.send_message(
                message.chat.id,
                self.localization.lang['something_went_wrong'],
                reply_markup=types.ReplyKeyboardRemove())
        finally:
            self.bot.clear_step_handler_by_chat_id(message.chat.id)

    def _auth_user(self, msg: types.Message, phone_number: str) -> bool:
        if phone_number is None:
            return False
        # go to file and check
        user_state = UserState(msg.chat.id, msg.from_user.id)
        user_state.authorized = True
        user_state.menu = MenuType.MAIN
        self.user_state_manager.update_state(user_state)
        return True

    def _get_phone_number(self, msg: types.Message):
        content_type = msg.content_type
        phone_number = None
        if content_type == 'contact':
            phone_number = msg.contact.phone_number
        if content_type == 'text':
            phone_number = msg.text
            return None
        return phone_number

    def _is_user_authorized(self, msg: types.Message) -> bool:
        user_state = self.user_state_manager.get_state(msg.from_user.id)
        if user_state is None:
            return False
        return user_state.authorized

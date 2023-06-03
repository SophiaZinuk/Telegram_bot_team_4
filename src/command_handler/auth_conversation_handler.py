from telebot import TeleBot
from telebot import types

from localization.localization import Localization
from menu.menu_manager import MenuManager
from menu.menu_type import MenuType
from state.user_state_manager import UserStateManager
from state.user_state import UserState


class AuthConversationHandler:

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

    def process_start(self, message: types.Message):
        is_authorized: bool = self._is_user_authorized(message)
        if is_authorized:
            self.bot.send_message(message.chat.id, self.localization.lang['choose_option'],
                                  reply_markup=self.menu_manager.get_menu(MenuType.MAIN))
        else:
            msg = self.bot.send_message(message.chat.id, self.localization.lang['send_number_or_share_contacts'],
                                        reply_markup=self.menu_manager.get_menu(MenuType.START))
            self.bot.register_next_step_handler(msg, self._process_phone_number)

    def _process_phone_number(self, message: types.Message):
        try:
            phone_number = self._get_phone_number(message)
            if phone_number is None:
                raise Exception(self.localization.lang['could_not_get_phone_number'])
            self._auth_user(message, phone_number)
            self.bot.send_message(message.chat.id, self.localization.lang['choose_option'],
                                  reply_markup=self.menu_manager.get_menu(MenuType.MAIN))
        except Exception as e:
            print(e)
            self.bot.reply_to(message, self.localization.lang['something_went_wrong'])

    def _auth_user(self, msg: types.Message, phone_number: str):
        user_state = UserState(msg.chat.id, msg.from_user.id)
        user_state.authorized = True
        user_state.menu = MenuType.MAIN
        self.user_state_manager.update_state(user_state)

    def _get_phone_number(self, msg):
        content_type = msg.content_type
        phone_number = None
        if content_type == 'contact':
            phone_number = msg.contact.phone_number
        if content_type == 'text':
            phone_number = msg.text
        return phone_number

    def _is_user_authorized(self, msg: types.Message) -> bool:
        user_state = self.user_state_manager.get_state(msg.from_user.id)
        if user_state is None:
            return False
        return user_state.authorized

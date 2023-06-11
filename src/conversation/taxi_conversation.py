from telebot import TeleBot
from telebot import types

from db.constant.application_status import ApplicationStatus
from db.constant.application_type import ApplicationType
from db.model.model import Application, ApplicationData, User
from db.service.application_service import ApplicationService
from db.service.user_service import UserService
from localization.localization import Localization
from menu.menu_manager import MenuManager
from state.taxi_application_state import TaxiApplicationState
from state.user_state import UserState
from state.user_state_manager import UserStateManager


class TaxiConversation:

    def __init__(
            self,
            bot: TeleBot,
            localization: Localization,
            menu_manager: MenuManager,
            user_state_manager: UserStateManager,
            application_service: ApplicationService,
            user_service: UserService
    ):
        self.bot = bot
        self.localization = localization
        self.menu_manager = menu_manager
        self.user_state_manager = user_state_manager
        self.application_service = application_service
        self.user_service = user_service

    def start_conversation(self, callback: types.CallbackQuery):
        try:
            msg = self.bot.send_message(callback.message.chat.id, 'Введіть номер таксі:')
            self.bot.register_next_step_handler(msg, self._process_taxi_number)
        except Exception as e:
            self.bot.send_message(
                callback.message.chat.id,
                self.localization.lang['something_went_wrong'])
            self.bot.clear_step_handler_by_chat_id(callback.message.chat.id)

    def _process_taxi_number(self, message: types.Message):
        try:
            taxi_number: str = self._get_taxi_number(message)
            self._update_state_with_taxi_application(message, taxi_number)
            user: User = self._save_taxi_application_to_db(message, taxi_number)
            reply_text: str = self.localization.lang['your_application_accepted_by_address'] + ' ' + user.address
            self.bot.send_message(message.chat.id, reply_text)
            self.bot.clear_step_handler_by_chat_id(message.chat.id)
        except Exception as e:
            print(e)
            self.bot.send_message(
                    message.chat.id,
                    self.localization.lang['something_went_wrong'])
            self.bot.clear_step_handler_by_chat_id(message.chat.id)

    def _get_taxi_number(self, msg: types.Message) -> str:
        return msg.text

    def _update_state_with_taxi_application(self, msg: types.Message, taxi_number: str):
        taxi_application: TaxiApplicationState = TaxiApplicationState()
        taxi_application.car_number = taxi_number
        self.user_state_manager.update_taxi_application(msg.from_user.id, taxi_application)

    def _save_taxi_application_to_db(self, msg: types.Message, taxi_number: str) -> User:
        user_state: UserState = self.user_state_manager.get_state(msg.from_user.id)
        user: User = self.user_service.find_user_by_id(user_state.db_id)

        application: Application = Application()
        application.created_by = user.id

        application_data: ApplicationData = ApplicationData()
        application_data.car_number = taxi_number

        application.application_type = ApplicationType.TAXI,
        application.application_status = ApplicationStatus.PENDING
        application.application_data = application_data
        self.application_service.create_application(application)
        return user


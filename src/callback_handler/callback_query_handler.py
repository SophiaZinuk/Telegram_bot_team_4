from telebot import types
from conversation.auth_conversation import AuthConversation
from callback_handler.callback_type import CallbackType
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler


class CallbackQueryHandler(GeneralCallbackQueryHandler):

    def __init__(
            self,
            auth_conversation: AuthConversation,
            main_menu_handler: GeneralCallbackQueryHandler
    ):
        self.auth_conversation = auth_conversation
        self.main_menu_handler = main_menu_handler
        self._init_handler_mapper()

    def handle(self, callback: types.CallbackQuery):
        handler: GeneralCallbackQueryHandler = self.handler_mapper[callback.data]
        handler.handle(callback)

    def _init_handler_mapper(self):
        self.handler_mapper = dict()
        self.handler_mapper[CallbackType.CREATE_APPLICATION] = self.main_menu_handler
        self.handler_mapper[CallbackType.APPLICATIONS_STATUS] = self.main_menu_handler
        self.handler_mapper[CallbackType.SECURITY_CONTACTS] = self.main_menu_handler
        self.handler_mapper[CallbackType.LOGOUT] = self.main_menu_handler

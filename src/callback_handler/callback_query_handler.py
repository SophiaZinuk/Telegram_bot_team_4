from telebot import types
from callback_handler.callback_type import CallbackType
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler


class CallbackQueryHandler(GeneralCallbackQueryHandler):

    def __init__(
            self,
            main_menu_handler: GeneralCallbackQueryHandler,
            applications_menu_callback_query_handler: GeneralCallbackQueryHandler
    ):
        self.main_menu_handler = main_menu_handler
        self.applications_menu_callback_query_handler = applications_menu_callback_query_handler
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

        self.handler_mapper[CallbackType.TAXI] = self.applications_menu_callback_query_handler
        self.handler_mapper[CallbackType.CARRIER] = self.applications_menu_callback_query_handler
        self.handler_mapper[CallbackType.GUESTS] = self.applications_menu_callback_query_handler
        self.handler_mapper[CallbackType.PARKING_PROBLEMS] = self.applications_menu_callback_query_handler
        self.handler_mapper[CallbackType.OTHER] = self.applications_menu_callback_query_handler
        self.handler_mapper[CallbackType.APPLICATIONS_BACK] = self.applications_menu_callback_query_handler

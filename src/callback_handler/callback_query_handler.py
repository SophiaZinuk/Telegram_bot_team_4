import telebot
from telebot import types
from callback_handler.admin.admin_callback_query_handler import AdminCallbackQueryHandler
from callback_handler.common.common_callback_query_handler import CommonCallbackQueryHandler
from callback_handler.user.user_callback_query_handler import UserCallbackQueryHandler
from localization.localization import Localization


class CallbackQueryHandler:

    def __init__(
            self,
            bot: telebot.TeleBot,
            localization: Localization,
            user_callback_query_handler: UserCallbackQueryHandler,
            admin_callback_query_handler: AdminCallbackQueryHandler,
            common_callback_query_handler: CommonCallbackQueryHandler
    ):
        self.bot = bot
        self.localization = localization
        self.user_callback_query_handler = user_callback_query_handler
        self.admin_callback_query_handler = admin_callback_query_handler
        self.common_callback_query_handler = common_callback_query_handler

    def handle(self, callback: types.CallbackQuery):
        try:
            is_admin_handler: bool = self.admin_callback_query_handler.is_handled(callback)
            if is_admin_handler:
                self.admin_callback_query_handler.handle(callback)
                return
            is_user_handler: bool = self.user_callback_query_handler.is_handled(callback)
            if is_user_handler:
                self.user_callback_query_handler.handle(callback)
                return
            is_common_handler: bool = self.common_callback_query_handler.is_handled(callback)
            if is_common_handler:
                self.common_callback_query_handler.handle(callback)
                return
        except Exception as e:
            print(e)
            self.bot.send_message(callback.message.chat.id,
                                  self.localization.lang['something_went_wrong'])

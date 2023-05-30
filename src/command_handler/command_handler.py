import telebot
from telebot import types
from conversation.auth_conversation import AuthConversation
from localization.localization import Localization
from command_handler.command import Command


class CommandHandler:

    def __init__(
            self,
            bot: telebot.TeleBot,
            auth_conversation: AuthConversation,
            localization: Localization
    ):
        self.bot = bot
        self.auth_conversation = auth_conversation
        self.localization = localization

    def handle_command(self, msg: types.Message):
        command: str = msg.text
        if command == '/' + Command.START:
            self._handle_start(msg)
        if command == '/' + Command.USE:
            self._handle_use(msg)
        if command == '/' + Command.ABOUT:
            self._handle_about(msg)

    def _handle_start(self, msg: types.Message):
        try:
            start_text: str = self._assemble_start_text()
            self.bot.send_message(msg.chat.id, start_text)
        except Exception as e:
            self.bot.send_message(
                msg.chat.id,
                self.localization.lang['something_went_wrong'],
                reply_markup=types.ReplyKeyboardRemove())

    def _handle_use(self, msg: types.Message):
        try:
            self.auth_conversation.start_conversation(msg)
        except Exception as e:
            self.bot.send_message(
                msg.chat.id,
                self.localization.lang['something_went_wrong'],
                reply_markup=types.ReplyKeyboardRemove())

    def _handle_about(self, msg: types.Message):
        try:
            self.bot.send_message(
                msg.chat.id, self.localization.lang['about_bot'])
        except Exception as e:
            self.bot.send_message(
                msg.chat.id,
                self.localization.lang['something_went_wrong'])

    def _assemble_start_text(self) -> str:
        text: str = ''
        text += self.localization.lang['use_following_commands'] + ':\n\n'
        text += '/' + Command.USE + ' - ' + \
            self.localization.lang['use_description'] + '\n'
        text += '/' + Command.ABOUT + ' - ' + \
            self.localization.lang['about_description'] + '\n\n'
        return text

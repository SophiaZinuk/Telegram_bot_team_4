from typing import List
from telebot.types import BotCommand
from localization.localization import Localization
from command_handler.command import Command


class CommandsMenu:

    def __init__(self, localization: Localization, ):
        self.localization = localization

    def create(self) -> List[BotCommand]:
        return [
            BotCommand(command='/' + Command.USE, description=self.localization.lang['use_description']),
            BotCommand(command='/' + Command.ABOUT, description=self.localization.lang['about_description'])
        ]

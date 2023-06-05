import sqlalchemy
import telebot
from telebot import TeleBot
from telebot import types

from conversation.auth_conversation import AuthConversation
from db.service.application_service import ApplicationService
from localization.language import Language
from localization.localization import Localization
from menu.menu_manager import MenuManager
from state.user_state_manager import UserStateManager
from command_handler.command_handler import CommandHandler
from callback_handler.callback_query_handler import CallbackQueryHandler
from callback_handler.main_menu_callback_query_handler import MainMenuCallbackQueryHandler
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler
from callback_handler.applications_menu_callback_query_handler import ApplicationsMenuCallbackQueryHandler
from menu.commands_menu import CommandsMenu
from command_handler.command import Command
from conversation.taxi_conversation import TaxiConversation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import atexit
from db.service.user_service import UserService

API_TOKEN: str = '6239359393:AAFHvCEytie9oAQ0F_X1rNiLOx2P5907O3c'
DATA_BASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/residental_bot'

# db
engine: sqlalchemy.Engine = create_engine(DATA_BASE_URL)
Session = sessionmaker(bind=engine)
session: Session = Session()

user_service: UserService = UserService(session)
application_service: ApplicationService = ApplicationService(session)

# bot
bot: TeleBot = telebot.TeleBot(API_TOKEN)

# localization
localization: Localization = Localization(Language.UA)

# menu
commands_menu: CommandsMenu = CommandsMenu(localization)

# menu manager
menu_manager: MenuManager = MenuManager(localization)

# user state
user_state_manager: UserStateManager = UserStateManager()

# conversations
auth_conversation: AuthConversation = AuthConversation(bot, localization, menu_manager, user_state_manager,
                                                       user_service)
taxi_conversation: TaxiConversation = TaxiConversation(bot, localization, menu_manager, user_state_manager,
                                                       application_service, user_service)

# handlers
command_handler: CommandHandler = CommandHandler(bot, auth_conversation, localization)
main_menu_callback_query_handler: GeneralCallbackQueryHandler = MainMenuCallbackQueryHandler(
    bot,
    localization,
    menu_manager,
    user_state_manager)
applications_menu_callback_query_handler: GeneralCallbackQueryHandler = ApplicationsMenuCallbackQueryHandler(
    bot,
    localization,
    menu_manager,
    user_state_manager,
    taxi_conversation
)
callback_query_handler: GeneralCallbackQueryHandler = CallbackQueryHandler(
    main_menu_callback_query_handler,
    applications_menu_callback_query_handler
)


def exit_handler():
    session.close()


@bot.message_handler(commands=[Command.START, Command.USE, Command.ABOUT])
def handle_command(message: types.Message):
    command_handler.handle_command(message)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(callback: types.CallbackQuery):
    callback_query_handler.handle(callback)


atexit.register(exit_handler)

bot.set_my_commands(commands_menu.create())
bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()
bot.infinity_polling()

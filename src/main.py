import atexit

import sqlalchemy
import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telebot import TeleBot
from telebot import types

from callback_handler.admin.admin_applications_pagination_menu_callback_query_handler import \
    AdminApplicationsPaginationMenuCallbackQueryHandler
from callback_handler.admin.admin_callback_query_handler import AdminCallbackQueryHandler
from callback_handler.admin.admin_single_application_callback_query_handler import \
    AdminSingleApplicationCallbackQueryHandler
from callback_handler.admin.main_admin_menu_callback_query_handler import MainAdminMenuCallbackQueryHandler
from callback_handler.callback_query_handler import CallbackQueryHandler
from callback_handler.common.common_callback_query_handler import CommonCallbackQueryHandler
from callback_handler.general_callback_query_handler import GeneralCallbackQueryHandler
from callback_handler.user.applications_menu_callback_query_handler import ApplicationsMenuCallbackQueryHandler
from callback_handler.user.applications_pagination_menu_callback_query_handler import \
    ApplicationsPaginationMenuCallbackQueryHandler
from callback_handler.user.main_menu_callback_query_handler import MainMenuCallbackQueryHandler
from callback_handler.user.single_application_callback_query_handler import SingleApplicationCallbackQueryHandler
from callback_handler.user.user_callback_query_handler import UserCallbackQueryHandler
from command_handler.command import Command
from command_handler.command_handler import CommandHandler
from conversation.auth_conversation import AuthConversation
from conversation.taxi_conversation import TaxiConversation
from db.service.application_service import ApplicationService
from db.service.user_service import UserService
from db.util.application_util import ApplicationUtil
from localization.dynamic_localization import DynamicLocalization
from localization.language import Language
from localization.localization import Localization
from menu.commands_menu import CommandsMenu
from menu.menu_manager import MenuManager
from state.user_state_manager import UserStateManager

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
dynamic_localization: DynamicLocalization = DynamicLocalization(localization)

# util
application_util: ApplicationUtil = ApplicationUtil(localization, dynamic_localization)

# menu
commands_menu: CommandsMenu = CommandsMenu(localization)

# menu manager
menu_manager: MenuManager = MenuManager(localization, dynamic_localization)

# user state
user_state_manager: UserStateManager = UserStateManager()

# conversations
auth_conversation: AuthConversation = AuthConversation(bot, localization, menu_manager, user_state_manager,
                                                       user_service)
taxi_conversation: TaxiConversation = TaxiConversation(bot, localization, menu_manager, user_state_manager,
                                                       application_service, user_service)

# handlers
command_handler: CommandHandler = CommandHandler(bot, auth_conversation, localization)
single_application_callback_query_handler: GeneralCallbackQueryHandler = SingleApplicationCallbackQueryHandler(
    bot,
    localization,
    menu_manager,
    user_state_manager,
    application_service
)
admin_single_application_callback_query_handler: GeneralCallbackQueryHandler = AdminSingleApplicationCallbackQueryHandler(
    bot,
    localization,
    menu_manager,
    user_state_manager,
    application_service,
    application_util
)
main_menu_callback_query_handler: GeneralCallbackQueryHandler = MainMenuCallbackQueryHandler(
    bot,
    localization,
    menu_manager,
    user_state_manager,
    application_service,
)
main_admin_menu_callback_query_handler: GeneralCallbackQueryHandler = MainAdminMenuCallbackQueryHandler(
    bot,
    localization,
    menu_manager,
    user_state_manager,
    application_service
)
applications_menu_callback_query_handler: GeneralCallbackQueryHandler = ApplicationsMenuCallbackQueryHandler(
    bot,
    localization,
    menu_manager,
    user_state_manager,
    taxi_conversation
)
applications_pagination_menu_callback_query_handler: GeneralCallbackQueryHandler = \
    ApplicationsPaginationMenuCallbackQueryHandler(
        bot,
        localization,
        menu_manager,
        user_state_manager,
        application_service,
        application_util
    )
admin_applications_pagination_menu_callback_query_handler: GeneralCallbackQueryHandler = \
    AdminApplicationsPaginationMenuCallbackQueryHandler(
        bot,
        localization,
        menu_manager,
        user_state_manager,
        application_service,
        application_util
    )
admin_callback_query_handler: AdminCallbackQueryHandler = AdminCallbackQueryHandler(
    bot,
    localization,
    user_state_manager,
    main_admin_menu_callback_query_handler,
    admin_applications_pagination_menu_callback_query_handler,
    admin_single_application_callback_query_handler
)

user_callback_query_handler: UserCallbackQueryHandler = UserCallbackQueryHandler(
    bot,
    localization,
    user_state_manager,
    main_menu_callback_query_handler,
    applications_menu_callback_query_handler,
    applications_pagination_menu_callback_query_handler,
    single_application_callback_query_handler
)

common_callback_query_handler: CommonCallbackQueryHandler = CommonCallbackQueryHandler(
    bot,
    localization,
    menu_manager,
    user_state_manager,
    application_service
)

callback_query_handler: CallbackQueryHandler = CallbackQueryHandler(
    bot,
    localization,
    user_callback_query_handler,
    admin_callback_query_handler,
    common_callback_query_handler
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

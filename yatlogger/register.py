import json
import random
from pathlib import Path
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, CallbackContext, Updater, Filters
from .config import get_config


DIGITS = 6


def run_register_service(config_search_dir: Path = None):
    config, config_path = get_config(config_search_dir, return_path=True)
    print("Using config file", config_path)

    code = random.randint(0, sum([9 * (10 ** i) for i in range(DIGITS)]))
    code = str(code).zfill(DIGITS)
    print(f"Enter this code on Telegram to register the chat to the bot:\n{code}\n")

    def _start(update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hello, if you want to register, send me the passcode as a message."
        )

    def _msg(update: Update, context: CallbackContext):
        if update.message.text == code:
            chat_id = update.effective_chat.id
            if chat_id in config["users"]:
                context.bot.send_message(
                    chat_id=chat_id,
                    text="Hey, I know you already!",
                )
            else:
                config["users"].append(chat_id)
                with open(config_path, "w") as f:
                    json.dump(config, f)

                print("Registered", chat_id)

                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"""Succesfully registered this chat.
Note that currently running instances will not log messages to this chat.
You can stop the register process on the logging machine now.""",
                )

    bot = Updater(token=config["token"], use_context=True)
    bot.dispatcher.add_handler(CommandHandler('start', _start))
    bot.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), _msg))

    print("Press Ctrl+C to stop the bot")

    bot.start_polling()
    bot.idle()

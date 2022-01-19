import re
import json
import random
from pathlib import Path
import json
import time

from .bot import send, get_updates
from .config import get_config


DIGITS = 6


def run_register_service(config_search_dir: Path = None):
    config, config_path = get_config(config_search_dir, return_path=True)
    print("Using config file", config_path)

    code = random.randint(0, (10 ** DIGITS) - 1)
    code = str(code).zfill(DIGITS)
    print(f"Enter this code on Telegram to register the chat to the bot:\n{code}\n")

    print("Press Ctrl+C to stop the bot")

    token = config["token"]
    last_processed_update = -1
    start_date = time.time()
    try:
        while True:
            data = get_updates(token)

            for update in data["result"]:
                if update["update_id"] <= last_processed_update:
                    continue
                last_processed_update = update["update_id"]

                if "message" in update:
                    if update["message"]["date"] < start_date:
                        # this message has been sent before the register process was started
                        continue

                    text = update["message"]["text"]
                    chat_id = update["message"]["chat"]["id"]
                    if text == "/start":
                        send("Hello, if you want to register, send me the passcode as a message.", chat_id, token)
                    elif re.match(r"^\d+$", text):
                        if text == code:
                            if chat_id in config["users"]:
                                send("Hey, I know you already!", chat_id, token)
                            else:
                                config["users"].append(chat_id)

                                with open(config_path, "w") as f:
                                    json.dump(config, f, indent=2)

                                print("Registered", chat_id)
                                send(f"""Succesfully registered this chat ({chat_id}).
Note that currently running instances will not log messages to this chat.
You can stop the register process on the logging machine now.""", chat_id, token)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Register process stopped")

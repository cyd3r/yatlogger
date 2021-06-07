# Yet Another Telegram Logger

A python library to log messages and exceptions to your [Telegram bot](https://core.telegram.org/bots).

## Setup

### 1. Create a bot

First, [create a new bot](https://core.telegram.org/bots#creating-a-new-bot). It's basically sending some messages to [@BotFather](https://t.me/botfather).

### 2. Create a config file (`.yatlogger.json`)

Next, create a file named `.yatlogger.json` and place it in the same directory as your code or in a one of the parent directories. The file must look like this:

``` json
{
    "token": "<your api key>"
}
```

Replace `<your api key>` with the API key you got from the BotFather.

### 3. Register chats

Your bot must know to which chats it should send the logs. So the next step is to register receiving chats.

Run `python -m yatlogger` to start the register service. As long as this service is running, you can register new chats.

To register a chat, start a chat with your bot and enter the 6 digit pin you see on the logging machine.

![register a new chat](https://raw.githubusercontent.com/cyd3r/yatlogger/main/docs/register_chat.jpg)

When you are done, you can simply interrupt the register service with <kbd>Ctrl</kbd> + <kbd>C</kbd>

## Usage

yatlogger registers itself as a handler for the built-in [logging](https://docs.python.org/3/library/logging.html) module. Here is an example:

``` python
import logging
import yatlogger

logger = yatlogger.register()
logger.setLevel(logging.INFO)

logger.info("Read this on your phone!")

raise ValueError("This unhandled exception will be sent to Telegram, too!")

```

And the resulting chat messages:

![log messages on telegram](https://raw.githubusercontent.com/cyd3r/yatlogger/main/docs/logs.jpg)

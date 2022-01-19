import urllib.parse
import urllib.request
import re
import json


API_ENDPOINT = "https://api.telegram.org/bot"


def escape_markdown(text: str) -> str:
    escape_chars = re.escape(r"_*[]()~`>#+-=|{}.!")
    return re.sub(f"([{escape_chars}])", r"\\\1", text)


def send(markdown: str, chat_id: str, token: str, is_escaped=False):
    # https://core.telegram.org/bots/api#sendmessage
    query = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": markdown if is_escaped else escape_markdown(markdown),
        "parse_mode": "MarkdownV2",
    })
    try:
        with urllib.request.urlopen(f"{API_ENDPOINT}{token}/sendMessage?{query}") as response:
            assert response.status == 200, "Could not send message"
    except:
        print(f"{API_ENDPOINT}{token}/sendMessage?{query}")
        raise


def get_updates(token):
    # https://core.telegram.org/bots/api#getting-updates
    query = urllib.parse.urlencode({
        "timeout": 60, 
    })
    with urllib.request.urlopen(f"{API_ENDPOINT}{token}/getUpdates?{query}") as response:
        assert response.status == 200
        text = response.read().decode()
    return json.loads(text)

from Util.json_handle import JsonHandler

data = JsonHandler("template/bot.json", "load")

VERSION = data["version"];
CLIENT_ID = data["client_id"];
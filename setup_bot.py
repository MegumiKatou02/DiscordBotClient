from Util.jsonLoad import JsonLoad

data = JsonLoad("template/bot.json")

VERSION = data["version"];
CLIENT_ID = data["client_id"];
import json

def JsonLoad(path: str):
    data: str
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
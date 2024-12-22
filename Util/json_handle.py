import json

def JsonHandler(path: str, action: str, key: str = None, value: str = None):
    if action == "load":
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}  
        except json.JSONDecodeError:
            return {}  
    elif action == "save":
        try:
            data = JsonHandler(path, "load")
            data[key] = value
            with open(path, 'w') as f:
                json.dump(data, f, indent=4) 
        except Exception as e:
            print(f"Lỗi khi ghi file JSON: {e}")

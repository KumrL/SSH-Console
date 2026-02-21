import json

class JsonManager:
    def __init__(self):
        self.json_file = "data/commands.json"

    def jread(self):
        with open(self.json_file, "r") as f:
            data = json.load(f)
            return data["commands"]

    def jwrite(self, name, command):
        data = self.jread()
        data.append({"name": name, "command": command})
        with open(self.json_file, "w") as f:
            data = {
                "commands" : data
            }
            json.dump(data, f, indent=4)
        return None

    def jdelete(self, id):
        data = self.jread()
        data.pop(id)
        with open(self.json_file, "w") as f:
            data = {
                "commands" : data
            }
            json.dump(data, f, indent=4)
        return None

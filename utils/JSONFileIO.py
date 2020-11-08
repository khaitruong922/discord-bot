import json
import os


class JSONFileIO:
    def __init__(self, file_name):
        self.file_name = file_name

    def get(self):
        with open(self.file_name) as file:
            return json.load(file)

    def write(self, data):
        with open(self.file_name, 'w') as file:
            json_text = json.dumps(data, indent=2)
            file.write(json_text)

    def get_size(self):
        return round(os.stat(self.file_name).st_size / 1024, 2)

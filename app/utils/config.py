import json


class Options:
    def __init__(self):
        f = open('app/utils/config.json')
        _options = json.load(f)
        f.close()
        self.width = _options["width"]
        self.height = _options["height"]
        self.fps = _options["fps"]
        self.ip = _options["ip"]
        self.port = _options["port"]
        self.threshold = _options["threshold"]


options = Options()

import json


class Options:
    def __init__(self):
        _file = open('app/utils/config.json')
        _options = json.load(_file)
        _file.close()
        self.width = _options["width"]
        self.height = _options["height"]
        self.fps = _options["fps"]
        self.ip = _options["ip"]
        self.port = _options["port"]
        self.threshold = _options["threshold"]
        self.frames_per_sample = _options["frames_per_sample"]

    def save_default_ip(self, ip):
        self.ip = ip
        _config = {
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "ip": self.ip,
            "port": self.port,
            "threshold": self.threshold,
            "frames_per_sample": self.frames_per_sample
        }
        _json_object = json.dumps(_config, indent=4)
        with open("app/utils/config.json", "w") as _file:
            _file.write(_json_object)


options = Options()

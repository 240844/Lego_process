import json


class Options:
    def __init__(self):
        try:
            _file = open('app/utils/config.json')
            _options = json.load(_file)
            _file.close()
            self.width = _options["width"]
            self.height = _options["height"]
            self.fps = _options["fps"]
            self.ip = _options["ip"]
            self.port = _options["port"]
            self.threshold = _options["threshold"]
            self.alarm_threshold = _options["alarm_threshold"]
            self.frames_per_sample = _options["frames_per_sample"]
            self.min_object_size = _options["min_object_size"]
            self.max_object_size = _options["max_object_size"]
        except FileNotFoundError:
            print("#### Config file not found. Creating new one.")
            self.loadDefault()
            self.saveConfig()
        except KeyError as e:
            print(f"#### Config file corrupted!!! {str(e)} not found.")
            self.loadDefault()


    def loadDefault(self):
        print("#### Loading default config.")
        self.width = 720
        self.height = 1280
        self.fps = 30
        self.ip = "192.168.1.16"
        self.port = 8080
        self.threshold = 0.5
        self.alarm_threshold = 0.5
        self.frames_per_sample = 5
        self.min_object_size = 300
        self.max_object_size = 9000

    def saveConfig(self):
        _config = {
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "ip": self.ip,
            "port": self.port,
            "threshold": self.threshold,
            "alarm_threshold": self.alarm_threshold,
            "frames_per_sample": self.frames_per_sample,
            "min_object_size": self.min_object_size,
            "max_object_size": self.max_object_size,
        }
        _json_object = json.dumps(_config, indent=4)
        with open("app/utils/config.json", "w") as _file:
            _file.write(_json_object)
        print("#### Config file saved.")


options = Options()

from jsonmerge import merge

class Server():
    def __init__(self, app):
        self.__app = app
        self.__config = {
                "server": {
                    "socket":"",
                    "ip":"0.0.0.0",
                    "port": 3000
                },
                "debug":False
            }

    def start(self, options=None):
        if options:
            self.__config = merge(self.__config, options)
        self.__app.run(debug=self.__config["debug"], port=self.__config["server"]["port"], host=self.__config["server"]["ip"])
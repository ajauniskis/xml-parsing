import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read("./app/config.ini")
    return config


config = read_config()

DATABASE_URL = config["DATABASE"]["url"]

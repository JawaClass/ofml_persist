import configparser
from pathlib import Path
import os

config = configparser.ConfigParser()
config_file = Path(os.path.dirname(os.path.abspath(__file__))) / 'config.ini'
suc = config.read(config_file)
 
if not suc:
    raise ValueError(f"No config.ini was found at {config_file}. Provide this file based on config.ini.sample")

db_config = {
    "host": config.get('database', 'host'),
    "port": config.getint('database', 'port'),
    "user": config.get('database', 'user'),
    "password": config.get('database', 'password'),
    "db": config.get('database', 'db'),
}

email_config = {
    "username": config.get('email', 'username'),
    "password": config.get('email', 'password'),
    "host": config.get('email', 'host'),
    "port": config.getint('email', 'port'),
    "tls": config.getboolean('email', 'tls'),
}
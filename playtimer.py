import configparser
import psutil
import json
import io
import os
import threading


def write_json(data):
    with open('data.json') as json_file:
        json.dump(data, json_file, indent=2)


def init():
    file_paths = ['data.json', 'config.ini', 'blacklist.txt', 'whitelist.txt']
    for path in file_paths:
        if not os.path.exists(path):
            open(path, 'w+').close()


    config_file = configparser.ConfigParser()
    config_file.read('config.ini')
    config = config_file['config']

    json_ = None
    with open('data.json', 'r') as json_file:
        json_ = json.load(json_file)
        json_file.close()

    for proc in psutil.process_iter():
        try:
            processName = str(proc.name())
            processID = proc.pid

            json_[processName] = {'index': 0, 'id': 0, 'playtime': 0}

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    write_json(json_)


init()

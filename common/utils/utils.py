import configparser
import hashlib
import json
import os
import subprocess
import time
from collections import namedtuple
from os import listdir
from os.path import isfile, join


def object_to_json(custom_object: object) -> str:
    json_str = None
    if custom_object is not None:
        json_str = json.dumps(custom_object)

    return json_str


def json_to_object(json_str: str) -> object:
    return json.loads(json_str)


def _custom_object_decoder(object_dict):
    return namedtuple('X', object_dict.keys())(*object_dict.values())


def write_file(file_path: str, content_str: str):
    file = open(file_path, "w")
    file.write(content_str)
    file.close()


def read_file(file_path: str) -> str:
    f = open(file_path, "r")
    content = f.read()
    f.close()
    return content


def get_files_dir(file_path):
    return [file for file in listdir(file_path) if isfile(join(file_path, file))]


def get_subdirs_name(path) -> list:
    return [f.name for f in os.scandir(path) if f.is_dir()]


def bytes_to_gib(bytes: int):
    return bytes / 0.000000000931323


def win_map_net_drive():
    server_config = configparser.ConfigParser()
    server_config.read("config/server.cfg")

    command = "net use " + server_config.get("global", "mappingLetter") + ": \\\\" + server_config.get("global",
                                                                                                       "serverIp") + server_config.get(
        "global", "pathName").replace("/", "\\") + " /USER:" + server_config.get("user",
                                                                                "userLogin") + " " + server_config.get(
        "user", "psswdLogin") + " /p:yes"

    subprocess.Popen(command)
    time.sleep(1)


def win_delete_net_drive():
    server_config = configparser.ConfigParser()
    server_config.read("config/server.cfg")
    subprocess.Popen("net use " + server_config.get("global", "mappingLetter") + "/delete")


def encrypt_txt(plain_txt: str):
    return hashlib.sha256(plain_txt.encode()).hexdigest()

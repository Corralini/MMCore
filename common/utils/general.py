import configparser
import glob
import os
import pathlib
import platform
import random
import shutil
import socket
import string
import time
from datetime import datetime
from typing import Iterable

import psutil
import win32serviceutil

from common.model.disk import Disk
from common.model.memory import Memory
from common.model.process import Process
from common.model.user import User
from common.utils.utils import write_file, read_file, get_files_dir, object_to_json, get_subdirs_name, json_to_object


def get_processes():
    return psutil.process_iter()


def parse_process(ps_process) -> Process:
    process = None
    if ps_process is not None:
        process = Process()
        if hasattr(ps_process, "pid"):
            process.set_id(ps_process.pid)
        if hasattr(ps_process, "name"):
            process.set_name(ps_process.name())
        if hasattr(ps_process, "status"):
            process.set_status(ps_process.status())
        if hasattr(ps_process, "create_time") and ps_process.create_time() != 0.0:
            process.set_started_date(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(ps_process.create_time())))

    return process


def parse_process_dict(process_dict) -> Process:
    process = None
    if process_dict is not None:
        process = Process()
        if "_id" in process_dict:
            process.set_id(process_dict['_id'])
        if "_name" in process_dict:
            process.set_name(process_dict['_name'])
        if "_status" in process_dict:
            process.set_status(process_dict['_status'])
        if "_started_date" in process_dict:
            process.set_started_date(process_dict['_started_date'])

    return process


def kill_process(pid):
    try:
        psutil.Process(int(pid)).terminate()
    except():
        print("Process with PID " + pid + " can not be stopped.")


def generate_file_name():
    return datetime.now().strftime("%d%m%Y%H%M%S") + ".dat"


def write_data(subfolder, data):
    server_config = configparser.ConfigParser()
    server_config.read("config/server.cfg")

    hostname = socket.gethostname()
    path = server_config.get("global", "mappingLetter") + ":/" + hostname + "/information/" + subfolder + "/"
    if not os.path.exists(path):
        os.makedirs(path)

    write_file(path + generate_file_name(), data)


# method to process files in instructions
def process_instructions():
    server_config = configparser.ConfigParser()
    server_config.read("config/server.cfg")

    hostname = socket.gethostname()
    path = server_config.get("global", "mappingLetter") + ":/" + hostname + "/instructions/"

    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    files = get_files_dir(path)

    for file in files:
        file_path = path + file
        if file.split("-")[1].split(".")[0] == "Pending":
            file_content = read_file(file_path)

            if file_content.split(";")[0] == "service":

                if platform.system() == "Windows":
                    services = _get_win_services()

                    for service in services:
                        if str(service.name()) == file_content.split(";")[1]:
                            new_name = path + instruction_name_file("Processing")
                            os.rename(file_path, new_name)
                            try:
                                if file_content.split(";")[2] == "start":
                                    win32serviceutil.StartService(service.name())
                                elif file_content.split(";")[2] == "stop":
                                    win32serviceutil.StopService(service.name())
                                elif file_content.split(";")[2] == "restart":
                                    win32serviceutil.RestartService(service.name())

                                os.rename(new_name, path + instruction_name_file("OK"))
                            except():
                                os.rename(new_name, path + instruction_name_file("KO"))

                elif platform.system() == "Linux":
                    pass

            elif file_content.split(";")[0] == "process":
                new_name = path + instruction_name_file("Processing")
                os.rename(file_path, new_name)
                try:
                    kill_process(file_content.split(";")[1])
                    os.rename(new_name, path + instruction_name_file("OK"))
                except():
                    os.rename(new_name, path + instruction_name_file("KO"))


def _get_win_services() -> Iterable:
    return psutil.win_service_iter()


# CPU usage
def get_cpu_usage():
    return psutil.cpu_percent()


# Memory data
def get_memory():
    return parse_memory(psutil.virtual_memory()._asdict())


# System Memory parse to own Memory Object
def parse_memory(sys_memory):
    memory = None
    if sys_memory is not None:
        memory = Memory()
        memory.set_total(sys_memory['total'])
        memory.set_available(sys_memory['available'])
        memory.set_used(sys_memory['used'])

    return memory


def get_disks_usage() -> list:
    main_config = configparser.ConfigParser()
    main_config.read("config/main.cfg")
    disks_config = main_config.items("disk")

    disks = []
    for key, disk in disks_config:
        disks.append(parse_disk(disk, shutil.disk_usage(disk)._asdict()))

    return disks


def parse_disk(name: str, sys_disk):
    disk = None
    if sys_disk is not None:
        disk = Disk()
        disk.set_name(name)
        disk.set_total(sys_disk['total'])
        disk.set_free(sys_disk['free'])
        disk.set_used(sys_disk['used'])
    return disk


def instruction_name_file(status="Pending") -> str:
    return datetime.now().strftime("%d%m%Y%H%M%S") + "-" + status + ".dat"


# Create file with instructions
def create_instruction(serverName, content):
    server_config = configparser.ConfigParser()
    server_config.read("config/server.cfg")

    file_path = server_config.get("global",
                                  "mappingLetter") + ":/" + serverName + "/instructions/" + instruction_name_file()

    write_file(file_path, content)


# Core create user session logged

def create_user_session(user: User):
    file_name = str(user.get_id()) + ''.join(
        random.choices(string.ascii_letters + string.digits, k=16 - len(str(user.get_id())))) + ".dat"
    path = ""
    if platform.system() == "Windows":
        path = str(pathlib.Path().resolve()) + "\\currentSessions\\"
    if platform.system() == "Linux":
        path = str(pathlib.Path().resolve()) + "/currentSessions/"

    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    write_file(path + file_name, object_to_json(user.__dict__))


def get_servers() -> list:
    server_config = configparser.ConfigParser()
    server_config.read("config/server.cfg")

    return get_subdirs_name(server_config.get("global", "mappingLetter") + ":/")


def get_latest_file(server_name, subfolder) -> pathlib.Path:
    server_config = configparser.ConfigParser()
    server_config.read("config/server.cfg")

    file_path = server_config.get("global",
                                  "mappingLetter") + ":/" + server_name + "/information/" + subfolder + "/"
    list_files = glob.glob(file_path + "*")

    file = None

    if len(list_files) != 0:
        file = pathlib.Path(max(list_files, key=os.path.getctime))

    return file


def parse_data(object_json_list):
    object_list_parsed = []

    for object_json in object_json_list:
        object_list_parsed.append(json_to_object(object_json))

    return object_list_parsed

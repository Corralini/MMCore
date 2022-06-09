import configparser
import pathlib
from os.path import exists

from flask import Flask, request, jsonify

from common.model.response import Response
from common.model.user import User
from common.utils.general import create_user_session, get_latest_file, parse_data, get_servers, create_instruction
from common.utils.utils import encrypt_txt, read_file, json_to_object, win_map_net_drive, win_delete_net_drive

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Welcome MMCore API'


@app.route('/detailed', methods=['POST'])
def detailed():
    response = Response()
    request_json = request.json
    session_path = _check_login(request_json["userId"])

    if exists(session_path):

        main_config = configparser.ConfigParser()
        main_config.read("config/main.cfg")

        serverName = request_json["serverName"]
        servers_data = {}

        if serverName is not None and serverName != "" and get_latest_file(serverName,
                                                                           "general") is not None and get_latest_file(
            serverName, "services") and get_latest_file(serverName, "processes"):
            data = {}

            # Parse info data
            try:
                last_info_file = get_latest_file(serverName, "general")

                info_object = json_to_object(read_file(str(last_info_file)))

                data["general"] = {last_info_file.stem: {"_cpu_usage": info_object["_cpu_usage"],
                                                         "_disks": parse_data(json_to_object(info_object["_disks"])),
                                                         "_memory": json_to_object(info_object["_memory"])}}

                # End parse General info

                # Parse services data

                last_services_file = get_latest_file(serverName, "services")

                data["services"] = {
                    last_services_file.stem: parse_data(json_to_object(read_file(str(last_services_file))))}

                # End parse services data

                # Parse process

                last_process_file = get_latest_file(serverName, "processes")

                data["processes"] = {
                    last_process_file.stem: parse_data(json_to_object(read_file(str(last_process_file))))}

                # End parse process

                servers_data[serverName] = data
                response.set_status("OK")
                response.set_data(servers_data)
            except ():
                response.set_status("KO")
                response.set_data({"error": "Unable to find data for " + serverName})

        else:
            response.set_status("KO")
            response.set_data({"error": "Unable to find data"})



    else:
        response.set_status("KO")
        response.set_data({"error": "User not login"})

    return jsonify(response.__dict__)


@app.route('/', methods=['POST'])
def home():
    response = Response()
    request_json = request.json
    session_path = _check_login(request_json["userId"])

    if exists(session_path):

        main_config = configparser.ConfigParser()
        main_config.read("config/main.cfg")
        servers_data = {}

        servers = get_servers()

        for server in servers:
            data = {}

            # Parse info data
            try:
                last_info_file = get_latest_file(server, "general")

                info_object = json_to_object(read_file(str(last_info_file)))

                data["general"] = {last_info_file.stem: {"_cpu_usage": info_object["_cpu_usage"],
                                                         "_disks": parse_data(json_to_object(info_object["_disks"])),
                                                         "_memory": json_to_object(info_object["_memory"])}}

                # End parse General info

                # Parse services data

                services = parse_data(json_to_object(read_file(str(get_latest_file(server, "services")))))

                serv_not_run_auto = []
                for service in services:
                    if service["_start_type"] == "automatic" and service["_status"] != "running":
                        serv_not_run_auto.append(service)

                data["serv_not_running_auto"] = serv_not_run_auto
                # End parse services data

                servers_data[server] = data
                response.set_status("OK")
                response.set_data(servers_data)

            except ():
                response.set_status("KO")
                response.set_data({"error": "Unable to find data for " + server})

    else:
        response.set_status("KO")
        response.set_data({"error": "User not login"})

    return jsonify(response.__dict__)


@app.route('/instruction', methods=['POST'])
def send_instruction():
    response = Response()
    request_json = request.json
    session_path = _check_login(request_json["userId"])

    if exists(session_path):
        server_name = request_json["serverName"]
        data_json = request_json["data"]
        if server_name is not None and server_name != "" and data_json is not None:
            type = data_json["type"]
            id = data_json["id"]
            action = ""
            if "action" in data_json:
                action = data_json["action"]

            instruction = ""

            if type is not None and type == "service" and action is not None and id is not None:
                instruction = str(type) + ";" + str(id) + ";" + str(action)
            elif type is not None and type == "process" and id is not None:
                instruction = str(type) + ";" + str(id)

            create_instruction(server_name, instruction)
            response.set_status("OK")

        else:
            response.set_status("KO")
            response.set_data({"error": "Invalid request"})

    else:
        response.set_status("KO")
        response.set_data({"error": "User not login"})

    return jsonify(response.__dict__)


@app.route('/login', methods=['POST'])
def login():
    user = User()
    user.set_id(6500)
    user.set_user("corral")
    user.set_psswd(encrypt_txt("abc123."))
    create_user_session(user)
    return 'Login brruuh'


def _check_login(userId):
    return str(pathlib.Path().resolve()) + "\\currentSessions\\" + userId + ".dat"


if __name__ == '__main__':
    win_map_net_drive()
    try:
        main_config = configparser.ConfigParser()
        main_config.read("config/main.cfg")

        app.run(debug=True, port=int(main_config.get("global", "port")), host='127.0.0.1')
    finally:
        win_delete_net_drive()

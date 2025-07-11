import re
import os

class GetContent:
    def __init__(self):
        self.write_keyword_name = "\nKeyword Name Here\n    "
        self.known_body_prefixes = ['--data', '--data-raw', '--form', '--data-urlencode']
        self.json_prefixes = ['json', '--data', '--data-raw']
        self.formdata_prefixes = ['formdata', '--form']
        self.urlencoded_prefixes = ['urlencoded', '--data-urlencode']
        self.header_prefix = "--header"

    def get_url(self, curl_path):
        with open(curl_path, encoding='utf-8') as f: 
            curl = f.read()

        url = re.search(r"'([^']+)", curl)
        url = url.group().replace("'", "")
        return url

    def get_headers(self, curl_path):
        with open(curl_path, encoding='utf-8') as f:
            curl = f.read()

        headers = re.findall(fr"{self.header_prefix}\s+'([^:]+):\s*([^']+)'", curl)
        headers_len = len(headers)

        indice = 0
        values_list = []

        while indice < headers_len:
            header_tuple = headers[indice]
            robot_format = f"{header_tuple[0]}={header_tuple[1]}"
            indice += 1
            values_list.append(f"...    {robot_format}\n    ")
        return values_list

    def content_formdata(self, robot_path, curl_path, body_prefix, has_file):
        indice = 0
        url = self.get_url(curl_path)

        with open(curl_path, encoding='utf-8') as f:
            curl = f.read()
            body = re.findall(fr"{body_prefix}\s+'([^']+)'", curl)
            body_len = len(body)

        with open(robot_path, 'a') as f:
            f.write(self.write_keyword_name)
            f.write(f"Create Session    session    {url}\n\n")
            f.write("    ${form_data}=    Create Dictionary\n    ")
            while indice < body_len:
                body_new = body[indice]
                f.write(f"...    {body_new}\n    ")
                indice += 1

        indice = 0
        with open(robot_path, 'a') as f:
            if has_file == "n":
                f.write("\n    ${response}=    REQUEST On Session    session    /\n    ...    data=${form_data}")
                return None
            f.write("\n    ${files}=    Create Dictionary\n    ...    file_path=here\n")
            f.write("\n    ${response}=    REQUEST On Session    session    /\n    ...    files=${files}\n    ...    data=${form_data}")

    def content_json(self, headers, robot_path, curl_path, body_prefix):
        indice = 0
        url = self.get_url(curl_path)

        with open(curl_path, encoding='utf-8') as f:
            curl = f.read()
            body_w_prefix = re.search(fr"{body_prefix}\s+'([^']+)'", curl)
            body = body_w_prefix.group(1)
            body = body.replace('\n', "").replace(" ", "")

        with open(robot_path, 'a') as f:
            f.write(self.write_keyword_name)
            f.write(f"Create Session    session    {url}\n\n")
            f.write("    ${headers}=    Create Dictionary\n    ")
            while indice < len(headers):
                header_value = headers[indice]
                f.write(header_value)
                indice += 1
            f.write(f"\n    ${{body}}=    Set Variable    {body}\n")
            f.write("\n    ${response}=    REQUEST On Session    session    /\n    ...    headers=${headers}\n    ...    data=${body}")

    def content_urlencoded(self, headers, robot_path, curl_path, body_prefix):
        indice = 0
        url = self.get_url(curl_path)

        with open(curl_path, encoding='utf-8') as f:
            curl = f.read()
            body_w_prefix = re.findall(fr"{body_prefix}\s+'([^']+)'", curl)
            body_len = len(body_w_prefix)

        with open(robot_path, 'a') as f:
            f.write(self.write_keyword_name)
            f.write(f"Create Session    session    {url}\n\n")
            f.write("    &{data}=    Create Dictionary\n    ")
            while indice < body_len:
                body = body_w_prefix[indice]
                f.write(f"...    {body}\n    ")
                indice += 1

        indice = 0
        with open(robot_path, 'a') as f:
            f.write("\n    ${headers}=    Create Dictionary\n    ")
            while indice < len(headers):
                header_value = headers[indice]
                f.write(header_value)
                indice += 1
            f.write("\n    ${response}=    REQUEST On Session    session    /\n    ...    headers=${headers}\n    ...    data=${data}")

    def no_body_requisition(self, headers, robot_path, curl_path):
        indice = 0
        url = self.get_url(curl_path)

        with open(robot_path, 'a') as f:
            f.write(self.write_keyword_name)
            f.write(f"Create Session    session    {url}\n\n")
            f.write("    ${headers}=    Create Dictionary\n    ")
            while indice < len(headers):
                header_value = headers[indice]
                f.write(header_value)
                indice += 1
            f.write("\n    ${response}=    REQUEST On Session    session    /\n    ...    headers=${headers}")

    def define_curl_type(self, headers, curl_path, robot_path, req_type):
        if req_type.lower() in self.formdata_prefixes:
            print("\nPrefix identified, formdata format selected\n")
            has_file = input("This request has a file? (Y/N):  ")
            has_file_formated = has_file.strip().lower()
            self.content_formdata(robot_path, curl_path, req_type, has_file_formated)

        elif req_type.lower() in self.json_prefixes:
            print("\nPrefix identified, json format selected\n")
            self.content_json(headers, robot_path, curl_path, req_type)

        elif req_type.lower() in self.urlencoded_prefixes:
            print("\nPrefix identified, urlencoded format selected\n")
            self.content_urlencoded(headers, robot_path, curl_path, req_type)

        elif req_type.lower() == "none":
            print("\nNone parameter received, changing request type.\n")
            self.no_body_requisition(headers, robot_path, curl_path)

class RobotCurl:
    content_class = GetContent()

    """
    Keep this way if you want to set paths here before execution
    Path to your curl file, save as .txt
    """
    # curl_path = "./curl.txt"
    # body_prefix = "--form"
    # robot_path = "./test.robot"

    """
    Keep this way if you want to type the paths on the terminal
    Path to your curl file, save as .txt
    """
    while True:
        curl_path = input("Give the path to the curl file: ")
        if os.path.exists(curl_path):
            break
    
    while True:
        robot_path = input("Give the path to write the robotframework code: ")
        if os.path.exists(robot_path):
            break

    with open(curl_path) as f:
        content = f.read()
        prefixes = re.findall(r"--[^\s]+", content)
        if prefixes[-1] != "--header" and prefixes[-1] != "--location":
            body_prefix = prefixes[-1]
        else:
            body_prefix = input("\nBody prefix not recognized.\nPlease type the requisition type or none if doesnt have body (formats: json, formdata or urlencoded): ")

    headers = content_class.get_headers(curl_path)
    content_class.define_curl_type(headers, curl_path, robot_path, body_prefix)
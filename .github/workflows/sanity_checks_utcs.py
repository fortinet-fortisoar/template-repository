import os
import re
import sys
import json
import language_tool_python
from datetime import datetime

current_year = datetime.now().year

copyright_pattern = re.compile(
    rf'"""\nCopyright start\nMIT License\nCopyright \(c\) {current_year} Fortinet Inc\nCopyright end\n"""',
    re.MULTILINE
)

tool = language_tool_python.LanguageTool('en-US')

CORRECT_UNICODE = "\u2713"
WRONG_UNICODE = "\u2715"
WARNING_UNICODE = "\u26A0"

CONNECTOR_CATEGORY = ['Analytics and SIEM', 'Authentication', 'Case Management', 'Threat Intelligence', 'Database',
                      'Deception', 'Email Gateway', 'Endpoint Security', 'Identity and Access Management',
                      'Authentication', 'Insider Threat', 'IT Services', 'Network Security', 'Utilities',
                      'Vulnerability and Risk Management', 'OT & IoT Security', 'Communication and Coordination',
                      'Compliance and Reporting', 'FortiSOAR Essentials', 'Monitoring',
                      'Firewall and Network Protection', 'Threat Hunting and Search', 'Web Application',
                      'Task Management', 'Enterprise mobility management', 'Digital assistant', 'Automation controller',
                      'Logging', 'Query Service', 'Threat Detection', 'Breach and Attack Simulation (BAS)',
                      'ML Service', 'Message Queueing Service', 'Security Posture Management', 'Compute Platform',
                      'Storage', 'Asset Management', 'Container Services', 'IT Service Management',
                      'Attack surface management', 'Malware Analysis', 'Cloud access security broker (CASB)',
                      'Cloud Security', 'Email Server', 'Email Security',
                      'DevOps and Digital Operations and Digital Operations', 'Ticket Management', 'Other']
OPERATION_CATEGORY = ["investigation", "containment", "remediation", "miscellaneous"]
PARAMETER_CATEGORY = ["text", "textarea", "integer", "datetime", "select", "multiselect", "checkbox", "password",
                      "json", "apiOperation", "email"]


def get_info_file_path():
    info_file_path = None
    for dirname, dirnames, filenames in os.walk('.'):
        if dirname in [".git", ".github"]:
            continue
        if "info.json" in filenames:
            info_file_path = dirname + "/info.json"
            break
    return info_file_path, dirname


def read_info(info_file_path: str) -> dict:
    file = open(info_file_path, "r")
    info = json.load(file)
    file.close()
    return info


class TestConnectorInfoSanity:
    def __init__(self, *args, **kwargs):
        self.info_file_path, self.dirname = get_info_file_path()
        self.connector_info = read_info(self.info_file_path)
        self.report = ""
        self.error = ""
        self.warning = ""
        self.failed_test_count = 0
        self.passed_test_count = 0
        self.warning_test_count = 0
        if self.connector_info:
            self.init_test()
        else:
            self.report += "Info.json not found.\n"

    def append_correct(self, message: str):
        self.passed_test_count += 1
        self.report += f"\033[32m{CORRECT_UNICODE} {message}\033[0m\n"

    def append_wrong(self, message: str):
        self.failed_test_count += 1
        self.report += f"\033[31m{WRONG_UNICODE} {message}\033[0m\n"
        self.error += f"\033[31m{WRONG_UNICODE} {message}\033[0m\n"

    def append_warning(self, message: str):
        self.warning_test_count += 1
        self.report += f"\033[33m{WARNING_UNICODE} {message}\033[0m\n"
        self.warning += f"\033[33m{WARNING_UNICODE} {message}\033[0m\n"

    def init_test(self):
        self.verify_copyright_block()
        self.verify_connector_name()
        self.verify_connector_label()
        self.verify_connector_version()
        self.verify_connector_publisher()
        self.verify_connector_category()
        self.verify_connector_logo()
        self.verify_connector_descriptions()
        self.verify_connector_docs_link()
        self.verify_configurations()

        for op in self.connector_info.get("operations", []):
            self.verify_operation(op)

    def verify_copyright_block(self):
        for dirname, dirnames, filenames in os.walk('.'):
            files_to_skip = ['./.github/workflows/sanity_checks_utcs.py', './.github/workflows/generate_utcs.py']
            for filename in filenames:
                if filename.endswith('.py'):  # Only target Python files
                    file_path = os.path.join(dirname, filename)
                    if file_path in files_to_skip:
                        continue
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        if copyright_pattern.search(content):
                            self.append_correct(f'Correct copyright block found in {file_path}.')
                        else:
                            self.append_wrong(f'Missing or incorrect copyright block in {file_path}!')

    def verify_connector_name(self):
        conn_name = self.connector_info.get("name")
        folder_name = self.dirname.split("/")[-1]
        if conn_name and conn_name == folder_name:
            self.append_correct("Connector name is valid.")
        else:
            self.append_wrong("Connector name is invalid.")

    def verify_connector_label(self):
        conn_label = self.connector_info.get("label")
        if conn_label:
            self.append_correct("Connector label is available.")
        else:
            self.append_wrong("Connector label is missing.")

    def verify_connector_version(self):
        conn_version = self.connector_info.get("version")
        valid_version_regex_pattern = re.compile("^[1-9]\\d*\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)$")
        if conn_version and re.fullmatch(valid_version_regex_pattern, conn_version):
            self.append_correct("Connector version is available and valid.")
        elif conn_version:
            self.append_wrong(f"Connector version is available, but invalid. Connector version: '{conn_version}'")
        else:
            self.append_wrong("Connector version is missing.")

    def verify_connector_publisher(self):
        conn_certified = self.connector_info.get("cs_approved")
        conn_publisher = self.connector_info.get("publisher", "")
        if conn_publisher:
            self.append_correct("Connector publisher is available.")
            if conn_certified and conn_publisher.strip() != "Fortinet":
                self.append_warning(f"Connector is certified, But connector publisher is: '{conn_publisher}'")
        else:
            self.append_wrong("Connector publisher is missing.")

    def verify_connector_descriptions(self):
        conn_desc = self.connector_info.get("description")
        if conn_desc:
            self.append_correct("Connector description is available.")
            if len(conn_desc) < len(self.connector_info.get("label")) * 3:
                self.append_warning("Connector description is too short.")
        else:
            self.append_wrong("Connector description is missing.")

    def verify_connector_category(self):
        category = self.connector_info.get("category")
        if isinstance(category, str) and category in CONNECTOR_CATEGORY:
            self.append_correct("Connector category is valid.")
        elif isinstance(category, list) and all(item in CONNECTOR_CATEGORY for item in category):
            self.append_correct("Connector category is valid.")
        else:
            self.append_wrong(f"Connector category is invalid. Category value: '{category}'")

    def verify_connector_logo(self):
        small_logo = self.connector_info.get("icon_small_name")
        large_logo = self.connector_info.get("icon_large_name")
        if small_logo and large_logo:
            self.append_correct("Connector logo is available.")
        else:
            self.append_wrong(
                f"Connector logo is invalid. Small logo value: '{small_logo}'; Large logo value: '{large_logo}'")

    def verify_connector_docs_link(self):
        doc_link = self.connector_info.get("help_online", "").strip()

        if doc_link and (doc_link.startswith("https://docs.fortinet.com/document/fortisoar") or
                         doc_link.startswith("https://github.com/fortinet-fortisoar")):
            self.append_correct("Connector doc link is available and valid.")
        elif doc_link:
            self.append_wrong(f"Connector doc link is available, but it is invalid. Connector Doc Link: '{doc_link}'")
        else:
            self.append_warning("Connector doc link is missing.")

    def verify_configurations(self):
        fields = self.connector_info.get("configuration", {}).get("fields", [])
        for field in fields:
            self.verify_parameter("Configurations", field)

    def verify_operation(self, operation):
        self.verify_operation_name(operation)
        self.verify_operation_title(operation)
        self.verify_operation_category(operation)
        self.verify_operation_descriptions(operation)
        self.verify_operation_output_schema(operation)

        for param in operation.get("parameters", []):
            self.verify_parameter(operation.get("title"), param)

    def verify_operation_name(self, operation):
        op_name = operation.get("operation")
        if op_name:
            self.append_correct(f"Operation '{op_name}' is available.")
        else:
            self.append_wrong("Operation name is missing.")

    def verify_operation_title(self, operation):
        op_title = operation.get("title")
        if op_title:
            self.append_correct(f"Operation: '{operation.get('operation')}'; Operation title is available.")
        else:
            self.append_wrong(f"Operation: '{operation.get('operation')}'; Operation title is missing.")

    def verify_operation_category(self, operation):
        op_category = operation.get("category")
        if op_category and op_category in OPERATION_CATEGORY:
            self.append_correct(f"Operation: '{operation.get('operation')}'-> Operation category is valid.")
        elif op_category:
            self.append_wrong(f"Operation: '{operation.get('operation')}'-> Operation category is available but invalid."
                              f"Operation Category: '{op_category}'")
        else:
            self.append_wrong(f"Operation: '{operation.get('operation')}' -> Operation category is missing.")

    def verify_operation_descriptions(self, operation):
        op_desc = operation.get("description")
        if op_desc:
            self.append_correct(f"Operation: '{operation.get('operation')}' -> Operation description is available.")
            if len(op_desc) < len(operation.get('operation')) * 3:
                self.append_warning(f"Operation: '{operation.get('operation')}' -> Operation description is too short.")
            errors = tool.check(op_desc)
            if errors:
                corrected_desc = tool.correct(op_desc)
                self.append_warning(f"Operation: '{operation.get('operation')}' -> Original Description: '{op_desc}' -> Corrected Description: '{corrected_desc}'")
        else:
            self.append_wrong(f"Operation: '{operation.get('operation')}' -> Operation description is missing.")

    def verify_operation_output_schema(self, operation):
        if "conditional_output_schema" in operation:
            op_output_schema = operation.get("conditional_output_schema")
        elif "api_output_schema" in operation:
            op_output_schema = operation.get("api_output_schema")
        else:
            op_output_schema = operation.get("output_schema")
        if op_output_schema:
            self.append_correct(
                f"Operation: '{operation.get('operation')}' -> Operation output schema is available.")
        else:
            self.append_wrong(
                f"Operation: '{operation.get('operation')}' -> Operation output schema is missing.")

    def verify_parameter(self, op_name, params):
        self.verify_parameter_name(op_name, params)
        self.verify_parameter_title(op_name, params)
        self.verify_parameter_type(op_name, params)
        self.verify_parameter_descriptions(op_name, params)
        self.verify_nested_parameter(op_name, params)

    def verify_nested_parameter(self, op_name, params):
        p_name = params.get("name")
        if params.get('onchange'):
            if params.get('type') == 'checkbox':
                if all(item in ['true', 'false'] for item in params.get("onchange").keys()):
                    self.append_correct(f"Operation: '{op_name}' -> Params: '{p_name}' -> Nested Params are available.")
                else:
                    self.append_wrong(f"Operation: '{op_name}' -> Params: '{p_name}' -> Nested Params are invalid.")
            if params.get('options'):
                if all(item in params.get("options") for item in params.get("onchange").keys()):
                    self.append_correct(f"Operation: '{op_name}' -> Params: '{p_name}' -> Nested Params are available.")
                else:
                    self.append_wrong(f"Operation: '{op_name}' -> Params: '{p_name}' -> Nested Params are invalid.")
            for onchange_params in params.get("onchange").values():
                for param in onchange_params:
                    self.verify_parameter(op_name, param)

    def verify_parameter_name(self, op_name, params):
        p_name = params.get("name")
        if p_name:
            self.append_correct(f"Operation: '{op_name}' -> Params: '{p_name}' is available.")
        else:
            self.append_wrong(f"Operation: '{op_name}' -> Params: '{p_name}' is missing.")

    def verify_parameter_title(self, op_name, params):
        p_title = params.get("title")
        p_name = params.get("name")
        if p_title:
            self.append_correct(f"Operation: '{op_name}' -> Params: '{p_name}' -> Params title is available.")
        else:
            self.append_wrong(f"Operation: '{op_name}' -> Params: '{p_name}' -> Params title is missing.")

    def verify_parameter_type(self, op_name, params):
        p_type = params.get("type")
        p_name = params.get("name")
        if p_type and p_type in PARAMETER_CATEGORY:
            self.append_correct(f"Operation: '{op_name}' -> Params: '{p_name}' -> Params type is available.")
        else:
            self.append_wrong(f"Operation: '{op_name}' -> Params: '{p_name}' -> Params type is missing.")

    def verify_parameter_descriptions(self, op_name, params):
        p_desc = params.get("description")
        p_name = params.get("name")
        if p_desc:
            self.append_correct(f"Operation: '{op_name}' -> Params: '{p_name}' -> Params description is available.")
            if len(p_desc) < len(p_name) * 3:
                self.append_warning(f"Operation: '{op_name}' -> Params: '{p_name}' -> Params descriptions is short.")
            errors = tool.check(p_desc)
            if errors:
                corrected_desc = tool.correct(p_desc)
                self.append_warning(f"Operation: '{op_name}' -> Params: '{p_name}' -> Original Description: '{p_desc}' -> Corrected Description: '{corrected_desc}'")
        else:
            self.append_wrong(f"Operation: '{op_name}' -> Params: '{p_name}' -> Params descriptions is missing.")


def main():
    test_conn = TestConnectorInfoSanity()
    print("----------------Report Start--------------\n")
    print(test_conn.report)
    sys.stdout.flush()
    print("----------------Report End----------------\n")
    sys.stdout.flush()

    total_checks = test_conn.passed_test_count + test_conn.failed_test_count + test_conn.warning_test_count
    if test_conn.error:
        if test_conn.warning:
            error_msg = f"\033[31mAll the checks didn't pass. '{test_conn.failed_test_count}' checks failed, " \
                        f"'{test_conn.warning_test_count}' checks had warnings out of '{total_checks}' checks.\n" \
                        + test_conn.warning + test_conn.error
        else:
            error_msg = f"\033[31mAll the checks didn't pass. '{test_conn.failed_test_count}' checks failed out of " \
                        f"'{total_checks}' checks.\n" + test_conn.error
        print(error_msg)
        sys.exit(1)

    if test_conn.warning:
        warning_msg = f"\033[33m'{test_conn.warning_test_count}' checks had warnings out of '{total_checks}' checks.\n" \
                      + test_conn.warning
        print(warning_msg)


if __name__ == '__main__':
    main()

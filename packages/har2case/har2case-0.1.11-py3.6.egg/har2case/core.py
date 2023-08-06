import base64
import io
import json
import logging
import sys
from collections import OrderedDict

import yaml
from har2case import utils
from har2case.compat import bytes, ensure_ascii, urlparse


class HarParser(object):

    IGNORE_REQUEST_HEADERS = [
        "host",
        "accept",
        "content-length",
        "connection",
        "accept-encoding",
        "accept-language",
        "origin",
        "referer",
        "cache-control",
        "pragma",
        "cookie",
        "upgrade-insecure-requests",
        ":authority",
        ":method",
        ":scheme",
        ":path"
    ]

    def __init__(self, file_path, filter_str=None, exclude_str=None):
        self.log_entries = utils.load_har_log_entries(file_path)
        self.user_agent = None
        self.filter_str = filter_str
        self.exclude_str = exclude_str or ""
        self.ordered_dict = True

    def init_dict(self):
        return OrderedDict() if self.ordered_dict else {}

    def _make_request_url(self, testcase_dict, entry_json):
        """ parse HAR entry request url and queryString, and make testcase url and params
        @param (dict) entry_json
            {
                "request": {
                    "url": "https://httprunner.top/home?v=1&w=2",
                    "queryString": [
                        {"name": "v", "value": "1"},
                        {"name": "w", "value": "2"}
                    ],
                },
                "response": {}
            }
        @output testcase_dict:
            {
                "name: "/home",
                "request": {
                    url: "https://httprunner.top/home",
                    params: {"v": "1", "w": "2"}
                }
            }
        """
        request_params = utils.convert_list_to_dict(
            entry_json["request"].get("queryString", [])
        )

        url = entry_json["request"].get("url")
        if not url:
            logging.exception("url missed in request.")
            sys.exit(1)

        parsed_object = urlparse.urlparse(url)
        if request_params:
            parsed_object = parsed_object._replace(query='')
            testcase_dict["request"]["url"] = parsed_object.geturl()
            testcase_dict["request"]["params"] = request_params
        else:
            testcase_dict["request"]["url"] = url

        testcase_dict["name"] = parsed_object.path

    def _make_request_method(self, testcase_dict, entry_json):
        """ parse HAR entry request method, and make testcase method.
        """
        method = entry_json["request"].get("method")
        if not method:
            logging.exception("method missed in request.")
            sys.exit(1)

        testcase_dict["request"]["method"] = method

    def _make_request_headers(self, testcase_dict, entry_json):
        """ parse HAR entry request headers, and make testcase headers.
            header in IGNORE_REQUEST_HEADERS will be ignored.
        @param (dict) entry_json
            {
                "request": {
                    "headers": [
                        {"name": "Host", "value": "httprunner.top"},
                        {"name": "Content-Type", "value": "application/json"},
                        {"name": "User-Agent", "value": "iOS/10.3"}
                    ],
                },
                "response": {}
            }
        @output testcase_dict:
            {
                "request": {
                    headers: {"Content-Type": "application/json"}
                }
            }
        """
        testcase_headers = {}
        for header in entry_json["request"].get("headers", []):
            if header["name"].lower() in self.IGNORE_REQUEST_HEADERS:
                continue
            if header["name"].lower() == "user-agent":
                if not self.user_agent:
                    self.user_agent = header["value"]
                continue

            testcase_headers[header["name"]] = header["value"]

        if testcase_headers:
            testcase_dict["request"]["headers"] = testcase_headers

    def _make_request_data(self, testcase_dict, entry_json):
        """ parse HAR entry request data, and make testcase request data
        @param (dict) entry_json
            {
                "request": {
                    "method": "POST",
                    "postData": {
                        "mimeType": "application/x-www-form-urlencoded; charset=utf-8",
                        "params": [
                            {"name": "a", "value": 1},
                            {"name": "b", "value": "2"}
                        }
                    },
                },
                "response": {...}
            }
        @output testcase_dict:
            {
                "request": {
                    "method": "POST",
                    "data": {"v": "1", "w": "2"}
                }
            }
        """
        method = entry_json["request"].get("method")
        if method in ["POST", "PUT", "PATCH"]:
            postData = entry_json["request"].get("postData", {})
            mimeType = postData.get("mimeType")

            # Note that text and params fields are mutually exclusive.
            if "text" in postData:
                post_data = postData.get("text")
            else:
                params = postData.get("params", [])
                post_data = utils.convert_list_to_dict(params)

            request_data_key = "data"
            if not mimeType:
                pass
            elif mimeType.startswith("application/json"):
                try:
                    post_data = json.loads(post_data)
                    request_data_key = "json"
                except utils.JSONDecodeError:
                    pass
            elif mimeType.startswith("application/x-www-form-urlencoded"):
                # post_data = utils.x_www_form_urlencoded(post_data)
                pass
            else:
                #TODO: make compatible with more mimeType
                pass

            testcase_dict["request"][request_data_key] = post_data

    def _make_validate(self, testcase_dict, entry_json):
        """ parse HAR entry response and make testcase validate.
        @param (dict) entry_json
            {
                "request": {},
                "response": {
                    "status": 200,
                    "headers": [
                        {
                            "name": "Content-Type",
                            "value": "application/json; charset=utf-8"
                        },
                    ],
                    "content": {
                        "size": 71,
                        "mimeType": "application/json; charset=utf-8",
                        "text": "eyJJc1N1Y2Nlc3MiOnRydWUsIkNvZGUiOjIwMCwiTWVzc2FnZSI6bnVsbCwiVmFsdWUiOnsiQmxuUmVzdWx0Ijp0cnVlfX0=",
                        "encoding": "base64"
                    }
                }
            }
        @output testcase_dict:
            {
                "validate": [
                    {"eq": ["status_code", 200]}
                ]
            }
        """
        testcase_dict["validate"].append(
            {"eq": ["status_code", entry_json["response"].get("status")]}
        )

        resp_content_dict = entry_json["response"].get("content")

        headers_mapping = utils.convert_list_to_dict(
            entry_json["response"].get("headers", [])
        )
        if "Content-Type" in headers_mapping:
            testcase_dict["validate"].append(
                {"eq": ["headers.Content-Type", headers_mapping["Content-Type"]]}
            )

        text = resp_content_dict.get("text")
        if not text:
            return

        mime_type = resp_content_dict.get("mimeType")
        if mime_type and mime_type.startswith("application/json"):

            encoding = resp_content_dict.get("encoding")
            if encoding and encoding == "base64":
                content = base64.b64decode(text).decode('utf-8')
                try:
                    resp_content_json = json.loads(content)
                except utils.JSONDecodeError:
                    logging.warning("response content can not be loaded as json.")
                    return
            else:
                resp_content_json = json.loads(text)

            if not isinstance(resp_content_json, dict):
                return

            for key, value in resp_content_json.items():
                if isinstance(value, (dict, list)):
                    continue

                testcase_dict["validate"].append(
                    {"eq": ["content.{}".format(key), value]}
                )

    def make_testcase(self, entry_json):
        """ extract info from entry dict and make testcase
        @param (dict) entry_json
            {
                "request": {
                    "method": "POST",
                    "url": "https://httprunner.top/api/v1/Account/Login",
                    "headers": [],
                    "queryString": [],
                    "postData": {},
                },
                "response": {
                    "status": 200,
                    "headers": [],
                    "content": {}
                }
            }
        """
        testcase_dict = self.init_dict()
        testcase_dict["name"] = ""
        testcase_dict["request"] = self.init_dict()
        testcase_dict["validate"] = []

        self._make_request_url(testcase_dict, entry_json)
        self._make_request_method(testcase_dict, entry_json)
        self._make_request_headers(testcase_dict, entry_json)
        self._make_request_data(testcase_dict, entry_json)
        self._make_validate(testcase_dict, entry_json)

        return testcase_dict

    def make_testcases(self):
        """ extract info from HAR log entries list and make testcase list
        """
        def is_exclude(url, exclude_str):
            exclude_str_list = exclude_str.split("|")
            for exclude_str in exclude_str_list:
                if exclude_str and exclude_str in url:
                    return True

            return False

        testcases = []
        for entry_json in self.log_entries:
            url = entry_json["request"].get("url")
            if self.filter_str and self.filter_str not in url:
                continue

            if is_exclude(url, self.exclude_str):
                continue

            testcases.append(
                {"test": self.make_testcase(entry_json)}
            )

        return testcases

    def make_config(self):
        """ sets config block of testset
        """
        config_dict = self.init_dict()
        config_dict["name"] = "testset description"
        config_dict["variables"] = []

        config_dict["request"] = self.init_dict()
        config_dict["request"]["base_url"] = ""
        config_dict["request"]["headers"] = {
            "User-Agent": self.user_agent
        }

        return {"config": config_dict}

    def make_testset(self, ordered_dict=True):
        """ Extract info from HAR file and prepare for testcase
        """
        self.ordered_dict = ordered_dict
        logging.debug("Extract info from HAR file and prepare for testcase.")
        testset = self.make_testcases()
        config = self.make_config()
        testset.insert(0, config)
        return testset

    def gen_yaml(self, yaml_file):
        """ dump HAR entries to yaml testset
        """
        self.testset = self.make_testset(False)
        logging.debug("Start to generate YAML testset.")

        with io.open(yaml_file, 'w', encoding="utf-8") as outfile:
            yaml.dump(self.testset, outfile, allow_unicode=True, default_flow_style=False, indent=4)

        logging.info("Generate YAML testset successfully: {}".format(yaml_file))

    def gen_json(self, json_file):
        """ dump HAR entries to json testset
        """
        self.testset = self.make_testset(True)
        logging.debug("Start to generate JSON testset.")

        with io.open(json_file, 'w', encoding="utf-8") as outfile:
            my_json_str = json.dumps(self.testset, ensure_ascii=ensure_ascii, indent=4)
            if isinstance(my_json_str, bytes):
                my_json_str = my_json_str.decode("utf-8")

            outfile.write(my_json_str)

        logging.info("Generate JSON testset successfully: {}".format(json_file))

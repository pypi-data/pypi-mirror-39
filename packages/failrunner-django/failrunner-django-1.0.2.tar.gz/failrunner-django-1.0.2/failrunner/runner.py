import re
import subprocess

import requests


class TestRunner:

    log_url = 'https://api.travis-ci.{urlsuffix}/v3/job/{job}/log.txt'
    line_regex = r'^(ERROR|FAIL): (.*?) \((.*?)\)'

    def __init__(self, manage_path: str, pipenv: bool,
                 fail_only: bool, error_only: bool, dry: bool):
        self.pipenv = pipenv
        self.manage_path = manage_path
        self.failed_only = fail_only
        self.errored_only = error_only
        self.dry = dry

        self.errored: list = []
        self.failed: list = []

    def get_tests(self, job_num: int, url_suffix: str) -> bool:
        rawlog_url = self.log_url.format(
            job=job_num,
            urlsuffix=url_suffix
        )

        line_regex = re.compile(self.line_regex)

        response = requests.get(rawlog_url)
        if response.status_code == 200:
            lines = response.text.split('\n')
            for line in lines:
                match = line_regex.match(line)
                if match:
                    fail_type = match.group(1)
                    test_function = match.group(2)
                    test_class = match.group(3)
                    full_test = test_class + '.' + test_function
                    if fail_type == 'ERROR':
                        self.errored.append(full_test)
                    else:
                        self.failed.append(full_test)
            return True

        print('Request for {} failed :('.format(rawlog_url))
        return False

    def run_tests(self) -> None:
        tests = self.tests_to_run
        command = ['python', 'manage.py', 'test'] + tests
        if self.pipenv:
            command = ['pipenv', 'run'] + command

        if self.dry:
            print(command)
        else:
            subprocess.run(command, cwd=self.manage_path)

    @property
    def tests_to_run(self) -> list:
        if self.failed_only:
            return self.failed

        if self.errored_only:
            return self.errored

        return self.failed + self.errored

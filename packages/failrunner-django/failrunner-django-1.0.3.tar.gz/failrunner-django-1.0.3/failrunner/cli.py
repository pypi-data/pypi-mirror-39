import argparse
import os
from sys import argv

from failrunner.runner import TestRunner


def main() -> None:
    default_args_env = 'FAILRUNNER_DEFAULT_ARGS'
    parser = argparse.ArgumentParser('Run failed travis tests')
    parser.add_argument('-j', '--job', metavar='J', type=int, nargs=1, help='Travis job number')
    parser.add_argument('-p', '--path', metavar='C', type=str, nargs='?',
                        help='Path to manage.py', default=os.getcwd())
    parser.add_argument('-e', '--pipenv', action='store_true', help='Run manage.py through pipenv')
    parser.add_argument('--fail-only', action='store_true', help='Run only failed tests')
    parser.add_argument('--error-only', action='store_true', help='Run only errored tests')
    parser.add_argument('--dry', action='store_true', help='Print command to be run, but don\'t run it')
    parser.add_argument('--org', action='store_true', help='Use travis-ci.org instead of travis-ci.com')

    args_list = argv[1:]
    if default_args_env in os.environ:
        args_list += os.environ.get(default_args_env, '').split(' ')
    args = parser.parse_args(args_list)

    runner = TestRunner(
        args.path,
        args.pipenv,
        args.fail_only,
        args.error_only,
        args.dry
    )

    urltype = 'com'
    if args.org:
        urltype = 'org'

    loaded = runner.get_tests(args.job[0], urltype)
    if not loaded:
        exit(1)

    runner.run_tests()


if __name__ == '__main__':
    main()

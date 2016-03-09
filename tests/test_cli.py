# coding=utf-8

import unittest

import mock
import six

import devpi_cleaner.cli


def _run(*args):
    with mock.patch('sys.stdout', new_callable=six.StringIO) as stdout:
        try:
            devpi_cleaner.cli.main(args)
        except SystemExit as error:
            if error.code != 0:
                raise
        return stdout.getvalue()


class CLITests(unittest.TestCase):
    def test_usage(self):
        output = _run('--help')
        self.assertIn('usage', output)

if __name__ == '__main__':
    unittest.main()

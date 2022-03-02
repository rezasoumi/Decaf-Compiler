from unittest import TestCase
from os import listdir
from os.path import abspath

from compiler.main import run


def read_file(file_address: str):
    handler = open(file_address, "r")
    content = handler.read()
    handler.close()
    return content


def is_local():
    return "roozbeh" in abspath(".")


def prefix():
    return "./test/" if is_local() else "./test/"


def assert_string_equals(self, expected: str, actual: str):

    #self.assertEqual(expected, actual)
    input1_lines = []
    input2_lines = []
    for line in expected.splitlines():
        l = line.strip()
        if l != "":
            input1_lines.append(l)

    for line in actual.splitlines():
        l = line.strip()
        if l != "":
            input2_lines.append(l)

  #  self.assertEqual(len(input1_lines), len(input2_lines))
    self.assertEqual(input1_lines, input2_lines)


class TtSequenceMeta(type):
    def __new__(cls, name, bases, dct):

        def gen_test(inp_file, expected_file, test_folder):
            def test(self):
                actual = run(test_folder + inp_file)
                expected = read_file(test_folder + expected_file)
                assert_string_equals(self, expected, actual)
            return test

        test_folder = prefix() + "in-out/"
        folder_content = sorted(listdir(test_folder))
        tests_count = len(folder_content) // 2
        for i in range(tests_count):
            inp_file = folder_content[2*i]
            expected_file = folder_content[2*i+1]

            method_name = f"test_{inp_file[:-3]}"
            dct[method_name] = gen_test(inp_file, expected_file, test_folder)

        ret = type.__new__(cls, name, bases, dct)
        return ret


class TestSequence(TestCase, metaclass=TtSequenceMeta):
    pass

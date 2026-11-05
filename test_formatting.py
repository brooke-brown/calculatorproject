"""Check that calculator.py meets the assignment's formatting rules.

Run with: python3 -m unittest test_formatting -v
"""

import ast
import re
import tokenize
import unittest
from pathlib import Path

CALCULATOR_PATH = Path(__file__).with_name("calculator.py")
REQUIRED_FUNCTIONS = ("add", "subtract", "multiply", "divide")
# The assignment sets these parameter names, so they are exempt from the
# descriptive name check.
REQUIRED_PARAMETERS = ("a", "b")
INDENT_WIDTH = 4
MAX_LINE_LENGTH = 79
BLANK_LINES_BEFORE_FUNCTION = 2
SNAKE_CASE = re.compile(r"^[a-z_][a-z0-9_]*$")


class FormattingTestCase(unittest.TestCase):
    """Load calculator.py once for all of the formatting tests."""

    @classmethod
    def setUpClass(cls):
        cls.source = CALCULATOR_PATH.read_text(encoding="utf-8")
        cls.lines = cls.source.splitlines()
        cls.tree = ast.parse(cls.source)
        cls.functions = [
            node for node in cls.tree.body
            if isinstance(node, ast.FunctionDef)
        ]

    def get_function(self, name):
        """Return the named function's AST node, or fail the test."""
        for function in self.functions:
            if function.name == name:
                return function
        self.fail(f"{name}() is not defined in calculator.py")


class TestIndentation(FormattingTestCase):
    """Indentation must be consistent and use 4 spaces."""

    def test_each_indent_level_is_four_spaces(self):
        levels = [0]
        with tokenize.open(CALCULATOR_PATH) as source_file:
            for token in tokenize.generate_tokens(source_file.readline):
                if token.type == tokenize.INDENT:
                    width = len(token.string)
                    self.assertEqual(
                        width - levels[-1],
                        INDENT_WIDTH,
                        f"line {token.start[0]}: indent is not 4 spaces",
                    )
                    levels.append(width)
                elif token.type == tokenize.DEDENT:
                    levels.pop()

    def test_no_tabs(self):
        for number, line in enumerate(self.lines, start=1):
            with self.subTest(line=number):
                self.assertNotIn("\t", line)


class TestDocstrings(FormattingTestCase):
    """Each required function must have a short docstring."""

    def test_each_function_has_a_docstring(self):
        for name in REQUIRED_FUNCTIONS:
            with self.subTest(function=name):
                docstring = ast.get_docstring(self.get_function(name))
                self.assertTrue(docstring, f"{name}() has no docstring")


class TestNames(FormattingTestCase):
    """Names must be descriptive and follow PEP 8."""

    def test_function_names_are_snake_case(self):
        for function in self.functions:
            with self.subTest(function=function.name):
                self.assertRegex(function.name, SNAKE_CASE)

    def test_local_variable_names_are_descriptive(self):
        for function in self.functions:
            for node in ast.walk(function):
                if not (
                    isinstance(node, ast.Name)
                    and isinstance(node.ctx, ast.Store)
                ):
                    continue
                if node.id in REQUIRED_PARAMETERS:
                    continue
                with self.subTest(function=function.name, variable=node.id):
                    self.assertGreater(len(node.id), 1, "name is too short")
                    self.assertRegex(node.id, SNAKE_CASE)


class TestPep8Layout(FormattingTestCase):
    """The file must follow basic PEP 8 layout rules."""

    def test_lines_are_at_most_79_characters(self):
        for number, line in enumerate(self.lines, start=1):
            with self.subTest(line=number):
                self.assertLessEqual(len(line), MAX_LINE_LENGTH)

    def test_no_trailing_whitespace(self):
        for number, line in enumerate(self.lines, start=1):
            with self.subTest(line=number):
                self.assertEqual(line, line.rstrip())

    def test_file_ends_with_one_newline(self):
        self.assertTrue(self.source.endswith("\n"), "no newline at end")
        self.assertFalse(self.source.endswith("\n\n"), "extra blank line")

    def test_two_blank_lines_before_each_function(self):
        for function in self.functions:
            if function is self.tree.body[0]:
                continue
            with self.subTest(function=function.name):
                index = function.lineno - 2
                while self.lines[index].startswith("#"):
                    index -= 1
                blank_lines = 0
                while index >= 0 and not self.lines[index].strip():
                    blank_lines += 1
                    index -= 1
                self.assertEqual(blank_lines, BLANK_LINES_BEFORE_FUNCTION)


if __name__ == "__main__":
    unittest.main()

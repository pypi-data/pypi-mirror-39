# -*- coding: utf-8 -*-
"""
Parses Polarion docstring.
"""

from __future__ import absolute_import, unicode_literals

import ast
from collections import namedtuple

FORMATED_KEYS = ("setup", "teardown")

DocstringsRecord = namedtuple("DocstringsRecord", "lineno column value")


def get_section_start(doc_list, section):
    """Finds the line with "section" (e.g. "Polarion", "testSteps", etc.)."""
    section = "{}:".format(section)
    for index, line in enumerate(doc_list):
        if section != line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        return index + 1, indent
    return None, None


# pylint: disable=too-few-public-methods,invalid-name
class DOCSTRING_SECTIONS(object):  # noqa
    """Valid sections in Polarion docstring."""

    polarion = "Polarion"
    steps = "testSteps"
    results = "expectedResults"


class DocstringParser(object):
    """Parser for single docstring."""

    SECTIONS = DOCSTRING_SECTIONS

    def __init__(self, docstring):
        self.docstring = docstring

    @staticmethod
    def _get_key_value(line):
        """Gets the key and value out of docstring line."""
        data = line.split(":")
        if len(data) == 1:
            data.append("")

        key = data[0].strip()

        value = ":".join(data[1:]).strip()
        if value == "None":
            value = None

        return key, value

    # pylint: disable=too-many-locals
    def lines_to_dict(self, lines, start=0, lineno_offset=0, stop=None):
        """Creates dictionary out of docstring lines.

        Includes column and line number info for each record.
        """
        if stop:
            lines = lines[start:stop]
        else:
            lines = lines[start:]

        lines_dict = {}
        indent = len(lines[0]) - len(lines[0].lstrip(" "))
        prev_key = None
        for num, line in enumerate(lines, 1):
            line_stripped = line.strip()
            if not line_stripped:
                break

            curr_indent = len(line) - len(line.lstrip(" "))

            if curr_indent < indent:
                break

            # check if the line should be appended to previous key
            first_word = line_stripped.split(" ")[0] or line_stripped
            if prev_key and curr_indent > indent and first_word[-1] != ":":
                sep = "\n" if prev_key in FORMATED_KEYS else " "
                prev_lineno, prev_indent, prev_value = lines_dict[prev_key]
                lines_dict[prev_key] = DocstringsRecord(
                    prev_lineno, prev_indent, "{}{}{}".format(prev_value, sep, line_stripped)
                )
                continue
            else:
                prev_key = None

            if curr_indent > indent:
                continue

            key, value = self._get_key_value(line)
            lines_dict[key] = DocstringsRecord(num + lineno_offset, indent, value)
            prev_key = key

        return lines_dict

    @staticmethod
    def lines_to_list(lines, start=0, lineno_offset=0, stop=None):
        """Creates list out of docstring lines.

        Includes column and line number info for each line.
        """
        if stop:
            lines = lines[start:stop]
        else:
            lines = lines[start:]

        lines_list = []
        indent = len(lines[0]) - len(lines[0].lstrip(" "))
        for num, line in enumerate(lines, 1):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            curr_indent = len(line) - len(line.lstrip(" "))
            if curr_indent < indent:
                break

            # check if the line should be appended to previous key
            first_word = line_stripped.split(" ")[0] or line_stripped
            if curr_indent > indent and first_word[-1] != ":":
                prev_lineno, prev_indent, prev_value = lines_list.pop()
                lines_list.append(
                    DocstringsRecord(
                        prev_lineno, prev_indent, "{} {}".format(prev_value, line_stripped)
                    )
                )
                continue

            if curr_indent > indent:
                continue
            lines_list.append(DocstringsRecord(num + lineno_offset, indent, line_stripped))

        return lines_list

    def strip_polarion_data(self):
        """Removes the Polarion section from the docstring."""
        docstring_list = self.docstring.split("\n")
        new_docstring_list = []
        indent = 0
        polarion_section = "{}:".format(self.SECTIONS.polarion)
        for line in docstring_list:
            if line.strip() == polarion_section:
                indent = len(line) - len(line.lstrip(" "))
                continue
            if indent:
                curr_indent = len(line) - len(line.lstrip(" "))
                if curr_indent > indent:
                    continue
            new_docstring_list.append(line)
        new_docstring = "\n".join(new_docstring_list).replace("\n\n", "\n")
        return new_docstring.strip()

    def parse(self):
        """Parses docstring to dictionary. E.g.:

        Polarion:
            assignee: mkourim
            casecomponent: nonexistent
            testSteps:
                1. Step with really long description
                   that doesn't fit into one line
                2. Do that
            expectedResults:
                1. Success outcome with really long description
                   that doesn't fit into one line
                2. 2
            caseimportance: low
            title: Some test with really long description
                   that doesn't fit into one line
            setup: Do this:
                   - first thing
                   - second thing

        This is not included.
        """
        doc_list = self.docstring.split("\n")

        polarion_start, __ = get_section_start(doc_list, self.SECTIONS.polarion)
        if not polarion_start:
            return None

        docstring_dict = self.lines_to_dict(doc_list, start=polarion_start)
        if self.SECTIONS.steps in docstring_dict and docstring_dict[self.SECTIONS.steps][2]:
            steps_start, __ = get_section_start(doc_list, self.SECTIONS.steps)
            steps_list = self.lines_to_list(
                doc_list, start=steps_start, lineno_offset=steps_start - polarion_start
            )
            docstring_dict[self.SECTIONS.steps] = steps_list
        if self.SECTIONS.results in docstring_dict and docstring_dict[self.SECTIONS.results][2]:
            results_start, __ = get_section_start(doc_list, self.SECTIONS.results)
            results_list = self.lines_to_list(
                doc_list, start=results_start, lineno_offset=results_start - polarion_start
            )
            docstring_dict[self.SECTIONS.results] = results_list

        return docstring_dict


class FileParser(object):
    """Parser for whole file."""

    SECTIONS = DOCSTRING_SECTIONS

    def __init__(self, filename, tree=None, tests_only=True):
        self.filename = filename
        self.tests_only = tests_only
        self.tree = tree or self.get_tree()

    def get_tree(self):
        """Returns ast tree."""
        with open(self.filename) as infile:
            source = infile.read()

        tree = ast.parse(source, filename=self.filename)
        return tree

    @staticmethod
    def get_docstring_from_func(func_node):
        """Gets docstring from function definition."""
        docstring = None
        try:
            if (
                func_node.body
                and isinstance(func_node.body[0], ast.Expr)
                and isinstance(func_node.body[0].value, ast.Str)
            ):
                docstring = func_node.body[0].value.s
        # pylint: disable=broad-except
        except Exception:
            return None

        # for Python2
        try:
            docstring = docstring.decode("utf-8")
        except AttributeError:
            pass

        return docstring

    def get_docstrings(self):
        """Returns parsed Polarion docstrings present in the python source file."""
        docstrings = []
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.FunctionDef):
                continue

            if self.tests_only and node.name.find("test_") != 0:
                continue

            docstring = self.get_docstring_from_func(node)

            # test doesn't have docstring, i.e. it's missing also the Polarion section
            if not docstring:
                docstrings.append(DocstringsRecord(node.body[0].lineno - 1, node.col_offset, {}))
                continue

            doc_list = docstring.split("\n")
            docstring_start = node.body[0].lineno - len(doc_list)
            polarion_start, polarion_column = get_section_start(doc_list, self.SECTIONS.polarion)

            if not polarion_start:
                # docstring is missing the Polarion section
                docstrings.append(DocstringsRecord(docstring_start + 1, node.col_offset + 4, {}))
                continue

            polarion_offset = docstring_start + polarion_start
            docstrings.append(
                DocstringsRecord(polarion_offset, polarion_column, parse_docstring(docstring))
            )

        return docstrings


# convenience functions


def parse_docstring(docstring):
    """Parses docstring to dictionary."""
    return DocstringParser(docstring).parse()


def strip_polarion_data(docstring):
    """Removes the Polarion section from the docstring."""
    return DocstringParser(docstring).strip_polarion_data()


def get_docstrings_in_file(filename, tree=None, tests_only=True):
    """Returns parsed Polarion docstrings present in the python source file."""
    return FileParser(filename, tree=tree, tests_only=tests_only).get_docstrings()

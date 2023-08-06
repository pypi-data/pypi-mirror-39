# -*- coding: utf-8 -*-
"""
Checks Polarion docstrings.
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
from collections import namedtuple

from pkg_resources import get_distribution

from polarion_docstrings import configuration, parser, utils

DocstringsError = namedtuple("DocstringsError", "lineno column message func")
FieldRecord = namedtuple("FieldRecord", "lineno column field")
ValidatedDocstring = namedtuple("ValidatedDocstring", "unknown invalid missing markers ignored")


# pylint: disable=too-many-instance-attributes
class DocstringsChecker(object):
    """Checker for Polarion docstrings."""

    IGNORED_FIELD = "P664"
    MISSING_SECTION = "P665"
    UNKNOWN_FIELD = "P666"
    INVALID_VALUE = "P667"
    MARKER_FIELD = "P668"
    MISSING_FIELD = "P669"

    def __init__(self, tree, filename, config, func):
        self.tree = tree
        self.filename = filename
        self.config = config
        self.func = func

    @staticmethod
    def validate_value(docstring_dict, key, valid_values):
        record = docstring_dict.get(key)
        if record is not None:
            return record.value in valid_values[key]
        return True

    @staticmethod
    def get_unknown_fields(docstring_dict, known_fields):
        unknown = [
            FieldRecord(docstring_dict[key].lineno, docstring_dict[key].column, key)
            for key in docstring_dict
            if key not in known_fields
        ]
        return unknown

    @classmethod
    def get_invalid_fields(cls, docstring_dict, valid_values):
        results = {
            key: cls.validate_value(docstring_dict, key, valid_values) for key in valid_values
        }
        invalid = [
            FieldRecord(docstring_dict[key].lineno, docstring_dict[key].column, key)
            for key, result in results.items()
            if not result
        ]
        return invalid

    @staticmethod
    def get_missing_fields(docstring_dict, required_keys):
        if not required_keys:
            return []
        missing = [key for key in required_keys if key not in docstring_dict]
        return missing

    @staticmethod
    def get_markers_fields(docstring_dict, marker_fields):
        if not marker_fields:
            return []
        markers = [
            FieldRecord(docstring_dict[key].lineno, docstring_dict[key].column, key)
            for key in marker_fields
            if key in docstring_dict
        ]
        return markers

    @staticmethod
    def get_ignored_fields(docstring_dict, ignored_fields):
        if not ignored_fields:
            return []
        ignored = [
            FieldRecord(docstring_dict[key].lineno, docstring_dict[key].column, key)
            for key in ignored_fields
            if key in docstring_dict
        ]
        return ignored

    def validate_docstring(self, docstring_dict):
        """Returns tuple with lists of problematic fields."""
        cfg_docstrings = self.config["docstrings"]
        unknown = self.get_unknown_fields(docstring_dict, self.config.get("default_fields"))
        invalid = self.get_invalid_fields(docstring_dict, cfg_docstrings.get("valid_values"))
        missing = self.get_missing_fields(docstring_dict, cfg_docstrings.get("required_fields"))
        markers = self.get_markers_fields(docstring_dict, cfg_docstrings.get("marker_fields"))
        ignored = self.get_ignored_fields(docstring_dict, cfg_docstrings.get("ignored_fields"))
        return ValidatedDocstring(unknown, invalid, missing, markers, ignored)

    # pylint:disable=too-many-locals
    def get_fields_errors(self, validated_docstring, docstring_dict, lineno=0, column=0):
        """Produces fields errors for the flake8 checker."""
        errors = []
        cfg_docstrings = self.config["docstrings"]
        marker_fields = cfg_docstrings.get("marker_fields") or {}
        ignored_fields = cfg_docstrings.get("ignored_fields") or {}

        for num, col, field in validated_docstring.unknown:
            errors.append(
                DocstringsError(
                    lineno + num,
                    col,
                    '{} Unknown field "{}"'.format(self.UNKNOWN_FIELD, field),
                    self.func,
                )
            )
        for num, col, field in validated_docstring.invalid:
            errors.append(
                DocstringsError(
                    lineno + num,
                    col,
                    '{} Invalid value "{}" of the "{}" field'.format(
                        self.INVALID_VALUE, docstring_dict[field].value, field
                    ),
                    self.func,
                )
            )
        for num, col, field in validated_docstring.markers:
            errors.append(
                DocstringsError(
                    lineno + num,
                    col,
                    '{} Field "{}" should be handled by the "{}" marker'.format(
                        self.MARKER_FIELD, field, marker_fields.get(field)
                    ),
                    self.func,
                )
            )
        for num, col, field in validated_docstring.ignored:
            errors.append(
                DocstringsError(
                    lineno + num,
                    col,
                    '{} Ignoring field "{}": {}'.format(
                        self.IGNORED_FIELD, field, ignored_fields.get(field)
                    ),
                    self.func,
                )
            )
        for field in validated_docstring.missing:
            errors.append(
                DocstringsError(
                    lineno,
                    column,
                    '{} Missing required field "{}"'.format(self.MISSING_FIELD, field),
                    self.func,
                )
            )

        if errors:
            errors = sorted(errors, key=lambda tup: tup[0])
        return errors

    @staticmethod
    def print_errors(errors):
        """Prints errors without using flake8."""
        for err in errors:
            print("line: {}:{}: {}".format(err.lineno, err.column, err.message), file=sys.stderr)

    def check_docstrings(self, docstrings):
        """Runs checks on each docstring."""
        errors = []
        for record in docstrings:
            if record.value:
                valdoc = self.validate_docstring(record.value)
                errors.extend(
                    self.get_fields_errors(valdoc, record.value, record.lineno, record.column)
                )
            else:
                errors.append(
                    DocstringsError(
                        record.lineno,
                        record.column,
                        '{} Missing "Polarion" section'.format(self.MISSING_SECTION),
                        self.func,
                    )
                )
        return errors

    def run_checks(self):
        """Checks docstrings in python source file."""
        docstrings = parser.get_docstrings_in_file(self.filename, tree=self.tree)
        errors = self.check_docstrings(docstrings)
        return errors

    def is_for_check(self):
        """Decides if the file should be checked."""
        # check only if configuration is valid
        cfg_valid = self.config.get("docstrings") or {}
        cfg_valid = cfg_valid.get("valid_values")
        if not (cfg_valid and self.config.get("default_fields")):
            return False

        abs_filename = os.path.abspath(self.filename)
        head, tail = os.path.split(abs_filename)

        # check only test files under polarion tests path
        if not (tail.startswith("test_") and utils.find_tests_marker(head or ".")):
            return False

        return True

    def get_errors(self):
        """Get errors in docstrings in python source file."""
        if not self.is_for_check():
            return []

        return self.run_checks()


def polarion_checks492(tree, filename):
    """The flake8 entry point."""
    config = configuration.get_config()
    return DocstringsChecker(tree, filename, config, polarion_checks492).get_errors()


try:
    # __package__ is not in python 2.7
    __version__ = get_distribution(__name__.split(".")[0]).version
# pylint: disable=broad-except
except Exception:
    # package is not installed
    __version__ = "0.0"

polarion_checks492.name = "polarion_checks"
polarion_checks492.version = __version__

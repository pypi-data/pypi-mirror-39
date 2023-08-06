# encoding: utf-8
# pylint: disable=missing-docstring

from __future__ import unicode_literals

from polarion_docstrings import parser

RESULTS = [
    (51, 0, {}),
    (55, 0, {}),
    (61, 4, {}),
    (70, 4, {"assignee": (1, 8, "mkourim"), "initialEstimate": (2, 8, "1/4")}),
    (10, 4, {}),
    (14, 8, {}),
    (
        21,
        8,
        {
            "assignee": (1, 12, "mkourim"),
            "caseautomation": (19, 12, "automated"),
            "casecomponent": (2, 12, "nonexistent"),
            "caseimportance": (11, 12, "low"),
            "caselevel": (18, 12, "level1"),
            "expectedResults": [
                (
                    8,
                    16,
                    "1. Success outcome with really long description that doesn't "
                    "fit into one line",
                ),
                (10, 16, "2. second"),
            ],
            "foo": (21, 12, "this is an unknown field"),
            "linkedWorkItems": (20, 12, "FOO, BAR"),
            "setup": (14, 12, "Do this:\n- first thing\n- second thing"),
            "teardown": (17, 12, "Tear it down"),
            "testSteps": [
                (4, 16, "1. Step with really long description that doesn't fit into one line"),
                (6, 16, "2. Do that"),
            ],
            "title": (
                12,
                12,
                "Some test with really long description that doesn't fit into one line",
            ),
            "description": (22, 12, "ignored"),
        },
    ),
]


def test_parser(source_file):
    docstrings = parser.get_docstrings_in_file(source_file)
    assert len(docstrings) == len(RESULTS)
    assert docstrings == RESULTS

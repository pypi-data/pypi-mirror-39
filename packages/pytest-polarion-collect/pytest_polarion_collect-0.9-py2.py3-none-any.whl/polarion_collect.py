# -*- coding: utf-8 -*-
"""pytest plugin for collecting polarion test cases data"""

from __future__ import print_function

import json
import os
import re

import pytest
import six

from polarion_docstrings import parser as docparser
from polarion_docstrings import utils

DUPLICATES = "duplicates.log"
TESTS_DATA = "tests_data.json"

STEP_NUMBERING = re.compile(r"[0-9]+[.)]? ?")


def pytest_addoption(parser):
    """Adds command line options."""
    group = parser.getgroup("Polarion: options related to test cases data collection")
    group.addoption(
        "--generate-json",
        action="store_true",
        default=False,
        help="generate JSON file with tests data",
    )


def extract_fixtures_values(item):
    """Extracts names and values of all the fixtures that the test has.

    Args:
        item: py.test test item
    Returns:
        :py:class:`dict` with fixtures and their values.
    """
    try:
        return item.callspec.params.copy()  # protect against accidential manipulation of the spec
    except AttributeError:
        # Some of the test items do not have callspec, so fall back
        # This can cause some problems if the fixtures are used in the guards in this case, but
        # that will tell use where is the problem and we can then find it out properly.
        return {}


def get_unicode_str(obj):
    """Makes sure obj is a unicode string."""
    if isinstance(obj, six.text_type):
        return obj
    if isinstance(obj, six.binary_type):
        return obj.decode("utf-8", errors="ignore")
    return six.text_type(obj)


def _get_docstring(item):
    try:
        return get_unicode_str(item.function.__doc__)
    except (AttributeError, UnicodeDecodeError):
        return ""


def _get_caselevel(item, parsed_docstring):
    caselevel = parsed_docstring.get("caselevel")
    if caselevel and caselevel.value:
        return caselevel.value

    try:
        tier = int(item.get_marker("tier").args[0])
    except (ValueError, AttributeError):
        tier = 0

    return tier


def _get_caseautomation(item, parsed_docstring):
    caseautomation = parsed_docstring.get("caseautomation")
    if caseautomation and caseautomation.value:
        return caseautomation.value

    if item.get_marker("manual"):
        return "manualonly"

    return "automated"


def _get_automation_script(item):
    return "{}#L{}".format(item.location[0], item.function.__code__.co_firstlineno)


def _get_description(item, docstring):
    try:
        description = docparser.strip_polarion_data(docstring)
    except ValueError as err:
        print("Cannot parse the description of {}: {}".format(item.location[2], err))
        description = ""

    return description


def _get_steps_and_results(parsed_docstring):
    if not parsed_docstring.get("testSteps"):
        return None

    test_steps = []
    expected_results = []

    steps = parsed_docstring.get("testSteps")
    results = parsed_docstring.get("expectedResults")
    steps = [STEP_NUMBERING.sub("", s.value) for s in steps]
    results = [STEP_NUMBERING.sub("", r.value) for r in results]

    for index, step in enumerate(steps):
        test_steps.append(step)

        try:
            result = results[index]
        except IndexError:
            result = ""
        expected_results.append(result)

    return test_steps, expected_results


def _get_assignee(parsed_docstring):
    assignee = parsed_docstring.get("assignee")
    if assignee and assignee.value:
        return assignee.value
    return None


def _get_initial_estimate(parsed_docstring):
    initial_estimate = parsed_docstring.get("initialEstimate")
    if initial_estimate and initial_estimate.value:
        return initial_estimate.value
    return None


def _get_requirement_name(item):
    try:
        return [item.get_marker("requirement").args[0]]
    except AttributeError:
        return None


def _get_linked_items(parsed_docstring):
    linked_items = parsed_docstring.get("linkedWorkItems")
    if linked_items and linked_items.value:
        return linked_items.value.split(",")
    return None


def get_testcase_data(test_name, tests, processed_tests, item):
    """Gets data for single test case entry."""
    if test_name in processed_tests:
        return
    processed_tests.append(test_name)

    testcase_data = {}

    docstring = _get_docstring(item)
    parsed_docstring = docparser.parse_docstring(docstring) or {}

    testcase_data["caseautomation"] = _get_caseautomation(item, parsed_docstring)

    if testcase_data["caseautomation"] == "automated":
        testcase_data["automation_script"] = _get_automation_script(item)

    testcase_title = parsed_docstring.get("title")
    testcase_title = testcase_title.value if testcase_title else test_name
    testcase_data["title"] = testcase_title

    test_steps = _get_steps_and_results(parsed_docstring)
    if test_steps:
        testcase_data["testSteps"], testcase_data["expectedResults"] = test_steps

    testcase_data["id"] = testcase_title
    testcase_data["assignee-id"] = _get_assignee(parsed_docstring)
    testcase_data["caselevel"] = _get_caselevel(item, parsed_docstring)
    testcase_data["description"] = _get_description(item, docstring)
    testcase_data["id"] = test_name
    testcase_data["initial-estimate"] = _get_initial_estimate(parsed_docstring)
    testcase_data["linked-items"] = _get_requirement_name(item) or _get_linked_items(
        parsed_docstring
    )
    testcase_data["params"] = list(extract_fixtures_values(item).keys()) or None
    testcase_data["nodeid"] = item.nodeid

    # save the rest of the fields as it is
    for field, record in parsed_docstring.items():
        if field not in testcase_data and hasattr(record, "value"):
            testcase_data[field] = record.value

    tests.append(testcase_data)


def _get_name(obj):
    if hasattr(obj, "_param_name"):
        # pylint: disable=protected-access
        return obj._param_name
    elif hasattr(obj, "name"):
        return obj.name
    return str(obj)


def get_testresult_data(test_name, tests, processed_tests, item):
    """Gets data for single test result entry."""
    if test_name in processed_tests:
        return
    processed_tests.append(test_name)

    testresult_data = {"title": test_name, "verdict": "waiting"}

    try:
        params = item.callspec.params
    except AttributeError:
        params = {}

    parameters = {p: _get_name(v) for p, v in params.items()}
    if parameters:
        testresult_data["params"] = parameters

    tests.append(testresult_data)


def gen_duplicates_log(items):
    """Generates log file containing non-unique test cases names."""
    test_param = re.compile(r"\[.*\]")
    names = {}
    duplicates = set()

    for item in items:
        name = test_param.sub("", item.location[2])
        path = item.location[0]

        name_record = names.get(name)
        if name_record:
            name_record.add(path)
        else:
            names[name] = {path}

    for name, paths in names.items():
        if len(paths) > 1:
            duplicates.add(name)

    with open(DUPLICATES, "w") as outfile:
        for test in sorted(duplicates):
            outfile.write("{}\n".format(test))


def write_json(data_dict, out_file):
    """Outputs data as JSON."""
    with open(out_file, "w") as out:
        json.dump(data_dict, out, indent=4)


def is_whitelisted(whitelist, blacklist, nodeid):
    """Checks if the nodeid is whitelisted."""
    if whitelist and whitelist.search(nodeid):
        return True
    if blacklist and blacklist.search(nodeid):
        return False
    return True


def is_test_dir(abs_filename, test_dirs_cache):
    """Checks if the test is in directory with Polarion tests and updates cache."""
    white, black = test_dirs_cache

    for tdir in white:
        if abs_filename.startswith(tdir):
            return True
    for tdir in black:
        if abs_filename.startswith(tdir):
            return False

    test_dir = os.path.dirname(abs_filename)
    test_top_dir = utils.find_tests_marker(test_dir)
    if test_top_dir:
        white.add(test_top_dir)
    else:
        black.add(test_dir)
    return bool(test_top_dir)


@pytest.mark.trylast
def pytest_collection_modifyitems(config, items):
    """Generates the JSON files using collected items."""
    if not (config.getoption("generate_json") and config.getoption("collectonly")):
        return

    gen_duplicates_log(items)

    tc_processed = []
    testcases = []
    tr_processed = []
    testsuites = []

    # cache of dirs with Polarion tests, cache of dirs with non-Polarion tests
    test_dirs_cache = set(), set()

    for item in items:
        if not is_test_dir(str(item.fspath), test_dirs_cache):
            continue

        name = item.location[2]

        get_testcase_data(name, testcases, tc_processed, item)
        get_testresult_data(name, testsuites, tr_processed, item)

    tests_data = {"testcases": testcases, "results": testsuites}
    write_json(tests_data, TESTS_DATA)

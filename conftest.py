"""This conftest.py module is automatically loaded during framework execution
    It includes mostly pytest framework configuration.
"""

import os
from datetime import datetime
from pathlib import Path

import dotenv
import pytest
import requests

from src.helpers.screenshots import Screenshots

LOGGERS = "TEST,PAGE,FIXTURE,API,GENERATOR"

dotenv.load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--log_lvl",
        action="store",
        dest="log_lvl",
        default="info",
        help="Select logging level: info or debug",
    )
    parser.addoption(
        "--screenshot-path",
        action="store",
        dest="screenshot_path",
        default="artefacts/screenshots",
        help="Path to the screenshots folder",
    )
    parser.addoption(
        "--additional-info",
        action="store",
        dest="additional_info",
        default="Build: ",
        help="Path to the screenshots folder",
    )
    parser.addoption(
        "--tracing-path",
        action="store",
        dest="tracing_path",
        default="artefacts/tracing",
        help="Path to store tracing",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    screenshot_path = ""
    report = outcome.get_result()

    setattr(item, "rep_" + report.when, report)
    extras = getattr(report, "extras", [])
    if report.when == "call" and "page" in item.funcargs:
        if report.failed and "page" in item.funcargs:
            page = item.funcargs["page"]
            tracing_path = item.config.option.tracing_path + "/" + item.name + ".zip"
            page.context.tracing.stop(path=tracing_path)
            screenshot_path = item.config.option.screenshot_path
            if screenshot_path:
                screenshots = Screenshots(
                    relative_path=Path(screenshot_path), page=page
                )
                screenshots.save_screenshot_as_file(item.name)
            screenshot_base64 = Screenshots(
                relative_path=Path(""), page=page
            ).save_screenshot_as_base64()
            extras.append(pytest_html.extras.image(screenshot_base64))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # add the screenshots to the html report
            page = item.funcargs["page"]
            screenshot_base64 = Screenshots(
                relative_path=Path(""), page=page
            ).save_screenshot_as_base64()
            extras.append(pytest_html.extras.image(screenshot_base64))
        report.extras = extras


def pytest_html_report_title(report):
    date = datetime.now().strftime("%B %d %Y %H:%M:%S")
    report.title = f"Report for automation run on {date}"

"""This conftest.py module is automatically loaded during framework execution
    It includes mostly pytest framework configuration.
"""

import os

import dotenv
import pytest
import requests

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

import os
import re
from datetime import datetime
from os import environ
from pathlib import Path
from typing import Callable, List

ENV_VARS = [
    "SITE_URL",
    "SITE_TITLE",
    "TIMEZONE",
    "REPO_URL",
    "LANDING_PAGE",
    "LANDING_TITLE",
    "LANDING_DESCRIPTION",
    "LANDING_BUTTON",
]

ZOLA_DIR = Path(__file__).resolve().parent
DOCS_DIR = ZOLA_DIR / "content" / "docs"


def print_step(msg: str):
    print(msg.center(100, "-"))


def process_lines(path: Path, fn: Callable[[str], str]):
    content = "\n".join([fn(line.rstrip()) for line in open(path, "r").readlines()])
    open(path, "w").write(content)
    print_step(str(path))
    print(content)


def step1():
    """
    Check environment variables
    """
    print_step("CHECKING ENVIRONMENT VARIABLES")
    for item in ENV_VARS:
        if item not in environ:
            print(f"WARNING: build.environment.{item} not set!")
            environ[item] = f"build.environment.{item}"
        else:
            print(f"{item}: {environ[item]}")


def step2():
    """
    Substitute netlify.toml settings into config.toml and landing page
    """

    print_step("SUBSTITUTING CONFIG FILE AND LANDING PAGE")

    def sub(line: str) -> str:
        for env_var in ENV_VARS:
            line = line.replace(f"___{env_var}___", environ[env_var])
        return line

    process_lines(ZOLA_DIR / "config.toml", sub)
    process_lines(ZOLA_DIR / "content" / "_index.md", sub)

if __name__ == "__main__":
    step1()
    step2()

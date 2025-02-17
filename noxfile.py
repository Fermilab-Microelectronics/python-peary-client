"""
noxfile.py Configuration file for Nox
"""

# pylint: disable=import-error
import os
import shutil

import nox

nox.options.error_on_external_run = True
nox.options.envdir = os.environ.get("NOX_ENVDIR", ".nox")


@nox.session(reuse_venv=True, default=False)
def build_venv(session):
    """Builds the virtual environment."""
    session.install("-e", ".[dev]")
    if session.posargs:
        for task in session.posargs[0]:
            task(session, *session.posargs[1:])


@nox.session(reuse_venv=True, default=False, python=False)
def clean(session):
    """Cleans the virtual environments."""
    session.log(f"Removing build artifacts from '{nox.options.envdir}'")
    shutil.rmtree(nox.options.envdir, ignore_errors=True)


@nox.session(reuse_venv=True, default=False)
def cli(session):
    """Runs the CLI."""
    session.notify("build_venv", posargs=([_cli], *session.posargs))


@nox.session(reuse_venv=True)
def lint(session):
    """Runs lint checks."""
    session.notify("build_venv", posargs=([_lint], *session.posargs))


@nox.session(reuse_venv=True)
def style(session):
    """Runs linters and fixers."""
    session.notify("build_venv", posargs=([_style], *session.posargs))


@nox.session(reuse_venv=True)
def test(session):
    """Runs tests."""
    session.notify("build_venv", posargs=([_test], *session.posargs))


def _cli(session, *args):
    """Executes the environment command for the CLI."""
    if session.posargs:
        session.run(*args)


def _lint(session):
    """Executes the environment command for the lint checks."""
    session.run("black", "--check", "--diff", "--color", ".")
    session.run("flake8", "src", "test")
    session.run("isort", "--check", "--diff", "--color", "--profile", "black", ".")
    session.run("pyprojectsort", "--diff")
    session.run("ruff", "check", "src")
    session.run("ruff", "check", "test", "--ignore=D,ANN,S101,PLR2004,UP012")
    session.run("pylint", "--enable-all-extensions", "src")
    session.run(
        "pylint",
        "--enable-all-extensions",
        "test",
        "--disable=duplicate-code",
        "--disable=magic-value-comparison",
        "--disable=missing-class-docstring",
        "--disable=missing-function-docstring",
        "--disable=missing-module-docstring",
        "--disable=missing-param-doc",
        "--disable=missing-type-doc",
        "--disable=no-self-use",
    )
    session.run("mypy", "src", "test")


def _style(session):
    """Executes the environment command for the stylers and fixers."""
    session.run("black", "--verbose", ".")
    session.run("isort", "--profile", "black", ".")
    session.run("pyprojectsort")


def _test(session, *args):
    """Executes the environment command for the tests."""
    session.run(
        "coverage",
        "run",
        "--source=src,test",
        "-m",
        "pytest",
        "--capture=sys",
        "-v",
        *args,
    )
    session.run("coverage", "report", "--fail-under=100", "--show-missing")

"""
noxfile.py Configuration file for Nox
"""

# pylint: disable=import-error
import os
import shutil

import nox

nox.options.reuse_venv = True
nox.options.error_on_external_run = True
nox.options.envdir = os.environ.get("NOX_ENVDIR", ".nox")


@nox.session(default=False, python=False)
def clean(session):
    """Clean up build artifacts."""
    session.log(f"Removing build artifacts from '{nox.options.envdir}'")
    shutil.rmtree(nox.options.envdir, ignore_errors=True)


@nox.session(default=False)
def cli(session):
    """Runs CLI"""
    session.install("-e", ".[dev]")
    session.run(*session.posargs)


@nox.session(tags=["check"])
def lint(session):
    """Runs lint checks"""
    session.install("-e", ".[dev]")
    session.run("black", "--check", "--diff", "--color", ".")
    session.run("flake8", "src", "test")
    session.run("isort", "--check", "--diff", "--color", "--profile", "black", ".")
    session.run("pyprojectsort", "--diff")
    session.run("ruff", "check", "src")
    session.run("ruff", "check", "test", "--ignore=D,ANN,S101,PLR2004,UP012")
    session.run("pylint", "src", "--enable-all-extensions")
    session.run(
        "pylint",
        "test",
        "--disable=missing-param-doc",
        "--disable=missing-type-doc",
        "--disable=duplicate-code",
        "--disable=missing-class-docstring",
        "--disable=missing-function-docstring",
        "--disable=missing-module-docstring",
    )
    session.run("mypy", "src", "test")


@nox.session(tags=["fix"])
def style(session):
    """Runs linters and fixers"""
    session.install("-e", ".[dev]")
    session.run("black", "--verbose", ".")
    session.run("isort", "--profile", "black", ".")
    session.run("pyprojectsort")


@nox.session(tags=["check"])
def test(session):
    """Runs tests"""
    session.install("-e", ".[dev]")
    session.run(
        "coverage",
        "run",
        "--source=src,test",
        "-m",
        "pytest",
        "--capture=sys",
        "-v",
        *session.posargs,
    )
    session.run("coverage", "report", "--fail-under=100", "--show-missing")

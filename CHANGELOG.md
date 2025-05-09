# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

```markdown
## [Unreleased] - YYYY-MM-DD
### Added
### Changed
### Deprecated
### Fixed
### Security
```

## [Unreleased] - YYYY-MM-DD
### Added
- Seperated the peary client package from another project to create this package.
- Increased the verbosity of the python package versions to include both the system
  packaes as well as the virtual environment packages.
- Added a class argument to the the `add_device` method of the `PearyProxy` class so
  users can define cusotme interfaces for devices.
- Python version is now reported with other dependecy versions in the gihub workflow.
- Added `py.typed` to the source packages to allow for mypy typing across dependencies.
- Created the supply classes that will be used to access the caribou board supplies.
- Added an optional checks flag to peary protocol class so intialization checks can
  be controlled during intialization.
### Changed
- Updated Nox to resuse the virtual environments accross sessions.
- Reduced the socket timeout for peary protocol from 10s to 1s.
- Updated the linter settings by removing unecessary disables and turning on more checks
  for the tests.
- Udpated the `PearyProxy` tests to removed cluttered redundant code for mocking
  internal socket communications.
- Tightened the requirements used to lint all of the tests.
- Rewrote the peary classes to accept protocol object directly instead of contructing
  the protocol from a socket.
- Removed the unecessary abstract interface classes.
### Deprecated
### Fixed
- Fixed bug with peary protocol socket calls where reading multiple buffers would cause
  the socket to hang due to incorrect usage of non-blocking operations.
- Added missing command line option to isolate python in github workflow:
  `python -m pip install --upgrade pip` -> `python -Im pip install --upgrade pip`
- Rewrote the class tests to use derived classes instead of monkeypatching everything.
- Removed unused `python-labtest` dependency.
### Security

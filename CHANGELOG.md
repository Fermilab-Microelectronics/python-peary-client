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
### Changed
- Updated Nox to resuse the virtual environments accross sessions.
- Reduced the socket timeout for peary protocol from 10s to 1s.
- Updated the linter settings by removing unecessary disables and turning on more checks
  for the tests.
### Deprecated
### Fixed
- Fixed bug with peary protocol socket calls where reading multiple buffers would cause
  the socket to hang due to incorrect usage of non-blocking operations.
### Security

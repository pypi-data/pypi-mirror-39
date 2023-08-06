# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.2.7]
### Fixed
- MemcachedKeyCharacterError was raised if a file was uploaded with åäö
  in the filename

## [0.2.3]
### Added
- `absolute_url` templatetag
- Tests for `absolute_reverse` and `absolute_url`

## [0.2.2]
### Added
- CODE\_OF\_CONDUCT.md
- Tests for Django 2.0

## [0.2.1]
### Added
- YAMLPrettyField dumps with unicode characters enabled
- MANIFEST.in with extra files

### Changed
- setup.py will read README.rst for it's `long_description`

## [0.2.0] - 2017-08-04
### Added
- YAMLPrettyField, based on JSONPrettyField
- JSONPrettyField automated tests

[Unreleased]: https://github.com/bulv1ne/django-utils/compare/v0.2.7...HEAD
[0.2.7]: https://github.com/bulv1ne/django-utils/compare/v0.2.6...v0.2.7
[0.2.6]: https://github.com/bulv1ne/django-utils/compare/v0.2.5...v0.2.6
[0.2.5]: https://github.com/bulv1ne/django-utils/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/bulv1ne/django-utils/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/bulv1ne/django-utils/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/bulv1ne/django-utils/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/bulv1ne/django-utils/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/bulv1ne/django-utils/compare/v0.1.3...v0.2.0

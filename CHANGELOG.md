# CHANGELOG

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Track.is_midi

## [0.1.0] - 2019-02-28

### Added

- `reapy.inside_reaper` context manager for efficient calls from outside REAPER and corresponding [documentation](https://python-reapy.readthedocs.io/en/latest/api_guide.html#improve-performance-with-reapy-inside-reaper)
- `reapy.defer` and `reapy.at_exit` to replace `RPR_defer` and `RPR_atexit` in a more stable way, and corresponding [documentation](https://python-reapy.readthedocs.io/en/latest/api_guide.html#non-blocking-loops-inside-reaper-with-reapy-defer-and-reapy-at-exit)
- `Track.add_fx` and `Take.add_fx`
- Documentation for uninstalling process [here](https://python-reapy.readthedocs.io/en/latest/install_guide.html)

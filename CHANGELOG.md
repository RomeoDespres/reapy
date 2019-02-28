# CHANGELOG

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- `Take.is_midi`
- `Take.n_cc` (number of MIDI CC on take)
- `Take.n_notes` (number of MIDI notes on take)
- `Take.n_text_sysex` (number of MIDI text/sysex on take)
- `Take.select_all_midi_events` and `Take.unselect_all_midi_events`
- class `reapy.MIDIEditor`
- `reapy.midi.reinit` (reset all MIDI devices)

## [0.1.0] - 2019-02-28

### Added

- `reapy.inside_reaper` context manager for efficient calls from outside REAPER and corresponding [documentation](https://python-reapy.readthedocs.io/en/latest/api_guide.html#improve-performance-with-reapy-inside-reaper)
- `reapy.defer` and `reapy.at_exit` to replace `RPR_defer` and `RPR_atexit` in a more stable way, and corresponding [documentation](https://python-reapy.readthedocs.io/en/latest/api_guide.html#non-blocking-loops-inside-reaper-with-reapy-defer-and-reapy-at-exit)
- `Track.add_fx` and `Take.add_fx`
- Documentation for uninstalling process [here](https://python-reapy.readthedocs.io/en/latest/install_guide.html)

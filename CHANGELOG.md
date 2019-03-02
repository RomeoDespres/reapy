# CHANGELOG

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

#### Audio/MIDI Device Management

- [`reapy.audio.get_n_inputs`]
- [`reapy.audio.get_n_outputs`]
- [`reapy.audio.get_input_latency`]
- [`reapy.audio.get_output_latency`]
- [`reapy.audio.get_input_names`]
- [`reapy.audio.get_output_names`]
- [`reapy.midi.get_max_inputs`]
- [`reapy.midi.get_max_outputs`]
- [`reapy.midi.get_n_inputs`]
- [`reapy.midi.get_n_outputs`]
- [`reapy.midi.get_input_names`]
- [`reapy.midi.get_output_names`]

#### Item Management

- [`Take.name`]

#### Envelope Management

- [`Envelope.parent`]
- [`Envelope.get_value`]
- [`Envelope.get_derivatives`]
- [`FXParam.add_envelope`]
- [`FXParam.envelope`]
- [`Take.envelopes`]
- [`Track.envelopes`]

#### MIDI Management

- [`Take.is_midi`]
- [`Take.n_cc`] (number of MIDI CC on take)
- [`Take.n_notes`] (number of MIDI notes on take)
- [`Take.n_text_sysex`] (number of MIDI text/sysex on take)
- [`Take.select_all_midi_events`] and [`Take.unselect_all_midi_events`]
- class [`reapy.MIDIEditor`]
- [`reapy.midi.reinit`] (reset all MIDI devices)

#### Project Management

- [`reapy.open_project`]

#### User Interface

- [`reapy.get_last_color_theme_file`]
- [`reapy.get_main_window`]

### Removed

#### Envelope Management

- `Track.get_envelope` (replaced by [`Track.envelopes`])


## [0.1.0] - 2019-02-28

### Added

- `reapy.inside_reaper` context manager for efficient calls from outside REAPER and corresponding [documentation](https://python-reapy.readthedocs.io/en/latest/api_guide.html#improve-performance-with-reapy-inside-reaper)
- `reapy.defer` and `reapy.at_exit` to replace `RPR_defer` and `RPR_atexit` in a more stable way, and corresponding [documentation](https://python-reapy.readthedocs.io/en/latest/api_guide.html#non-blocking-loops-inside-reaper-with-reapy-defer-and-reapy-at-exit)
- [`Track.add_fx`] and [`Take.add_fx`]
- [Documentation for uninstalling process](https://python-reapy.readthedocs.io/en/latest/install_guide.html)

[//]: # (LINKS)
[`AutomationItem.delete_points_in_range`]: reapy.core.html#reapy.core.AutomationItem.delete_points_in_range
[`AutomationItem.length`]: reapy.core.html#reapy.core.AutomationItem.length
[`AutomationItem.n_points`]: reapy.core.html#reapy.core.AutomationItem.n_points
[`AutomationItem.pool`]: reapy.core.html#reapy.core.AutomationItem.pool
[`AutomationItem.position`]: reapy.core.html#reapy.core.AutomationItem.position
[`Envelope.delete_points_in_range`]: reapy.core.html#reapy.core.Envelope.delete_points_in_range
[`Envelope.get_derivatives`]: reapy.core.html#reapy.core.Envelope.get_derivatives
[`Envelope.get_value`]: reapy.core.html#reapy.core.Envelope.get_value
[`Envelope.n_items`]: reapy.core.html#reapy.core.Envelope.n_items
[`Envelope.n_points`]: reapy.core.html#reapy.core.Envelope.n_points
[`Envelope.name`]: reapy.core.html#reapy.core.Envelope.name
[`Envelope.parent`]: reapy.core.html#reapy.core.Envelope.parent
[`FX.close_ui`]: reapy.core.html#reapy.core.FX.close_ui
[`FX.copy_to_take`]: reapy.core.html#reapy.core.FX.copy_to_take
[`FX.copy_to_track`]: reapy.core.html#reapy.core.FX.copy_to_track
[`FX.delete`]: reapy.core.html#reapy.core.FX.delete
[`FX.disable`]: reapy.core.html#reapy.core.FX.disable
[`FX.enable`]: reapy.core.html#reapy.core.FX.enable
[`FX.is_enabled`]: reapy.core.html#reapy.core.FX.is_enabled
[`FX.is_online`]: reapy.core.html#reapy.core.FX.is_online
[`FX.is_ui_open`]: reapy.core.html#reapy.core.FX.is_ui_open
[`FX.make_offline`]: reapy.core.html#reapy.core.FX.make_offline
[`FX.make_online`]: reapy.core.html#reapy.core.FX.make_online
[`FX.move_to_take`]: reapy.core.html#reapy.core.FX.move_to_take
[`FX.move_to_track`]: reapy.core.html#reapy.core.FX.move_to_track
[`FX.n_params`]: reapy.core.html#reapy.core.FX.n_params
[`FX.name`]: reapy.core.html#reapy.core.FX.name
[`FX.open_ui`]: reapy.core.html#reapy.core.FX.open_ui
[`FX.params`]: reapy.core.html#reapy.core.FX.params
[`FX.preset_file`]: reapy.core.html#reapy.core.FX.preset_file
[`FX.preset_index`]: reapy.core.html#reapy.core.FX.preset_index
[`FX.preset`]: reapy.core.html#reapy.core.FX.preset
[`FX.use_next_preset`]: reapy.core.html#reapy.core.FX.use_next_preset
[`FX.use_previous_preset`]: reapy.core.html#reapy.core.FX.use_previous_preset
[`FXParam.add_envelope`]: reapy.core.html#reapy.core.FXParam.add_envelope
[`FXParam.envelope`]: reapy.core.html#reapy.core.FXParam.envelope
[`FXParam.name`]: reapy.core.html#reapy.core.FXParam.name
[`Item.active_take`]: reapy.core.html#reapy.core.Item.active_take
[`Item.add_take`]: reapy.core.html#reapy.core.Item.add_take
[`Item.get_info_value`]: reapy.core.html#reapy.core.Item.get_info_value
[`Item.get_take`]: reapy.core.html#reapy.core.Item.get_take
[`Item.is_selected`]: reapy.core.html#reapy.core.Item.is_selected
[`Item.length`]: reapy.core.html#reapy.core.Item.length
[`Item.n_takes`]: reapy.core.html#reapy.core.Item.n_takes
[`Item.position`]: reapy.core.html#reapy.core.Item.position
[`Item.project`]: reapy.core.html#reapy.core.Item.project
[`Item.split`]: reapy.core.html#reapy.core.Item.split
[`Item.takes`]: reapy.core.html#reapy.core.Item.takes
[`Item.track`]: reapy.core.html#reapy.core.Item.track
[`MIDIEditor.mode`]: reapy.core.html#reapy.core.MIDIEditor.mode
[`MIDIEditor.perform_action`]: reapy.core.html#reapy.core.MIDIEditor.perform_action
[`MIDIEditor.take`]: reapy.core.html#reapy.core.MIDIEditor.take
[`MIDIEditor`]: reapy.core.html#reapy.core.MIDIEditor
[`Marker.delete`]: reapy.core.html#reapy.core.Marker.delete
[`Marker`]: reapy.core.html#reapy.core.Marker
[`Project.add_marker`]: reapy.core.html#reapy.core.Project.add_marker
[`Project.add_region`]: reapy.core.html#reapy.core.Project.add_region
[`Project.add_track`]: reapy.core.html#reapy.core.Project.add_track
[`Project.any_track_solo`]: reapy.core.html#reapy.core.Project.any_track_solo
[`Project.begin_undo_block`]: reapy.core.html#reapy.core.Project.begin_undo_block
[`Project.bpi`]: reapy.core.html#reapy.core.Project.bpi
[`Project.bpm`]: reapy.core.html#reapy.core.Project.bpm
[`Project.bypass_fx_on_all_tracks`]: reapy.core.html#reapy.core.Project.bypass_fx_on_all_tracks
[`Project.can_redo`]: reapy.core.html#reapy.core.Project.can_redo
[`Project.can_undo`]: reapy.core.html#reapy.core.Project.can_undo
[`Project.cursor_position`]: reapy.core.html#reapy.core.Project.cursor_position
[`Project.disarm_rec_on_all_tracks`]: reapy.core.html#reapy.core.Project.disarm_rec_on_all_tracks
[`Project.end_undo_block`]: reapy.core.html#reapy.core.Project.end_undo_block
[`Project.get_selected_item`]: reapy.core.html#reapy.core.Project.get_selected_item
[`Project.get_selected_track`]: reapy.core.html#reapy.core.Project.get_selected_track
[`Project.is_dirty`]: reapy.core.html#reapy.core.Project.is_dirty
[`Project.length`]: reapy.core.html#reapy.core.Project.length
[`Project.make_current_project`]: reapy.core.html#reapy.core.Project.make_current_project
[`Project.mark_dirty`]: reapy.core.html#reapy.core.Project.mark_dirty
[`Project.markers`]: reapy.core.html#reapy.core.Project.markers
[`Project.master_track`]: reapy.core.html#reapy.core.Project.master_track
[`Project.mute_all_tracks`]: reapy.core.html#reapy.core.Project.mute_all_tracks
[`Project.n_items`]: reapy.core.html#reapy.core.Project.n_items
[`Project.n_markers`]: reapy.core.html#reapy.core.Project.n_markers
[`Project.n_regions`]: reapy.core.html#reapy.core.Project.n_regions
[`Project.n_selected_items`]: reapy.core.html#reapy.core.Project.n_selected_items
[`Project.n_selected_tracks`]: reapy.core.html#reapy.core.Project.n_selected_tracks
[`Project.n_tempo_markers`]: reapy.core.html#reapy.core.Project.n_tempo_markers
[`Project.n_tracks`]: reapy.core.html#reapy.core.Project.n_tracks
[`Project.name`]: reapy.core.html#reapy.core.Project.name
[`Project.path`]: reapy.core.html#reapy.core.Project.path
[`Project.pause`]: reapy.core.html#reapy.core.Project.pause
[`Project.perform_action`]: reapy.core.html#reapy.core.Project.perform_action
[`Project.play_rate`]: reapy.core.html#reapy.core.Project.play_rate
[`Project.play_state`]: reapy.core.html#reapy.core.Project.play_state
[`Project.play`]: reapy.core.html#reapy.core.Project.play
[`Project.redo`]: reapy.core.html#reapy.core.Project.redo
[`Project.regions`]: reapy.core.html#reapy.core.Project.regions
[`Project.save`]: reapy.core.html#reapy.core.Project.save
[`Project.select_all_items`]: reapy.core.html#reapy.core.Project.select_all_items
[`Project.selected_envelope`]: reapy.core.html#reapy.core.Project.selected_envelope
[`Project.selected_items`]: reapy.core.html#reapy.core.Project.selected_items
[`Project.selected_tracks`]: reapy.core.html#reapy.core.Project.selected_tracks
[`Project.stop`]: reapy.core.html#reapy.core.Project.stop
[`Project.time_selection`]: reapy.core.html#reapy.core.Project.time_selection
[`Project.tracks`]: reapy.core.html#reapy.core.Project.tracks
[`Project.undo`]: reapy.core.html#reapy.core.Project.undo
[`Project.unmute_all_tracks`]: reapy.core.html#reapy.core.Project.unmute_all_tracks
[`Project`]: reapy.core.html#reapy.core.Project
[`Region.add_rendered_track`]: reapy.core.html#reapy.core.Region.add_rendered_track
[`Region.delete`]: reapy.core.html#reapy.core.Region.delete
[`Region.remove_rendered_track`]: reapy.core.html#reapy.core.Region.remove_rendered_track
[`Region.rendered_tracks`]: reapy.core.html#reapy.core.Region.rendered_tracks
[`Region`]: reapy.core.html#reapy.core.Region
[`Send.delete`]: reapy.core.html#reapy.core.Send.delete
[`Send`]: reapy.core.html#reapy.core.Send
[`Source.filename`]: reapy.core.html#reapy.core.Source.filename
[`Source.length`]: reapy.core.html#reapy.core.Source.length
[`Source.n_channels`]: reapy.core.html#reapy.core.Source.n_channels
[`Source.sample_rate`]: reapy.core.html#reapy.core.Source.sample_rate
[`Source.type`]: reapy.core.html#reapy.core.Source.type
[`Take.envelopes`]: reapy.core.html#reapy.core.Take.envelopes
[`Take.get_info_value`]: reapy.core.html#reapy.core.Take.get_info_value
[`Take.is_midi`]: reapy.core.html#reapy.core.Take.is_midi
[`Take.item`]: reapy.core.html#reapy.core.Take.item
[`Take.make_active_take`]: reapy.core.html#reapy.core.Take.make_active_take
[`Take.n_cc`]: reapy.core.html#reapy.core.Take.n_cc
[`Take.n_envelopes`]: reapy.core.html#reapy.core.Take.n_envelopes
[`Take.n_fxs`]: reapy.core.html#reapy.core.Take.n_fxs
[`Take.n_notes`]: reapy.core.html#reapy.core.Take.n_notes
[`Take.n_text_sysex`]: reapy.core.html#reapy.core.Take.n_text_sysex
[`Take.name`]: reapy.core.html#reapy.core.Take.name
[`Take.select_all_midi_events`]: reapy.core.html#reapy.core.Take.select_all_midi_events
[`Take.source`]: reapy.core.html#reapy.core.Take.source
[`Take.track`]: reapy.core.html#reapy.core.Take.track
[`Take.unselect_all_midi_events`]: reapy.core.html#reapy.core.Take.unselect_all_midi_events
[`TimeSelection.is_looping`]: reapy.core.html#reapy.core.TimeSelection.is_looping
[`TimeSelection.loop`]: reapy.core.html#reapy.core.TimeSelection.loop
[`TimeSelection.looping`]: reapy.core.html#reapy.core.TimeSelection.looping
[`TimeSelection.shift`]: reapy.core.html#reapy.core.TimeSelection.shift
[`TimeSelection.unloop`]: reapy.core.html#reapy.core.TimeSelection.unloop
[`Track.add_item`]: reapy.core.html#reapy.core.Track.add_item
[`Track.add_midi_item`]: reapy.core.html#reapy.core.Track.add_midi_item
[`Track.add_send`]: reapy.core.html#reapy.core.Track.add_send
[`Track.automation_mode`]: reapy.core.html#reapy.core.Track.automation_mode
[`Track.color`]: reapy.core.html#reapy.core.Track.color
[`Track.delete`]: reapy.core.html#reapy.core.Track.delete
[`Track.depth`]: reapy.core.html#reapy.core.Track.depth
[`Track.envelopes`]: reapy.core.html#reapy.core.Track.envelopes
[`Track.instrument`]: reapy.core.html#reapy.core.Track.instrument
[`Track.is_selected`]: reapy.core.html#reapy.core.Track.is_selected
[`Track.items`]: reapy.core.html#reapy.core.Track.items
[`Track.make_only_selected_track`]: reapy.core.html#reapy.core.Track.make_only_selected_track
[`Track.n_envelopes`]: reapy.core.html#reapy.core.Track.n_envelopes
[`Track.n_fxs`]: reapy.core.html#reapy.core.Track.n_fxs
[`Track.n_items`]: reapy.core.html#reapy.core.Track.n_items
[`Track.n_receives`]: reapy.core.html#reapy.core.Track.n_receives
[`Track.n_sends`]: reapy.core.html#reapy.core.Track.n_sends
[`Track.name`]: reapy.core.html#reapy.core.Track.name
[`Track.select`]: reapy.core.html#reapy.core.Track.select
[`Track.unselect`]: reapy.core.html#reapy.core.Track.unselect
[`add_reascript`]: reapy.core.reaper.html#reapy.core.reaper.reaper.add_reascript
[`arm_command`]: reapy.core.reaper.html#reapy.core.reaper.reaper.arm_command
[`at_exit`]: reapy.core.reaper.html#reapy.core.reaper.defer.at_exit
[`audio.get_input_latency`]: reapy.core.reaper.html#reapy.core.reaper.audio.get_input_latency
[`audio.get_input_names`]: reapy.core.reaper.html#reapy.core.reaper.audio.get_input_names
[`audio.get_n_inputs`]: reapy.core.reaper.html#reapy.core.reaper.audio.get_n_inputs
[`audio.get_n_outputs`]: reapy.core.reaper.html#reapy.core.reaper.audio.get_n_outputs
[`audio.get_output_latency`]: reapy.core.reaper.html#reapy.core.reaper.audio.get_output_latency
[`audio.get_output_names`]: reapy.core.reaper.html#reapy.core.reaper.audio.get_output_names
[`audio.init`]: reapy.core.reaper.html#reapy.core.reaper.audio.init
[`audio.is_prebuffer`]: reapy.core.reaper.html#reapy.core.reaper.audio.is_prebuffer
[`audio.is_running`]: reapy.core.reaper.html#reapy.core.reaper.audio.is_running
[`audio.quit`]: reapy.core.reaper.html#reapy.core.reaper.audio.quit
[`clear_console`]: reapy.core.reaper.html#reapy.core.reaper.reaper.clear_console
[`clear_peak_cache`]: reapy.core.reaper.html#reapy.core.reaper.reaper.clear_peak_cache
[`dB_to_slider`]: reapy.core.reaper.html#reapy.core.reaper.reaper.dB_to_slider
[`defer`]: reapy.core.reaper.html#reapy.core.reaper.defer.defer
[`delete_ext_state`]: reapy.core.reaper.html#reapy.core.reaper.reaper.delete_ext_state
[`disarm_command`]: reapy.core.reaper.html#reapy.core.reaper.reaper.disarm_command
[`get_armed_command`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_armed_command
[`get_command_id`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_command_id
[`get_command_name`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_command_name
[`get_exe_dir`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_exe_dir
[`get_ext_state`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_ext_state
[`get_global_automation_mode`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_global_automation_mode
[`get_ini_file`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_ini_file
[`get_last_color_theme_file`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_last_color_theme_file
[`get_last_touched_track`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_last_touched_track
[`get_main_window`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_main_window
[`get_reaper_version`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_reaper_version
[`get_resource_path`]: reapy.core.reaper.html#reapy.core.reaper.reaper.get_resource_path
[`midi.get_active_editor`]: reapy.core.reaper.html#reapy.core.reaper.midi.get_active_editor
[`midi.get_input_names`]: reapy.core.reaper.html#reapy.core.reaper.midi.get_input_names
[`midi.get_max_inputs`]: reapy.core.reaper.html#reapy.core.reaper.midi.get_max_inputs
[`midi.get_max_outputs`]: reapy.core.reaper.html#reapy.core.reaper.midi.get_max_outputs
[`midi.get_n_inputs`]: reapy.core.reaper.html#reapy.core.reaper.midi.get_n_inputs
[`midi.get_n_outputs`]: reapy.core.reaper.html#reapy.core.reaper.midi.get_n_outputs
[`midi.get_output_names`]: reapy.core.reaper.html#reapy.core.reaper.midi.get_output_names
[`midi.reinit`]: reapy.core.reaper.html#reapy.core.reaper.midi.reinit
[`open_project`]: reapy.core.reaper.html#reapy.core.reaper.reaper.open_project
[`os.listdir`]: reapy.core.reaper.html#reapy.core.reaper.os.listdir
[`os.path.isfile`]: reapy.core.reaper.html#reapy.core.reaper.os.path.isfile
[`perform_action`]: reapy.core.reaper.html#reapy.core.reaper.reaper.perform_action
[`print`]: reapy.core.reaper.html#reapy.core.reaper.reaper.print
[`remove_reascript`]: reapy.core.reaper.html#reapy.core.reaper.reaper.remove_reascript
[`rgb_from_native`]: reapy.core.reaper.html#reapy.core.reaper.reaper.rgb_from_native
[`rgb_to_native`]: reapy.core.reaper.html#reapy.core.reaper.reaper.rgb_to_native
[`set_ext_state`]: reapy.core.reaper.html#reapy.core.reaper.reaper.set_ext_state
[`set_global_automation_mode`]: reapy.core.reaper.html#reapy.core.reaper.reaper.set_global_automation_mode
[`show_console_message`]: reapy.core.reaper.html#reapy.core.reaper.reaper.show_console_message
[`show_message_box`]: reapy.core.reaper.html#reapy.core.reaper.reaper.show_message_box
[`slider_to_dB`]: reapy.core.reaper.html#reapy.core.reaper.reaper.slider_to_dB
[`time.time`]: reapy.core.reaper.html#reapy.core.reaper.time.time
[`update_arrange`]: reapy.core.reaper.html#reapy.core.reaper.reaper.update_arrange
[`update_timeline`]: reapy.core.reaper.html#reapy.core.reaper.reaper.update_timeline
[`view_prefs`]: reapy.core.reaper.html#reapy.core.reaper.reaper.view_prefs

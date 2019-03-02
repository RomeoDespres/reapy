# CHANGELOG

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

#### Audio Management

- class [`AudioAccessor`]
- [`Take.add_audio_accessor`], [`Track.add_audio_accessor`]

#### Audio/MIDI Device Management

- [`audio.get_n_inputs`], [`audio.get_n_outputs`]
- [`audio.get_input_latency`], [`audio.get_output_latency`]
- [`audio.get_input_names`], [`audio.get_output_names`]
- [`midi.get_max_inputs`], [`midi.get_max_outputs`]
- [`midi.get_n_inputs`], [`midi.get_n_outputs`]
- [`midi.get_input_names`], [`midi.get_output_names`]

#### Envelope Management

- [`Envelope.parent`]
- [`Envelope.get_value`]
- [`Envelope.get_derivatives`]
- [`FXParam.add_envelope`]
- [`FXParam.envelope`]
- [`Take.envelopes`], [`Track.envelopes`]

#### FX Management

- [`FX.open_chain`], [`FX.close_chain`], [`FX.open_floating_window`], [`FX.close_floating_window`], [`FX.window`]
- [`FXParam.normalized`] for getting and setting normalized param values
- [`FXParam.formatted`], [`FXParam.format_value`], [`NormalizedFXParam.format_value`]
- [`Take.visible_fx`], [`Track.visible_fx`]
- [`Track.fxs`] and [`Take.fxs`] now support negative indexing

#### Item Management

- [`Item.delete`]
- [`Item.update`]
- [`Project.items`]
- [`Take.name`]

#### MIDI Management

- [`Take.is_midi`]
- [`Take.n_cc`], [`Take.n_notes`], [`Take.n_text_sysex`]
- [`Take.select_all_midi_events`], [`Take.unselect_all_midi_events`]
- class [`MIDIEditor`]
- [`midi.reinit`] (reset all MIDI devices)

#### Project Management

- [`open_project`]

#### Track Management

- [`Project.solo_all_tracks`], [`Project.unsolo_all_tracks`]
- [`Track.parent_track`]

#### User Interface

- [`get_last_color_theme_file`]
- [`get_main_window`]

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
[`AutomationItem.delete_points_in_range`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.AutomationItem.delete_points_in_range
[`AutomationItem.length`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.AutomationItem.length
[`AutomationItem.n_points`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.AutomationItem.n_points
[`AutomationItem.pool`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.AutomationItem.pool
[`AutomationItem.position`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.AutomationItem.position
[`Envelope.delete_points_in_range`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Envelope.delete_points_in_range
[`Envelope.get_derivatives`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Envelope.get_derivatives
[`Envelope.get_value`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Envelope.get_value
[`Envelope.n_items`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Envelope.n_items
[`Envelope.n_points`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Envelope.n_points
[`Envelope.name`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Envelope.name
[`Envelope.parent`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Envelope.parent
[`FX.close_chain`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.close_chain
[`FX.close_floating_window`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.close_floating_window
[`FX.close_ui`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.close_ui
[`FX.copy_to_take`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.copy_to_take
[`FX.copy_to_track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.copy_to_track
[`FX.delete`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.delete
[`FX.disable`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.disable
[`FX.enable`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.enable
[`FX.is_enabled`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.is_enabled
[`FX.is_online`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.is_online
[`FX.is_ui_open`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.is_ui_open
[`FX.make_offline`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.make_offline
[`FX.make_online`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.make_online
[`FX.move_to_take`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.move_to_take
[`FX.move_to_track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.move_to_track
[`FX.n_params`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.n_params
[`FX.name`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.name
[`FX.open_chain`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.open_chain
[`FX.open_floating_window`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.open_floating_window
[`FX.open_ui`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.open_ui
[`FX.params`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.params
[`FX.preset_file`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.preset_file
[`FX.preset_index`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.preset_index
[`FX.preset`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.preset
[`FX.use_next_preset`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.use_next_preset
[`FX.use_previous_preset`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.use_previous_preset
[`FX.window`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FX.window
[`FXParam.add_envelope`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FXParam.add_envelope
[`FXParam.envelope`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FXParam.envelope
[`FXParam.format_value`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FXParam.format_value
[`FXParam.formatted`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FXParam.formatted
[`FXParam.name`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FXParam.name
[`FXParam.normalized`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.FXParam.normalized
[`Item.active_take`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.active_take
[`Item.add_take`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.add_take
[`Item.delete`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.delete
[`Item.get_info_value`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.get_info_value
[`Item.get_take`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.get_take
[`Item.is_selected`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.is_selected
[`Item.length`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.length
[`Item.n_takes`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.n_takes
[`Item.position`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.position
[`Item.project`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.project
[`Item.split`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.split
[`Item.takes`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.takes
[`Item.track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.track
[`Item.update`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Item.update
[`MIDIEditor.mode`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.MIDIEditor.mode
[`MIDIEditor.perform_action`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.MIDIEditor.perform_action
[`MIDIEditor.take`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.MIDIEditor.take
[`MIDIEditor`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.MIDIEditor
[`Marker.delete`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Marker.delete
[`Marker`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Marker
[`NormalizedFXParam.format_value`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.NormalizedFXParam.format_value
[`Project.add_marker`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.add_marker
[`Project.add_region`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.add_region
[`Project.add_track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.add_track
[`Project.any_track_solo`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.any_track_solo
[`Project.begin_undo_block`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.begin_undo_block
[`Project.bpi`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.bpi
[`Project.bpm`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.bpm
[`Project.bypass_fx_on_all_tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.bypass_fx_on_all_tracks
[`Project.can_redo`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.can_redo
[`Project.can_undo`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.can_undo
[`Project.cursor_position`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.cursor_position
[`Project.disarm_rec_on_all_tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.disarm_rec_on_all_tracks
[`Project.end_undo_block`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.end_undo_block
[`Project.get_selected_item`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.get_selected_item
[`Project.get_selected_track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.get_selected_track
[`Project.is_dirty`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.is_dirty
[`Project.items`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.items
[`Project.length`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.length
[`Project.make_current_project`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.make_current_project
[`Project.mark_dirty`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.mark_dirty
[`Project.markers`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.markers
[`Project.master_track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.master_track
[`Project.mute_all_tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.mute_all_tracks
[`Project.n_items`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.n_items
[`Project.n_markers`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.n_markers
[`Project.n_regions`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.n_regions
[`Project.n_selected_items`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.n_selected_items
[`Project.n_selected_tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.n_selected_tracks
[`Project.n_tempo_markers`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.n_tempo_markers
[`Project.n_tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.n_tracks
[`Project.name`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.name
[`Project.path`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.path
[`Project.pause`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.pause
[`Project.perform_action`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.perform_action
[`Project.play_rate`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.play_rate
[`Project.play_state`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.play_state
[`Project.play`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.play
[`Project.redo`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.redo
[`Project.regions`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.regions
[`Project.save`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.save
[`Project.select_all_items`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.select_all_items
[`Project.selected_envelope`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.selected_envelope
[`Project.selected_items`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.selected_items
[`Project.selected_tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.selected_tracks
[`Project.solo_all_tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.solo_all_tracks
[`Project.stop`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.stop
[`Project.time_selection`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.time_selection
[`Project.tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.tracks
[`Project.undo`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.undo
[`Project.unmute_all_tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.unmute_all_tracks
[`Project.unsolo_all_tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project.unsolo_all_tracks
[`Project`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Project
[`Region.add_rendered_track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Region.add_rendered_track
[`Region.delete`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Region.delete
[`Region.remove_rendered_track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Region.remove_rendered_track
[`Region.rendered_tracks`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Region.rendered_tracks
[`Region`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Region
[`Send.delete`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Send.delete
[`Send`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Send
[`Source.filename`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Source.filename
[`Source.length`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Source.length
[`Source.n_channels`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Source.n_channels
[`Source.sample_rate`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Source.sample_rate
[`Source.type`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Source.type
[`Take.add_fx`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.add_fx
[`Take.envelopes`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.envelopes
[`Take.get_info_value`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.get_info_value
[`Take.is_midi`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.is_midi
[`Take.item`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.item
[`Take.make_active_take`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.make_active_take
[`Take.n_cc`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.n_cc
[`Take.n_envelopes`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.n_envelopes
[`Take.n_fxs`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.n_fxs
[`Take.n_notes`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.n_notes
[`Take.n_text_sysex`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.n_text_sysex
[`Take.name`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.name
[`Take.select_all_midi_events`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.select_all_midi_events
[`Take.source`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.source
[`Take.track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.track
[`Take.unselect_all_midi_events`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.unselect_all_midi_events
[`Take.visible_fx`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Take.visible_fx
[`TimeSelection.is_looping`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.TimeSelection.is_looping
[`TimeSelection.loop`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.TimeSelection.loop
[`TimeSelection.looping`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.TimeSelection.looping
[`TimeSelection.shift`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.TimeSelection.shift
[`TimeSelection.unloop`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.TimeSelection.unloop
[`Track.add_fx`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.add_fx
[`Track.add_item`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.add_item
[`Track.add_midi_item`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.add_midi_item
[`Track.add_send`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.add_send
[`Track.automation_mode`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.automation_mode
[`Track.color`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.color
[`Track.delete`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.delete
[`Track.depth`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.depth
[`Track.envelopes`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.envelopes
[`Track.instrument`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.instrument
[`Track.is_selected`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.is_selected
[`Track.items`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.items
[`Track.make_only_selected_track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.make_only_selected_track
[`Track.n_envelopes`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.n_envelopes
[`Track.n_fxs`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.n_fxs
[`Track.n_items`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.n_items
[`Track.n_receives`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.n_receives
[`Track.n_sends`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.n_sends
[`Track.name`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.name
[`Track.parent_track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.parent_track
[`Track.select`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.select
[`Track.unselect`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.unselect
[`Track.visible_fx`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.html#reapy.core.Track.visible_fx
[`add_reascript`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.add_reascript
[`arm_command`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.arm_command
[`at_exit`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.defer.at_exit
[`audio.get_input_latency`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.audio.get_input_latency
[`audio.get_input_names`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.audio.get_input_names
[`audio.get_n_inputs`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.audio.get_n_inputs
[`audio.get_n_outputs`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.audio.get_n_outputs
[`audio.get_output_latency`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.audio.get_output_latency
[`audio.get_output_names`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.audio.get_output_names
[`audio.init`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.audio.init
[`audio.is_prebuffer`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.audio.is_prebuffer
[`audio.is_running`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.audio.is_running
[`audio.quit`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.audio.quit
[`clear_console`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.clear_console
[`clear_peak_cache`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.clear_peak_cache
[`dB_to_slider`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.dB_to_slider
[`defer`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.defer.defer
[`delete_ext_state`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.delete_ext_state
[`disarm_command`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.disarm_command
[`get_armed_command`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_armed_command
[`get_command_id`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_command_id
[`get_command_name`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_command_name
[`get_exe_dir`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_exe_dir
[`get_ext_state`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_ext_state
[`get_global_automation_mode`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_global_automation_mode
[`get_ini_file`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_ini_file
[`get_last_color_theme_file`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_last_color_theme_file
[`get_last_touched_track`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_last_touched_track
[`get_main_window`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_main_window
[`get_reaper_version`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_reaper_version
[`get_resource_path`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.get_resource_path
[`midi.get_active_editor`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.midi.get_active_editor
[`midi.get_input_names`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.midi.get_input_names
[`midi.get_max_inputs`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.midi.get_max_inputs
[`midi.get_max_outputs`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.midi.get_max_outputs
[`midi.get_n_inputs`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.midi.get_n_inputs
[`midi.get_n_outputs`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.midi.get_n_outputs
[`midi.get_output_names`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.midi.get_output_names
[`midi.reinit`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.midi.reinit
[`open_project`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.open_project
[`os.listdir`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.os.listdir
[`os.makedirs`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.os.makedirs
[`os.path.isfile`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.os.path.isfile
[`perform_action`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.perform_action
[`print`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.print
[`remove_reascript`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.remove_reascript
[`rgb_from_native`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.rgb_from_native
[`rgb_to_native`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.rgb_to_native
[`set_ext_state`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.set_ext_state
[`set_global_automation_mode`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.set_global_automation_mode
[`show_console_message`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.show_console_message
[`show_message_box`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.show_message_box
[`slider_to_dB`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.slider_to_dB
[`time.time`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.time.time
[`update_arrange`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.update_arrange
[`update_timeline`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.update_timeline
[`view_prefs`]: https://python-reapy.readthedocs.io/en/latest/reapy.core.reaper.html#reapy.core.reaper.reaper.view_prefs

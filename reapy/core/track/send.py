import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.tools import depends_on_sws


class Send(ReapyObject):
    """Track send.

    Attributes
    ----------
    index : int
        position on the track
    is_muted : bool
    is_phase_flipped : bool
    track_id : str
    type : str
        can be 'send', 'hardware' or 'receive'
    """

    _class_name = "Send"

    def __init__(self, track=None, index=0, track_id=None, type="send"):
        if track_id is None:
            message = "One of `track` or `track_id` must be specified."
            assert track is not None, message
            track_id = track.id
        self.index = index
        self.track_id = track_id
        self.type = type

    def _get_int_type(self):
        types = {
            "hardware": 1,
            "send": 0,
            "receive": -1,
        }
        int_type = types[self.type]
        return int_type

    @property
    def _kwargs(self):
        return {
            "index": self.index,
            "track_id": self.track_id,
            "type": self.type
        }

    def delete(self):
        """
        Delete send.
        """
        RPR.RemoveTrackSend(self.track_id, self._get_int_type(), self.index)

    @property
    def dest_track(self):
        """
        Destination track.

        :type: Track
        """
        id_ = self.get_info('P_DESTTRACK')
        return reapy.Track(id_)

    @reapy.inside_reaper()
    def flip_phase(self):
        """
        Toggle whether phase is flipped.
        """
        self.is_phase_flipped = not self.is_phase_flipped

    def get_info(self, param_name):
        """Get raw info from GetTrackSendInfo_Value.

        Parameters
        ----------
        param_name : str
            B_MUTE : bool *
            B_PHASE : bool *, true to flip phase
            B_MONO : bool *
            D_VOL : double *, 1.0 = +0dB etc
            D_PAN : double *, -1..+1
            D_PANLAW : double *,1.0=+0.0db, 0.5=-6dB, -1.0 = projdef etc
            I_SENDMODE : int *, 0=post-fader, 1=pre-fx, 2=post-fx (deprecated),
                                3=post-fx
            I_AUTOMODE : int * : automation mode (-1=use track automode,
                                0=trim/off, 1=read, 2=touch, 3=write, 4=latch)
            I_SRCCHAN : int *, index,&1024=mono, -1 for none
            I_DSTCHAN : int *, index, &1024=mono, otherwise stereo pair,
                                hwout:&512=rearoute
            I_MIDIFLAGS : int *, low 5 bits=source channel 0=all, 1-16,
                                next 5 bits=dest channel, 0=orig,
                                1-16=chan
            P_DESTTRACK : read only, returns MediaTrack *,
                                destination track,
                                only applies for sends/recvs
            P_SRCTRACK : read only, returns MediaTrack *,
                                source track, only applies for sends/recvs
            P_ENV:<envchunkname : read only, returns TrackEnvelope *.
                                Call with :<VOLENV, :<PANENV, etc appended.


        Returns
        -------
        Union[bool, track id(str)]
        """
        value = RPR.GetTrackSendInfo_Value(
            self.track_id, self._get_int_type(), self.index, param_name
        )
        return value

    @depends_on_sws
    def get_sws_info(self, param_name):
        """Raw value from BR_GetSetTrackSendInfo.

        Parameters
        ----------
        param_name : str
            B_MUTE : send mute state (1.0 if muted, otherwise 0.0)
            B_PHASE : send phase state (1.0 if phase is inverted, otherwise 0.0)
            B_MONO : send mono state (1.0 if send is set to mono, otherwise 0.0)
            D_VOL : send volume (1.0=+0dB etc...)
            D_PAN : send pan (-1.0=100%L, 0=center, 1.0=100%R)
            D_PANLAW : send pan law (1.0=+0.0db, 0.5=-6dB,
                        -1.0=project default etc...)
            I_SENDMODE : send mode (0=post-fader, 1=pre-fx, 2=post-fx(deprecated),
                        3=post-fx)
            I_SRCCHAN : audio source starting channel index or -1 if audio send
                        is disabled (&1024=mono...note that in that case, when
                        reading index, you should do (index XOR 1024) to get
                        starting channel index)
            I_DSTCHAN : audio destination starting channel index (&1024=mono
                        (and in case of hardware output &512=rearoute)...
                        note that in that case, when reading index, you should do
                        (index XOR (1024 OR 512)) to get starting channel index)
            I_MIDI_SRCCHAN : source MIDI channel, -1 if MIDI send is disabled
                            (0=all, 1-16)
            I_MIDI_DSTCHAN : destination MIDI channel, -1 if MIDI send is disabled
                            (0=original, 1-16)
            I_MIDI_SRCBUS : source MIDI bus, -1 if MIDI send is disabled
                            (0=all, otherwise bus index)
            I_MIDI_DSTBUS : receive MIDI bus, -1 if MIDI send is disabled
                            (0=all, otherwise bus index)
            I_MIDI_LINK_VOLPAN : link volume/pan controls to MIDI

        Returns
        -------
        float
        """
        value = RPR.BR_GetSetTrackSendInfo(
            self.track_id, self._get_int_type(), self.index, param_name, False,
            0.0
        )
        return value

    @property
    def is_mono(self):
        """
        Whether send is mono or stereo.

        :type: bool
        """
        is_mono = bool(self.get_info("B_MONO"))
        return is_mono

    @is_mono.setter
    def is_mono(self, mono):
        self.set_info("B_MONO", mono)

    @property
    def is_muted(self):
        """
        Whether send is muted.

        :type: bool
        """
        is_muted = bool(self.get_info("B_MUTE"))
        return is_muted

    @is_muted.setter
    def is_muted(self, is_muted):
        """
        Mute or unmute send.

        Parameters
        ----------
        is_muted : bool
            Whether to mute or unmute send.
        """
        self.set_info("B_MUTE", is_muted)

    @property
    def is_phase_flipped(self):
        """
        Whether send phase is flipped (i.e. signal multiplied by -1).

        :type: bool
        """
        is_phase_flipped = bool(self.get_info("B_PHASE"))
        return is_phase_flipped

    @is_phase_flipped.setter
    def is_phase_flipped(self, flipped):
        self.set_info("B_PHASE", flipped)

    @property
    @depends_on_sws
    def midi_source(self):
        """
        Send MIDI properties on the send track.

        Returns
        -------
        Tuple[int bus, int channel]
        """
        retval = []
        with reapy.inside_reaper():
            for par in ('I_MIDI_SRCBUS', 'I_MIDI_SRCCHAN'):
                retval.append(int(self.get_sws_info(par)))
        return tuple(retval)

    @midi_source.setter
    def midi_source(self, value):
        with reapy.inside_reaper():
            for par, val in zip(('I_MIDI_SRCBUS', 'I_MIDI_SRCCHAN'), value):
                self.set_info_br(par, val)

    @property
    @depends_on_sws
    def midi_dest(self):
        """
        Send MIDI properties on the destination track.

        Returns
        -------
        Tuple[int bus, int channel]
        """
        retval = []
        with reapy.inside_reaper():
            for par in ('I_MIDI_DSTBUS', 'I_MIDI_DSTCHAN'):
                retval.append(int(self.get_sws_info(par)))
        return tuple(retval)

    @midi_dest.setter
    def midi_dest(self, value):
        with reapy.inside_reaper():
            for par, val in zip(('I_MIDI_DSTBUS', 'I_MIDI_DSTCHAN'), value):
                self.set_info_br(par, val)

    def mute(self):
        """
        Mute send.
        """
        self.is_muted = True

    @property
    def pan(self):
        """
        Send pan (from -1=left to 1=right).

        :type: float
        """
        pan = self.get_info("D_PAN")
        return pan

    @pan.setter
    def pan(self, pan):
        """
        Set send pan.

        Parameters
        ----------
        pan : float
            New pan between -1 (left) and 1 (right).
        """
        self.set_info("D_PAN", pan)

    def set_info(self, param_name, value):
        RPR.SetTrackSendInfo_Value(
            self.track_id, self._get_int_type(), self.index, param_name, value
        )

    @depends_on_sws
    def set_sws_info(self, param_name, value):
        RPR.BR_GetSetTrackSendInfo(
            self.track_id, self._get_int_type(), self.index, param_name, True,
            value
        )

    @property
    @depends_on_sws
    def source_track(self):
        """
        Source track.

        :type: Track
        """
        id_ = self.get_info('P_SRCTRACK')
        print('(MediaTrack*)0x{0:0{1}X}'.format(int(id_), 16), id_)
        id2 = RPR.BR_GetMediaTrackSendInfo_Track(
            self.track_id, self._get_int_type(), self.index, 0
        )
        print(id2)
        return reapy.Track(id_)

    def unmute(self):
        """
        Unmute send.
        """
        self.is_muted = False

    @property
    def volume(self):
        """
        Send volume.

        :type: float
        """
        volume = self.get_info("D_VOL")
        return volume

    @volume.setter
    def volume(self, volume):
        self.set_info("D_VOL", volume)

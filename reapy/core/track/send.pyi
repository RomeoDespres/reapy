import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
import typing as ty


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
    index: int
    track_id: ty.Union[str, int]
    type: str

    def __init__(self,
                 track: ty.Optional[reapy.Track] = None,
                 index: int = 0,
                 track_id: ty.Optional[ty.Union[str, int]] = None,
                 type: str = "send") -> None:
        ...

    def _get_int_type(self) -> int:
        ...

    @property
    def _kwargs(self) -> ty.Dict[str, object]:
        ...

    def delete(self) -> None:
        """
        Delete send.
        """
        ...

    @reapy.inside_reaper()
    def flip_phase(self) -> None:
        """
        Toggle whether phase is flipped.
        """
        ...

    def get_info(self, param_name: str) -> float:
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
                                1-16=chanP_DESTTRACK : read only, 
                                returns MediaTrack *,
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
        ...

    def get_info_br(self, param_name: str) -> float:

        ...

    @property
    def is_mono(self) -> bool:
        """
        Whether send is mono or stereo.

        :type: bool
        """
        ...

    @is_mono.setter
    def is_mono(self, mono: bool) -> None:
        ...

    @property
    def is_muted(self) -> bool:
        """
        Whether send is muted.

        :type: bool
        """
        ...

    @is_muted.setter
    def is_muted(self, is_muted: bool) -> None:
        """
        Mute or unmute send.

        Parameters
        ----------
        is_muted : bool
            Whether to mute or unmute send.
        """
        ...

    @property
    def is_phase_flipped(self) -> bool:
        """
        Whether send phase is flipped (i.e. signal multiplied by -1).

        :type: bool
        """
        ...

    @is_phase_flipped.setter
    def is_phase_flipped(self, flipped: bool) -> None:
        ...

    def mute(self) -> None:
        """
        Mute send.
        """
        ...

    @property
    def midi_source(self) -> ty.Tuple[int, int]:
        """
        Send MIDI properties on the send track.

        Returns
        -------
        List[int bus, int channel]
        """
        ...

    @midi_source.setter
    def midi_source(self, value: ty.Tuple[int, int]) -> None: ...

    @property
    def midi_dest(self) -> ty.Tuple[int, int]:
        """
        Send MIDI properties on the send track.

        Returns
        -------
        List[int bus, int channel]
        """
        ...

    @midi_dest.setter
    def midi_dest(self, value: ty.Tuple[int, int]) -> None: ...

    @property
    def pan(self) -> float:
        """
        Send pan (from -1=left to 1=right).

        :type: float
        """
        ...

    @pan.setter
    def pan(self, pan: float) -> None:
        """
        Set send pan.

        Parameters
        ----------
        pan : float
            New pan between -1 (left) and 1 (right).
        """
        ...

    def set_info(self, param_name: str, value: float) -> None:
        ...

    def set_info_br(self, param_name: str, value: float) -> None:
        ...

    @property
    def source_track(self) -> reapy.Track:
        """
        Source track.

        :type: Track
        """
        ...

    def unmute(self) -> None:
        """
        Unmute send.
        """
        ...

    @property
    def volume(self) -> float:
        """
        Send volume.

        :type: float
        """
        ...

    @volume.setter
    def volume(self, volume: float) -> None:
        ...

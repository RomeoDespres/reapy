from reapy import reascript_api as RPR

class Send:

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
            "send": 0
        }
        int_type = types[self.type]
        return int_type
    
    def _to_dict(self):
        return {
                "__reapy__": True,
                "class": "Send",
                "args": (),
                "kwargs": {
                    "index": self.index,
                    "track_id": self.track_id,
                    "type": self.type
                }
            }
    
    def delete(self):
        """
        Delete send.
        """
        RPR.RemoveTrackSend(self.track_id, self._get_int_type(), self.index)
from reapy import reascript_api as RPR

class Send:

    def __init__(self, track=None, index=0, track_id=None):
        if track_id is None:
            message = "One of `track` or `track_id` must be specified."
            assert track is not None, message
            track_id = track.id
        self.index = index
        self.track_id = track_id
    
    def _to_dict(self):
        return {
                "__reapy__": True,
                "class": "Send",
                "args": (),
                "kwargs": {
                    "index": self.index, "track_id": self.track_id
                }
            }
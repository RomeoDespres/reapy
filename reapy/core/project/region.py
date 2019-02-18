from reapy import reascript_api as RPR

class Region:

    def __init__(
        self, parent_project=None, index=None, parent_project_id=None
    ):
        if parent_project_id is None:
            message = (
                "One of `parent_project` or `parent_project_id` must be "
                "specified."
            )
            assert parent_project is not None, message
            parent_project_id = parent_project.id
        self.project_id = parent_project_id
        self.index = index
        
    def _to_dict(self):
        return {
            "__reapy__": True,
            "class": "Region",
            "args": (),
            "kwargs": {
                "index": self.index, "parent_project_id": self.envelope_id
            }
        }
        
    def delete(self):
        """
        Delete region.
        """
        RPR.DeleteProjectMarker(self.project_id, self.index, True)
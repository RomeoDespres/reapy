from pathlib import Path
import reapy

def validate_path(path:str, ext:str=None, isFolder:bool=False) -> str:
    """
        Check if a file or folder exists

        Parameters
        ----------
        path : str
            Path to the file or folder (relative to the REAPER project)
        ext : str
            The file extension required. If it doesn't match the actual file, it will raise
        isFolder : bool, optional
            Search for a folder instead of a file

        Returns
        -------
        fullPath_str : str
            The path to the file or folder.
    """
    ...
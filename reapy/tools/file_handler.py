from pathlib import Path
import reapy


def validate_path(path, ext=None, isFolder=False):
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
    curProject          = reapy.Project()
    curProjectFolder    = Path(curProject.path)
    fullPath            = curProjectFolder / path
    fullPath_str        = fullPath.as_posix()
   #check if folder exists
    if isFolder:
        valid = fullPath.is_dir()
        if not valid : raise NotADirectoryError(fullPath_str)
    #check if file exists
    else:
        valid = fullPath.is_file()
        if not valid : raise IsADirectoryError(fullPath_str)
        #validate extension
        if ext:
            valid = True if fullPath.suffix == ext else False
            if not valid : raise TypeError(f'"{fullPath_str}" file extension must be "{ext}" ')
            pass
    
    if not valid :
        raise FileNotFoundError(fullPath_str)
    
    return fullPath_str
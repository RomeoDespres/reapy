from pathlib import Path
import reapy

#based on : http://reaper.fm/about.php#technical
READABLE_FORMATS = ['.acid','.aiff', '.avi', 'bwf', '.cda', '.edl', '.flac', '.kar', '.midi', '.mid', '.mogg', '.mov', '.mp3', '.mp4', '.m4p', '.m4v', '.mpeg' ,'.ogg', '.ogv', '.mov', '.bwav', '.rx2', '.syx', '.w64', '.wav', '.wave', '.wv', '.wmv']

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

        file_ext = fullPath.suffix.lower()
        if file_ext not in READABLE_FORMATS : raise TypeError(f'"{fullPath_str}" file type "{file_ext}" is not supported by REAPER')
        #validate extension
        if ext:
            valid = True if file_ext == ext.lower() else False
            if not valid : raise TypeError(f'"{fullPath_str}" file extension must be "{ext}" ')
            pass
    
    if not valid :
        raise FileNotFoundError(fullPath_str)
    
    return fullPath_str
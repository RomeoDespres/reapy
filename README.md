# reapy

`reapy` is a nice pythonic wrapper around the quite unpythonic [ReaScript Python API](https://www.reaper.fm/sdk/reascript/reascripthelp.html#p "ReaScript Python API documentation") for [REAPER](https://www.reaper.fm/ "REAPER").

## Getting Started

### Installing

1. First install from `pip`:

```
pip install python-reapy
```
2. Enable from REAPER.


### `reapy` from inside

Import `reapy` and use it instead of `reaper_python` in your ReaScripts.

```python
from reapy import CURRENT_PROJECT as project
project.print("Hello from inside, world!")
```

This Hello World is equivalent to the following.

```python
from reaper_python import *
RPR_ShowConsoleMsg("Hello from inside, world!")
```

### `reapy` from outside

To use `reapy` from outside REAPER, you need to load and execute the ReaScript [enable_reapy.py](reapy/reascript_api/dist_api/enable_reapy.py). It sets up a local server inside REAPER. Every import of `reapy` outside REAPER will become a client of this server and request ReaScript API calls from it.

Then you can use `reapy` as any other Python module in your projects, and interact with REAPER from outside.

```python
from reapy import CURRENT_PROJECT as project
project.print("Hello from outside, world!")
```
## Usage

### ReaScript API

All ReaScript API functions are available in `reapy` in the sub-module `reapy.reascript_api`. Note that in ReaScript Python API, all function names start with `"RPR_"`. That unnecessary pseudo-namespace has been removed in `reapy`. Thus, you shall call `reapy.reascript_api.GetCursorPosition` in order to trigger `reaper_python.RPR_GetCursorPosition`. See example below.

```python
>>> from reapy import reascript_api as RPR
>>> RPR.GetCursorPosition()
0.0
>>> RPR.SetEditCurPos(1, True, True)
>>> RPR.GetCursorPosition()
1.0
```
### `reapy` API

The purpose of `reapy` is to provide a more pythonic API as a substitute for ReaScript API. Below is the `reapy` way of executing the example above.

```python
>>> from reapy import CURRENT_PROJECT as project
>>> project.cursor_position
0.0
>>> project.cursor_position = 1
>>> project.cursor_position
1.0
```
The table [api.csv](docs/api.csv) matches ReaScript functions with their `reapy` counterparts.

## Author

* **Roméo Després** - *Initial work* - [RomeoDespres](https://github.com/RomeoDespres)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.


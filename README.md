# reapy

`reapy` is a nice pythonic wrapper around the quite unpythonic [ReaScript Python API](https://www.reaper.fm/sdk/reascript/reascripthelp.html#p "ReaScript Python API documentation") for [REAPER](https://www.reaper.fm/ "REAPER").

## Contents

1. [Installation](#installation)
2. [Usage](#usage)
    * [ReaScript API](#reascript-api)
    * [`reapy` API](#reapy-api)
    * [Performance](#performance)
    * [Documentation](#documentation)
3. [Contributing](#contributing)
4. [Author](#author)
5. [License](#license)

## Installation

1. First install from `pip`:

```
pip install python-reapy
```

2. Run:

```
python -m reapy
```

Paths to your Python DLL and to `reapy` configuration scripts get printed.

3. If you haven't enabled Python in REAPER yet, go to *Options > Preferences... > Plug-ins > ReaScript*. Check *Enable Python for use with ReaScript*, and fill *Custom path to Python dll directory* and *Force ReaScript to use specific Python .dll* with the directory path and the file name of the Python DLL.

4. Enable `reapy` dist API by running the corresponding ReaScript (*Actions > Show action list > Reascript : Load...* and browse for the script path).

You're all set! You can now import `reapy` from inside or outside REAPER as any standard Python module.

Instead of creating a new ReaScript containing:

```python
from reaper_python import *
RPR_ShowConsoleMsg("Hello world!")
```

you can open your usual Python shell and type:

```python
>>> import reapy
>>> reapy.print("Hello world!")
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

Note that if you have the [SWS extension](http://sws-extension.org/) installed, the additional ReaScript functions it provides will be available in `reapy.reascript_api` and usable inside and outside REAPER as well.

### `reapy` API

The purpose of `reapy` is to provide a more pythonic API as a substitute for ReaScript API. Below is the `reapy` way of executing the example above.

```python
>>> import reapy
>>> project = reapy.Project() # Current project
>>> project.cursor_position
0.0
>>> project.cursor_position = 1
>>> project.cursor_position
1.0
```
The [translation table](https://python-reapy.readthedocs.io/en/latest/api_table.html) matches ReaScript functions with their `reapy` counterparts.

### Performance

When used from inside REAPER, `reapy` has almost identical performance than native ReaScript API. Yet when it is used from the outside, the performance is quite worse. More precisely, since external API calls are processed in a `defer` loop inside REAPER, there can only be around 30 to 60 of them per second. In a time-critical context, you should make use of the `reapy.inside_reaper` context manager.

```python
>>> import reapy
>>> project = reapy.Project() # Current project
>>> # Unefficient (and useless) call
>>> bpms = [project.bpm for _ in range(1000)] # Takes at least 30 seconds...
>>> # Efficient call
>>> with reapy.inside_reaper():
...     bpms = [project.bpm for _ in range(1000)]
...
>>> # Takes only 0.1 second!
    
```

While `reapt.inside_reaper` saves time on defered calls, performance outside REAPER can be increased within method `map` which exsists on every notable `reapy` object. Within `object.map("method_name", iterables={"arg_name":[<list of values>]}, defaults{"def_arg_name":value})` performance can be insreased with saving on socket connections between outside and inside scripts.

```python
import reapy
take = reapy.Project().selected_items[0].active_take

@reapy.inside_reaper()
def test():
    for i in [6.0] * 1000000:
        take.time_to_ppq(6.0)

def test_map():
    take.map('time_to_ppq', iterables={'time': [6.0] * 1000000})

test()      # runs 140s
test_map()  # runs 12s as from outside as from inside
```

### Documentation

Check the [documentation](https://python-reapy.readthedocs.io/ "reapy online documentation") and especially the [API guide](https://python-reapy.readthedocs.io/en/latest/api_guide.html) and [Translation Table](https://python-reapy.readthedocs.io/en/latest/api_table.html) for more information.

## Contributing

For now, about a half of ReaScript API has a `reapy` counterpart, the docs are far from great, and many bugs are waiting to be found. Feel free to improve the project by checking the [contribution guide](CONTRIBUTING.md)!

## Author

**Roméo Després** - [RomeoDespres](https://github.com/RomeoDespres)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.



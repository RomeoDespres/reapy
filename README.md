# reapy

`reapy` is a nice pythonic wrapper around the terribly non-pythonic [ReaScript Python API](https://www.reaper.fm/sdk/reascript/reascripthelp.html#p "ReaScript Python API documentation") for [REAPER](https://www.reaper.fm/ "REAPER").

## Getting Started

### Installing

No installer is available yet. Note that to use `reapy` from outside REAPER, you need to load and execute the ReaScript [reapy/reascript_api/dist_api/enable_reapy.py](reapy/reascript_api/dist_api/enable_reapy.py).

Then from anywhere (i.e. inside or outside REAPER) you can run the following:

```python
>>> from reapy import CURRENT_PROJECT as project
>>> project.cursor_position
0.0
>>> from reapy import reascript_api as RPR
>>> RPR.GetCursorPosition()
0.0
>>> 
```

## Author

* **Roméo Després** - *Initial work* - [RomeoDespres](https://github.com/RomeoDespres)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.


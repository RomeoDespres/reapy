"""
Define base Program class.

Notes
-----
Runing ``from reapy.tools import Program`` only imports this
``Program`` class if called from inside REAPER. If not, then the
subclass ``reapy.tools.dist_program.Program``, which overrides
``Program.run``, is imported.
"""
import importlib

import reapy
from reapy import reascript_api as RPR


class ModuleFunctionsCache(dict):
    """Caching dict-like class that lazily resolves function/method in module.
    """

    def __init__(self, module, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__module__ = module

    def __missing__(self, func_name):
        func = eval(func_name, self.__module__.__dict__)
        self[func_name] = func
        return func


class FunctionsCache(dict):
    """Caching dict-like class that imports module lazily on demand
        and stores
    """

    def __missing__(self, module_name):
        module = importlib.import_module(module_name)
        self[module_name] = ModuleFunctionsCache(module)
        return self[module_name]


_FUNCTIONS_CACHE = FunctionsCache()


class Program:

    _func = None

    def __init__(self, code, *output):
        """
        Build program.

        Parameters
        ----------
        code : str or function object or tuple of two strings
            Code to execute. Note that if all lines except the empty first ones
            have constant indentation, this indentation is removed (allows for
            docstring code).
            Can only be a function object if wrapped with Program.run_inside
            and then called outside.
            Can only be a tuple of strings if received from external code.
        output : iterable (contains strings or single None)
            Variable names for which values at the end of the program are
            returned after execution.
            If output contains single value which is None it means external code
                wants to create Program instance with link to reapy function
        """
        if output and output[-1] is None:
            # it is a Program instance created in Program.run_inside decorator
            # otherwise output would be empty or first name would be not None
            self._code = self.parse_func(code)
        else:
            self._code = self.parse_code(code)
        self._output = tuple(output)

    def to_dict(self):
        """
        Return dict representation of program.

        Returns
        -------
        rep : dict
            dict representation of program. A new program with same state can
            be created from `rep` with `Program(**rep)`.
        """
        return (self._code,) + self._output

    def parse_func(self, func_obj):
        if type(func_obj) in (list, tuple):
            # got link to reapy function from outside, let's find it to use
            module_name, func_qualname = func_obj
            self._func = _FUNCTIONS_CACHE[module_name][func_qualname]
        else:
            # got func in external code, need to encode it to send to Reaper
            return func_obj.__module__, func_obj.__qualname__

    def parse_code(self, code):
        """
        Return code with correct indentation.

        Parameters
        ----------
        code : str
            Code to be parsed.

        Returns
        -------
        code : str
            Parsed code.
        """
        code = code.replace("\t", " "*4)
        lines = code.split("\n")
        while lines[0] == "":
            lines.pop(0)
        indentation = len(lines[0]) - len(lines[0].lstrip(" "))
        lines = [line[indentation:] for line in lines]
        code = "\n".join(lines)
        return code

    def run(self, **input):
        """
        Run program and return output.

        Parameters
        ----------
        input : dict
            Dictionary with variable names as keys variables values as values.
            Passed as input to the program when running.

            If program was created within Program.run_inside decorator
            then input is {'args': args_tuple, 'kwargs': kwargs_dict}

        Returns
        -------
        output : tuple
            Output values.
        """
        if self._func is not None:
            # func wrapped with Program.run_inside and called from external code
            return self._func(*input['args'], **input['kwargs'])

        input.update({"RPR": RPR, "reapy": reapy})
        exec(self._code, input)
        output = tuple(input[o] for o in self._output)
        return output

    @staticmethod
    def run_inside(func):
        return func

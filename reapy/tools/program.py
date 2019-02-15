import reapy


class Program:
    
    def __init__(self, code, *output):
        """
        Build program.
        
        Parameters
        ----------
        code : str
            Code to execute. Note that if all lines except the empty first ones
            have constant indentation, this indentation is removed (allows for
            docstring code).
        input : dict
            Dictionary with variable names as keys variables values as values.
            Passed as input to the program when running.
        output : iterable of str
            Variable names for which values at the end of the program are
            returned after execution.
        """
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
        
        Returns
        -------
        output : tuple
            Output values.
        """
        input.update({"RPR": RPR, "reapy": reapy})
        exec(self._code, input)
        output = tuple(input[o] for o in self._output)
        return output
        
        
from reapy import reascript_api as RPR
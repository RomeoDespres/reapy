import re
import textwrap
import typing as ty
import builtins
import json
import platform as plt
import os
import requests
import typing_extensions as te


def get_header_contents() -> str:
    """
    Get js_ReaScriptAPI header from GitHub as raw string.

    Returns
    -------
    str
    """
    root_raw = 'https://raw.githubusercontent.com/'
    header = (
        'juliansader/ReaExtensions/master/js_ReaScriptAPI/' +
        'Source%20code/js_ReaScriptAPI_def.h'
    )
    r = requests.get("{}{}".format(root_raw, header))
    return r.content.decode()


def write_binary_file(target_dir: str) -> None:
    """
    Get binary extension file from GitHub.

    Parameters
    ----------
    target_dir : str
        target directory path, usually:
        "{}{}{}".format(reapy.get_resource_path, os.sep, UserPlugins)
    """
    root_api = 'https://api.github.com/repos/'
    repo = 'juliansader/ReaExtensions/contents/js_ReaScriptAPI/'
    url = "%s%s" % (root_api, repo)
    r = requests.get(url)
    tree = json.loads(r.content)
    name = ''
    for item in tree:
        if item['name'] > name:
            name = item['name']
            bindir = item

    r = requests.get(bindir['_links']['self'])
    tree = json.loads(r.content)

    ext_need = {
        ('Linux', '64bit'): '.so',
        ('Windows', '64bit'): '64.dll',
        ('Windows', '32bit'): '32.dll',
        ('Darwin', '64bit'): '64.dylib',
        ('Darwin', '32bit'): '32.dylib',
    }
    ext_real = plt.system(), plt.architecture()[0]

    for item in tree:
        if item['name'].endswith(ext_need[ext_real]):
            bin_url = item['download_url']
            bin_name = item['name']
    r = requests.get(bin_url)

    with open(
        os.path.normpath("%s%s%s" % (target_dir, os.sep, bin_name)), 'wb'
    ) as f:
        f.write(r.content)


ArgsT = ty.Dict[str, str]

FuncdefT = te.TypedDict(
    'FuncdefT', {
        'name': str,
        'return': str,
        'doc': str,
        'args': ArgsT
    }
)


class Parcer:
    """Parces cpp header of js_ReaScriptExtensions.

    Attributes
    ----------
    defs : List[FuncdefT]
        list of parced function defs
    """

    def __init__(
        self,
        file: ty.Optional[str] = None,
        raw_str: ty.Optional[str] = None
    ) -> None:
        self._re_line = re.compile(r'(?!//).*{ APIFUNC\(.+')
        self._re_parce_line = re.compile(r'".*?"')
        self._re_sub = re.compile(r'[\s\{\}]')
        self._re_sub_q = re.compile(r'\\"')
        self._re_name = re.compile(r'.*APIFUNC\((.+?)\)')
        self.types_str: ty.Set[str] = set()
        if file is not None:
            with open(file) as f:
                self.defs = self._parce(f.readlines())
        if raw_str is not None:
            self.defs = self._parce(raw_str.splitlines())

    def _parce(self, lines: ty.List[str]) -> ty.List[FuncdefT]:
        defs = []
        for line in lines:
            line = line.strip()
            if re.match(self._re_line, line):
                defs.append(self._parce_line(line))
        return defs

    def _parce_line(self, line: str) -> FuncdefT:
        line = self._re_sub_q.sub("'", line)
        m = self._re_parce_line.findall(line)
        ret, types, names, doc = m
        doc = re.sub(r'\\n', '\n', doc)
        out: FuncdefT = {}  # type:ignore
        name = self._re_name.match(line).group(1)  # type:ignore

        out['name'] = name
        out['return'] = ret[1:-1]
        out['args'] = {}
        self.types_str.add(out['return'])
        for type_, name in zip(types[1:-1].split(','), names[1:-1].split(',')):
            if type_ == '':
                continue
            type_ = type_.replace('const ', '')
            name = re.sub(r'[\(\)]', '', name)
            if name in builtins.__dict__:
                name += '_'
            out['args'][name] = type_
            self.types_str.add(type_)
        out['doc'] = doc[1:-1]
        # if name == "JS_Window_GetRect":
        # print(out)

        # print(out)
        return out


TypeDefT = te.TypedDict(
    'TypeDefT', {
        'def': str,
        'ref': str,
        'prot': str,
        'call': str,
        'ret': str,
        'default': str,
    }
)

_types_to_match: ty.Dict[str, TypeDefT] = {
    'ptr':
        {
            'def': '{type_}',
            'ref': 'ct.c_uint64',
            'prot': '',
            'call': 'packp("{type_}", str({arg}))',
            'ret': 'Pointer(unpackp("{type_}", ret), "{type_}")',
            'default': '',
        },
    'void*':
        {
            'def': 'VoidPtr',
            # 'ref': 'ct.c_uint64',
            'ref': 'ct.c_void_p',
            'prot': '',
            'call': 'packp("void*", str({arg}))',
            'ret': 'VoidPtr(unpackp("void*", ret))',
            'default': '',
        },
    'void':  # noob formatting comment
        {
            'def': 'None',
            'ref': 'None',
            'prot': '',
            'call': '',
            'ret': '',
            'default': '',
        },
    'double*':
        {
            'def': 'float',
            'ref': 'ct.c_void_p',
            'prot': 'prot_{arg} = ct.c_double({val})',
            'call': 'ct.byref(prot_{arg})',
            'ret': 'float(prot_{arg}.value)',
            'default': '1.0',
        },
    'int*':
        {
            'def': 'int',
            'ref': 'ct.c_void_p',
            'prot': 'prot_{arg} = ct.c_int({val})',
            'call': 'ct.byref(prot_{arg})',
            'ret': 'prot_{arg}.value',
            'default': '1',
        },
    'bool*':
        {
            'def': 'bool',
            'ref': 'ct.c_void_p',
            'prot': 'prot_{arg} = ct.c_byte({val})',
            'call': 'ct.byref(prot_{arg})',
            'ret': 'bool(prot_{arg}.value)',
            'default': 'False',
        },
    'char*':
        {
            'def': 'str',
            'ref': 'ct.c_char_p',
            'prot':
                ('prot_{arg} = packs_l({arg}, size=len({arg}.encode(encoding))'
                    ', encoding=encoding)'),
            'call': 'prot_{arg}',
            'ret': 'unpacks_l(prot_{arg}, want_raw=want_raw)',
            'default': 'prot_{arg} = packs_l("", size={size}, encoding=encoding)',
        },
    'double':
        {
            'def': 'float',
            'ref': 'ct.c_double',
            'prot': '',
            'call': 'ct.c_double({arg})',
            'ret': 'float({arg})',
            'default': '',
        },
    'int':
        {
            'def': 'int',
            'ref': 'ct.c_int',
            'prot': '',
            'call': 'ct.c_int({arg})',
            'ret': 'int({arg})',
            'default': '',
        },
    'bool':
        {
            'def': 'bool',
            'ref': 'ct.c_byte',
            'prot': '',
            'call': 'ct.c_byte({arg})',
            'ret': 'bool({arg})',
            'default': '',
        },
    'char':
        {
            'def': 'bytes',
            'ref': 'ct.c_char',
            'prot': '',
            'call': 'ct.c_char({arg})',
            'ret': 'bytes({arg})',
            'default': '',
        },
}

_def_templ = """
@reapy.inside_reaper()
def {def_name}({def_args}) -> {def_ret}:
    \"""
    {doc}

    Returns
    -------
    {doc_ret}
    \"""
    a = _ft['{api_name}']
    f = ct.CFUNCTYPE({ref_ret}, {ref_args})(a)
    {prot_args}
    ret = f({call_args})
    return {ret_full}
"""

_class_def_templ = """
class {type_}(Pointer):
    pass
"""

_module_templ = \
    """\"\"\"Autogenerated API for ReaExtensions by Julian Sader.

Repo on GitHub: https://github.com/juliansader/ReaExtensions
Theme on ReaperForums: https://forum.cockos.com/showthread.php?t=212174
\"\"\"

import typing as ty
import reapy
import ctypes as ct
from reapy.core import ReapyObject
if reapy.is_inside_reaper():
    from reapy.additional_api import packp, unpackp, packs_l, unpacks_l
    from reaper_python import _ft
else:
    from reapy.additional_api import packp, unpackp

MAX_STRBUF = 4 * 1024 * 1024

__all__: ty.List[str] = [
    {all_}
]


class Pointer(ReapyObject):

    def __init__(
        self, ptr: ty.Union[str, int], ptr_str: str = "void*"
    ) -> None:
        self.__args = ptr, ptr_str
        if isinstance(ptr, str):
            self._str = ptr
            self._int = packp(ptr_str, ptr)
            return
        if isinstance(ptr, int):
            self._str = unpackp(ptr_str, ptr)
            self._int = ptr
            return
        raise TypeError("expect int or str, passed %s" % ptr)

    @property
    def _args(self) -> ty.Tuple[ty.Union[str, int], str]:
        return self.__args

    def __str__(self) -> str:
        return self._str

    def __int__(self) -> int:
        return self._int

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (str, Pointer)):
            return self._str == other
        if isinstance(other, int):
            return self._int == other
        return False

    def __hash__(self) -> int:
        return int(self)


class VoidPtr(Pointer):
    pass

{class_defs}

{defs}
"""


class FuncBuilder:
    """Builds API as python code.

    Attributes
    ----------
    matched_types : Dict[str, TypeDefT]
        matched ctypes to python types, considering their definitions
    parcer : Parcer
    """

    def __init__(self, parcer: Parcer) -> None:
        self.parcer = parcer
        self._re_ptr = re.compile(r'[A-Z].+\*')
        self.all: ty.List[str] = ["Pointer", "VoidPtr"]
        self.matched_types = self._match_types()

    def _match_types(self) -> ty.Dict[str, TypeDefT]:
        out: ty.Dict[str, TypeDefT] = {}
        for type_ in self.parcer.types_str:
            if type_ in _types_to_match:
                out[type_] = _types_to_match[type_]
                continue
            if self._re_ptr.match(type_):
                out[type_] = _types_to_match['ptr']
                self.all.append(type_[:-1])
                continue
            raise TypeError('Cannot match {}'.format(type_))
        return out

    def _match_def_args(
        self, args: ty.Dict[str, str], out_names: ty.List[str],
        opt_names: ty.List[str], opt_defs: ty.List[str]
    ) -> str:
        defs = {}
        kwargs = {}
        types = set()
        for a, t in args.items():
            matched_t = self.matched_types[t]['def']
            types.add(matched_t)
            if a in out_names:
                if matched_t == 'str':
                    kwargs['want_raw'] = 'bool=False'
                continue
            if a in opt_names:
                odct = opt_defs.pop(0).split(':')
                # print(opt_defs_c)
                defs[odct[0]] = odct[1]
                continue
            defs[a] = matched_t.format(type_=t[:-1])
        if 'str' in types:
            kwargs['encoding'] = 'str="utf-8"'
        defs.update(kwargs)
        return ', '.join(
            '{arg}: {type_}'.format(arg=a, type_=t) for a, t in defs.items()
        )

    def _match_def_ret(
        self, ret: str, args: ty.Dict[str, str], out_names: ty.List[str]
    ) -> str:
        base = self.matched_types[ret]['def'].format(type_=ret).strip('*')
        if not out_names:
            return base
        total_names = out_names
        if base == 'None' and len(total_names) == 1:
            return self.matched_types[args[total_names[0]]]['def']
        if base != 'None':
            out = 'ty.Tuple[{ret}, {args}]'
        else:
            out = 'ty.Tuple[{args}]'
        return out.format(
            ret=base.format(type_=ret[:-1]),
            args=', '.join(
                self.matched_types[args[n]]['def'].format(type_=args[n][:-1])
                for n in total_names
            )
        )

    def _match_call_args(
        self, args: ty.Dict[str, str], opt_names: ty.List[str],
        out_names: ty.List[str], opt_calls: ty.List[str],
        out_calls: ty.List[str]
    ) -> ty.Tuple[ty.List[str], str]:
        """
        Returns
        -------
        Tuple[List[str], str]
            prototype defs, calls line
        """
        prots, calls = [], []

        for a, t in args.items():
            if a not in [*opt_names, *out_names]:
                matched_call = self.matched_types[t]['call']
                calls.append(matched_call.format(type_=t, arg=a))
                if self.matched_types[t]['def'] == 'str':
                    prots.append(
                        self.matched_types[t]['prot'].format(arg=a, type_=t)
                    )
                continue
            elif a in opt_names:
                calls.append(opt_calls.pop(0))
                continue
            elif a in out_names:
                calls.append(out_calls.pop(0))
                continue
            raise KeyError(a)
        return prots, ', '.join(calls)

    def _match_optional_args(
        self, args: ArgsT
    ) -> ty.Tuple[ty.List[str], ty.List[str], ty.List[str], ty.List[str]]:
        """
        Returns
        -------
        Tuple[List[str], List[str], List[str], List[str]]
            names, defs, prots, calls
        """
        defs, calls, prots, names = [], [], [], []
        def_t = "{arg}: ty.Optional[{type_}]=None"
        call_t = "None if {arg} is None else {call}"
        prot_t = "{prot} if {arg} is not None else None"
        for a, t in args.items():
            if a.find('Optional') == -1:
                continue
            names.append(a)
            a = a.replace('InOptional', '')
            m_def = self.matched_types[t]['def'].format(type_=t)
            defs.append(def_t.format(arg=a, type_=m_def))

            m_prot = self.matched_types[t]['prot'].format(
                arg=a, val=a, type_=t
            )
            if m_prot:
                prots.append(prot_t.format(prot=m_prot, arg=a))

            m_call = self.matched_types[t]['call'].format(arg=a, type_=t)
            calls.append(call_t.format(arg=a, call=m_call))
        return names, defs, prots, calls

    def _match_out_args(
        self, args: ArgsT
    ) -> ty.Tuple[ty.List[str], ty.List[str], ty.List[str], ty.List[str],
                  ty.List[str]]:
        """
        Returns
        -------
        Tuple[ty.List[str], ty.List[str], ty.List[str], ty.List[str],
            ty.List[str]]
            names, prots, calls, rets, docs
        """
        rets, calls, prots, names, docs = [], [], [], [], []
        for a, t in args.items():
            if a.find('Out') == -1 or not t.endswith('*'):
                continue
            if a.endswith('_sz'):
                # still, only three size args supports passing byref
                # until the better times I'll leave this as it is
                args[a] = t.replace('*', '')
                continue
            names.append(a)
            a_orig = a
            a = a.replace('Out', '')
            if self.matched_types[t]['def'] == 'str':
                m_prot = self.matched_types[t]['default'].format(
                    arg=a, type_=t, size="{}_sz".format(a_orig)
                )
            else:
                m_prot = self.matched_types[t]['prot'].format(
                    arg=a, val=self.matched_types[t]['default'], type_=t
                )
            prots.append(m_prot)

            m_call = self.matched_types[t]['call'].format(arg=a, type_=t)
            calls.append(m_call)

            m_ret = self.matched_types[t]['ret'].format(arg=a, type_=t)
            rets.append(m_ret)
            docs.append(
                "{arg}: {type_}".format(
                    arg=a,
                    type_=self.matched_types[t]['def'].format(arg=a, type_=t)
                )
            )
        return names, prots, calls, rets, docs

    def build_def(self, item: FuncdefT) -> str:
        """
        Build the single def from parced funcdef.

        Parameters
        ----------
        item : FuncdefT

        Returns
        -------
        str
            multiline python definition
        """
        def_name = item['name'].replace('JS_', '')
        self.all.append(def_name)

        (opt_names, opt_defs, opt_prots,
         opt_calls) = self._match_optional_args(item['args'])
        (out_names, out_prots, out_calls, out_rets,
         out_docs) = self._match_out_args(item['args'])
        def_ret = self._match_def_ret(
            ret=item['return'], args=item['args'], out_names=out_names
        )
        doc = textwrap.fill(
            item['doc'],
            replace_whitespace=False,
        ).replace('\n', '\n    ')
        ret_def_str = self.matched_types[item['return']]['def']
        if ret_def_str == 'None':
            doc_ret_ret: ty.List[str] = []
        else:
            doc_ret_ret = ["ret_value: {}".format(ret_def_str)]
        doc_ret = '\n    '.join([*doc_ret_ret, *out_docs])
        api_name = item['name']
        ref_ret = self.matched_types[item['return']]['ref']
        ref_args = ', '.join(
            '{type_}'.format(type_=self.matched_types[t]['ref'])
            for t in item['args'].values()
        )
        norm_prots, call_args = self._match_call_args(
            item['args'], opt_names, out_names, opt_calls, out_calls
        )
        ret_ret = self.matched_types[item['return']]['ret'].format(
            type_=item['return'], arg='ret'
        )
        ret_full = ret_ret + (', ' if ret_ret and out_rets else '')
        ret_full += ', '.join(out_rets)
        prot_args = '\n    '.join([*opt_prots, *out_prots, *norm_prots])
        def_args = self._match_def_args(
            item['args'], out_names, opt_names, opt_defs
        )

        return _def_templ.format(
            def_name=def_name,
            def_args=def_args,
            def_ret=def_ret,
            doc=doc,
            doc_ret=doc_ret,
            api_name=api_name,
            ref_ret=ref_ret,
            ref_args=ref_args,
            prot_args=prot_args,
            call_args=call_args,
            ret_full=ret_full
        )

    def _match_pointer_types(self) -> ty.List[str]:
        out: ty.List[str] = []
        for t in self.matched_types.keys():
            if t not in _types_to_match:
                out.append(t[:-1])
        return out

    def build_module(self) -> str:
        """
        Build the whole module, based on parced defs.

        Returns
        -------
        str
            multiline str of the generated module
        """
        defs = self.parcer.defs
        defs_str = [self.build_def(def_) for def_ in defs]
        code = _module_templ.format(
            all_=',\n    '.join('"%s"' % s for s in self.all),
            class_defs='\n'.join(
                _class_def_templ.format(type_=t)
                for t in self._match_pointer_types()
            ),
            defs='\n'.join(defs_str)
        )

        # mybe some code formatter should be here
        return code


def generate_js_api(bin_dir: str, api_filepath: str) -> None:
    """
    Get ReaExtensions and generate apropriate files.

    Parameters
    ----------
    bin_dir : str
        binary file directory usually:
        "{}{}{}".format(reapy.get_resource_path, os.sep, UserPlugins)

    api_filepath : str
        file to be imported by end-user, 'reapy/core/gui/JS_API.py' ?
    """
    header_raw = get_header_contents()
    write_binary_file(bin_dir)
    prc = Parcer(raw_str=header_raw)
    builder = FuncBuilder(prc)
    module_str = builder.build_module()
    with open(api_filepath, 'w') as f:
        f.write(module_str)
    with open('JS_API.py', 'r') as f:
        lines = []
        ignore = False
        for line in f.readlines():
            if ignore and ']' in line:
                line = '\n' + line
                ignore = False
            if not ignore:
                lines.append(line)
            if '__all__: ty.List[str] = [' in line:
                ignore = True
                lines.append(',\n    '.join('"%s"' % s for s in builder.all))
    with open('JS_API.py', 'w') as f:
        f.writelines(lines)


if __name__ == '__main__':
    import reapy
    api_filepath = os.path.join(
        os.path.dirname(__file__), "_JS_API_generated.py"
    )
    bin_dir = os.path.join(reapy.get_resource_path(), "UserPlugins")
    # print(api_filepath)
    # print(bin_dir)
    generate_js_api(bin_dir, api_filepath)

"""Make the Pythran files for ahead-of-time compilation
=======================================================

User API
--------

.. autofunction:: make_pythran_files

Internal API
------------

.. autofunction:: parse_py_code

.. autofunction:: get_code_functions

.. autofunction:: get_codes_from_functions

.. autofunction:: make_pythran_code_functions

.. autofunction:: make_pythran_code

.. autofunction:: make_pythran_file

.. autofunction:: mock_modules

"""

from tokenize import tokenize, untokenize, COMMENT, INDENT, DEDENT, STRING, NAME

import os
from logging import DEBUG

from token import tok_name
from io import BytesIO
from pathlib import Path
from runpy import run_module, run_path
import sys
from unittest.mock import MagicMock as Mock
from contextlib import contextmanager

from typing import Iterable, Optional

try:
    import black
except ImportError:
    black = False

from .log import logger, set_log_level
from .annotation import compute_pythran_types_from_valued_types
from .util import has_to_build, get_source_without_decorator
from .compat import open
import fluidpythran


def parse_py_code(code: str):
    """Parse the code of a .py file and return data"""

    blocks = []
    signatures_blocks = {}
    code_blocks = {}

    functions = set()
    signatures_func = {}

    imports = []

    has_to_find_name_block = False
    has_to_find_signatures = False
    has_to_find_code_block = False
    in_def = False

    g = tokenize(BytesIO(code.encode("utf-8")).readline)
    for toknum, tokval, a, b, c in g:

        if (
            toknum == COMMENT
            and tokval.startswith("# pythran ")
            and "import" in tokval
        ):
            imports.append(tokval.split("# pythran ", 1)[1])

        if toknum == NAME and tokval == "use_pythranized_block":
            has_to_find_name_block = True
            has_to_find_signatures = True
            has_to_find_code_block = "after use_pythranized_block"

        if has_to_find_name_block and toknum == STRING:
            name_block = eval(tokval)
            has_to_find_name_block = False
            blocks.append(name_block)

        if toknum == COMMENT and tokval.startswith("# pythran def "):
            in_def = True
            signature_func = tokval.split("# pythran def ", 1)[1]
            name_func = signature_func.split("(")[0]
            functions.add(name_func)

            if name_func not in signatures_func:
                signatures_func[name_func] = []

            if ")" in tokval:
                in_def = False
                signatures_func[name_func].append(signature_func)

        if in_def:
            if toknum == COMMENT:
                if "# pythran def " in tokval:
                    tokval = tokval.split("(", 1)[1]
                signature_func += tokval.replace("#", "").strip()
                if ")" in tokval:
                    in_def = False
                    signatures_func[name_func].append(signature_func)

        if has_to_find_signatures and toknum == COMMENT:
            if tokval.startswith("# pythran block "):
                in_signature = True
                signature = tokval.split("# pythran block ", 1)[1]
            elif in_signature:
                signature += tokval[1:].strip()
                if ")" in tokval and "-> (" not in tokval or tokval.endswith(")"):
                    in_signature = False

                    if name_block not in signatures_blocks:
                        signatures_blocks[name_block] = []
                    signatures_blocks[name_block].append(signature)

        if has_to_find_code_block == "in block":

            if toknum == DEDENT:
                logger.debug(
                    f"code_blocks[name_block]: {code_blocks[name_block]}"
                )

                code_blocks[name_block] = untokenize(code_blocks[name_block])
                has_to_find_code_block = False
            else:
                code_blocks[name_block].append((toknum, tokval))

        if (
            has_to_find_code_block == "after use_pythranized_block"
            and toknum == INDENT
        ):
            has_to_find_code_block = "in block"
            code_blocks[name_block] = []

        logger.debug((tok_name[toknum], tokval))

    return (
        blocks,
        signatures_blocks,
        code_blocks,
        functions,
        signatures_func,
        imports,
    )


def get_code_functions(code: str, func_names: Iterable[str]):
    """Get the code of function from a path and function names"""

    indent = 0
    in_def = False
    codes = {}

    g = tokenize(BytesIO(code.encode("utf-8")).readline)
    for toknum, tokval, a, b, c in g:

        if toknum == INDENT:
            indent += 1

        if toknum == DEDENT:
            indent -= 1

        if in_def == "def" and tokval in func_names:
            in_def = tokval
            codes[in_def] = [(NAME, "def")]

        if indent == 0 and toknum == NAME and tokval == "def":
            in_def = "def"

        if in_def and in_def != "def":

            if toknum == COMMENT and tokval.startswith("# pythran"):
                continue

            if indent == 0 and toknum == DEDENT:
                codes[in_def] = untokenize(codes[in_def])
                in_def = False
            else:
                codes[in_def].append((toknum, tokval))

        logger.debug((indent, tok_name[toknum], tokval))

    return codes


def get_codes_from_functions(functions: dict):
    """create a dict {name: code} from {name: function}

    """
    codes = {}

    for name, func in functions.items():
        code = get_source_without_decorator(func)
        codes[name] = code

    return codes


def make_pythran_code_functions(
    functions: Iterable[str], signatures_func: dict, codes_functions: dict
):
    """Create the pythran code for all functions

    Parameters
    ----------

    functions : list

    signatures_func : dict

    codes_functions: dict

    """
    code_pythran = ""

    for name_func in functions:

        try:
            signatures = signatures_func[name_func]
        except KeyError:
            logger.warning("No Pythran signature for function " + name_func)
            continue

        if not signatures:
            raise RuntimeError("No Pythran signature for function " + name_func)

        for signature in signatures:
            code_pythran += f"# pythran export {signature}\n"

        code = codes_functions[name_func]

        code_pythran += f"\n{code}\n\n"

    return code_pythran


def make_pythran_code(path_py: Path):
    """Create a pythran code from a Python file"""

    with open(path_py) as file:
        code = file.read()

    namespace = None
    if "# FLUIDPYTHRAN_NO_IMPORT" not in code:
        # we have to import the module!
        fluidpythran.aheadoftime.is_transpiling = True
        try:
            namespace = run_path(str(path_py))
        except ImportError:
            name_mod = ".".join(
                path_py.absolute().relative_to(os.getcwd()).with_suffix("").parts
            )
            sys.path.insert(0, "")
            try:
                namespace = run_module(name_mod)
            except ImportError:
                logger.error(
                    f"fluidpythran was unable to import module {name_mod}: "
                    "no Pythran file created. "
                    "You could add '# FLUIDPYTHRAN_NO_IMPORT' "
                    "in the module if needed..."
                    "You could mock modules by using the argument mocked_modules to "
                    "the function make_pythran_files."
                )
                raise
            finally:
                del sys.path[0]
        fluidpythran.aheadoftime.is_transpiling = False

    (
        blocks,
        signatures_blocks,
        code_blocks,
        functions,
        signatures_func,
        imports,
    ) = parse_py_code(code)

    if logger.isEnabledFor(DEBUG):
        logger.debug(
            f"""
blocks: {blocks}\n
signatures_blocks: {signatures_blocks}\n
code_blocks:  {code_blocks}\n
functions: {functions}\n
signatures_func: {signatures_func}\n
imports: {imports}\n"""
        )

    code_pythran = ""
    if imports:
        code_pythran += "\n" + "\n".join(imports) + "\n"

    module_name = Path(path_py).with_suffix("").name
    if module_name in fluidpythran.aheadoftime.modules:
        fp = fluidpythran.aheadoftime.modules[module_name]
        fp._make_signatures_from_annotations()
        functions = fp.functions.keys()
        signatures_func_annot = fp.signatures_func
        codes_functions = get_codes_from_functions(fp.functions)

        # merge signatures introduced by type annotations and by Pythran commands
        signatures_func_all = signatures_func.copy()
        for name_func, signatures in signatures_func_annot.items():
            if name_func not in signatures_func_all:
                signatures_func_all[name_func] = []
            signatures_func_all[name_func].extend(signatures)
    else:
        codes_functions = get_code_functions(code, functions)
        signatures_func_all = signatures_func

    code_pythran += make_pythran_code_functions(
        functions, signatures_func_all, codes_functions
    )

    # blocks...

    # we check that some types correspond to fluidpythran types
    # we can do that only if the module has been imported

    types_variables_blocks = {}
    return_block = {}
    for name_block, list_str_types_variables in signatures_blocks.items():
        types_variables_blocks[name_block] = []

        for str_types_variables in list_str_types_variables:
            types_variables = {}
            lines = str_types_variables.split("(", 1)[1].split(")")[0].split(";")
            for line in lines:
                type_, str_variables = line.strip().split(" ", 1)

                if namespace is not None and type_ in namespace:
                    type_ = namespace[type_]
                else:
                    try:
                        type_ = eval(type_)
                    except (SyntaxError, TypeError):
                        pass

                variables = [
                    variable.replace(",", "").strip()
                    for variable in str_variables.split(",")
                ]

                types_variables[type_] = variables

            types_variables_blocks[name_block].append(types_variables)

            if list_str_types_variables and "->" in str_types_variables:
                return_block[name_block] = str_types_variables.split("->", 1)[1]

    for name_block, list_types_variables in tuple(types_variables_blocks.items()):
        new_list_types_variables = []
        for types_variables in list_types_variables:
            sequence_types = compute_pythran_types_from_valued_types(
                types_variables.keys()
            )
            variabless = types_variables.values()
            # print("variabless", variabless)
            for types in sequence_types:
                new_types_variables = {}
                for type_, variables in zip(types, variabless):
                    if type_ not in new_types_variables:
                        new_types_variables[type_] = variables
                    else:
                        new_types_variables[type_] = (
                            new_types_variables[type_] + variables
                        )
                new_list_types_variables.append(new_types_variables)

        types_variables_blocks[name_block] = new_list_types_variables

    # print("types_variables_blocks", types_variables_blocks)

    variables_types_block = {}
    for name_block, list_types_variables in types_variables_blocks.items():
        variables_types_block[name_block] = []
        for types_variables in list_types_variables:
            variables_types = {}
            for type_, variables in types_variables.items():
                for variable in variables:
                    variables_types[variable] = type_
                variables_types

            variables_types_block[name_block].append(variables_types)

    # print("variables_types_block", variables_types_block)

    arguments_blocks = {}

    for name_block, list_variables_types in variables_types_block.items():
        # add "pythran export" for blocks

        # print("list_variables_types", list_variables_types)

        tmp = []

        for variables_types in list_variables_types:
            if variables_types in tmp:
                continue
            tmp.append(variables_types)
            str_types = variables_types.values()
            str_variables = ", ".join(str_types)
            code_pythran += f"# pythran export {name_block}({str_variables})\n"

        # add code for blocks
        variables = list_variables_types[0].keys()
        arguments_blocks[name_block] = list(variables)

        str_variables = ", ".join(variables)

        code_pythran += f"\ndef {name_block}({str_variables}):\n"

        code_block = code_blocks[name_block]

        code_pythran += 4 * " " + code_block.replace("\n", "\n" + 4 * " ") + "\n"

        if name_block in return_block:
            code_pythran += f"    return {return_block[name_block]}\n"

    if arguments_blocks:
        code_pythran += "# pythran export arguments_blocks\n"
        code_pythran += "arguments_blocks = " + str(arguments_blocks) + "\n"

    if code_pythran:
        code_pythran += (
            "\n# pythran export __fluidpythran__\n"
            f"__fluidpythran__ = ('{fluidpythran.__version__}',)"
        )

    if black:
        code_pythran = black.format_str(code_pythran, line_length=82)

    return code_pythran


def make_pythran_file(
    path_py: Path,
    force=False,
    log_level=None,
    mocked_modules: Optional[Iterable] = None,
):
    """Create a Python file from a Python file (if necessary)"""
    if log_level is not None:
        set_log_level(log_level)

    path_py = Path(path_py)

    if path_py.absolute().parent.name == "__pythran__":
        logger.debug(f"skip file {path_py}")
        return
    if not path_py.name.endswith(".py"):
        raise ValueError(
            "fluidpythran only processes Python file. Cannot process {path_py}"
        )

    path_dir = path_py.parent / "__pythran__"
    path_pythran = path_dir / ("_" + path_py.name)

    if not has_to_build(path_pythran, path_py) and not force:
        logger.info(f"File {path_pythran} already up-to-date.")
        return

    with mock_modules(mocked_modules):
        code_pythran = make_pythran_code(path_py)

    if not code_pythran:
        return

    if path_pythran.exists() and not force:
        with open(path_pythran) as file:
            code_pythran_old = file.read()

        if code_pythran_old == code_pythran:
            logger.info(f"Code in file {path_pythran} already up-to-date.")
            return

    logger.debug(f"code_pythran:\n{code_pythran}")

    path_dir.mkdir(exist_ok=True)

    with open(path_pythran, "w") as file:
        file.write(code_pythran)

    logger.info(f"File {str(path_pythran)} written")

    return path_pythran


def make_pythran_files(
    paths: Iterable[Path],
    force=False,
    log_level=None,
    mocked_modules: Optional[Iterable] = None,
):
    """Create Pythran files from a list of Python files"""

    if log_level is not None:
        set_log_level(log_level)

    paths_out = []
    for path in paths:
        path_out = make_pythran_file(
            path, force=force, mocked_modules=mocked_modules
        )
        if path_out:
            paths_out.append(path_out)

    if paths_out:
        nb_files = len(paths_out)
        if nb_files == 1:
            conjug = "s"
        else:
            conjug = ""

        logger.warning(
            f"{nb_files} files created or updated need{conjug}"
            " to be pythranized"
        )

    return paths_out


class _MyMock(Mock):
    @classmethod
    def __getattr__(cls, name):
        return Mock()


@contextmanager
def mock_modules(modules):
    """Context manager to mock modules

    Examples
    --------

    .. code::

        with mock_modules(("h5py", "reikna.fft", "reikna.transformations")):
            code_pythran = make_pythran_code(path_py)

    """
    if modules is not None:
        modules = set(modules)
        modules.difference_update(set(sys.modules.keys()))
        sys.modules.update((mod_name, _MyMock()) for mod_name in modules)

    try:
        yield None
    finally:
        if modules is not None:
            for mod_name in modules:
                sys.modules.pop(mod_name)

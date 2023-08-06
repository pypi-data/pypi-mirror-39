#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Static functional purity analysis for Python.

Copyright © 2018 Gary Brandt Bucher, II. Maintained under the MIT License at:
https://github.com/brandtbucher/flython
"""


__all__ = ("main", "PurityError")
__author__ = "Brandt Bucher"
__credits__ = "Everyone on the Investment Systems team at Research Affiliates."
__date__ = "December 11, 2018"
__version__ = "0.0.0"


from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from argparse import SUPPRESS
import builtins
from dis import get_instructions
from dis import opname
from importlib.util import find_spec
from os import walk
from os.path import abspath
from os.path import join
from os.path import split
from re import findall
import sys
from types import CodeType
from types import SimpleNamespace


try:  # pragma: no cover

    from typing import Any
    from typing import Callable
    from typing import FrozenSet
    from typing import Generator
    from typing import Iterable
    from typing import List
    from typing import Optional
    from typing import Sequence
    from typing import Tuple
    from typing import Union

except ImportError:  # pragma: no cover

    # Python 3.4-:

    class FakeType:
        """Placeholder type in absence of typing.py on Python 3.4."""

        def __getitem__(self, *types: str) -> "FakeType":
            """Return another FakeType when subscripted."""

            return self

    Any = FakeType()
    Callable = FakeType()  # type: ignore
    FrozenSet = FakeType()  # type: ignore
    Generator = FakeType()  # type: ignore
    Iterable = FakeType()  # type: ignore
    List = FakeType()  # type: ignore
    Optional = FakeType()  # type: ignore
    Sequence = FakeType()  # type: ignore
    Tuple = FakeType()  # type: ignore
    Union = FakeType()  # type: ignore


# TODO: Check redefinitions.


DO_NOT_LOAD_DYNAMIC = frozenset(
    name
    for name in (
        "breakpoint",
        "delattr",
        "eval",
        "exec",
        "globals",
        "locals",
        "setattr",
    )
    if name in dir(builtins)
)
DO_NOT_LOAD_IO = frozenset(("input", "open", "print"))

# TODO: sorted, dir, vars... Exceptions?
DO_NOT_LOAD_MUTABLES = frozenset(("bytearray", "dict", "list", "set"))
DO_NOT_MODIFY = frozenset(dir(builtins)) - frozenset(("__doc__",))

PRAGMA_SKIP = "skip"
PRAGMA_IGNORE = "ignore"
PRAGMAS = (PRAGMA_SKIP, PRAGMA_IGNORE)
PATTERN = r"#\s*flython\s*:\s*({})\b".format("|".join(PRAGMAS))


HELP_NO_DYNAMIC = 'Don\'t allow "{}", or "{}".'.format(
    '", "'.join(sorted(DO_NOT_LOAD_DYNAMIC)[:-1]), sorted(DO_NOT_LOAD_DYNAMIC)[-1]
)
HELP_NO_IO = 'Don\'t allow "{}", or "{}".'.format(
    '", "'.join(sorted(DO_NOT_LOAD_IO)[:-1]), sorted(DO_NOT_LOAD_IO)[-1]
)
HELP_NO_MUTABLES = "Don't allow mutable built-in types."
HELP_NO_RAISE = 'Don\'t allow "raise" statements.'
HELP_SKIP_IMPORTS = "Don't check imports."
HELP_STRICT = "Same as --no-dynamic --no-io --no-mutables --no-raise."

# TODO: Fix these:
# TODO: PurityNotes?

ERROR_DELETE_ATTRIBUTE_KNOWN = "Attempt to delete variable attribute {target}."
ERROR_DELETE_ATTRIBUTE_UNKNOWN = "Attempt to delete variable attribute."
ERROR_DELETE_GLOBAL = "Attempt to delete global variable {name!r}."
ERROR_DELETE_ITEM_KNOWN = "Attempt to delete contained item {target}."
ERROR_DELETE_ITEM_UNKNOWN = "Attempt to delete contained item."
ERROR_DELETE_NONLOCAL = "Attempt to delete nonlocal variable {name!r}."
ERROR_DELETE_UNKNOWN = "Attempt to delete variable {name!r} of unknown scope."
ERROR_IMPORT_BUILTIN = "Attempt to import uncheckable built-in module {name!r}."
ERROR_IMPORT_EXTENSION = "Attempt to import uncheckable extension module {name!r}."
ERROR_IMPORT_IMPURE = "Attempt to import impure module {name!r}."
ERROR_IMPORT_MISSING = "Attempt to import missing module {name!r}."
ERROR_IMPORT_SCOPED = "Attempt to import {name!r}. Import at the module level instead."
ERROR_IMPORT_STAR = "Attempt to import '*'. Import explicit names instead."
ERROR_INPLACE_OP_KNOWN = "Attempt to modify variable. Use normal assignment ({target} = {target} {op} {value}) instead of augmented assignment ({target} {op}= {value})."
ERROR_INPLACE_OP_UNKNOWN = "Attempt to modify variable. Use normal assignment (<left> = <left> {op} <right>) instead of augmented assignment (<left> {op}= <right>)."
ERROR_LOAD_DYNAMIC = "Attempt to load dynamic function {name!r}."
ERROR_LOAD_IO = "Attempt to load I/O function {name!r}."
ERROR_LOAD_MUTABLES = "Attempt to use mutable built-in type {name!r}."
ERROR_RAISE = "Attempt to raise exception."
ERROR_SHADOW_BUILTIN = "Attempt to shadow built-in variable {name!r}."
ERROR_STORE_ATTRIBUTE_KNOWN = (
    "Attempt to store value {value} to variable attribute {target}."
)
ERROR_STORE_ATTRIBUTE_UNKNOWN = "Attempt to store value to variable attribute."
ERROR_STORE_GLOBAL = "Attempt to store global variable {name!r}."
ERROR_STORE_ITEM_KNOWN = "Attempt to store value {value} to contained item {target}."
ERROR_STORE_ITEM_UNKNOWN = "Attempt to store value to contained item."
ERROR_STORE_NONLOCAL = "Attempt to store nonlocal variable {name!r}."


class FlythonError(RuntimeError):
    """Indicates an internal error in Flython."""


class PurityError(SyntaxError):
    """Indicates a violation of functional purity."""


class PurityNote(SyntaxWarning):
    """Suggests a possible improvement to functional purity."""


Context = Tuple[Optional[str], int, None, Optional[str]]
Errors = Generator[SyntaxError, None, None]


# def scoped(scoped: bool, arg: str, context: Context) -> Errors:
#    if not scoped:
#        return (PurityError(
#            "Only initialization, imports, and definitions may take place at the module level.",
#            context,
#        ),)
#    return ()


# def module(message: str) -> Callable[[bool, str, Context], Tuple[]]:
#    def handler(scoped: bool, arg: str, context: Context) -> Tuple[]:
#        if scoped:
#            return (PurityError(message.format(arg=arg), context),)
#        return ()
#
#    return handler


# TODO: arg type is string for all of these???


def impure(message: str) -> Callable[..., Errors]:
    """Create and return an unconditionally impure opcode handler."""

    def handler(*, arg: str, context: Context, **unused: Any) -> Errors:
        """Unconditionally yield a formatted PurityError."""

        yield PurityError(message.format(name=arg), context)

    return handler


def inplace_op(op: str) -> Callable[..., Errors]:
    """Create and return an unconditionally impure opcode handler for augmented assignment."""

    def handler(
        *,
        context: Context,
        options: SimpleNamespace,
        stack: Tuple[Any, ...],
        **unused: Any
    ) -> Errors:
        """Yield a PurityError formatted for augmented assignment if mutable types are allowed."""

        if options.no_mutables:
            return

        if 2 <= len(stack):
            message = ERROR_INPLACE_OP_KNOWN.format(
                target=stack[-2], op=op, value=stack[-1]
            )
        else:
            message = ERROR_INPLACE_OP_UNKNOWN.format(op=op)

        yield PurityError(message, context)

    return handler


def mutable(kind: str) -> Callable[..., Errors]:  # TODO: Signature?
    """Create and return an opcode handler for the provided mutable type."""

    def handler(*, context: Context, options: SimpleNamespace, **unused: Any) -> Errors:
        """Yield a PurityError if mutable types are disallowed."""

        if options.no_mutables:
            yield PurityError(ERROR_LOAD_MUTABLES.format(name=kind), context)

    return handler


def check_name(
    *, arg: str, context: Context, options: SimpleNamespace, **unused: Any
) -> Errors:
    """Yield PurityErrors if the provided `arg` is present in configured blacklists."""

    if options.no_dynamic:
        if arg in DO_NOT_LOAD_DYNAMIC:
            yield PurityError(ERROR_LOAD_DYNAMIC.format(name=arg), context)

    if options.no_io:
        if arg in DO_NOT_LOAD_IO:
            yield PurityError(ERROR_LOAD_IO.format(name=arg), context)

    if options.no_mutables:
        if arg in DO_NOT_LOAD_MUTABLES:
            yield PurityError(ERROR_LOAD_MUTABLES.format(name=arg), context)


def delete_subscr(*, context: Context, stack: Tuple[Any, ...], **unused: Any) -> Errors:
    """Unconditionally yield a PurityError formatted for subscript deletion."""

    if 2 <= len(stack):

        item = "{outer}[{inner}]".format(inner=stack[-1], outer=stack[-2])

        message = ERROR_DELETE_ITEM_KNOWN.format(target=item)

    else:

        message = ERROR_DELETE_ITEM_UNKNOWN

    yield PurityError(message, context)


def delete_attr(
    *, arg: str, context: Context, stack: Tuple[Any, ...], **unused: Any
) -> Errors:
    """Unconditionally yield a PurityError formatted for attribute deletion."""

    if stack:

        item = "{}.{}".format(stack[-1], arg)

        message = ERROR_DELETE_ATTRIBUTE_KNOWN.format(target=item)

    else:

        message = ERROR_DELETE_ATTRIBUTE_UNKNOWN.format(target=arg)

    yield PurityError(message, context)


def import_from(
    *, arg: str, context: Context, scoped: bool, options: SimpleNamespace, **unused: Any
) -> Errors:
    """Yield a formatted PurityError if `scoped`."""

    if scoped:
        yield PurityError(ERROR_IMPORT_SCOPED.format(name=arg), context)


def import_name(
    *,
    arg: str,
    context: Context,
    options: SimpleNamespace,
    scoped: bool,
    sourcelines: Sequence[str],
    stack: Tuple[Any, ...],
    **unused: Any
) -> Errors:
    """Yield a formatted PurityError if `scoped`, and follow import (if configured)."""

    if scoped:
        yield PurityError(ERROR_IMPORT_SCOPED.format(name=arg), context)

    # TODO: Move this check to check_import?
    if not options.skip_imports and PRAGMA_SKIP not in pragmas(sourcelines, context[1]):
        yield from check_import(int(stack[-2]), arg, stack[-1], context, options)


def import_star(
    *, arg: str, context: Context, options: SimpleNamespace, **unused: Any
) -> Errors:
    """Unconditionally yield a PurityError formatted for starred imports."""

    yield PurityError(ERROR_IMPORT_STAR.format(name=arg), context)


def load_const(
    *, arg: str, options: SimpleNamespace, sourcelines: Sequence[str], **unused: Any
) -> Errors:
    """..."""

    if isinstance(arg, CodeType):
        yield from check_code(arg, True, sourcelines, options)


def load_fast(*, arg: str, context: Context, **unused: Any) -> Errors:
    """..."""

    yield from shadowed(arg, context)


def pure(**unused: Any) -> Errors:
    """Return control to caller."""

    yield from ()  # type: ignore  # https://github.com/python/mypy/issues/4444


def raise_varargs(
    *, context: Context, options: SimpleNamespace, **unused: Any
) -> Errors:
    """..."""

    if options.no_raise:
        yield PurityError(ERROR_RAISE, context)


def store_attr(
    *, arg: str, context: Context, stack: Tuple[Any, ...], **unused: Any
) -> Errors:
    """Unconditionally yield a PurityError formatted for attribute assignment."""

    if 2 <= len(stack):

        item = "{}.{}".format(stack[-1], arg)
        value = str(stack[-2])

        message = ERROR_STORE_ATTRIBUTE_KNOWN.format(target=item, value=value)

    else:

        message = ERROR_STORE_ATTRIBUTE_UNKNOWN.format(target=arg)

    yield PurityError(message, context)


def store_fast(*, arg: str, context: Context, **unused: Any) -> Errors:
    """..."""

    yield from shadowed(arg, context)


def store_global(*, arg: str, context: Context, scoped: bool, **unused: Any) -> Errors:
    """..."""

    if scoped:
        yield PurityError(ERROR_STORE_GLOBAL.format(name=arg), context)
    yield from shadowed(arg, context)


def store_name(*, arg: str, context: Context, **unused: Any) -> Errors:
    """..."""

    yield from shadowed(arg, context)
    # TODO: Scoped could be dangerous, but class definitions use this. Stack?


def store_subscr(*, context: Context, stack: Tuple[Any, ...], **unused: Any) -> Errors:
    """Unconditionally yield a PurityError formatted for subscript assignment."""

    if 2 <= len(stack) and stack[-2] == "__annotations__":
        return  # pragma: no cover  # Python 3.7+

    if 3 <= len(stack):

        item = "{outer}[{inner}]".format(inner=stack[-1], outer=stack[-2])
        value = str(stack[-3])

        message = ERROR_STORE_ITEM_KNOWN.format(target=item, value=value)

    else:

        message = ERROR_STORE_ITEM_UNKNOWN

    yield PurityError(message, context)


OPS = {
    "BUILD_CONST_KEY_MAP": mutable(
        "dict"
    ),  # TODO: Unfortunately, used for function annotations!
    "BUILD_LIST": mutable("list"),
    "BUILD_LIST_UNPACK": mutable("list"),
    "BUILD_MAP": mutable("dict"),
    "BUILD_MAP_UNPACK": mutable("dict"),
    "BUILD_SET": mutable("set"),
    "BUILD_SET_UNPACK": mutable("set"),
    "DELETE_ATTR": delete_attr,
    "DELETE_DEREF": impure(ERROR_DELETE_NONLOCAL),
    "DELETE_GLOBAL": impure(ERROR_DELETE_GLOBAL),
    "DELETE_NAME": impure(ERROR_DELETE_UNKNOWN),
    "DELETE_SUBSCR": delete_subscr,
    "IMPORT_FROM": import_from,
    "IMPORT_NAME": import_name,
    "IMPORT_STAR": import_star,
    "INPLACE_ADD": inplace_op("+"),
    "INPLACE_AND": inplace_op("&"),
    # "INPLACE_FLOOR_DIVIDE": inplace_op("//"),  # Not overloaded by mutables.
    # "INPLACE_LSHIFT": inplace_op("<<"),  # Not overloaded by mutables.
    # "INPLACE_MATRIX_MULTIPLY": inplace_op("@"),  # Not overloaded by mutables.
    # "INPLACE_MODULO": inplace_op("%"),  # Not overloaded by mutables.
    "INPLACE_MULTIPLY": inplace_op("*"),
    "INPLACE_OR": inplace_op("|"),
    # "INPLACE_POWER": inplace_op("**"),  # Not overloaded by mutables.
    # "INPLACE_RSHIFT": inplace_op(">>"),  # Not overloaded by mutables.
    "INPLACE_SUBTRACT": inplace_op("-"),
    # "INPLACE_TRUE_DIVIDE": inplace_op("/"),  # Not overloaded by mutables.
    "INPLACE_XOR": inplace_op("^"),
    # "LIST_APPEND": mutable("list"),  # TODO: Print a note here?
    "LOAD_CONST": load_const,
    # "LOAD_DEREF": check_name,  # Fine?
    "LOAD_FAST": load_fast,
    "LOAD_GLOBAL": check_name,
    "LOAD_NAME": check_name,
    # "MAP_ADD": mutable("dict"),  # TODO: Print a note here?
    "RAISE_VARARGS": raise_varargs,
    # "SET_ADD": mutable("set"),  # TODO: Print a note here?
    "STORE_ATTR": store_attr,
    "STORE_DEREF": impure(ERROR_STORE_NONLOCAL),
    "STORE_FAST": store_fast,
    "STORE_GLOBAL": store_global,
    # "STORE_MAP": mutable("dict"),  # Python 3.4: uses BUILD_MAP first, so fine.
    "STORE_NAME": store_name,
    "STORE_SUBSCR": store_subscr,
}


# Get just the ones we need:
IMPURE = tuple(OPS.get(op, pure) for op in opname)


def check_code(
    code: CodeType, scoped: bool, sourcelines: Sequence[str], options: SimpleNamespace
) -> Errors:
    """Check the provided code object for functional purity."""

    line = code.co_firstlineno

    if scoped and PRAGMA_SKIP in pragmas(sourcelines, line):
        return

    stack = ()  # type: Tuple[str, ...]

    for op in get_instructions(code):

        if op.starts_line is not None:
            line = op.starts_line

        context = (code.co_filename, line, None, sourceline(sourcelines, line))

        for error in IMPURE[op.opcode](  # type: ignore
            scoped=scoped,
            arg=op.argval,
            context=context,
            options=options,
            sourcelines=sourcelines,
            stack=stack,
        ):

            if PRAGMA_IGNORE not in pragmas(sourcelines, error.lineno):
                yield error

        # TODO: Clean up error reporting, strings, etc. argrepr or argval???

        # constant
        # 'name'
        # "'string'"  strings should not be repr'd, names should if alone and guranteed!

        if op.opname == "LOAD_CONST":
            stack = stack + (op.argrepr if isinstance(op.argval, str) else op.argval,)
        elif op.opname == "LOAD_ATTR":
            try:
                stack = stack[:-1] + (str(stack[-1]) + "." + op.argval,)
            except IndexError:
                stack = ()
        elif op.opname in frozenset(
            (
                "LOAD_FAST",
                "LOAD_GLOBAL",
                "LOAD_CLOSURE",
                "LOAD_NAME",
                "LOAD_DEREF",
                "LOAD_CLASSDEREF",
            )
        ):
            stack = stack + (op.argrepr,)
        else:
            stack = ()


def check_import(
    level: int,
    name: str,
    fromlist: Iterable[str],
    context: Context,
    options: SimpleNamespace,
) -> Errors:
    """Check the provided import for functional purity."""

    if 1 < level:

        path = sys.path[0] or abspath(".")

        while 1 < level:
            path = split(path)[0]
            level = level - 1

        sys.path[0] = path  # flython: ignore  # TODO: Rework.

    names = name.split(".")

    # TODO: Check if package?

    spec = find_spec(names[0])

    if spec is None:
        yield PurityError(ERROR_IMPORT_MISSING.format(name=name), context)

    elif spec.origin is None:
        yield PurityError(ERROR_IMPORT_BUILTIN.format(name=name), context)

    elif not spec.origin.endswith(".py"):
        yield PurityError(ERROR_IMPORT_EXTENSION.format(name=name), context)

    elif any(check_path(spec.origin, options)):
        yield PurityError(ERROR_IMPORT_IMPURE.format(name=name), context)

    elif 1 < len(names):
        sys.path[0] = split(spec.origin)[0]  # flython: ignore  # TODO: Rework.
        yield from check_import(0, ".".join(names[1:]), fromlist, context, options)

    elif fromlist and spec.submodule_search_locations is not None:

        for target in fromlist:
            for location in spec.submodule_search_locations:

                # TODO: Check module namespace!

                sys.path[0] = location  # flython: ignore  # TODO: Rework.
                result = find_spec(target)

                if result is not None and result.origin is not None:
                    if any(check_path(result.origin, options)):
                        yield PurityError(
                            ERROR_IMPORT_IMPURE.format(name=name), context
                        )
                        break

    sys.path[0] = ""  # flython: ignore  # TODO: Rework.


def check_path(
    filepath: str, options: SimpleNamespace
) -> Generator[Union[OSError, SyntaxError], None, None]:
    """Check the provided filepath for functional purity."""

    try:

        with open(filepath) as module:
            source = module.read()

        sourcelines = tuple(source.splitlines())
        code = compile(source, filepath, "exec")

    except IsADirectoryError:

        for path, directories, files in walk(filepath):
            for file in files:
                if file.endswith(".py"):
                    yield from check_path(join(path, file), options)

    # TODO: Wrap these?
    except (OSError, SyntaxError) as error:

        yield error

    else:

        yield from check_code(code, False, sourcelines, options)


def pragmas(sourcelines: Sequence[str], line: int) -> FrozenSet[str]:
    """..."""

    return frozenset(findall(PATTERN, sourceline(sourcelines, line)))


def sourceline(sourcelines: Sequence[str], line: int) -> str:
    """..."""

    return sourcelines[line - 1] if sourcelines else ""


def shadowed(name: str, context: Context) -> Errors:
    """..."""

    if name in DO_NOT_MODIFY:
        yield PurityError(ERROR_SHADOW_BUILTIN.format(name=name), context)


def main(
    *modules: str,
    no_dynamic: bool = False,
    no_io: bool = False,
    no_mutables: bool = False,
    no_raise: bool = False,
    skip_imports: bool = False
) -> Generator[Union[OSError, SyntaxError], None, None]:
    """..."""

    options = SimpleNamespace(
        no_dynamic=no_dynamic,
        no_io=no_io,
        no_mutables=no_mutables,
        no_raise=no_raise,
        skip_imports=skip_imports,
    )

    for filepath in sorted(frozenset(modules)):
        yield from check_path(filepath, options)


def _main() -> int:
    """Parse and execute the Flython's command-line arguments."""

    # TODO: ConfigParser
    # TODO: Epilog?

    parser = ArgumentParser(
        usage=SUPPRESS,
        epilog="\0",
        add_help=False,
        description="\0\n" + __doc__.splitlines()[0],
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument("-h", "--help", action="help", help=SUPPRESS)
    parser.add_argument("-v", "--verbose", action="store_true", help=SUPPRESS)
    parser.add_argument(
        "--version",
        action="version",
        version="\0\n" + __version__ + "\n\0",
        help=SUPPRESS,
    )

    options = parser.add_argument_group("Options", description="")

    # options.add_argument("modules", nargs="*", help=SUPPRESS)
    options.add_argument("--no-dynamic", action="store_true", help=HELP_NO_DYNAMIC)
    options.add_argument("--no-io", action="store_true", help=HELP_NO_IO)
    options.add_argument("--no-mutables", action="store_true", help=HELP_NO_MUTABLES)
    options.add_argument("--no-raise", action="store_true", help=HELP_NO_RAISE)
    options.add_argument("--skip-imports", action="store_true", help=HELP_SKIP_IMPORTS)
    options.add_argument("--strict", action="store_true", help=HELP_STRICT)

    args, modules = parser.parse_known_args()

    failed = 0

    for error in main(
        *modules,
        no_dynamic=args.no_dynamic or args.strict,
        no_io=args.no_io or args.strict,
        no_mutables=args.no_mutables or args.strict,
        no_raise=args.no_raise or args.strict,
        skip_imports=args.skip_imports
    ):

        failed = failed + 1

        if args.verbose and isinstance(error, SyntaxError):
            print("\n", error, "\n ↳  ", error.text.strip(), sep="")
        else:
            print(error)

    if args.verbose and failed:
        print()

    return min(failed, 127)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(_main())

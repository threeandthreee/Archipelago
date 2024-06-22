import ast
import typing

from jinja2 import Environment
from jinja2.ext import Extension

from .ast import AstGenerator
from .emit import emit_dict, emit_list, emit_set

def create_filters(ast_generator: AstGenerator) -> dict[str, typing.Callable[..., typing.Any]]:
    def to_code(target: typing.Any, kind: str) -> ast.expr:
        if kind == "constant":
            return ast.Constant(target)
        if kind == "tuple":
            return ast.Tuple([ast.Constant(el) for el in target])
        each_func: typing.Callable[..., ast.expr] | None = getattr(ast_generator, f"create_ast_call_{kind}")
        if each_func is None:
            raise RuntimeError(f"No function to emit {kind}")
        return each_func(target)

    def emit_list_internal(lst: list[typing.Any], kind: str) -> str:
        return emit_list([to_code(el, kind) for el in lst])

    def emit_set_internal(lst: list[typing.Any], kind: str) -> str:
        return emit_set([to_code(el, kind) for el in lst])

    def emit_dict_internal(dct: list[tuple[typing.Any, typing.Any]], kind_key: str, kind_value: str) -> str:
        return emit_dict(list(zip(
            [to_code(k, kind_key) for k, _ in dct],
            [to_code(v, kind_value) for _, v in dct]
        )))

    return {
        "to_code": to_code,
        "emit_list": emit_list_internal,
        "emit_set": emit_set_internal,
        "emit_dict": emit_dict_internal,
    }


class CrossCodeJinjaExtensionBase(Extension):
    """
    Abstract class serving as a basis for this module's jinja extension. It provides filters to be used by this
    APWorld's template files.

    This has to be abstract because the Jinja API seems to require all extensions to be passed in by type, not by
    instance. Use this module's `create_jinja_extension` function to create a concrete type.
    """
    _ast_generator: AstGenerator

    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.filters.update(create_filters(self._ast_generator))

def create_jinja_extension(ast_generator: AstGenerator) -> type[Extension]:
    """
    Generates a concrete instance of this module's `CrossCodeJinjaExtensionBase`
    """

    class CrossCodeJinjaExtension(CrossCodeJinjaExtensionBase):
        _ast_generator = ast_generator

    return CrossCodeJinjaExtension

import ast
import typing

from ..types.world import WorldData

def emit_list(lst: list[ast.AST], indent: str = "    ") -> str:
    after = ",\n"

    return "[\n" + "".join([indent + ast.unparse(item) + after for item in lst]) + "]"

def emit_dict(items: list[tuple[ast.AST, ast.AST]], indent: str = "    ") -> str:
    after = ",\n"

    return "{\n" + "".join([f"{indent}{ast.unparse(key)}: {ast.unparse(value)}{after}" for key, value in items]) + "}"

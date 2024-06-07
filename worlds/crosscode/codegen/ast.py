import typing
import ast

from ..types.condition import Condition
from ..types.locations import AccessInfo, LocationData
from ..types.regions import RegionConnection
from ..types.items import ItemData, ItemPoolEntry, ProgressiveChainEntry, SingleItemData


class AstGenerator:
    def create_ast_call_condition(self, condition: Condition) -> ast.Call:
        result = ast.Call(
            func=ast.Name(condition.__class__.__name__),
            args=[],
            keywords=[ast.keyword(arg=key, value=ast.Constant(value)) for key, value in condition.__dict__.items()],
        )
        ast.fix_missing_locations(result)

        return result

    def create_ast_call_condition_list(self, conditions: typing.Optional[list[Condition]]) -> ast.expr:
        if conditions is None:
            return ast.Constant(None)
        result = ast.List(elts=[])

        for condition in conditions:
            result.elts.append(self.create_ast_call_condition(condition))

        ast.fix_missing_locations(result)
        return result

    def create_ast_call_location(self, data: LocationData) -> ast.Call:
        ast_item = ast.Call(
            func=ast.Name("LocationData"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="code",
                    value=ast.Constant(data.code)
                ),
                ast.keyword(
                    arg="name",
                    value=ast.Constant(data.name)
                ),
            ]
        )

        if data.area is not None:
            ast_item.keywords.append(ast.keyword(arg="area", value=ast.Constant(data.area)))

        if data.metadata is not None:
            ast_item.keywords.append(ast.keyword(
                arg="metadata",
                value=ast.Dict(
                    keys=[ast.Constant(x) for x in data.metadata.keys()],
                    values=[ast.Constant(x) for x in data.metadata.values()],
                )
            ))

        if data.access is not None:
            ast_item.keywords.append(ast.keyword("access", self.create_ast_call_access_info(data.access)))

        ast.fix_missing_locations(ast_item)
        return ast_item

    def create_ast_call_single_item(self, data: SingleItemData):
        ast_item = ast.Call(
            func=ast.Name("SingleItemData"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="item_id",
                    value=ast.Constant(data.item_id)
                ),
                ast.keyword(
                    arg="name",
                    value=ast.Constant(data.name)
                ),
                ast.keyword(
                    arg="classification",
                    value=ast.Attribute(
                        value=ast.Name("ItemClassification"),
                        attr=data.classification.name
                    )
                ),
            ]
        )

        if data.unique:
            ast_item.keywords.append(ast.keyword(
                arg="unique",
                value=ast.Constant(True)
            ))

        ast.fix_missing_locations(ast_item)
        return ast_item

    def create_ast_call_item(self, data: ItemData):
        ast_item = ast.Call(
            func=ast.Name("ItemData"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="item",
                    value=ast.Subscript(
                        value=ast.Name("single_items_dict"),
                        slice=ast.Constant(data.item.name),
                        ctx=ast.Load()
                    )
                ),
                ast.keyword(
                    arg="amount",
                    value=ast.Constant(data.amount)
                ),
                ast.keyword(
                    arg="combo_id",
                    value=ast.Constant(data.combo_id)
                )
            ]
        )
        ast.fix_missing_locations(ast_item)
        return ast_item

    def create_ast_call_item_ref(self, data: ItemData):
        ast_item = ast.Subscript(
            value=ast.Name("items_dict"),
            slice=ast.Tuple(elts=[
                ast.Constant(data.item.name),
                ast.Constant(data.amount)]
            ),
            ctx=ast.Load()
        )
        ast.fix_missing_locations(ast_item)
        return ast_item

    def create_ast_call_progressive_chain_entry(self, entry: ProgressiveChainEntry):
        ast_item = ast.Call(
            func=ast.Name("ProgressiveChainEntry"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="item",
                    value=self.create_ast_call_item_ref(entry.item),
                ),
            ]
        )

        if entry.metadata is not None:
            keys = [ast.Constant(k) for k in entry.metadata.keys()]
            values = [ast.Constant(k) for k in entry.metadata.values()]

            ast_item.keywords.append(ast.keyword(
                arg="metadata",
                value=ast.Dict(
                    keys=keys,
                    values=values,
                )
            ))

        ast.fix_missing_locations(ast_item)
        return ast_item

    def create_ast_call_item_pool_entry(self, entry: ItemPoolEntry):
        ast_item = ast.Call(
            func=ast.Name("ItemPoolEntry"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="item",
                    value=self.create_ast_call_item_ref(entry.item),
                ),
                ast.keyword(
                    arg="quantity",
                    value=ast.Constant(entry.quantity)
                ),
            ]
        )

        if entry.metadata is not None:
            keys = [ast.Constant(k) for k in entry.metadata.keys()]
            values = [ast.Constant(k) for k in entry.metadata.values()]

            ast_item.keywords.append(ast.keyword(
                arg="metadata",
                value=ast.Dict(
                    keys=keys,
                    values=values,
                )
            ))

        ast.fix_missing_locations(ast_item)
        return ast_item
        
    def create_ast_call_region_connection(self, conn: RegionConnection):
        ast_region = ast.Call(
            func=ast.Name("RegionConnection"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="region_from",
                    value=ast.Constant(conn.region_from)
                ),
                ast.keyword(
                    arg="region_to",
                    value=ast.Constant(conn.region_to)
                ),
                ast.keyword(
                    arg="cond",
                    value=self.create_ast_call_condition_list(conn.cond)
                ),
            ]
        )

        ast.fix_missing_locations(ast_region)

        return ast_region

    def create_ast_call_access_info(self, access: AccessInfo):
        ast_call = ast.Call(
            func=ast.Name("AccessInfo"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="region",
                    value=ast.Constant(access.region)
                ),
            ]
        )

        if access.clearance != "Default":
            ast_call.keywords.append(ast.keyword("clearance", ast.Constant(access.clearance)))

        if access.cond is not None and access.cond != []:
            ast_call.keywords.append(ast.keyword("cond", self.create_ast_call_condition_list(access.cond)))

        ast.fix_missing_locations(ast_call)

        return ast_call

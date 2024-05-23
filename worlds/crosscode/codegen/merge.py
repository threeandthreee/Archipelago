import typing

T = typing.TypeVar("T", dict[str, typing.Any], list)

def __replace(_, addon) -> typing.Any:
    return addon

def __find(original, addon: dict[str, typing.Any]) -> typing.Any:
    it: typing.Optional[typing.Iterable[typing.Tuple[typing.Any, typing.Any]]] = None
    if "content" not in addon:
        raise RuntimeError("FIND was not given content")

    if isinstance(original, dict):
        it = original.items()
    elif isinstance(original, list):
        it = enumerate(original)

    if it is None:
        raise RuntimeError("Cannot replace non-iterable")

    query = addon["query"]
    content = addon["content"]

    for key, orig_value in it:
        if type(orig_value) != type(query):
            continue

        matches = False
        if isinstance(query, dict):
            for query_key in query:
                if query_key not in orig_value or orig_value[query_key] != query[query_key]:
                    break
            else:
                matches = True
        elif orig_value == query:
            matches = True

        if not matches:
            continue

        if addon["mode"] == "merge":
            original[key] = merge(original[key], content)
            return original
        elif addon["mode"] == "replace":
            original[key] = content
            return original

        break

__funcs: dict[str, typing.Callable[[typing.Any, dict[str, typing.Any]], typing.Any]] = {
    "REPLACE": __replace,
    "FIND": __find,
}

def diff_one(original: T, addon, name) -> T:
    try:
        func = __funcs[name]
    except KeyError:
        raise RuntimeError("Unknown action '{name}'")

    return func(original, addon)

def diff(original: T, addonList) -> T:
    if isinstance(addonList, list):
        for addon in addonList:
            name = addon["action"]
            diff_one(original, addon, name)
        return original
    elif isinstance(addonList, dict):
        name = addonList["action"]
        return diff_one(original, addonList, name)

    raise RuntimeError(f"Cannot apply diff of type {type(addonList)}")

def merge(original: T, addon: T, apply_diffs=True) -> T:
    if isinstance(original, dict):
        if not isinstance(addon, dict):
            raise RuntimeError(f"Cannot merge type {type(original)} with {type(addon)}")

        for key, value in addon.items():
            splitkey = key.split('::')
            if len(splitkey) == 1 or not apply_diffs:
                if key not in original:
                    original[key] = value
                else:
                    merge(original[key], addon[key])
            elif len(splitkey) == 2:
                realkey, func = splitkey

                if func == "DIFF":
                    original[realkey] = diff(original[realkey], value)
                else:
                    original[realkey] = diff_one(original[realkey], value, func)
            else:
                raise RuntimeError(f"Malformed key '{key}'")

        return original

    if isinstance(original, list):
        if not isinstance(addon, list):
            raise RuntimeError(f"Cannot merge type {type(original)} with {type(addon)}")
        original.extend(addon)

        return original

    else:
        raise RuntimeError(f"Type {type(original)} cannot be merged")

import re
import typing

T = typing.TypeVar("T", dict[str, typing.Any], list)

def merge(original: T, addon: T, patch=True) -> T:
    if isinstance(original, dict):
        if not isinstance(addon, dict):
            raise RuntimeError(f"Cannot merge type {type(original)} with {type(addon)}")

        for key, value in addon.items():
            # regex key. we'll want to match it against all other keys.
            if patch and key == "*":
                for key2, value2 in original.items():
                    merge(value2, value, patch)

            # glob key. matches every single other key.
            elif patch and key[0] == "/" and key[-1] == "/":
                pattern = re.compile(key[1:-1])

                for key2, value2 in original.items():
                    if pattern.match(key2):
                        merge(value2, value, patch)
            
            # normal key. we just want to get that key and merge it.
            elif key not in original:
                original[key] = value
            else:
                merge(original[key], addon[key], patch)

        return original

    if isinstance(original, list):
        if not isinstance(addon, list):
            raise RuntimeError(f"Cannot merge type {type(original)} with {type(addon)}")
        original.extend(addon)

        return original

    else:
        raise RuntimeError(f"Type {type(original)} cannot be merged")

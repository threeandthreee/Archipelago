from worlds.ff6wc.Options import Flagstring


def test_parser() -> None:
    fs = Flagstring("-a b c d -e f -g")

    assert fs.has_flag("-a"), f"{fs.value=}"
    assert fs.has_flag("-e"), f"{fs.value=}"
    assert fs.has_flag("-g"), f"{fs.value=}"

    assert not fs.has_flag("b"), f"{fs.value=}"
    assert not fs.has_flag("b c d"), f"{fs.value=}"
    assert not fs.has_flag("f"), f"{fs.value=}"

    assert fs.get_flag("-a") == "b c d", f"{fs.value=}"
    assert fs.get_flag("-e") == "f", f"{fs.value=}"
    assert fs.get_flag("-g") == "", f"{fs.value=}"


def test_no_hyphen_start() -> None:
    fs = Flagstring("a b c d -e f -g")

    assert not fs.has_flag("-a"), f"{fs.value=}"
    assert fs.has_flag("-e"), f"{fs.value=}"
    assert fs.has_flag("-g"), f"{fs.value=}"

    assert not fs.has_flag("b"), f"{fs.value=}"
    assert not fs.has_flag("b c d"), f"{fs.value=}"
    assert not fs.has_flag("f"), f"{fs.value=}"

    assert fs.get_flag("-e") == "f", f"{fs.value=}"
    assert fs.get_flag("-g") == "", f"{fs.value=}"

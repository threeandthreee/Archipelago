import json
from typing import Any

from BaseClasses import CollectionState


# In the .jsonc files we use, a location or region connection's "access rule" is defined
# by a "requires" key, whose value is an array of "criteria" strings or objects.
# These rules are designed to be evaluated by both this Python code and
# (in the future) the game mod's C# code for the in-game tracker.

# In particular: this eval_rule() function is the main piece of code which will have to
# be implemented in both languages, so it's important we keep the implementations in sync


def eval_rule(state: CollectionState, p: int, rule: [Any]) -> bool:
    return all(eval_criterion(state, p, criterion) for criterion in rule)


def eval_criterion(state: CollectionState, p: int, criterion: Any) -> bool:
    # all valid criteria are dicts
    if isinstance(criterion, dict):
        # we're only using JSON objects / Python dicts here as discriminated unions,
        # so there should always be exactly one key-value pair
        if len(criterion.items()) != 1:
            return False
        key, value = next(iter(criterion.items()))

        # { "item": "..." } and { "anyOf": [ ... ] } and { "location": "foo" } and { "region": "bar" }
        # mean exactly what they sound like, and those are the only kinds of criteria.
        if key == "item" and isinstance(value, str):
            return state.has(value, p)
        elif key == "anyOf" and isinstance(value, list):
            return any(eval_criterion(state, p, sub_criterion) for sub_criterion in value)
        elif key == "location" and isinstance(value, str):
            return state.can_reach(value, "Location", p)
        elif key == "region" and isinstance(value, str):
            return state.can_reach(value, "Region", p)

    raise ValueError("Unable to evaluate rule criterion: " + json.dumps(criterion))

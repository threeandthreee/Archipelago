from math import ceil


def getRequiredCount(total, percentage, round_method=ceil):
    required_count = round_method(total * percentage / 100)
    if required_count == 0:
        required_count += 1

    return int(required_count)
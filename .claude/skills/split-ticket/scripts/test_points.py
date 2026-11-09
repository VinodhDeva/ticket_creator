#!/usr/bin/env python3
from points import estimate, to_points

SCALE = [1, 2, 3, 5, 8]
TEAM = {"days_per_point": 1.5, "scale": SCALE, "max_points": 5}

assert to_points(1.5, 1.5, SCALE) == 1
assert to_points(1.6, 1.5, SCALE) == 2
assert to_points(4.5, 1.5, SCALE) == 3
assert to_points(0.6, 0.2, SCALE) == 3  # float noise must not round up to 5
assert to_points(13, 1.5, SCALE) is None  # beyond the largest scale value

for bad in (0, -1):
    try:
        to_points(bad, 1.5, SCALE)
    except ValueError:
        pass
    else:
        raise AssertionError(f"days={bad} should be rejected")

result = estimate([{"title": "a", "days": 3}, {"title": "b", "days": 8}, {"title": "c", "days": 20}], TEAM)
assert [i["points"] for i in result["items"]] == [2, 8, None]
assert [i["needs_split"] for i in result["items"]] == [False, True, True]
assert result["total_points"] == 10
assert result["capacity_days"] == 15

print("ok")

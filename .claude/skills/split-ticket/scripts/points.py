#!/usr/bin/env python3
"""Convert day estimates to story points. Usage: points.py TEAM.json < plan.json"""
import json
import sys


def to_points(days, days_per_point, scale):
    """Return the smallest scale value covering days, or None if the scale is too small."""
    if days <= 0:
        raise ValueError(f"days must be positive, got {days}")
    # Float noise (0.6 / 0.2 = 3.0000000000000004) must not bump a ticket up a scale step.
    raw = round(days / days_per_point, 6)
    return next((s for s in sorted(scale) if s >= raw), None)


def estimate(plan, team):
    days_per_point, scale, max_points = team["days_per_point"], team["scale"], team["max_points"]
    if days_per_point <= 0 or not scale:
        raise ValueError("team needs days_per_point > 0 and a non-empty scale")

    items = []
    for item in plan:
        points = to_points(item["days"], days_per_point, scale)
        items.append({**item, "points": points, "needs_split": points is None or points > max_points})

    total_points = sum(i["points"] or 0 for i in items)
    return {
        "items": items,
        "total_days": sum(i["days"] for i in items),
        "total_points": total_points,
        # Rounding up to the scale makes this higher than total_days.
        "capacity_days": total_points * days_per_point,
    }


def main():
    try:
        with open(sys.argv[1]) as f:
            team = json.load(f)
        result = estimate(json.load(sys.stdin), team)
    except (IndexError, OSError, KeyError, TypeError, ValueError) as e:
        sys.exit(f"points.py: {e!r}")
    print(json.dumps(result, indent=2))
    if any(i["needs_split"] for i in result["items"]):
        sys.exit(2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Check opaque sRGB colour-pair contrast, not complete game accessibility."""

import argparse
import json
import math
import re
import sys


def luminance(colour):
    if not isinstance(colour, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", colour):
        raise ValueError("colour must be opaque sRGB #RRGGBB; alpha is unsupported")
    channels = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in channels]
    return sum(v * w for v, w in zip(linear, (0.2126, 0.7152, 0.0722)))


def check(foreground, background, minimum=4.5):
    if isinstance(minimum, bool) or not isinstance(minimum, (int, float)) or not 1 <= minimum <= 21 or not math.isfinite(minimum):
        raise ValueError("minimum must be finite and between 1 and 21")
    first, second = luminance(foreground), luminance(background)
    ratio = (max(first, second) + 0.05) / (min(first, second) + 0.05)
    return {
        "kind": "calculated_colour_pair", "foreground": foreground,
        "background": background, "ratio": ratio, "minimum": minimum,
        "meets_selected_minimum": ratio >= minimum,
        "assumptions": ["Opaque sRGB colours", "Uniform background", "Unrounded comparison"],
        "limitations": "Not an accessibility certificate; ignores text size, alpha, gradients, motion, focus and actual rendering.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--foreground", required=True)
    parser.add_argument("--background", required=True)
    parser.add_argument("--minimum", type=float, default=4.5,
                        help="Chosen design threshold, default 4.5 from WCAG ordinary text; native game use is a benchmark")
    args = parser.parse_args()
    try:
        result = check(args.foreground, args.background, args.minimum)
    except ValueError as exc:
        print("Input error: %s" % exc, file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["meets_selected_minimum"] else 1


if __name__ == "__main__":
    sys.exit(main())

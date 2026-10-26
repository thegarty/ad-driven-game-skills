# Colour-pair helper

From this skill's directory:

```sh
python3 scripts/contrast_check.py --foreground '#FFFFFF' --background '#12372A'
python3 scripts/contrast_check.py --foreground '#777777' --background '#FFFFFF' --minimum 4.5
```

The second command deliberately fails the chosen threshold (exit 1). Exit 0
means the pair passes; exit 2 means invalid input. Hex colours need shell quotes
because `#` may otherwise start a comment. Only opaque six-digit sRGB is accepted.

The helper converts channels to linear light, calculates relative luminance and
uses `(lighter + 0.05) / (darker + 0.05)`. It compares the unrounded ratio. White
against black returns 21; identical colours return 1. Inputs are explicit design
colours, not sampled observations from a device screenshot.

The default 4.5 is WCAG's ordinary-text benchmark. WCAG is a web standard; this
check alone does not certify a native game. Choosing another threshold needs a
stated reason. Alpha, gradients, imagery, glyph rendering, small text, colour-only
meaning and animation need separate checks. Place a stable surface behind text
on busy art and inspect real devices, large text, focus and selected states.

Formula/criterion verified 2026-10-26: [W3C relative luminance](https://www.w3.org/TR/WCAG22/#dfn-relative-luminance)
and [Understanding contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

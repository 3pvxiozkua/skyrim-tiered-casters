#!/usr/bin/env python3
"""Sanity-check every _DISTR.ini in this project before it ships.

This does not talk to the game. It checks the things that are cheap to check
offline and expensive to discover in a live playthrough:

  * the line shape (FormType = a|b|c|d|e|f|g) and the field count
  * the level-filter grammar, including the school index range
  * the trait-filter grammar
  * the chance value, including the deterministic "!" suffix
  * duplicate identical lines, which SPID would apply twice

Anything SPID itself would only warn about at runtime (an EditorID that is not
in the load order) is out of scope here - that shows up in
po3_SpellPerkItemDistributor.log.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

FORM_TYPES = {
    "Form", "Spell", "LevSpell", "Perk", "Item", "Shout", "Package",
    "Outfit", "SleepOutfit", "Keyword", "Faction", "Skin",
}

LEVEL_TOKEN = re.compile(r"^(w?\d+(\(\d+(/\d*)?\))?|\d+(/\d*)?)$")
# One trait segment: optional +/- modifier followed by exactly one trait letter.
# Documented traits: F Female, M Male, U Unique, S Summonable, C Child,
# L Leveled, T Teammate, D Dead (7.2+).
TRAIT_SEGMENT = re.compile(r"^[-+]?[FMUSCLTD]$")
CHANCE = re.compile(r"^\d+(\.\d+)?!?$")


def check_level_field(value, errors, where):
    if value in ("", "NONE"):
        return
    tokens = [t.strip() for t in value.split(",")]
    level_seen = 0
    for token in tokens:
        if not LEVEL_TOKEN.match(token):
            errors.append("%s: unparseable level/skill token %r" % (where, token))
            continue
        if "(" in token:
            index = int(re.match(r"^w?(\d+)", token).group(1))
            if index > 17:
                errors.append("%s: school index %d is out of range (0-17)" % (where, index))
            inner = token[token.index("(") + 1:-1]
            if "/" in inner:
                lo, hi = inner.split("/", 1)
                if hi and int(hi) < int(lo):
                    errors.append("%s: skill range %r is inverted" % (where, token))
        else:
            level_seen += 1
    if level_seen > 1:
        errors.append("%s: %d level expressions, SPID only honours the last one"
                      % (where, level_seen))


def check_traits(value, errors, where):
    if value in ("", "NONE"):
        return
    # Traits are "/"-separated and all must match; each may carry its own modifier,
    # so "-U/-C/-T" (not unique AND not a child AND not a teammate) is legal.
    for segment in value.split("/"):
        if not TRAIT_SEGMENT.match(segment.strip()):
            errors.append("%s: unparseable trait segment %r in %r"
                          % (where, segment, value))
            return


def check_file(path):
    errors = []
    lines_seen = {}
    entries = 0
    with open(path, encoding="utf-8") as fh:
        raw = fh.read().splitlines()

    for number, line in enumerate(raw, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith(";"):
            continue
        where = "%s:%d" % (os.path.basename(path), number)
        if "=" not in stripped:
            errors.append("%s: not a key = value line: %r" % (where, stripped))
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if key not in FORM_TYPES:
            errors.append("%s: unknown form type %r" % (where, key))
            continue
        fields = [f.strip() for f in value.split("|")]
        if len(fields) > 7:
            errors.append("%s: %d fields, the format allows 7" % (where, len(fields)))
        if not fields[0]:
            errors.append("%s: empty form reference" % where)
            continue
        while len(fields) < 7:
            fields.append("")
        check_level_field(fields[3], errors, where)
        check_traits(fields[4], errors, where)
        if fields[6] and not CHANCE.match(fields[6]):
            errors.append("%s: unparseable chance %r" % (where, fields[6]))
        elif fields[6]:
            value_float = float(fields[6].rstrip("!"))
            if value_float < 0 or value_float > 100:
                errors.append("%s: chance %r outside 0-100" % (where, fields[6]))
        signature = "|".join(fields)
        if signature in lines_seen:
            errors.append("%s: duplicate of line %d" % (where, lines_seen[signature]))
        else:
            lines_seen[signature] = number
        entries += 1

    return entries, errors


def main():
    targets = []
    for sub in ("src/Presets", "src/Modules"):
        folder = os.path.join(ROOT, sub)
        if not os.path.isdir(folder):
            continue
        for name in sorted(os.listdir(folder)):
            if name.endswith("_DISTR.ini"):
                targets.append(os.path.join(folder, name))

    if not targets:
        print("no _DISTR.ini files found")
        return 1

    total = 0
    failures = 0
    for path in targets:
        entries, errors = check_file(path)
        total += entries
        status = "ok" if not errors else "FAIL"
        print("%-42s %3d lines  %s" % (os.path.basename(path), entries, status))
        for error in errors:
            print("    ! %s" % error)
        failures += len(errors)

    print("\n%d files, %d distribution lines, %d problems" % (len(targets), total, failures))
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())

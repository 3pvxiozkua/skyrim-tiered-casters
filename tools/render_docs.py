#!/usr/bin/env python3
"""Render docs/FORMS.md from tools/spec.json so the reference table can never
disagree with the configs that actually ship."""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    with open(os.path.join(HERE, "spec.json"), encoding="utf-8") as fh:
        spec = json.load(fh)

    out = []
    out.append("# Record reference")
    out.append("")
    out.append("Every form this mod distributes, what it is, and why it is there. All of them are")
    out.append("vanilla `Skyrim.esm` records referenced by **EditorID** rather than FormID.")
    out.append("")
    out.append("That choice is deliberate: EditorIDs are resolved by SPID against whatever is loaded,")
    out.append("so a game update that renumbers records cannot break these lines, and the configs stay")
    out.append("readable without an xEdit session. If a line ever fails to resolve, SPID logs it and")
    out.append("skips that one line - nothing else in the file is affected.")
    out.append("")
    out.append("## Archetype tables")
    out.append("")

    for arch in spec["archetypes"]:
        out.append("### %s" % arch["title"])
        out.append("")
        out.append("Matched by string filter `%s`." % arch["match"])
        out.append("")
        out.append(arch["blurb"])
        out.append("")
        out.append("| EditorID | School | Skill floor | Level floor | Tier | Chance | Why |")
        out.append("| --- | --- | --- | --- | --- | --- | --- |")
        for line in arch["lines"]:
            out.append("| `%s` | %s | %d | %d | %d | %d%% | %s |"
                       % (line["spell"], line["school"], line["skill"], line["level"],
                          line["tier"], line["chance"], line["why"]))
        out.append("")

    out.append("## Optional modules")
    out.append("")
    for module in spec["modules"]:
        out.append("### %s" % module["title"])
        out.append("")
        out.append(module["blurb"])
        out.append("")
        out.append("| EditorID | School | Skill floor | Chance | Why |")
        out.append("| --- | --- | --- | --- | --- |")
        for line in module["lines"]:
            out.append("| `%s` | %s | %d | %d%% | %s |"
                       % (line["spell"], line["school"], line["skill"], line["chance"], line["why"]))
        out.append("")

    spells = []
    for arch in spec["archetypes"]:
        for line in arch["lines"]:
            if line["spell"] not in spells:
                spells.append(line["spell"])
    for module in spec["modules"]:
        for line in module["lines"]:
            if line["spell"] not in spells:
                spells.append(line["spell"])

    out.append("## Unique forms used")
    out.append("")
    out.append("`%d` distinct spell records, no items, no perks, no keywords, no new records." % len(spells))
    out.append("")
    out.append("```")
    for spell in sorted(spells):
        out.append(spell)
    out.append("```")
    out.append("")
    out.append("Tiers follow the game's own progression: 1 apprentice, 2 apprentice/adept,")
    out.append("3 adept/expert, 4 expert. No master-tier spell is distributed - those are ritual")
    out.append("spells in vanilla and handing them to a random warlock reads as a bug.")
    out.append("")

    path = os.path.join(ROOT, "docs", "FORMS.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print("wrote %s (%d spells)" % (os.path.relpath(path, ROOT), len(spells)))


if __name__ == "__main__":
    main()

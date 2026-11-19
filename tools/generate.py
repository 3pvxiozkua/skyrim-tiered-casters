#!/usr/bin/env python3
"""Build the SPID _DISTR.ini files for Tiered Casters from one table.

Every distribution line in this mod is generated from the SPEC below so that the
three difficulty presets can never drift apart from each other.

School indices are Skyrim's own actor-value order, which is what SPID's skill
filter expects:
    12 Alteration | 13 Conjuration | 14 Destruction | 15 Illusion | 16 Restoration
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MOD_NAME = "Tiered Casters"
VERSION = "1.0.0"

# Traits applied to every archetype line: not unique, not a child, not a teammate.
TRAITS = "-U/-C/-T"

SCHOOL = {
    12: "Alteration",
    13: "Conjuration",
    14: "Destruction",
    15: "Illusion",
    16: "Restoration",
}

# ---------------------------------------------------------------------------
# Archetypes. "match" is an SPID string filter (NPC name or EditorID, * = wildcard).
# "tier" is a rough power band so presets can cap how deep a distribution goes:
#   1 novice/apprentice, 2 apprentice/adept, 3 adept/expert, 4 expert
# ---------------------------------------------------------------------------
ARCHETYPES = [
    {
        "id": "necromancer",
        "title": "Necromancer",
        "match": "*Necromancer",
        "blurb": "Vanilla necromancers lean on Conjuration and Destruction but only ever "
                 "carry the opening spells of both schools.",
        "lines": [
            ("ConjureFamiliar", 13, 25, 10, 1, 70, "first summon, so a fresh necromancer has a bodyguard"),
            ("Firebolt", 14, 30, 12, 1, 70, "replaces Flames as the default attack"),
            ("RaiseZombie", 13, 40, 18, 2, 60, "starts recycling the corpses the player leaves behind"),
            ("IceSpike", 14, 40, 20, 2, 60, "second element, so fights are not all fire"),
            ("ConjureFlameAtronach", 13, 50, 28, 3, 55, "mid-game summon"),
            ("Fireball", 14, 55, 30, 3, 55, "area pressure once Destruction is trained"),
            ("Incinerate", 14, 70, 45, 4, 45, "expert tier, reserved for late-game casters"),
        ],
    },
    {
        "id": "warlock",
        "title": "Warlock",
        "match": "*Warlock",
        "blurb": "Shock specialists. Vanilla warlocks never get past Lightning Bolt, and they "
                 "never use the armour spells their Alteration skill pays for.",
        "lines": [
            ("LightningBolt", 14, 30, 10, 1, 70, "core attack"),
            ("Stoneflesh", 12, 30, 14, 1, 55, "survives the first arrow volley"),
            ("ChainLightning", 14, 50, 26, 3, 55, "punishes players who bring followers"),
            ("Ironflesh", 12, 55, 34, 3, 45, "armour spell upgrade"),
            ("Thunderbolt", 14, 70, 45, 4, 45, "expert tier"),
        ],
    },
    {
        "id": "conjurer",
        "title": "Conjurer",
        "match": "*Conjurer",
        "blurb": "Pure summoners. Their whole identity is the summon list, and vanilla stops it "
                 "at Flame Atronach.",
        "lines": [
            ("ConjureFamiliar", 13, 25, 8, 1, 75, "always-on opening summon"),
            ("ConjureFlameAtronach", 13, 40, 18, 2, 60, "second summon tier"),
            ("ConjureFrostAtronach", 13, 55, 28, 3, 50, "third summon tier"),
            ("ConjureStormAtronach", 13, 70, 40, 4, 40, "top summon tier"),
        ],
    },
    {
        "id": "forsworn-shaman",
        "title": "Forsworn Shaman",
        "match": "*Shaman",
        "blurb": "Reach shamans are Restoration/Illusion casters in the lore and single-school "
                 "spell plinkers in the game.",
        "lines": [
            ("Oakflesh", 12, 25, 8, 1, 55, "cheap early defence"),
            ("FastHealing", 16, 25, 10, 1, 65, "heals through the first burst of damage"),
            ("Fury", 15, 25, 12, 1, 55, "turns the camp against itself"),
            ("CloseWounds", 16, 50, 25, 3, 50, "mid-game sustain"),
            ("Fear", 15, 50, 28, 3, 45, "crowd control"),
            ("Ironflesh", 12, 60, 35, 4, 40, "late-game defence"),
        ],
    },
    {
        "id": "vampire",
        "title": "Vampire",
        "match": "*Vampire",
        "blurb": "Vampires get frost and drain only. Higher ranks should feel like predators, "
                 "not like bandits with fangs.",
        "lines": [
            ("Fear", 15, 25, 15, 1, 50, "predator opening"),
            ("RaiseZombie", 13, 40, 25, 2, 40, "raises the bodies in the room"),
            ("IceStorm", 14, 45, 28, 3, 45, "area frost"),
            ("IcySpear", 14, 65, 45, 4, 40, "expert tier"),
        ],
    },
    {
        "id": "pyromancer",
        "title": "Pyromancer",
        "match": "*Pyromancer",
        "blurb": "Elemental specialists whose name already promises a full spell line.",
        "lines": [
            ("Firebolt", 14, 25, 12, 1, 70, "fire line, tier 1"),
            ("Fireball", 14, 45, 25, 2, 60, "fire line, tier 2"),
            ("Incinerate", 14, 65, 40, 4, 50, "fire line, tier 3"),
        ],
    },
    {
        "id": "cryomancer",
        "title": "Cryomancer",
        "match": "*Cryomancer",
        "blurb": "Frost line, mirroring the pyromancer table.",
        "lines": [
            ("IceSpike", 14, 25, 12, 1, 70, "frost line, tier 1"),
            ("IceStorm", 14, 45, 25, 2, 60, "frost line, tier 2"),
            ("IcySpear", 14, 65, 40, 4, 50, "frost line, tier 3"),
        ],
    },
    {
        "id": "electromancer",
        "title": "Electromancer",
        "match": "*Electromancer",
        "blurb": "Shock line, mirroring the pyromancer table.",
        "lines": [
            ("LightningBolt", 14, 25, 12, 1, 70, "shock line, tier 1"),
            ("ChainLightning", 14, 45, 25, 2, 60, "shock line, tier 2"),
            ("Thunderbolt", 14, 65, 40, 4, 50, "shock line, tier 3"),
        ],
    },
]

# ---------------------------------------------------------------------------
# Presets only change three numbers: how deep the tiers go, how much the level
# floor shifts, and how the chance is scaled. Nothing else is preset-dependent.
# ---------------------------------------------------------------------------
PRESETS = [
    {
        "id": "vanillaplus",
        "file": "TieredCasters_VanillaPlus_DISTR.ini",
        "title": "Vanilla+",
        "level_delta": 6,
        "chance_mult": 0.75,
        "max_tier": 2,
        "blurb": "Same spell lists as vanilla for most of the game. Only the late-game casters "
                 "get anything new, and only at reduced odds.",
    },
    {
        "id": "standard",
        "file": "TieredCasters_Standard_DISTR.ini",
        "title": "Standard",
        "level_delta": 0,
        "chance_mult": 1.0,
        "max_tier": 4,
        "blurb": "The intended experience: every archetype reaches its full table, gated by "
                 "level and by the skill the spell actually needs.",
    },
    {
        "id": "ruthless",
        "file": "TieredCasters_Ruthless_DISTR.ini",
        "title": "Ruthless",
        "level_delta": -4,
        "chance_mult": 1.25,
        "max_tier": 4,
        "blurb": "Everything arrives four levels earlier and almost always lands. Expect "
                 "expert-tier spells in the thirties.",
    },
]

# ---------------------------------------------------------------------------
# Optional modules. These are installed independently of the preset.
# ---------------------------------------------------------------------------
ALL_CASTERS = ",".join(a["match"] for a in ARCHETYPES)

MODULES = [
    {
        "id": "healers",
        "file": "TieredCasters_Healers_DISTR.ini",
        "title": "Restoration Self-Heal",
        "blurb": "Casters who actually trained Restoration patch themselves up mid-fight "
                 "instead of standing in the open at 10% health.",
        "lines": [
            ("FastHealing", 16, 40, 35, "any caster with Restoration 40"),
            ("CloseWounds", 16, 60, 25, "any caster with Restoration 60"),
        ],
    },
    {
        "id": "armor",
        "file": "TieredCasters_Armor_DISTR.ini",
        "title": "Alteration Armour Spells",
        "blurb": "The armour-spell ladder, handed out by Alteration skill rather than by "
                 "archetype, so a warlock and a shaman both get what they trained for.",
        "lines": [
            ("Oakflesh", 12, 20, 55, "Alteration 20"),
            ("Stoneflesh", 12, 40, 50, "Alteration 40"),
            ("Ironflesh", 12, 60, 40, "Alteration 60"),
            ("Ebonyflesh", 12, 80, 30, "Alteration 80"),
        ],
    },
    {
        "id": "illusion",
        "file": "TieredCasters_Illusion_DISTR.ini",
        "title": "Illusion Pressure",
        "blurb": "Fury, Fear and Calm handed to the casters whose lore supports them. Off by "
                 "default because fear and calm effects change how a fight reads.",
        "lines": [
            ("Fury", 15, 30, 45, "Illusion 30"),
            ("Fear", 15, 45, 40, "Illusion 45"),
            ("Calm", 15, 60, 25, "Illusion 60"),
        ],
    },
]


def level_filter(level, school, skill):
    """Build the SPID level-filter field: level floor plus a school skill floor.

    A single number means "this value or higher" for both halves of the field, so
    the bare forms `30` and `14(55)` are used rather than `30/` and `14(55/)` -
    both halves of a range are optional in SPID, but an empty upper bound is the
    one form the reference does not spell out.
    """
    return "%d,%d(%d)" % (max(1, level), school, skill)


def spell_line(spell, school, skill, level, chance):
    fields = [
        spell,
        "",  # string filters are filled in per archetype
        "NONE",
        level_filter(level, school, skill),
        TRAITS,
        "1",
        "%d!" % chance,
    ]
    return fields


def header(title, blurb, extra=None):
    lines = [
        "; %s %s - %s" % (MOD_NAME, VERSION, title),
        "; %s" % blurb,
        ";",
        "; Requires: Spell Perk Item Distributor (SPID) 7.x by powerofthree",
        ";   https://www.nexusmods.com/skyrimspecialedition/mods/36869",
        "; Install: drop this file into Skyrim Special Edition/Data (mod managers do it for you).",
        "; Remove: delete this file. Nothing is written to your save.",
        ";",
        "; Line format:",
        ";   Spell = <EditorID>|<string filters>|<form filters>|<level filters>|<traits>|<count>|<chance>",
        ";   - string filters: NPC name or EditorID, * is a wildcard",
        ";   - level filters : <level>,<schoolIndex>(<skill>)  -> both floors must be met",
        ";   - traits        : -U not unique, -C not a child, -T not a teammate",
        ";   - chance        : 0-100, the ! suffix makes the roll deterministic per NPC per save",
        ";",
    ]
    if extra:
        lines.extend("; %s" % line for line in extra)
        lines.append(";")
    return lines


def render_preset(preset):
    out = header(preset["title"] + " preset", preset["blurb"])
    total = 0
    for arch in ARCHETYPES:
        out.append("")
        out.append("; --- %s ---------------------------------------------------------" % arch["title"])
        out.append("; %s" % arch["blurb"])
        for spell, school, skill, level, tier, chance, why in arch["lines"]:
            if tier > preset["max_tier"]:
                continue
            lvl = max(1, level + preset["level_delta"])
            ch = min(100, max(1, int(round(chance * preset["chance_mult"]))))
            out.append(";   %-24s %-12s skill %-3d level %-3d -> %d%%  (%s)"
                       % (spell, SCHOOL[school], skill, lvl, ch, why))
            out.append("Spell = %s|%s|NONE|%s|%s|1|%d!"
                       % (spell, arch["match"], level_filter(lvl, school, skill), TRAITS, ch))
            total += 1
    out.append("")
    out.append("; %d distribution lines in this preset." % total)
    return "\n".join(out) + "\n"


def render_module(module):
    out = header(module["title"], module["blurb"])
    out.append("; Applies to: %s" % ALL_CASTERS)
    out.append("")
    for spell, school, skill, chance, why in module["lines"]:
        out.append(";   %-16s %-12s skill %-3d -> %d%%  (%s)"
                   % (spell, SCHOOL[school], skill, chance, why))
        out.append("Spell = %s|%s|NONE|%d(%d)|%s|1|%d!"
                   % (spell, ALL_CASTERS, school, skill, TRAITS, chance))
    out.append("")
    out.append("; %d distribution lines in this module." % len(module["lines"]))
    return "\n".join(out) + "\n"


def main():
    written = []
    presets_dir = os.path.join(ROOT, "src", "Presets")
    modules_dir = os.path.join(ROOT, "src", "Modules")
    os.makedirs(presets_dir, exist_ok=True)
    os.makedirs(modules_dir, exist_ok=True)

    for preset in PRESETS:
        path = os.path.join(presets_dir, preset["file"])
        with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
            fh.write(render_preset(preset))
        written.append(path)

    for module in MODULES:
        path = os.path.join(modules_dir, module["file"])
        with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
            fh.write(render_module(module))
        written.append(path)

    meta = {
        "mod": MOD_NAME,
        "version": VERSION,
        "archetypes": [
            {
                "id": a["id"],
                "title": a["title"],
                "match": a["match"],
                "blurb": a["blurb"],
                "lines": [
                    {
                        "spell": spell,
                        "school": SCHOOL[school],
                        "skill": skill,
                        "level": level,
                        "tier": tier,
                        "chance": chance,
                        "why": why,
                    }
                    for spell, school, skill, level, tier, chance, why in a["lines"]
                ],
            }
            for a in ARCHETYPES
        ],
        "presets": [
            {k: v for k, v in p.items() if k != "file"} for p in PRESETS
        ],
        "modules": [
            {
                "id": m["id"],
                "title": m["title"],
                "blurb": m["blurb"],
                "lines": [
                    {"spell": s, "school": SCHOOL[school], "skill": skill,
                     "chance": ch, "why": why}
                    for s, school, skill, ch, why in m["lines"]
                ],
            }
            for m in MODULES
        ],
    }
    with open(os.path.join(ROOT, "tools", "spec.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    for path in written:
        print("wrote %s" % os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()

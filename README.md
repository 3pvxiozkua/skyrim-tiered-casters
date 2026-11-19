# Tiered Casters

A Spell Perk Item Distributor config mod for Skyrim Special / Anniversary Edition that gives enemy
casters a spell line matching their level and the school skills they actually trained.

No plugin. No scripts. No SKSE plugin of its own. Six text files, and the game's own spell AI does
the rest.

---

## The problem

Vanilla enemy casters are locked to a fixed spell list for the whole game. A necromancer in a
level 12 barrow and a necromancer in a level 45 ruin carry the same two spells, and both of them are
the spells a level 5 apprentice gets. Meanwhile the caster's *skills* keep climbing with the player,
so a late-game warlock is paying for a Destruction skill of 70 while throwing Lightning Bolt.

The result is a fight that starts interesting and ends up being a damage check against a target
dummy that occasionally sparks.

Tiered Casters fixes the mismatch without touching a single NPC record: SPID hands out the spells,
gated by the caster's own level and the skill that spell belongs to. A caster only gets a spell when
they could plausibly have learned it.

## What it changes

Eight caster archetypes, each with its own table:

| Archetype | Matched by | Schools |
| --- | --- | --- |
| Necromancer | name / EditorID contains `Necromancer` | Conjuration, Destruction |
| Warlock | `Warlock` | Destruction, Alteration |
| Conjurer | `Conjurer` | Conjuration |
| Forsworn Shaman | `Shaman` | Restoration, Illusion, Alteration |
| Vampire | `Vampire` | Illusion, Conjuration, Destruction |
| Pyromancer | `Pyromancer` | Destruction (fire line) |
| Cryomancer | `Cryomancer` | Destruction (frost line) |
| Electromancer | `Electromancer` | Destruction (shock line) |

Example, the necromancer table on the Standard preset:

| Spell | School | Skill floor | Level floor | Chance |
| --- | --- | --- | --- | --- |
| Conjure Familiar | Conjuration | 25 | 10 | 70% |
| Firebolt | Destruction | 30 | 12 | 70% |
| Raise Zombie | Conjuration | 40 | 18 | 60% |
| Ice Spike | Destruction | 40 | 20 | 60% |
| Conjure Flame Atronach | Conjuration | 50 | 28 | 55% |
| Fireball | Destruction | 55 | 30 | 55% |
| Incinerate | Destruction | 70 | 45 | 45% |

Every line in every file is preceded by a comment saying which spell, which school, which floors and
which chance it uses, so retuning is a matter of editing a number.

## What it does not do

- It does not remove spells. A high-level necromancer still knows Flames; they simply also know
  Fireball and Incinerate. If you want the old spells stripped out, that needs a plugin, and this
  mod is deliberately not one.
- It does not touch unique NPCs. `-U` is on every line, so Serana, Dragon Priests, quest bosses and
  named court wizards are left exactly as the game made them.
- It does not touch children (`-C`) or anyone flagged as a teammate (`-T`), so your followers and
  the NPCs a quest hands you are safe.
- It does not touch creatures. Only the eight archetypes above, matched by name.

## Requirements

| Requirement | Notes |
| --- | --- |
| Skyrim Special Edition or Anniversary Edition | SE 1.5.39 or newer. Tested on 1.6.1170 and 1.7.104. |
| [SKSE64](https://skse.silverlock.org/) | The build that matches your game version. |
| [Address Library for SKSE Plugins](https://www.nexusmods.com/skyrimspecialedition/mods/32444) | Version matching your game version. |
| [Spell Perk Item Distributor](https://www.nexusmods.com/skyrimspecialedition/mods/36869) | 7.x recommended. Anything from 6.x up understands every line in this mod. |

Nothing else. No USSEP dependency, no DLC dependency, no master files edited.

Skyrim VR works with the VR build of SPID; the configs are identical.

## Installation

### Mod manager (recommended)

Install the archive with MO2 or Vortex and let the FOMOD run. It asks two things:

1. **Difficulty preset** - Standard (default), Vanilla+, or Ruthless.
2. **Optional modules** - Restoration Self-Heal and Alteration Armour Spells are on by default,
   Illusion Pressure is off.

The installer copies the chosen files straight into `Data`. There is no plugin to enable and no
load order to worry about.

### Manual

Copy the preset you want and any modules you want out of the archive into
`Skyrim Special Edition/Data/`, so they sit next to `Skyrim.esm`:

```
Data/
  TieredCasters_Standard_DISTR.ini
  TieredCasters_Healers_DISTR.ini
  TieredCasters_Armor_DISTR.ini
```

SPID scans `Data` for `*_DISTR.ini` at load. Subfolders work too if your manager handles them, but
flat in `Data` is the safest manual layout.

## Presets

| Preset | Tiers distributed | Level floors | Chances |
| --- | --- | --- | --- |
| Vanilla+ | first two only | +6 levels | x0.75 |
| Standard | all four | unchanged | x1.00 |
| Ruthless | all four | -4 levels | x1.25 |

Vanilla+ is for players who want the mid-game to read as vanilla and only want late-game casters to
surprise them. Ruthless puts expert-tier spells in the mid-thirties.

You can switch presets at any time: delete the old `TieredCasters_*_DISTR.ini` and drop in the new
one. Nothing is baked into your save.

## Optional modules

| Module | Effect |
| --- | --- |
| Restoration Self-Heal | Any caster with Restoration 40 gets Fast Healing (35%), Restoration 60 gets Close Wounds (25%). |
| Alteration Armour Spells | Oakflesh at Alteration 20, Stoneflesh 40, Ironflesh 60, Ebonyflesh 80, applied to every caster archetype. |
| Illusion Pressure | Fury at Illusion 30, Fear 45, Calm 60. Off by default. |

## How the gating works

SPID's level filter field takes two kinds of expression: a level range, and a skill range written as
`<schoolIndex>(<min>/<max>)`. Skyrim's school indices are 12 Alteration, 13 Conjuration,
14 Destruction, 15 Illusion, 16 Restoration. All conditions in that field must be met, so

```
Spell = Fireball|*Necromancer|NONE|30/,14(55/)|-U/-C/-T|1|55!
```

reads as: give Fireball to non-unique, non-child, non-teammate NPCs whose name contains
"Necromancer", who are at least level 30 and have Destruction 55 or better, at a 55% chance.

The `!` after the chance makes the roll deterministic: the same NPC either always gets the spell or
never does, and that decision stays stable across saves. Without it, a caster could gain or lose
Incinerate every time the cell reloads, which looks like a bug.

Level is evaluated against the NPC's calculated level, and SPID 7.2+ distributes when an actorbase
first loads into the world rather than at main menu. A bandit ruin you clear at level 12 and a ruin
you clear at level 40 therefore do not produce the same casters, which is the entire point.

## Verifying that it worked

Open `Documents/My Games/Skyrim Special Edition/SKSE/po3_SpellPerkItemDistributor.log` after a
session. You should see your files listed, a `[Results]` section, and no lines containing
`Unable to find` or `Failed to find`.

In game, the quickest check is a high-level dungeon with a necromancer or a warlock: they should be
throwing Fireball or Chain Lightning, not just Flames and Sparks.

If nothing appears, in order of likelihood:

1. SPID is not installed, or its SKSE plugin did not load (check `SKSE/skse64.log` for
   `SpellPerkItemDistributor.dll`).
2. Your Address Library does not match your game version, which makes SPID fail silently.
3. You are early in the game. Level and skill floors are the point of the mod; at level 8 most
   casters genuinely do not qualify.

## Compatibility

- **Safe to add and remove mid-save.** SPID writes into NPC actorbases at load time and does not
  create records, so removing the files removes the effect. If you remove it mid-save, casters keep
  the spells they were given until their actorbase is rebuilt by the game - start a new cell and
  they are back to vanilla.
- **Load order is irrelevant.** No records are edited, so there is nothing to conflict over.
- **Stacks with other SPID mods.** If you also run Enemy (R)Evolution of Skyrim, NPC Spell Variance
  or similar, the spell sets are added on top of each other, not replaced. If the result is too
  spicy, drop to the Vanilla+ preset rather than uninstalling one of them.
- **Mod-added casters get covered.** Matching is by name and EditorID, so a mod that adds its own
  "Necromancer" enemies gets the same table.
- **Does not interact with** combat overhauls, encounter mods, or anything that edits NPC records;
  it only appends spells to the actorbase at runtime.

## Tuning it yourself

Every file is plain text. Want your necromancers to get Incinerate at level 35 instead of 45? Change
`45/` to `35/` on that line. Want a spell for an archetype this mod does not cover? Add a line:

```
Spell = IceStorm|*Hagraven|NONE|20/,14(40/)|-U/-C/-T|1|60!
```

Keep the seven fields, keep the `|` separators, and check the SPID reference for anything beyond the
filters used here.

## Credits

- **powerofthree** for Spell Perk Item Distributor, without which none of this is possible.
- **meh321** for the Address Library, and the SKSE team for SKSE.
- Bethesda, for the spell list this mod is built out of.

## Permissions

Do what you like with these files: reupload, fork, fold into a modlist, translate, rewrite the
tables. Credit is appreciated, not required. No assets are included that are not plain text.

## Licence

MIT for the config files, the tooling and the documentation. See `LICENSE`.

# Tiered Casters

### Enemy casters finally learn spells that match their level

Vanilla gives every enemy mage a fixed spell list for the entire game. A necromancer guarding a
level 12 barrow and a necromancer guarding a level 45 ruin both carry the same two apprentice
spells, even though their Destruction skill has been climbing the whole time. Tiered Casters hands
out spells through Spell Perk Item Distributor, gated by the caster's own level **and** by the school
skill that spell belongs to, so a caster only gets a spell they could plausibly have learned.

Six text files. No plugin, no scripts, no records edited, nothing to load-order. It cannot conflict
with anything, it cannot dirty your save, and it keeps working after a game update as long as SPID
does.

---

## Features

**Eight caster archetypes, each with its own table**

Necromancer, Warlock, Conjurer, Forsworn Shaman, Vampire, Pyromancer, Cryomancer, Electromancer.
Each one gets spells from the schools its lore actually supports - necromancers summon and burn,
shamans heal and hex, warlocks lean shock and armour spells, pyromancers get the fire line.

**Gated by level and by skill**

Fireball needs level 30 *and* Destruction 55. Incinerate needs level 45 and Destruction 70. A caster
who has not trained the school does not get the spell, no matter how high the player is.

**Deterministic rolls**

Every chance is rolled with SPID's `!` suffix, so a given NPC either always has the spell or never
does, and that answer is stable across saves. No casters flickering between spellbooks on cell
reload.

**Unique NPCs left alone**

`-U/-C/-T` on every line: no unique NPCs, no children, no teammates. Serana, Dragon Priests, named
court wizards and quest bosses keep their hand-built kits. Your followers are never touched.

**Three presets, switchable at any time**

| Preset | What it does |
| --- | --- |
| Vanilla+ | First two tiers only, level floors +6, chances x0.75 |
| Standard | Full tables, as designed |
| Ruthless | Level floors -4, chances x1.25, expert spells in the mid-thirties |

**Three optional modules**

- Restoration Self-Heal - casters patch themselves up mid-fight instead of dying politely.
- Alteration Armour Spells - oakflesh through ebonyflesh, by Alteration skill.
- Illusion Pressure - Fury, Fear and Calm. Off by default.

**FOMOD installer**

Pick a preset, tick the modules, done. Manual install is three file copies if you prefer.

---

## Requirements

- Skyrim Special Edition or Anniversary Edition (SE 1.5.39 and newer; tested on 1.6.1170 and 1.7.104)
- [SKSE64](https://skse.silverlock.org/) matching your game version
- [Address Library for SKSE Plugins](https://www.nexusmods.com/skyrimspecialedition/mods/32444) matching your game version
- [Spell Perk Item Distributor](https://www.nexusmods.com/skyrimspecialedition/mods/36869) 7.x

Skyrim VR works with the VR build of SPID.

---

## Installation

Install with MO2 or Vortex and run the FOMOD. To install manually, copy the preset you want plus any
modules into `Skyrim Special Edition/Data/`:

```
Data/
  TieredCasters_Standard_DISTR.ini
  TieredCasters_Healers_DISTR.ini
  TieredCasters_Armor_DISTR.ini
```

There is no ESP. Nothing to enable. Nothing to sort.

---

## Compatibility

- No records edited, so load order is irrelevant and nothing conflicts.
- Add and remove mid-save freely.
- Stacks with Enemy (R)Evolution of Skyrim, NPC Spell Variance and similar SPID mods - the spell sets
  add up rather than replace each other. If the result is too much, drop to Vanilla+.
- Mod-added casters are covered, because matching is by name and EditorID rather than by FormID.

---

## Checking that it is running

`Documents/My Games/Skyrim Special Edition/SKSE/po3_SpellPerkItemDistributor.log` should list the
files and show a `[Results]` block with no `Unable to find` lines. In game, the fastest test is a
high-level necromancer or warlock: they should be casting Fireball or Chain Lightning.

---

## Changelog

### 1.0.0 - 2026-11-19

- First release.
- Eight archetype tables: Necromancer, Warlock, Conjurer, Forsworn Shaman, Vampire, Pyromancer,
  Cryomancer, Electromancer.
- Three presets: Vanilla+, Standard, Ruthless.
- Three optional modules: Restoration Self-Heal, Alteration Armour Spells, Illusion Pressure.
- FOMOD installer with preset and module selection.
- Deterministic chance rolls throughout, so spellbooks stay stable per NPC.

---

## Credits

powerofthree for Spell Perk Item Distributor. meh321 for the Address Library. The SKSE team.

## Permissions

Reupload, fork, fold into a modlist, translate, rewrite the tables - all fine. Credit appreciated,
not required. MIT licensed.

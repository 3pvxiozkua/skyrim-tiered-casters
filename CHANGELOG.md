# Changelog

## 1.0.0 - 2026-11-19

First release.

**Content**

- Eight archetype tables, each gated by level and by the school skill the spell requires:
  Necromancer (7 lines), Warlock (5), Conjurer (4), Forsworn Shaman (6), Vampire (4),
  Pyromancer (3), Cryomancer (3), Electromancer (3).
- Three presets generated from one table so they cannot drift apart: Vanilla+, Standard, Ruthless.
- Three optional modules: Restoration Self-Heal, Alteration Armour Spells, Illusion Pressure.
- FOMOD installer with one preset step and one module step.

**Engineering**

- `tools/generate.py` builds all six configs from a single spec, so a balance change lands in every
  preset at once.
- `tools/validate_distr.py` checks line shape, level and skill filter grammar, trait grammar, chance
  range and duplicate lines before anything ships.
- `tools/build.py` regenerates, validates, stages and packages the archive.
- All chances use SPID's deterministic `!` suffix so an NPC's spellbook does not change between
  sessions.

**Compatibility**

- No plugin, no scripts, no records edited. Load order irrelevant, mid-save add and remove safe.
- Every distributed form is a vanilla Skyrim.esm record referenced by EditorID, so the configs
  survive plugin updates and do not depend on FormIDs that shift between game versions.

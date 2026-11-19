# Record reference

Every form this mod distributes, what it is, and why it is there. All of them are
vanilla `Skyrim.esm` records referenced by **EditorID** rather than FormID.

That choice is deliberate: EditorIDs are resolved by SPID against whatever is loaded,
so a game update that renumbers records cannot break these lines, and the configs stay
readable without an xEdit session. If a line ever fails to resolve, SPID logs it and
skips that one line - nothing else in the file is affected.

## Archetype tables

### Necromancer

Matched by string filter `*Necromancer`.

Vanilla necromancers lean on Conjuration and Destruction but only ever carry the opening spells of both schools.

| EditorID | School | Skill floor | Level floor | Tier | Chance | Why |
| --- | --- | --- | --- | --- | --- | --- |
| `ConjureFamiliar` | Conjuration | 25 | 10 | 1 | 70% | first summon, so a fresh necromancer has a bodyguard |
| `Firebolt` | Destruction | 30 | 12 | 1 | 70% | replaces Flames as the default attack |
| `RaiseZombie` | Conjuration | 40 | 18 | 2 | 60% | starts recycling the corpses the player leaves behind |
| `IceSpike` | Destruction | 40 | 20 | 2 | 60% | second element, so fights are not all fire |
| `ConjureFlameAtronach` | Conjuration | 50 | 28 | 3 | 55% | mid-game summon |
| `Fireball` | Destruction | 55 | 30 | 3 | 55% | area pressure once Destruction is trained |
| `Incinerate` | Destruction | 70 | 45 | 4 | 45% | expert tier, reserved for late-game casters |

### Warlock

Matched by string filter `*Warlock`.

Shock specialists. Vanilla warlocks never get past Lightning Bolt, and they never use the armour spells their Alteration skill pays for.

| EditorID | School | Skill floor | Level floor | Tier | Chance | Why |
| --- | --- | --- | --- | --- | --- | --- |
| `LightningBolt` | Destruction | 30 | 10 | 1 | 70% | core attack |
| `Stoneflesh` | Alteration | 30 | 14 | 1 | 55% | survives the first arrow volley |
| `ChainLightning` | Destruction | 50 | 26 | 3 | 55% | punishes players who bring followers |
| `Ironflesh` | Alteration | 55 | 34 | 3 | 45% | armour spell upgrade |
| `Thunderbolt` | Destruction | 70 | 45 | 4 | 45% | expert tier |

### Conjurer

Matched by string filter `*Conjurer`.

Pure summoners. Their whole identity is the summon list, and vanilla stops it at Flame Atronach.

| EditorID | School | Skill floor | Level floor | Tier | Chance | Why |
| --- | --- | --- | --- | --- | --- | --- |
| `ConjureFamiliar` | Conjuration | 25 | 8 | 1 | 75% | always-on opening summon |
| `ConjureFlameAtronach` | Conjuration | 40 | 18 | 2 | 60% | second summon tier |
| `ConjureFrostAtronach` | Conjuration | 55 | 28 | 3 | 50% | third summon tier |
| `ConjureStormAtronach` | Conjuration | 70 | 40 | 4 | 40% | top summon tier |

### Forsworn Shaman

Matched by string filter `*Shaman`.

Reach shamans are Restoration/Illusion casters in the lore and single-school spell plinkers in the game.

| EditorID | School | Skill floor | Level floor | Tier | Chance | Why |
| --- | --- | --- | --- | --- | --- | --- |
| `Oakflesh` | Alteration | 25 | 8 | 1 | 55% | cheap early defence |
| `FastHealing` | Restoration | 25 | 10 | 1 | 65% | heals through the first burst of damage |
| `Fury` | Illusion | 25 | 12 | 1 | 55% | turns the camp against itself |
| `CloseWounds` | Restoration | 50 | 25 | 3 | 50% | mid-game sustain |
| `Fear` | Illusion | 50 | 28 | 3 | 45% | crowd control |
| `Ironflesh` | Alteration | 60 | 35 | 4 | 40% | late-game defence |

### Vampire

Matched by string filter `*Vampire`.

Vampires get frost and drain only. Higher ranks should feel like predators, not like bandits with fangs.

| EditorID | School | Skill floor | Level floor | Tier | Chance | Why |
| --- | --- | --- | --- | --- | --- | --- |
| `Fear` | Illusion | 25 | 15 | 1 | 50% | predator opening |
| `RaiseZombie` | Conjuration | 40 | 25 | 2 | 40% | raises the bodies in the room |
| `IceStorm` | Destruction | 45 | 28 | 3 | 45% | area frost |
| `IcySpear` | Destruction | 65 | 45 | 4 | 40% | expert tier |

### Pyromancer

Matched by string filter `*Pyromancer`.

Elemental specialists whose name already promises a full spell line.

| EditorID | School | Skill floor | Level floor | Tier | Chance | Why |
| --- | --- | --- | --- | --- | --- | --- |
| `Firebolt` | Destruction | 25 | 12 | 1 | 70% | fire line, tier 1 |
| `Fireball` | Destruction | 45 | 25 | 2 | 60% | fire line, tier 2 |
| `Incinerate` | Destruction | 65 | 40 | 4 | 50% | fire line, tier 3 |

### Cryomancer

Matched by string filter `*Cryomancer`.

Frost line, mirroring the pyromancer table.

| EditorID | School | Skill floor | Level floor | Tier | Chance | Why |
| --- | --- | --- | --- | --- | --- | --- |
| `IceSpike` | Destruction | 25 | 12 | 1 | 70% | frost line, tier 1 |
| `IceStorm` | Destruction | 45 | 25 | 2 | 60% | frost line, tier 2 |
| `IcySpear` | Destruction | 65 | 40 | 4 | 50% | frost line, tier 3 |

### Electromancer

Matched by string filter `*Electromancer`.

Shock line, mirroring the pyromancer table.

| EditorID | School | Skill floor | Level floor | Tier | Chance | Why |
| --- | --- | --- | --- | --- | --- | --- |
| `LightningBolt` | Destruction | 25 | 12 | 1 | 70% | shock line, tier 1 |
| `ChainLightning` | Destruction | 45 | 25 | 2 | 60% | shock line, tier 2 |
| `Thunderbolt` | Destruction | 65 | 40 | 4 | 50% | shock line, tier 3 |

## Optional modules

### Restoration Self-Heal

Casters who actually trained Restoration patch themselves up mid-fight instead of standing in the open at 10% health.

| EditorID | School | Skill floor | Chance | Why |
| --- | --- | --- | --- | --- |
| `FastHealing` | Restoration | 40 | 35% | any caster with Restoration 40 |
| `CloseWounds` | Restoration | 60 | 25% | any caster with Restoration 60 |

### Alteration Armour Spells

The armour-spell ladder, handed out by Alteration skill rather than by archetype, so a warlock and a shaman both get what they trained for.

| EditorID | School | Skill floor | Chance | Why |
| --- | --- | --- | --- | --- |
| `Oakflesh` | Alteration | 20 | 55% | Alteration 20 |
| `Stoneflesh` | Alteration | 40 | 50% | Alteration 40 |
| `Ironflesh` | Alteration | 60 | 40% | Alteration 60 |
| `Ebonyflesh` | Alteration | 80 | 30% | Alteration 80 |

### Illusion Pressure

Fury, Fear and Calm handed to the casters whose lore supports them. Off by default because fear and calm effects change how a fight reads.

| EditorID | School | Skill floor | Chance | Why |
| --- | --- | --- | --- | --- |
| `Fury` | Illusion | 30 | 45% | Illusion 30 |
| `Fear` | Illusion | 45 | 40% | Illusion 45 |
| `Calm` | Illusion | 60 | 25% | Illusion 60 |

## Unique forms used

`23` distinct spell records, no items, no perks, no keywords, no new records.

```
Calm
ChainLightning
CloseWounds
ConjureFamiliar
ConjureFlameAtronach
ConjureFrostAtronach
ConjureStormAtronach
Ebonyflesh
FastHealing
Fear
Fireball
Firebolt
Fury
IceSpike
IceStorm
IcySpear
Incinerate
Ironflesh
LightningBolt
Oakflesh
RaiseZombie
Stoneflesh
Thunderbolt
```

Tiers follow the game's own progression: 1 apprentice, 2 apprentice/adept,
3 adept/expert, 4 expert. No master-tier spell is distributed - those are ritual
spells in vanilla and handing them to a random warlock reads as a bug.

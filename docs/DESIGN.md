# Design notes

Why the mod is built this way, and what it deliberately refuses to do.

## The constraint

The brief for this mod was a config-only mod: no Creation Kit, no plugin, no scripts. That rules out
editing NPC records, which is how most enemy overhauls solve this problem, and it leaves exactly one
lever: **SPID can append forms to an actorbase at load time.**

Appending is a weaker tool than editing. You cannot remove Flames from a necromancer, you cannot
change their level, and you cannot give them a new combat style. So the design has to work *with*
what vanilla already gives an NPC rather than around it.

That constraint turns out to be a feature. A config that only appends is:

- **load-order independent** - there is nothing to win or lose a conflict over;
- **update proof** - no addresses, no plugin, so a game patch cannot break it;
- **mid-save safe** - remove the file, and the next cell load hands out nothing.

For a mod that touches combat balance, being able to switch it off mid-playthrough without residue
matters more than being able to rewrite a record.

## What the actual defect is

Vanilla enemy casters have a fixed spell list for the whole game. Two things go wrong with that:

1. **The list does not scale.** A level 45 necromancer has a Destruction skill in the seventies and
   is still casting Flames. The NPC's *stats* scale; their *options* do not.
2. **The list ignores training.** A warlock with Alteration 45 has never once cast an armour spell,
   because no one ever put one in their list.

Both are the same bug wearing different clothes: the spell list is disconnected from the numbers the
game is already tracking. Tiered Casters reconnects them, using the skill the spell actually needs
as the gate.

## Why skill floors and not level floors alone

Level alone is a crude proxy. Enemy levels scale with the player, so at player level 30 nearly every
caster in the game passes a level-30 check, including the ones in starter dungeons that the game
deliberately keeps weak.

Skills are the more honest signal. They are set per class, they climb with the NPC, and they are the
number the game itself uses to decide whether a spell is appropriate. Requiring *both* - a level
floor and a school floor - produces a curve that is steep where it should be steep and flat where the
player is already comfortable.

It also means the mod cannot produce the classic config-mod failure: an unlevelled NPC with a fixed
low skill suddenly casting expert spells because the player is level 60. They will not, because their
Destruction never got there.

## Why name matching and not factions or classes

Faction and class filters are more "correct" in an xEdit sense, but they are also the filters most
likely to be wrong in someone else's load order, and they silently miss mod-added NPCs.

Name and EditorID matching has the opposite trade-off: it is slightly fuzzy, and it picks up mod-added
casters for free. A mod that adds its own "Necromancer" enemies gets this table without a patch. That
is worth more to a player than taxonomic purity.

The exclusion traits do the safety work that the name match cannot: `-U` keeps unique NPCs out,
`-C` keeps children out, `-T` keeps teammates out. Everything the name filter over-matches is
handled there.

## Why not remove the old spells

Because removing a spell requires a plugin, and the moment this ships a plugin it inherits every
problem a plugin has: a record conflict with every other enemy overhaul, a load-order position to
argue about, and a save that remembers it was there.

The trade-off is honest and documented in the readme: a high-level necromancer still knows Flames,
and will sometimes cast it. That is a small cost for a mod that cannot break a load order.

## The presets

Three presets exist because "enemy casters should be more interesting" means different things to
different players, and because a config mod that only ships one balance point gets uninstalled the
first time someone finds it too much.

All three are generated from one table, so a balance change lands in all of them at once and they can
never drift apart. Only three numbers change:

| Preset | Tier cap | Level delta | Chance multiplier |
| --- | --- | --- | --- |
| Vanilla+ | 2 | +6 | x0.75 |
| Standard | 4 | 0 | x1.00 |
| Ruthless | 4 | -4 | x1.25 |

Vanilla+ is the "I want to forget this is installed until level 40" option. Ruthless is the
"I want a room with two warlocks to be a decision" option.

## Deterministic chances

Every chance carries SPID's `!` suffix. Without it the roll is re-evaluated when the NPC is
distributed again, which means a caster can gain or lose a spell between sessions - and a player who
notices will report it as a bug, correctly.

With it, the same NPC always gets the same answer, so the mod reads as authored content rather than
as noise.

## What is not covered, on purpose

- **Dragon Priests.** They are all unique, so `-U` excludes them, and they already have hand-built
  high-tier kits. Adding to them would be gilding.
- **Hagravens.** Creatures, not NPCs; the name filter would catch them but the trait assumptions do
  not hold.
- **Master-tier spells.** Those are ritual spells in vanilla. A random warlock with Blizzard reads
  as a bug, not as difficulty.
- **Bandits and Forsworn rank and file.** They are not casters, and giving them spells to make fights
  harder is a different mod with a different design.

## Verifying it

The tooling in `tools/` exists because a config mod's failure mode is silence. Nothing crashes; a
malformed line is simply skipped, and the player concludes the mod does nothing.

`tools/validate_distr.py` checks the parts that are checkable offline: field count, the level and
skill filter grammar including school index range, trait grammar, chance range, and duplicate lines.
`tools/generate.py` guarantees the three presets stay consistent. `tools/build.py` refuses to package
if validation fails.

What the tooling cannot check is whether an EditorID exists in a given load order - that is what
`po3_SpellPerkItemDistributor.log` is for, and the readme tells players exactly where to look.

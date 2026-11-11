# Case study: from a vague lobby request to a structured prompt

A worked example of the whole workflow. Use it as a pattern, not a template: other tasks (UI, systems, vehicles) reuse the same moves with different content.

## Contents
1. The situation
2. What went wrong with the first prompt
3. What the improved prompt changed
4. Excerpts to imitate
5. Second round: reviewing the agent's first screenshots
6. Lessons

## 1. The situation

The user had a Roblox kart-racing game with a weak "3D garage" lobby. Their request was a loose feature list plus reference images: a shop with an NPC, a garage to pick karts and characters, two podiums with top-3 winners and confetti, three match portals (Free Race, Trophy Path, Solo) with waiting areas and a persistent matchmaking overlay, a "random place", and a "mysterious place" behind a tunnel with a purple portal. They wanted references replicated exactly and roads wide enough for karts to drift.

The first agent produced a flat blue plain with a grid texture, tiny scattered arches, three blue boxes as a podium, and a glowing yellow ray on the NPC.

## 2. What went wrong with the first prompt

| Failure | Cause in the prompt |
|---|---|
| Generic scene instead of the reference look | Images were .avif/.webp; the agent likely could not read them, and the prompt gave no written description |
| Open plain with no walls | The prompt never said the lobby is an enclosed hall |
| Everything spread out and tiny | "Widen the roads" was applied to the whole space; no rule that props keep reference proportions |
| Extra decorations (rays on the NPC) | No exact NPC spec |
| Agent stopped when it felt good enough | "Compare and fix until it matches" was subjective; no checklist or evidence |
| Generic "engine/codebase" approach | Platform not named; no build method |
| Messy layout, empty zones, floating entrances | No layout map, no purpose rule, no sealed-space rule |

## 3. What the improved prompt changed

1. Named the platform and tools: "Roblox Studio, Luau", inspect the project first.
2. Converted the images to PNG and wrote a per-image element list with stable IDs (S-01 ... M-09), exact sign text, counts, positions, colors, materials, and lighting.
3. Defined the global visual language once (palette, materials, lighting, recurring motifs) and described reusable kit modules (arch, sign plate, LED band, speaker stack, bleacher, crate, emblem, turntable, portal gate).
4. Added hard structural rules: one sealed building, each room a closed box with thick walls, openings cut into walls, nothing floating, no purposeless areas.
5. Gave an ASCII layout map with logical grouping (services west, play north, results east, exploration south) and a spawn with sight lines.
6. Derived scale from measurable anchors (kart width, avatar height) with fallbacks, and stated that only corridors, doorways, and plazas widen while props keep reference proportions.
7. Phased the build with gates: audit, lighting and kit, shell, rooms one at a time, logic, UI, validation. Each gate required evidence.
8. Replaced "match exactly" with an element-ID pass/fail table and matched-camera screenshots, plus closed-shell, empty-zone, drive, and flow tests.
9. Protected existing systems: reuse data and remotes, move the old lobby to a backup container.
10. Added behavior specs as state machines (matchmaking) and server-authoritative rules (podium results, removing players standing on a podium when a new result arrives), with dev commands to simulate them.
11. Added a UI theme module, a HUD layout, and a minimap generated from the same layout config.
12. Added a decisions log and a final report with unverified items listed.

## 4. Excerpts to imitate

**Hard structural rule (short, with a test):**
```
One closed building. Every room is a closed box (floor, 4 walls, ceiling) with walls at least 12 studs thick.
The only openings are gateway arches cut INTO those walls (tunnel depth = wall thickness). No arch, sign or prop may float
in empty space. Test: orbit the camera outside the building; you must see only a closed shell, never void or skybox.
```

**ID-tagged element spec:**
```
- S-02 Curved horizontal band wrapping over the arch, wider than it: LED mosaic of light-blue/cyan rectangles with a few gold tiles.
- S-03 Center of the band: chamfered arrow-shaped sign plate pointing down, cobalt face, double border (gold outer, light inner),
  white bold italic "SHOP", black/white checkered flag square on its right, gold-edged chevron tip at the bottom.
- S-10 Left wall: grid of rectangular frames, 4 columns x 5 rows, yellow outlines. Right wall: same grid in pink/magenta.
```

**Scale from anchors:**
```
Read the real kart model (width, length, turn radius, drift radius). Corridors/roads/plazas >= 5x kart width. Gateway opening
>= 5x kart width and >= 24 studs high. Fallback if unknown: kart 7 wide x 12 long, avatar ~5 tall. Proportions of props and
architecture stay as in the references; only roads, doorways, tunnels, and plazas get the extra width.
```

**Gate with evidence:**
```
Gate after each room: every element ID marked yes/no for presence and correct proportion/color; a screenshot taken from the
reference camera angle next to the reference image. A room passes only if every ID is "yes". If your tools cannot take
screenshots, say so explicitly; never claim a match you did not verify.
```

**Behavior as a state machine:**
```
Matchmaking states: idle -> searching(n/N) -> found -> starting -> in_match, plus cancelled. One shared overlay component driven
by that state (players found n/N + Cancel). The player may leave the waiting room and roam the lobby while searching.
Only one active search at a time; starting another asks to cancel the first.
```

## 5. Second round: reviewing the agent's first screenshots

The agent's first screenshot showed real progress: a sealed hall, dark blue atmosphere, spawn circles, a "PLAY" arch in the reference style, a directory board, a minimap, and HUD buttons. Review mode then found:
- The central crest emblem was far too large and crude; the prompt said "pedestal with the crest" without a size (prompt gap). Fix: about 12 studs tall, mounted in a wall alcove, with shape details.
- The floor was a flat bright fill instead of worn tiles with grout lines (fidelity shortfall). Fix: large slate tiles, visible joints, slight reflection.
- Lighting lacked contrast (surface and light). Fix: darker ambient, spotlights on poles and signs, bloom only on neon.
- Checkered bands were large blocks instead of thin bands (fidelity). Fix: continuous bands about 3 studs high.
- HUD buttons overlapped the minimap (bug). Fix: move them below or into the bottom bar.

The correction message listed five numbered items with measurements, ended with "re-run the checklist and send a side-by-side screenshot", and the reply explained which parts were prompt gaps.

## 6. Lessons

- The biggest lever was making the references readable and putting their content in the prompt as text.
- Anything that was "obvious" to the user (enclosed hall, no empty zones, props keep proportions) had to be written as a rule with a test.
- Measurable checklists beat adjectives, and gates with evidence stop early "done" claims.
- Tell the agent exactly what may change (corridor width) and what must not (prop proportions), or it will change everything.
- Review the first output quickly, praise what is real, and send small numeric corrections; then patch the prompt only where the gap was in the prompt.
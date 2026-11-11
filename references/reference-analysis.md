# Prompt blueprints

Start from the master skeleton, drop sections the task does not need, then append the add-ons for the task type(s). Write in the imperative, address the agent as "you", and keep sentences short.

## Contents
1. Master skeleton
2. Add-on: 3D environment / map / lobby / level
3. Add-on: UI / HUD / menus
4. Add-on: Gameplay system (combat, abilities, inventory, quests, progression)
5. Add-on: Vehicle / movement / controller
6. Add-on: NPC / dialogue / AI / cutscene
7. Add-on: Data / economy / monetization
8. Add-on: Multiplayer / matchmaking / teleport
9. Add-on: VFX / audio / animation polish
10. Add-on: Bug fix / refactor / optimization
11. Add-on: Clone a feature from screenshots or video
12. Length and tone

## 1. Master skeleton

```
# MISSION: <one sentence outcome>
<2-4 sentences: what exists now, what is wrong with it, what the finished result is.>
Autonomy rule: work without asking questions; decide, log decisions in <docs/decisions.md>; do not stop until every acceptance item is verified.

## 0. Non-negotiable rules
<5-8 hard constraints: structural rules, what to preserve, what never to do.>

## 1. Platform and tools
Roblox Studio, Luau. <Tools the agent has.> <Project conventions to follow.>
Inspect the existing project first: <services/containers/scripts to read>.

## 2. References (source of truth)
<File names + how to open them (convert avif/webp to PNG). Statement that the written specs below win if images cannot be read.>

## 3. Build method
<Procedural/config-driven build, kit-first modules, naming and folder conventions, anchoring/collision rules, performance budget.>

## 4. Scale and constraints (measure first)
<Anchors to measure; formulas; fallback values; which are hard vs suggested.>

## 5. Structure / layout / flow
<Zones or screens, adjacency map (ASCII), circulation, entry and exit points, hierarchy.>

## 6. Visual language
<Palette with Color3 values, materials, lighting settings, recurring motifs / kit modules.>

## 7. Element specs
<One block per zone/screen with ID-tagged elements. Mark inferred items.>

## 8. Behavior and logic
<Systems, states, server/client split, data flow, edge cases, defaults for ambiguities.>

## 9. Build order with gates
<Numbered phases. Each ends with a gate: what must be demonstrably true before moving on.>

## 10. Verification (evidence required)
<Element-ID table, matched-camera screenshots, functional tests, negative tests, performance check. Honest-reporting rule.>

## 11. Final report
<Deliverables, files, derived numbers, decisions, stubs/TODOs, unverified items, evidence.>
```

Section choice rules:
- Tiny fix: sections 0, 1, 8 (reproduction + expected), 10, 11 only.
- New feature without visuals: skip 2, 6, 7 (use behavior/spec instead).
- Visual rebuild: all sections, with 5-7 being the bulk.

## 2. Add-on: 3D environment / map / lobby / level

Must include:
- **Sealed-space rule:** every room is a closed volume (floor, walls, ceiling) with thick walls; openings are cut into walls; no floating gates/signs/props; exterior inspection test (orbit camera, no void or skybox visible).
- **Purpose rule:** every zone has a name, a function, and signage; an "empty-zone test" in verification.
- **Layout map in ASCII** with compass directions and adjacency; logical grouping (services, play, social, exploration); a clear spawn with sight lines to the main destinations; signage hierarchy.
- **Room size table** (suggested values) and the drivability/walkability minimums from measured anchors.
- **Kit-first build:** reusable modules (arch, sign plate, LED band, pillar, trim, screen, light pole, speaker stack, crate, bench, emblem...) built once, instanced everywhere, driven by one config.
- **Lighting block:** Technology, ambient, Atmosphere, Bloom, ColorCorrection, light placements; ceilings closed for interiors.
- **Interactive anchors:** triggers, proximity prompts, teleports with their volumes and return points.
- **Navigation aids** if the world has more than 3-4 zones: minimap or directory board, zone banner, waypoint.
- **Traversal tests:** walk and drive (or fly-through) every route at full speed; fix clipping and dead ends.
- **Performance:** part budget per zone, anchoring, CanCollide/CanQuery off for decor, instancing, limit shadow-casting lights.
- **Backup-then-replace** of the old area.

## 3. Add-on: UI / HUD / menus

Must include:
- A **theme module** (colors, font family and weight/style, corner/chamfer style, stroke, button states, sounds) so all UI is consistent and restylable in one place.
- **Layout map** per screen (anchor points and rough sizes), HUD zones (top-left identity, top-right map, bottom-center prompts, etc.), avoidance of Roblox's built-in top bar, chat, and mobile controls.
- **Responsive rules:** `UIScale` or scale-based sizes, `UIAspectRatioConstraint` where needed, safe areas/insets, minimum touch target size, tested at a phone and a desktop viewport.
- **Input:** keyboard/mouse, touch, gamepad (selection order, `Selectable`), key hints that change per input type.
- **States:** default, hover, pressed, disabled, loading, empty, error. Persistent overlays vs modal windows. Z-order and what can open on top of what.
- **Data binding:** which server state each element reads, update frequency, and that the client never decides outcomes.
- **Cleanup:** remove superseded UI; no overlapping elements (state which collisions to test).
- For clones from screenshots: pixel measurements as percentages or scale values, not absolute pixels, plus a tolerance.

## 4. Add-on: Gameplay system

Must include:
- **Rules in plain language** plus a **state machine** or table of states and transitions.
- **Server authority:** what the server owns, what the client may request, remote names and payloads, validation, rate limiting.
- **Data model:** attributes/values/modules, where config lives (single tunables module), what persists.
- **Edge cases:** disconnects, respawn, teleport mid-action, simultaneous requests, player leaving, server shutdown.
- **Feedback:** UI, sounds, VFX per event.
- **Tests:** a debug command or dev panel to trigger each state; unit tests for pure logic (state machines, cooldown math).
- **Balance knobs** exposed in one config.

## 5. Add-on: Vehicle / movement / controller

Must include:
- Measure the existing vehicle or character (dimensions, speed, turn radius, drift behavior) and express space and obstacle sizes relative to it.
- Physics approach (constraint-based, custom raycast controller, `VehicleSeat`), network ownership of the vehicle, client/server split for responsiveness vs exploit resistance.
- Camera behavior, input mapping across devices, mount/dismount flow, respawn/flip recovery.
- A **drive test**: full-speed laps through the whole area, drifting through corners, no clipping or stuck points.
- Surface/friction rules, collision groups between vehicles and players.

## 6. Add-on: NPC / dialogue / AI / cutscene

Must include:
- NPC appearance spec (for a classic noob: yellow head and arms, blue torso, green legs, default smile; or a described outfit), rig type (R6/R15), idle/wave animation.
- Interaction design: proximity prompt text, range, key, what opens, what happens if the player leaves mid-conversation.
- Dialogue/AI behavior as states; pathfinding rules if mobile; spawn/despawn rules.
- Cutscenes: camera path keyframes, duration, skip control, and restoring player control and camera afterward.

## 7. Add-on: Data / economy / monetization

Must include:
- **Reuse the project's existing data layer** (profile library or DataStore wrapper); do not add a second one.
- Schema with defaults, versioning/migration plan, session locking or save-conflict policy, retries with `pcall`, save on leave and on interval.
- Server-side validation of every purchase/spend; never trust client prices or amounts.
- Developer Products via `MarketplaceService.ProcessReceipt` (idempotent, returns the correct status), gamepasses via ownership checks, premium benefits if used.
- A **mock/stub mode** for Studio testing and a clear TODO list for real product IDs.
- Never invent real asset or product IDs; use placeholders in one config file.

## 8. Add-on: Multiplayer / matchmaking / teleport

Must include:
- Explicit **state machine** (for example `idle -> searching(n/N) -> found -> starting -> in_match`, plus `cancelled`) driving one shared UI component.
- Use the existing backend if any; otherwise a mock service behind an interface (`TeleportService` reserved servers and `MemoryStoreService` queues are typical real implementations).
- Rules for concurrent actions (only one active search, what happens when the player starts something else), cancel behavior, timeouts, partial parties, disconnects.
- Lobby persistence: the player must stay free to move while waiting; the overlay persists across areas.
- Consistency: all clients see the same shared state (results, podiums, queues); server is the source of truth.
- Tests: simulate N players, cancellation at each state, and a failed teleport.

## 9. Add-on: VFX / audio / animation polish

Must include:
- Effects defined by trigger, duration, emitter/beam/trail parameters in ranges, color tied to the palette, and a cleanup rule (Debris or explicit destroy).
- Performance caps: particle counts, distance culling, quality toggles for low-end mobile.
- Audio: categories (music, UI, ambience, SFX) with `SoundGroup`s, volume defaults, spatial vs global, placeholders for missing asset IDs.
- Animated environment elements (rotating rings, swirling portals, flowing light streaks): method (TweenService, RunService, particle emitters, beams, Texture offsets) and a rule to stop work when far from players.

## 10. Add-on: Bug fix / refactor / optimization

Must include:
- **Reproduction steps**, expected vs actual, output logs/errors, and when it started if known.
- Scope fence: which scripts/instances may change; what must not.
- Root cause first: ask the agent to state the cause with evidence before editing.
- Minimal change; no unrelated refactors; keep public interfaces and remote names.
- Regression test or manual test steps; before/after measurements for performance work (frame time, memory, instance count, remote traffic).

## 11. Add-on: Clone a feature from screenshots or video

Must include:
- Treat the reference as behavior spec, not just look: list states and transitions seen across the frames.
- Layout measurements in relative units; color/typography/spacing tokens; icon and asset list (what exists vs what is a placeholder).
- Explicit "do not copy" boundaries: no copying of protected branding, names, or assets belonging to others; recreate the function with original art unless the user owns the assets.
- Acceptance via side-by-side screenshots at the same viewport.

## 12. Length and tone

- Aim for the shortest prompt that removes the failure modes. Full rebuilds can run 2,000-4,000 words; small tasks should stay under about 400.
- Prefer lists, tables, and ID-tagged lines over paragraphs. Use bold sparingly for hard rules.
- Explain the reason behind a rule in one clause when it prevents a likely mistake ("keep props at reference proportions; only widen corridors"). Agents follow rules better when they know the goal.
- Do not paste generic Roblox tutorials; include only facts that change the agent's decisions.
- Put hard rules early and the report spec last, because those are the parts agents most often skip.
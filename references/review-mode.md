# Review mode: diagnosing agent output and writing corrections

Use this when the user shares screenshots (or descriptions) of what an agent built and asks what is wrong, what to change, or why the first attempt failed.

## Contents
1. Protocol
2. Defect classes
3. Priority order for corrections
4. Correction message template
5. Prompt patches
6. Convergence tactics
7. Honesty and limits

## 1. Protocol

1. **Identify what you are looking at.** Which zone/screen, which camera angle, which references apply. If the user shows a grid of reference vs agent output, work out which side is which before judging; if unsure, state your assumption in one line.
2. **Build a quick element table** for the visible area: reference element ID, status in the output (present / partial / wrong / missing), and one short note. Use the IDs from the original prompt when they exist; otherwise create temporary ones.
3. **Check proportions with anchors.** Compare sizes using the avatar, door, or vehicle as a ruler ("the emblem is about 3 avatars tall; the reference shows about 1"). Scale errors are the most common and the most visible.
4. **Check structure rules:** sealed rooms, floating objects, purposeless areas, orphan old content, doorways that open into void.
5. **Check surface and light:** flat color fills vs tiled/worn surfaces, missing contrast, bloom on everything vs only on neon, missing local lights, visible default grid or baseplate.
6. **Check UI:** overlaps, elements covering the minimap or the Roblox top bar, text legibility, consistency with the theme, mobile safe areas, redundant buttons.
7. **Name real progress first.** Be specific ("sealed hall, closed ceiling, spawn pads, directory board and minimap are in place"), because it tells the user what to keep and what the agent already understands.
8. **Diagnose causes,** not only symptoms (section 2). Tell the user honestly which part of the problem was the prompt.
9. **Write the correction message** (section 4) and, if the cause was a prompt gap, a prompt patch (section 5).

## 2. Defect classes

| Class | Typical sign | Typical fix |
|---|---|---|
| Prompt gap | A feature is absent or wrong because the prompt never said it, or said it vaguely (no size, no count, no placement) | Patch the prompt with a measurable spec |
| Misread reference | The agent could not decode or interpret the image, producing a generic scene | Supply PNGs, tiles, and written specs; ask for a written visual summary first |
| Scale error | Hero props too big/small, cramped or empty rooms | Give ratios to anchors, require measured values, add a check |
| Structure failure | Floating gates, void between rooms, unexplained empty areas | Restate sealed-space and purpose rules; add the exterior and empty-zone tests |
| Fidelity shortfall | Right objects, wrong shapes/colors/materials/lighting | Per-element specs, kit module rebuilt in isolation, palette values, material table |
| Platform limit | Textures that need uploads, complex organic shapes, unavailable fonts | Accept a simplified substitute, list what the user can upload later |
| Process failure | Claims of completion without checks, no screenshots, rules ignored | Add gates, evidence requirements, honest-reporting rule |
| Bug | Overlaps, scripts erroring, state not updating | Repro steps, logs, scoped fix |

## 3. Priority order for corrections

Fix in this order, because later items depend on earlier ones:
1. Structure and layout (sealed rooms, adjacency, circulation, purpose)
2. Scale and proportions of major elements
3. Composition of the hero elements (arches, stages, gates, counters)
4. Surfaces, color, and lighting
5. Secondary props and signage details
6. UI and HUD layout and overlaps
7. Animation and polish

Limit one round to the five to seven highest-impact corrections. A long list causes the agent to skim; the rest goes in the next round.

## 4. Correction message template

Write it so the user can paste it directly to the agent, in English unless asked otherwise:

```
Visual corrections for <zone/screen> (apply now):
1. <Element ID/name>: <what is wrong, with a measurement>. Replace with <specific shape/size/color/material/position>. Reference: <image file>.
2. ...
Then re-run the element checklist for this zone, capture a screenshot from the reference camera angle, and report each element as pass/fail.
```

Rules for the items:
- Use numbers and anchors: "about 12 studs tall", "thin bands about 3 studs high", "grid of 4 x 5 frames".
- Say what to remove as well as what to add.
- Point to the reference file for each item.
- Avoid adjectives that only restate the problem ("make it better", "more realistic").
- End with the verification step so the agent produces evidence, not a claim.

## 5. Prompt patches

When the review shows a prompt gap, offer a short block to append to the original prompt (for example "Platform and visual method", "Scale rules", "Visual acceptance"). Mark where it overrides earlier text ("overrides section 5.1 where they conflict"). Do not rewrite the whole prompt unless asked; patches keep the agent's context stable.

## 6. Convergence tactics

If the same defect survives two rounds:
- Shrink the step: ask for the single module on an empty test baseplate, compared to the cropped reference tile, before placing it in the world.
- Convert the spec to numbers: part-by-part dimensions and offsets.
- Provide a zoomed tile of the reference and ask for a written description of the tile first, then a build from that description.
- Replace an unreachable detail with a defined simplified version.
- Change the workflow: generate by script from parameters, so adjustments are a parameter change, not a rebuild.
- If the agent keeps declaring success without evidence, require a per-element results table in every reply and refuse "done" without it.

## 7. Honesty and limits

- You usually see one screenshot per zone. Say what you cannot judge (other rooms, behavior, performance, mobile layout) instead of guessing.
- Distinguish what is certainly wrong from what might be a camera-angle effect.
- Do not blame the user or the model. Explain causes plainly and focus on the next action.
- When the agent is still working, treat the screenshot as a work in progress: give corrections that will not conflict with unfinished parts, and note what is probably still to come.
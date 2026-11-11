# Roblox platform notes for prompt writing

Include only the facts that change an agent's decisions for the task at hand. Roblox evolves; when a detail is critical (API names, limits), tell the agent to verify against current Roblox documentation or by inspecting the project instead of trusting memory.

## Contents
1. Naming the platform and tools
2. Project structure and client/server split
3. Scale and units
4. Building: parts, materials, CSG, meshes
5. Lighting and atmosphere
6. Screens, signs, and animated surfaces
7. UI (ScreenGui) rules
8. Interaction, teleports, and streaming
9. Vehicles and physics
10. Avatars, skins, NPCs
11. Data, purchases, matchmaking
12. Performance and testing
13. Assets, security, and policy

## 1. Naming the platform and tools
- Always write "Roblox Studio, Luau" in the prompt. Never write "the engine" or "the framework".
- Find out which tools the agent has: live Studio access (an MCP server or plugin that can read/write the DataModel, run code, take screenshots), file-based sync (Rojo, with the project on disk), or only generated scripts that the user pastes. The prompt must say which one to use and what to do if a capability is missing (for example "if you cannot take screenshots, say so; do not claim visual matches").
- Tell the agent to inspect the existing place/project first: containers (`Workspace`, `ReplicatedStorage`, `ServerStorage`, `ServerScriptService`, `StarterGui`, `StarterPlayer`, `Lighting`), existing modules, remotes, tags, and attributes.

## 2. Project structure and client/server split
- Server code in `ServerScriptService`; server-only modules/assets in `ServerStorage`; shared modules and remotes in `ReplicatedStorage`; client code in `StarterPlayer/StarterPlayerScripts` or `StarterGui`; character-scoped code in `StarterCharacterScripts`.
- The server is the authority for anything that matters (currency, inventory, match results, podium contents, queue state). The client requests via `RemoteEvent`/`RemoteFunction`; the server validates (type, range, cooldown, ownership) and applies.
- Replicated state can use attributes or values on shared instances; large or frequent state should go through remotes with throttling.
- Use `CollectionService` tags to find interactive objects instead of hard-coded paths; keep tunables (sizes, colors, labels, timers) in one config module.
- Follow the project's existing naming and module patterns; do not introduce a second framework.

## 3. Scale and units
- 1 stud is about 0.28 m. A default avatar is roughly 5 to 5.5 studs tall; default `WalkSpeed` is 16 studs/s; a normal door is about 7 studs tall; one stair step is about 1 stud.
- A single part's size is limited per axis (2048 studs); long walls are built from several parts.
- Measure the real kart/character/prop in the project instead of assuming. Give fallback numbers only if measuring is impossible.
- For roofed areas, ceiling height must clear the tallest arch/sign plus lights; tall spectacle rooms commonly need 60 to 100 studs.

## 4. Building: parts, materials, CSG, meshes
- Set `Anchored = true` on everything static. Decorative parts: `CanCollide = false`, `CanQuery = false`, `CanTouch = false` unless needed; use `CastShadow = false` for small details.
- Materials: do not leave everything as default `Plastic`. Use `Neon` for glow, `SmoothPlastic` for glossy paint, `Concrete`/`Slate`/`Pavement` for floors and walls, `Brick`/`Cobblestone`/`Limestone` for stone trim, `WoodPlanks`, `Metal`/`DiamondPlate`, `Fabric`. `MaterialVariant` and `SurfaceAppearance` (on MeshParts) give PBR detail when textures exist.
- Walls with openings: build the wall from segments around the opening, or cut it with CSG (`SubtractAsync`/`UnionAsync`). Verify collisions after CSG because unions can change collision fidelity.
- Curved architecture (arches, rings, domes): generate by script from segments placed along an arc, or use CSG; parameterize radius, thickness, depth, and segment count so the shape can be tuned and rebuilt.
- Prefer building modules as `Model`s with a `PrimaryPart` and use `PivotTo` to place them. Keep a kit folder of reusable modules.
- Use `MeshPart.CollisionFidelity = Box` or `Hull` for decor that needs collision, and `RenderFidelity` settings for distant detail.
- Free-form sculpture from primitives is time-consuming; allow the agent to approximate organic emblems with stacked wedges/cylinders/neon outlines and flag them as "simplified" in the report.

## 5. Lighting and atmosphere
- `Lighting.Technology` options: `Future` (best quality, highest cost), `ShadowMap`, `Voxel`, `Compatibility`. Choose based on the target devices and say it in the prompt.
- For neon-lit interiors: darker `Ambient`/`OutdoorAmbient`, moderate `Brightness`, `Atmosphere` with low density and cool color, `BloomEffect` (tune `Intensity`, `Size`, `Threshold` so only neon blooms), light `ColorCorrectionEffect` for tint and saturation. Enclosed rooms need a ceiling; otherwise the sky shows.
- Use `SpotLight`/`PointLight`/`SurfaceLight` for focal lighting on signs, poles, and key props. Set `Shadows = false` on decorative lights and limit shadow-casting lights; they are expensive.
- Different rooms can have different moods by placing local lights and color accents, since `Lighting` is global. If a global change is needed per zone (for example a dark room vs a bright hall), use local lights and darker materials, or tween `Lighting` values when the player enters a zone.

## 6. Screens, signs, and animated surfaces
- Screens and signs: `SurfaceGui` on a part (`Face`, `SizingMode`, `PixelsPerStud`, `Brightness`, `LightInfluence`, `AlwaysOnTop` as needed) hosting `Frame`s, `TextLabel`s, and `ImageLabel`s. Sign text must use the exact wording from the spec, with a bold (often italic) font and glow via a neon backing or `UIStroke`.
- Custom patterns (comic speed lines, halftone dots, checkered bands) need either uploaded image assets or procedural substitutes: tiled `Frame`s with `UIGradient`, rotating gradients, `Texture`/`Decal` with a placeholder asset ID, or particle/beam streaks. Say which one to use and what to list as "needs upload".
- Animated elements: `TweenService` for rotations and pulses, `RunService.Heartbeat` for continuous motion, `ParticleEmitter`/`Beam`/`Trail` for sparks, vortexes, and light streaks. Add a distance check so effects stop when no player is near.
- Confetti and similar bursts: a `ParticleEmitter` with several color keypoints, a short `Lifetime`, gravity through `Acceleration`, bursts with `Emit`, and cleanup after the effect.

## 7. UI (ScreenGui) rules
- Use scale-based sizing with `UIScale`, `UIAspectRatioConstraint`, `UISizeConstraint`, and layout objects (`UIListLayout`, `UIGridLayout`, `UIPadding`). Avoid fixed pixel layouts.
- Respect safe areas: use `ScreenGui.ScreenInsets` (for example `CoreUISafeInsets` or `TopbarSafeInsets`) instead of hard-coding the top bar height; keep bottom corners clear of the mobile thumbstick and jump button; avoid the default chat area.
- Touch targets should be comfortably large (around 44 px minimum equivalent); support gamepad navigation (`Selectable`, `GuiService.SelectedObject`) and show input-appropriate key hints.
- Style: `UICorner`/`UIStroke`/`UIGradient`, `FontFace` via `Font.new` with built-in families (for example Montserrat, Gotham, Builder Sans) at bold/italic weights. Put colors and fonts in one theme module.
- Hide or replace default CoreGui elements deliberately with `StarterGui:SetCoreGuiEnabled`; do not leave two systems doing the same job.
- Overlap check: list the UI elements on each screen and test them at a phone-sized and a desktop-sized viewport (Studio's device emulator).
- Persistent overlays (such as a matchmaking status) live in their own `ScreenGui` with a defined `DisplayOrder` and are driven by shared state, not by the screen that started them.

## 8. Interaction, teleports, and streaming
- Interaction: `ProximityPrompt` (`ActionText`, `ObjectText`, `HoldDuration`, `MaxActivationDistance`, `RequiresLineOfSight`, key) handled through `ProximityPromptService` or the prompt's `Triggered` event. For zones, use invisible trigger volumes with `Touched`/`GetPartsInPart` or spatial queries, and handle players who stand inside when the state changes.
- In-place teleports: set the character `PivotTo` on the server (or via a validated request). Define destination parts and safe return/exit points. When `Workspace.StreamingEnabled` is on, request streaming around the destination (`Player:RequestStreamAroundAsync`) before moving large distances.
- Cross-place or server teleports use `TeleportService` (`TeleportAsync` with `TeleportOptions`, reserved servers for private matches). Handle `TeleportInitFailed`.
- When players must be cleared from a spot (for example a podium when new winners appear), the prompt must specify the trigger volume, the safe destination, and the rule that the clear action runs on the server.

## 9. Vehicles and physics
- Vehicles can use `VehicleSeat`, constraint-based builds (`HingeConstraint`, `SpringConstraint`), or custom raycast controllers. Karts that need arcade drifting usually use custom or tuned physics; do not rewrite an existing working controller unless asked.
- Network ownership: the occupant's client normally simulates the vehicle (`SetNetworkOwner`); validate speed/position on the server for competitive modes.
- Use collision groups (`PhysicsService:RegisterCollisionGroup`, `BasePart.CollisionGroup`) to control vehicle-vs-player and vehicle-vs-decor collisions.
- Dimensions drive level design: measure width, length, turning radius, and drift arc at top speed, and derive corridor and doorway sizes from them.

## 10. Avatars, skins, NPCs
- Players spawn with their own avatar by default. "Default Roblox model" normally means the player's standard avatar with no override; custom characters are applied with `Humanoid:ApplyDescription` or by replacing the character model on the server.
- Rig types: R6 (classic blocky, six body parts plus head) and R15 (more joints, default today). Specify which the NPC uses.
- The classic noob: yellow head and arms, blue torso, green legs, smile face. Build it from a `HumanoidDescription` or a stored rig model, and add an idle or wave animation with `Animator`.
- Mounting, equipping, and unequipping vehicles/characters should be explicit flows with HUD buttons and key bindings, and the choice must persist through the data layer.

## 11. Data, purchases, matchmaking
- Persist through the project's existing data layer; otherwise `DataStoreService` with `UpdateAsync`, `pcall`, retry/backoff, save on player removal and on `BindToClose`.
- Developer Products require `MarketplaceService.ProcessReceipt` with idempotent handling; gamepasses are checked by ownership; never trust client-supplied prices.
- Matchmaking and queues: `MemoryStoreService` (queues, sorted maps) for cross-server state, `MessagingService` for cross-server messages, `TeleportService` to move players into matches. Wrap them behind an interface so a mock can run in Studio.

## 12. Performance and testing
- Define a per-zone budget (instance/part count, number of lights, particle caps) and a target of smooth frame rate on low-end mobile. Verify with the Developer Console (F9) and the MicroProfiler (Ctrl+F6) when the agent can.
- Enable `StreamingEnabled` for large worlds, and mark must-always-exist models as persistent; test teleports and sealed rooms with streaming on.
- Test modes: Play Solo, local server with multiple clients, device emulator for phone and tablet viewports, gamepad where possible.
- Provide dev/debug triggers (simulate a race ending, simulate N players found, fast-forward a timer) so features can be verified without real traffic; gate them behind Studio or an admin flag.

## 13. Assets, security, and policy
- Images, audio, and meshes are referenced by asset ID; assets must be owned by or permitted for the experience or they will not load. Never invent asset IDs; use placeholders from one config and list what needs uploading.
- Free models and Creator Store assets can contain malicious scripts. Tell the agent to inspect any inserted model's scripts (look for `require` of unknown asset IDs, obfuscated code, `getfenv`/`setfenv`, hidden `HttpService` calls) and to delete scripts it does not need.
- Respect Roblox Community Standards and intellectual property: recreate functions and layouts with original art, and do not copy branded characters or protected assets unless the user owns them.
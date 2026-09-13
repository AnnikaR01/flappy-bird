# Flappy Bird Clone — learning Python game programming from first principles by building a real, playable Flappy Bird clone in pygame

**Assumes:** Some prior Python exposure (variables, loops, conditionals feel at least a little familiar) — no separate fundamentals track, but Phase 0 folds in a light refresher rather than assuming total fluency.
**Structure:** 8 phases + capstone, strictly sequential — each phase's build is the starting point for the next phase's code, mirroring how a real project grows incrementally rather than being rewritten from scratch each time.

## Phase 0 — Setup + a text-based "flap" simulator
**Question:** How do you get a Python project running with `uv`, and what does the actual game logic look like before any graphics are involved?
**New skills (refresher, not new):** `uv init`/`uv run`, variables, a loop, a conditional, a function — reinforced through toy code, not re-taught from zero.
**Tools:** `uv` only (no external packages yet).
**Build:** A pure-text simulation — a variable `height` starts at some value, a loop runs a few "ticks," each tick either "falls" (height decreases) or "flaps" (height increases) based on simple input, and prints the bird's height each tick, ending if height drops to 0 or below ("you hit the ground").
**Stretch (optional):** Let the user type `f` to flap or hit Enter to fall, each tick, instead of a scripted sequence.

## Phase 1 — A real window with pygame
**Question:** How does a real game actually get pixels on screen and stay running, frame after frame, without freezing or quitting immediately?
**New skills:** installing an external library, the game loop pattern (event handling → update → draw, repeated every frame), `pygame`'s event queue, drawing a basic shape.
**Tools:** `pygame` (`uv add pygame`).
**Build:** An 800x600 window with a solid sky-blue background and a circle (the "bird," standing in for a sprite for now) drawn at a fixed position. The window closes cleanly when the user clicks the close button — no crash, no hang.
**Stretch:** Draw a simple green rectangle at the bottom of the screen as "the ground."

## Phase 2 — Input without physics yet (extends Phase 1)
**Question:** How does a game go from "draw once" to "respond to what the player does"?
**New skills:** keyboard event handling (`pygame.KEYDOWN`, key constants), updating a variable's value in response to input, redrawing every frame so changes are visible.
**Tools:** `pygame` (same as Phase 1).
**Build:** Pressing the space bar instantly moves the bird's circle up by a fixed number of pixels (no falling yet — that's next phase). The bird should visibly jump each time space is pressed, and stay in place otherwise.
**Stretch:** Clamp the bird so it can't move above the top of the window.

## Phase 3 — Real physics: gravity, velocity, and the flap impulse (extends Phase 2)
**Question:** What actual math makes a game character feel like it's "falling," and why does a fixed per-frame timestep matter?
**New skills:** velocity as a variable that changes position each frame, acceleration (gravity) as a constant added to velocity each frame, replacing instant teleport-up with an upward velocity "impulse" from a flap, `pygame.time.Clock()` for a stable frame rate.
**Tools:** `pygame` (same).
**Build:** The bird now continuously falls under gravity (position += velocity, velocity += gravity, every frame) and pressing space sets velocity to a negative "flap" value instead of teleporting position. Tuning gravity and flap-strength constants by feel is the actual exercise here.
**Grounding note (real, not invented):** we'll verify together that real game gravity constants are *tuned game-design values*, not literal real-world 9.8 m/s² — that's a real, documented technique in game development (values are chosen for feel, at pixel scale, not physical accuracy), not a shortcut we're inventing.
**Stretch:** Add a maximum fall speed (terminal velocity) so the bird doesn't accelerate forever.

## Phase 4 — Pipes, scrolling, and collision (extends Phase 3)
**Question:** How do obstacles move toward the player, spawn repeatedly, and actually end the game on contact?
**New skills:** a list holding multiple obstacle objects, moving multiple things each frame, spawning new obstacles on a timer, removing off-screen ones, rectangle-based collision detection.
**Tools:** `pygame.Rect` and its real `colliderect()` method (given directly, not guessable — it's genuine pygame API vocabulary).
**Build:** Pipes made of paired rectangles (top + bottom, with a gap) scroll from right to left, new pairs spawn at a regular interval, old ones are removed once off-screen, and the game ends (stops updating, shows a message) when the bird's rect collides with any pipe or the ground.
**Stretch:** Randomize the vertical position of the gap each time a pipe spawns.

## Phase 5 — Scoring and game states (extends Phase 4)
**Question:** How does a game track "you're playing" vs. "you lost" vs. "you're about to play again," and how does score actually get counted?
**New skills:** a simple state variable (e.g., `"playing"` / `"game_over"`) controlling what update/draw logic runs, incrementing a score when the bird passes a pipe, rendering text on screen (`pygame.font`).
**Tools:** `pygame.font` (given directly — real, specific API).
**Build:** A visible score counter that increments each time the bird fully passes a pipe pair, a game-over screen showing the final score, and pressing space on the game-over screen resets everything and starts a new run.
**Stretch:** Track and display a "best score this session" alongside the current score.

## Phase 6 — Polish: sound and visuals (extends Phase 5)
**Question:** What's the real difference between "a working game" and "a game that feels good," and how do you add that without restructuring what already works?
**New skills:** loading and playing sound effects, loading an image and using it instead of a plain shape, basic parallax/background movement.
**Tools:** `pygame.mixer` for sound, `pygame.image.load()` for sprites (both given directly — genuine pygame API).
**Build:** A flap sound effect, a "hit" sound on collision, and the bird drawn as an actual image instead of a circle (a simple free/self-made sprite is fine).
**Stretch:** A scrolling background that moves slower than the pipes (parallax), and/or the game speeding up gradually the longer a run lasts.

## Phase 7 — Persistence: saving your high score (extends Phase 6)
**Question:** How does a game remember something (like a high score) after it's closed and reopened?
**New skills:** file I/O, `json` for structured save data, reading a file that might not exist yet (first run).
**Tools:** Python's built-in `json` module (no install needed).
**Build:** The best score is saved to a small `.json` file on game-over if it's a new record, and loaded back in when the game starts, so the high score genuinely persists across separate runs of the program.
**Stretch:** Store a small list of the last 5 scores, not just the single best.

## Capstone — pick one (each builds on Phases 4–7)
Pick whichever sounds most fun — none is "more correct" than another:

1. **Faithful classic** — polish the base game until it feels genuinely tight and fair: tuned physics, clean visuals/sound, solid scoring and persistence. The "do the fundamentals really well" option.
2. **Difficulty modes** — add selectable difficulty (pipe gap size, scroll speed, gravity strength) chosen from a simple menu before each run, using everything from Phase 5's state system.
3. **Twist mode** — add one genuinely new mechanic on top of the base game (e.g., a power-up that temporarily widens the gap, or slow-motion for a few seconds) — a good option if you want one more "figure out something new" challenge before finishing.

## Pacing

| Phase | Focus | Depends on |
|---|---|---|
| 0 | Setup + refresher | — |
| 1 | Window + game loop | 0 |
| 2 | Keyboard input | 1 |
| 3 | Gravity/physics | 2 |
| 4 | Pipes + collision | 3 |
| 5 | Scoring + states | 4 |
| 6 | Sound + visuals | 5 |
| 7 | Save/load | 6 |
| Capstone | Pick one | 4, 5, 6, 7 |

## Review

One comprehensive review happens after the capstone, not after each phase — grouped by topic (game loop, physics, collision, state, persistence), starting with concrete "what does this code do" questions before any abstract ones. Any real gaps it uncovers get short, targeted hands-on practice — not a generic re-teach of everything.

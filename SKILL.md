---
name: feature-walkthrough
description: Use when someone wants to show a customer or stakeholder a feature that has not been built yet - a narrated, self-playing walkthrough of a proposed feature, styled to look like their real application, produced as one self-contained HTML file. Triggers on "/feature-walkthrough", "mock up this feature", "show them what it would look like", "demo a feature we haven't built", "feature request demo", "get approval on a feature".
---

# Feature walkthrough

Turn a codebase and a description of a proposed feature into a single HTML file that
plays a narrated walkthrough of that feature as if it already existed.

The output is one file. No build step, no dependencies, no server, no network calls.
The person you send it to double-clicks it and it plays.

## What it produces

A page that opens with a card saying "this is what we think we heard", then plays
itself: a caption appears, a spotlight grows out of the caption onto the exact part
of the screen being described, and the screen actually moves — lists filter, panels
open, settings cycle through real values. The viewer can pause, step back and forward,
jump to any step, or replay. At the end it asks the only question that matters:
does this look right? Their answer comes back as copyable text, a downloadable file,
or a pre-filled email.

The point is to find out whether you understood the request **before** you build it.

## The controls the viewer gets

The transport bar along the bottom is part of the engine, so every walkthrough has
all of it without you writing a line:

| Control | What it does |
| --- | --- |
| Step dots, `◀` `▶` | Jump to any step, or move one at a time. |
| `Pause` / `Play` | Stops the tour where it is, and the narration with it. |
| `Replay` | Puts the mockup back to its opening state and starts again. |
| `1×` | Cycles the speed: 1×, 1.5×, 2×, 0.75×. |
| `Voice on` / `Voice off` | Reads the narration aloud. |
| Speaker | Mutes and unmutes without turning the narration off. |
| Slider | Sets the narration volume. Dragging it to zero is a mute. |

Two things are worth knowing about the voice. It uses a voice already installed on
the viewer's machine, so the narration works with the network off, exactly like the
rest of the file. And browsers refuse to play audio until the viewer has interacted
with the page, so the voice switches itself on only when they actually press **Show
me**. If the intro card simply times out, the walkthrough starts silent and the Voice
button turns it on.

Speed changes the step timing and the speaking rate together, and applies from the
next sentence so the current one is not cut off. When the voice is on, each step
waits for its sentence to finish rather than guessing at a duration, so the narration
and the pacing cannot drift apart.

**Recorded narration (optional).** To use a real recorded voice instead of the
browser's built-in one, put one audio clip per tour step into `NARRATION_CLIPS`
in the CONFIG section. Use the same order as `TOUR`, and embed each clip as a
`data:audio/mpeg;base64,...` URI so the page still fetches nothing. The engine plays
the clips through two players: while one step's clip plays, the next step's clip is
loaded into the other player, so there is no gap when the step changes. Every tap
that turns the voice on (Show me, Voice) unlocks both players, which iOS requires.
Leave `NARRATION_CLIPS` empty to keep the built-in voice.

**The tour pauses itself when the page is out of view.** Browsers slow or stop a
hidden page's timers (another tab, another app, a locked phone), while recorded
audio can keep going, so the voice and the picture used to drift apart. Now the tour
pauses when the page is hidden and carries on from the same spot when it comes back.
`sleep()` inside a step also holds still while the tour is paused, so Pause freezes
the moving picture as well as the voice. Engine code that must keep ticking while
paused uses `rawSleep()`.

**Because a viewer can jump to any step, every step must set up its own screen.**
Never write a step whose `run` depends on the step before it having run: put the
scene, the filters and the open panels that step needs inside that step.

## Every image lives inside the file

The file fetches nothing, so it may not reference one either. A logo, an avatar,
an icon or a screenshot goes in as **inline `<svg>`** or as a **`data:` URI**,
never as a path or a URL. An `<img src="logo.png">` works on your machine and
shows a broken-image icon on theirs, on the first screen, on a page whose whole
claim is that it needs nothing.

If you cannot embed an image, draw it. A wordmark set in the product's own type
beats a broken picture of one.

## What you need from the user

Exactly two things. Ask for both, then stop and wait.

1. **The codebase** — a path to the repository of the application the feature belongs to.
2. **What the feature should do** — in as much detail as they can give.

If they give you one and not the other, ask for the missing one. Do not start
without both. A walkthrough built without reading the codebase looks like a generic
template, and a walkthrough built from a one-line description shows the wrong feature.

## Procedure

### Step 1 — Read the codebase

This is the step that makes the result convincing, and it is the step that is
tempting to skip. Do not skip it.

Read `reference/reading-the-codebase.md` and follow it. You are extracting three
things: the real theme values, the real component shapes, and the real vocabulary.

Never invent a colour, a font, a field name, or a piece of domain terminology that
you could have read from the codebase instead.

### Step 2 — Say back what you understood, and wait

Before building anything, tell the user in plain language:

- which application this is, and how you can tell
- the visual style you extracted, naming the actual values
- what you believe the feature does, broken into three or four points
- the walkthrough you intend to script, as a numbered list of steps

Then stop and ask them to correct it. This costs one message and saves a rebuild.
It is also exactly what the intro card will say, so the work is not wasted.

Only continue once they confirm.

### Step 3 — Build the file

Copy `template/walkthrough-template.html` to a new file named for the feature and
fill in the five sections marked YOURS. They are numbered in the file:

1. **Theme tokens** — the values from step 1
2. **Mockup CSS** — the fake screen's styles, matching the real product's components
3. **Mockup markup** — the fake screen itself, replacing the placeholder entirely
4. **Mockup state** — fake data using the product's real vocabulary, plus `renderMockup()` and `resetMockup()`
5. **The tour** — the narration script

Read `reference/writing-the-tour.md` before writing the tour. The tour is the
difference between something people watch to the end and something they close.

Leave everything marked ENGINE alone. It is proven and it is not worth re-deriving.

Put the finished file wherever the user is working, not in a temporary directory.
Name it after the feature, for example `expiring-quotes-walkthrough.html`.

### Step 4 — Check it actually runs

Do not hand over a file you have not seen work. Read
`reference/verifying.md` and run the checks there. At minimum, confirm the
JavaScript parses and the page renders with the spotlight on the right element.

### Step 5 — Hand it over

Tell the user the full path to the file and that they can open it by
double-clicking it or send it to anyone as an attachment.

If they want the reviewer's answer to come back automatically rather than by
copy and paste, read `reference/sharing-the-result.md` — it covers the optional
webhook and how to put the file on a web address. Do not set any of that up
unless they ask.

## Rules

**Fake the data, never the vocabulary.** Invent company names, amounts and dates.
Never invent what the product calls things. If the codebase says "policy" do not
write "record". If a status is "BOUND AND ISSUED" do not shorten it. Getting a
customer's own words wrong is what makes a mockup feel like it was made by someone
who was not listening.

**Fix the date.** Pin a constant `TODAY` in the file. A walkthrough that computes
dates from the real clock looks wrong a month later.

**Show the feature working, not the feature existing.** A step that says "here is the
new panel" is weak. A step that says "the list filters to exactly the four that need
you" and then filters the list is what sells it.

**Do not build the feature.** This is a drawing of a feature, not an implementation.
Never modify the codebase you were pointed at. Read from it only.

**It has to work on a phone.** Reviewers open the link on their phone, often
sideways. Keep the mockup markup inside `<div id="stage">` and size it with
`var(--sw)` / `var(--sh)`, never `100vw` / `100vh`. The engine draws the stage at
desktop size (`STAGE_MIN_W` x `STAGE_MIN_H`) and scales it down to fit, so nothing
runs off the side. If you paste in CSS captured from the real app, rewrite its
viewport units the same way and neutralise its width media queries, or the app
falls into its own mobile layout inside the scaled stage.

**One file, no dependencies.** No CDN links, no fonts fetched over the network, no
frameworks. It has to work on a laptop with no internet, opened from a file path,
possibly years from now.

## Reference

- `reference/reading-the-codebase.md` — how to extract the theme, components and vocabulary
- `reference/writing-the-tour.md` — how to script a walkthrough people watch to the end
- `reference/verifying.md` — how to confirm the file works before you hand it over
- `reference/sharing-the-result.md` — optional: webhooks and hosting
- `template/walkthrough-template.html` — the engine, with the five slots
- `example/` — a complete worked example, with notes on why it is built the way it is

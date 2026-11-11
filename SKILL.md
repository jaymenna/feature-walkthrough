---
name: feature-walkthrough
description: Use when someone wants to show a customer or stakeholder a feature that has not been built yet - a narrated, self-playing walkthrough of a proposed feature, styled to look like their real application, produced as one self-contained HTML file. Triggers on "/feature-walkthrough", "mock up this feature", "show them what it would look like", "demo a feature we haven't built", "feature request demo", "get approval on a feature".
---

# Feature walkthrough

Turn a codebase and a description of a proposed feature into a single HTML file that
plays a narrated walkthrough of that feature as if it already existed.

The output is one file. No build step, no dependencies, no server, no network calls.
The person you send it to double-clicks it and it plays.

## HARD RULE: screens come from the real app's source, never drawn by hand (Jay, 2026-11-11)

Every screen in a walkthrough is captured from the real application running from its
own source code: its real DOM, its real CSS as written, its real components, fonts,
colours and layout. A hand-drawn imitation (theme values plus your own CSS and markup)
is never allowed, however close it looks. Jay rejected hand-drawn walkthroughs on
2026-10-28 and again on 2026-11-11: "Make sure that you use the base code, the source
code, to use the styles, colors, and layout so it looks like it exactly comes from it."

How, for a React/Mantine app such as the system Convene Risk Partners uses:
1. Run the app locally from the branch that has the screens (a local server on a
   spare port, local database only). Never use live.
2. Open the real page with Playwright (headless, `--mute-audio`), abort every non-GET
   request so nothing is saved, and put made-up data in place. For a feature that is
   not built yet, render the parts that already exist elsewhere in the app (for example
   the Attento MTC component the new screen will reuse) with Playwright `page.route`
   answering the API with invented JSON, and capture that real component.
3. Freeze input values into attributes, remove every hidden option list
   (`.mantine-Combobox-dropdown, [role=listbox], [role=option]`, real names live there),
   then take the page's HTML and the Mantine modal portals.
4. Read the CSS as written (each stylesheet file and every `<style>` text), never
   `cssRules.cssText`. Keep `<html data-mantine-color-scheme="light">` and set
   `html { font-size: 16px }` in the walkthrough.
5. Only where the new feature adds something that exists nowhere yet, build it inside
   the captured page from the same captured Mantine classes, never from new CSS.
6. Checking the finished page stays static (check_template.sh, a JavaScript parse, curl),
   per the global no-sound rule, unless Jay asks in that message for it to be played.
7. Capture EVERY state of a reused component from the real app, never assemble one
   (Jay, 2026-11-11, Arch MTC document reading). For a Documents card that means: empty,
   drag-over (dispatch a real `dragenter` with a DataTransfer), each file added (set the
   real hidden file input; answer `POST /api/files/staging` with invented JSON), the real
   dialog (click its real button and take the `.mantine-Modal-root` portal), working
   (answer the job as `running`) and done (answer it as `done`). A dialog or alert put
   together from Mantine class names is a hand drawing, even when the classes are real.
   A button that needs a sign-in (Import from Outlook needs `window.__msalAccount`) is
   switched on with `addInitScript`, never drawn.
8. Splice into the template at the line that is exactly `<div id="stage">`. The template
   also says `<div id="stage">` inside a comment; cutting from there deletes the stage and
   the page shows only a giant logo (published that way on 2026-11-11). check_template.sh
   now fails such a page.
9. A captured Mantine modal inside the stage needs `.mantine-Modal-root` absolute with
   `inset: 0`, and `.mantine-Modal-overlay` / `.mantine-Modal-inner` absolute with
   `inset: 0; width: 100%; height: 100%`, or the dialog collapses to nothing.
10. Before publishing, look at the page: render the file with JavaScript disabled
   (Playwright `javaScriptEnabled: false`, `--mute-audio`; nothing on the page executes,
   so nothing can play) and check the stage and the first screen. When Jay asks for it to
   be played, play every step headless with `--mute-audio` and `speechSynthesis` removed,
   never press "Show me", and look at a picture of each step before giving the link.
   Screen states can also be checked in a harness page that holds ONLY the captured
   stage and the screen code (section 7, with `$`, `sleep`, `spotReveal` stubbed): no
   engine, no tour, no voice code, so nothing can play. Look at every spotlight target:
   a target below the fold (a table row) needs its own scroll in that step.

## LANDMINES: traps already hit, never hit again (Jay, 2026-11-11)

Whenever the cause of a broken walkthrough is found, add it here the same day, and add a
check for it to scripts/check_template.sh when it can be checked. Jay: "I'm tired of
encountering the same error over and over again."

1. **Giant logo, tour "1 / 1", nothing else on screen.** The builder found
   `<div id="stage">` inside the template comment and pasted the page into the comment.
   Splice only at the line that is exactly `<div id="stage">`; check_template.sh fails it.
   Hit on several Arch MTC walkthroughs on 2026-11-11, vehicle summary included.
2. **Open questions vanish from the review card.** The engine overwrites `#apSubtitle`
   with `textContent` at start. Put open questions in their own element after it;
   check_template.sh fails a page with markup inside `#apSubtitle`.
3. **Dialogs render transparent.** `<html data-mantine-color-scheme="light">` was lost;
   check_template.sh fails it.
4. **A captured page jumps to Workspace.** The line is switched off in the local database
   (other tabs change it). Switch it on inside the capture only, with Playwright
   `page.route('**/api/lines*')` returning the same answer with that line `enabled: true`.
   Never change the database for a capture.
5. **An open Select dropdown is not found.** Mantine's dropdown is `position: fixed`, so
   `offsetParent` is null. Find it by `[role=listbox]` and take its
   `.mantine-Popover-dropdown` parent. Mark the highlighted option with the real
   `data-combobox-selected` attribute, never a class of your own.
6. **`page.goto(..., { waitUntil: 'networkidle' })` never returns** on Convene (it polls).
   Use `load` plus a wait of 5 to 6 seconds.
7. **A card scrolls to the wrong place.** Convene cards report offsetTop 0. Scroll with
   getBoundingClientRect and leave about 190 px for the menu bar and the sticky page toolbar.
8. **A real component that is not on any page yet** (a `MessageAlert` with the new
   words): render it from source in a temporary Vite harness (a `wt-harness.html` plus
   one `.jsx` in the client folder that mounts the component in `MantineProvider`; run
   `npx vite --port <spare>`), capture its outerHTML, then trash both files. Never
   assemble it from class names.
9. **check_template.sh says "script does not parse" on a page fetched from try.undtec.com.**
   Cloudflare adds its own `<script>` before `</body>` of every served page, and the check
   reads it together with the page's script. The page is fine. Run the check on the local
   file, and prove the published copy is the same file with `sha256sum` on nodes-live.
10. **Rate on a captured quote page does nothing or shows "Not filled in: ...".** The
   page saves before it rates, so the local test policy needs every required field
   (County, Agency, Agent, Underwriter): fill them in the captured load answer
   (`page.route` on the quote GET), answer the save POST and the rate POST with invented
   JSON, and wait for the dialog's own text (`WITHIN GUIDELINES`), never for
   `.mantine-Modal-root` (one hidden root per modal is always in the page).
11. **The toolbar shows the test policy's old premium** ("$13,838 rated · decline").
   Set the stored rating fields (`rated_total_premium`, `rated_status`, `rated_reasons`,
   `rated_breakdown`) in the captured load answer to the invented figures too.
12. **A captured POWERS page looks a size too big.** `html { font-size: 16px }` (step 4 above)
   is right for Convene only. POWERS sets `html { font-size: var(--ut-text-size) }` (14px), so
   the override enlarges every rem. Check the captured CSS for its own `html` font-size first and
   add no override when it has one. Hit on the NEIU Agents Type badges walkthrough, 2026-11-11.
13. **The capture gets no API answers and the page stays blank.** `page.route('**/api/**')` also
   matches the Vite dev server's own source files (`/src/api/queryClient.ts`), so the app's code
   is answered with JSON. Route by pathname: `page.route((u) => u.pathname.startsWith('/api/'), ...)`.
   Hit on the same walkthrough, 2026-11-11.

Worked examples: docs/decline-at-intake-walkthrough.html and
.claude/arch-mtc-rating-basis-walkthrough/capture.cjs in the convene-app repo.

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

### The voice

Set `VOICE` in the CONFIG section to one of three values:

| `VOICE` | What the viewer hears |
| --- | --- |
| `'builtin'` (default) | A voice already installed on the viewer's machine. Nothing is downloaded, and it works with the network off. |
| `'elevenlabs'` | A recorded ElevenLabs clip for every step, listed in `VOICE_CLIPS`. |
| `'none'` | No voice. The tour paces itself and the voice controls are hidden. |

**Every step has its own narration.** There is no single long voice track. A step
starts its own sentence or clip, runs its screen, and waits for that narration to
end. Then there is a full **1.5-second** gap, and only then does the next step start.
The voice and the screen cannot drift apart, and a viewer who jumps to any step
hears that step's own narration.

**The tour plays 10% slower than the old 1x.** The engine applies one pace,
`VOICE_PACE = 0.9`, to the speaking rate, the recorded clips (pitch kept) and the
silent step timing. The speed button multiplies it.

**Recorded clips load a few steps ahead, one at a time.** For `'elevenlabs'` the
player downloads one clip at a time, nearest first: the step on screen, then the
steps after it in order. The next two clips are always kept ready, and when there is
time it carries on up to eight steps ahead. It never loads the whole tour at the
start, and a clip that has arrived is kept, so stepping back does not download it
again. If the viewer jumps ahead, the clips for the new step and the two after it
come first. A clip that cannot play does not stop the tour: that step falls back to
its silent reading time.

To make the clips, run:

```
ELEVENLABS_API_KEY=... python scripts/make_voice_clips.py path/to/walkthrough.html --update-html
```

It reads each step's `text` from `TOUR`, asks ElevenLabs for that sentence alone,
writes `voice/step-01.mp3`, `voice/step-02.mp3`, ... beside the page, and sets
`VOICE` and `VOICE_CLIPS` in the page. Run it again after you change a sentence: only
the changed steps are asked for again. `--say "TRIA=Tree-uh"` changes how a term is
spoken without changing the caption. `--voice-id` picks the voice (the default is
Eric). Add `--embed` to put the clips inside the page as `data:` URIs, so it stays
one file that plays with the network off; the clips still play one step at a time.

Browsers refuse to play sound until the viewer has interacted with the page, so the
voice switches itself on only when they press **Show me**, and that tap unlocks the
sound for the rest of the visit. If the intro card simply times out, the walkthrough
starts silent and the Voice button turns it on.

Speed applies from the next sentence, so the current one is not cut off.

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
copy and paste, read `reference/sharing-the-result.md` — it covers the
try.undtec.com relay and how to put the file on a web address. Do not set any of
that up unless they ask.

**NEXT_PROMPT is the entire build prompt followed by the entire test plan (Jay, 2026-11-09),
never one sentence.** Read `reference/next-prompt.md` before you set it. The Slack post has two
parts: the top is for the people in the channel (decision, assignee, comments, link), and the code
block is for the AI. The draft-email request is never in the post; the reviewer sees it on screen.

**Every review card has a checkbox at the bottom (Jay, 2026-11-09, permanent):** "Draft an email
to <CLIENT_CONTACT> for approval?" (set `CLIENT_CONTACT` and `CLIENT_EMAIL_SUMMARY` in CONFIG).
When it is checked, the reviewer's done screen shows a full prompt to paste into their own Claude
Code, which saves the email as a draft in their outgoing mailbox with the Underwriters Technologies
template, never sent. Nothing about it goes to Slack. Never remove the checkbox.

**Any email shown in a walkthrough is the person's own Google or Microsoft mailbox, not part of
Underwriters Technologies.** Draw it as their email app (Gmail or Outlook Drafts), never as a panel inside the system.

The review card (template version 2, `TEMPLATE_VERSION = 2` in CONFIG) has exactly
three choices: Approved, Approve with the following changes, Denied. It also has an
"Assign the node to" list, filled from `ASSIGNEES` (name → Slack user id; the list
hides when `ASSIGNEES` is empty), and `REVIEWER` pre-fills "Your name" with the node
creator. With `FEEDBACK_ENDPOINT`, `FEEDBACK_KEY`, `PAGE_PATH`, `WALKTHROUGH_URL` and
`NEXT_PROMPT` set, Send posts the decision to the relay, which posts it in the
node's Slack channel with the assignee, the link and the prompt in a code block.
`scripts/check_template.sh [page]` checks any page for all of this.

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
possibly years from now. The one exception is the recorded voice: its clips may sit
in a `voice/` folder beside the page when the page is hosted. Send that folder with
the page, or use `--embed` when the page must travel as one file.

## Reference

- `reference/reading-the-codebase.md` — how to extract the theme, components and vocabulary
- `reference/writing-the-tour.md` — how to script a walkthrough people watch to the end
- `reference/verifying.md` — how to confirm the file works before you hand it over
- `reference/sharing-the-result.md` — optional: webhooks and hosting
- `template/walkthrough-template.html` — the engine, with the five slots
- `example/` — a complete worked example, with notes on why it is built the way it is

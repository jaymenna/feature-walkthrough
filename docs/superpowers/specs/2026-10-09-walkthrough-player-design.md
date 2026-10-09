# Walkthrough player: one canonical, robust engine

Date: 2026-10-09. Branch: narration-clips-and-sync. Approved by Jay in the
session that produced
~/.claude/adversarial-reviews/adversarial-review-walkthrough-serving-2026-10-09.md.

## Problem

Narrated walkthroughs (one self-contained HTML file each, 0.6 to 9 MB, with
ElevenLabs MP3 clips embedded as base64) stall, start without the voice, and
slow to a crawl. The audit found four root causes:

1. Seven hand-patched player variants are live; no canonical engine.
2. No variant calls play() synchronously inside the viewer's tap, so Safari,
   iPhone and in-app browsers reject every clip; one variant then forces
   voiceOn and races through the captions 620 ms apart.
3. The engine is the last 1 percent of a multi-megabyte chunked download; a
   slow or dropped transfer shows a half-drawn page and nothing else.
4. Every wait counts 80 ms timer ticks instead of the clock, so a hidden tab
   (Chrome throttles to one tick per second, then one per minute) turns each
   step into 19 seconds, then 19 minutes, of dead air.

## Scope

In scope: template/walkthrough-template.html (engine CSS, intro card
structure, engine script), a new scripts/check-playback.mjs test gate, and
the docs that describe the behaviour (SKILL.md, reference/verifying.md, and
the "no start card" and "Blocked sound" sections of
~/.claude/skills/deliver-for-customer/SKILL.md).

Out of scope: republishing the 19 live pages on try.undtec.com, rebuilding the
McGowan demo, nginx pre-compression on the nodes-live droplet, and the
Cloudflare exemption for /mockups/*. Each is a separate decision.

The one-file, no-network, double-click-to-play contract stays.

## Behaviour

### Sound card

The intro card (#hero) keeps its YOURS words. Its foot has two buttons and no
countdown: `Play with voice` (primary, id heroVoice) and `Read silently`
(id heroSilent). Nothing starts until one is tapped, on every device.

- `Play with voice`: inside the click handler, synchronously, the engine
  sets voiceOn true, sets the single audio element's src to clip 1's Blob
  URL at the current volume, and calls play(). The card fades, the tour
  starts, and step 1 follows the clip that is already playing instead of
  restarting it.
- `Read silently`: voiceOn false; the tour runs on the silent pacing.
- Clicking the card's backdrop does nothing. There is no timeout.

### Audio

- On boot, each entry of NARRATION_CLIPS (data:audio/mpeg;base64,...) is
  decoded once into a Blob and a Blob URL. The base64 string is dropped after
  conversion. Pages with no clips keep the browser speech path unchanged.
- One Audio element (`narrator`) for the whole session. No second element.
- Two flags. `voiceOn` is what the viewer asked for. `audioUnlocked` is what
  the browser has allowed; it becomes true on the first `playing` event and
  false when play() rejects with NotAllowedError.
- When play() is rejected: the step falls back to silent pacing, and a small
  grey line `Click anywhere for sound` (id soundHint) appears in the lower
  left. The next pointerdown anywhere outside the transport bar hides the
  line and replays the current step with voice, calling play() inside that
  handler. The Voice button, the mute button and the volume slider keep
  their current behaviour and each calls play() inside its own click.
- playbackRate follows the speed button as today.

### Waits and watchdogs

- `speak(text)` resolves true on `ended`. It resolves false on `error`, on
  play() rejection, when no `playing` event arrives within 6 s of play(),
  or when unpaused playing time exceeds duration divided by speed plus 4 s
  (120 s when the duration is unknown). Time is measured with
  performance.now() and excludes paused time.
- `hold(ms)` is a deadline: it sleeps until performance.now() reaches the
  deadline, extends the deadline by any time spent paused, and still throws
  "superseded" when the tour token changes.
- In playFrom, when the voice is on the step waits for speak(); if speak()
  resolved false, the step then holds for the silent duration (2.6 s or
  3.4 s by caption length, divided by speed) minus the time already spent,
  never the 620 ms voice follow-on.
- visibilitychange hidden: pause the tour and the audio (already on the
  branch). visible: resume. pagehide: stop the audio. pageshow with
  `persisted` true: re-run the current step with playFrom(currentStep,
  tourAuto).

### Loading line

An inline script immediately after `<body>` creates a fixed, centred grey
line `Loading the walkthrough...` (id wtLoading). At 8 s it reads `Still
loading on a slow connection...`; at 30 s a `Reload` button appears beside
it that calls location.reload(). The engine removes the element as its first
act at boot. If the engine never runs (truncated transfer, parse error), the
line and the button stay.

### Engine contract

- `const ENGINE_VERSION = '2.0.0'` at the top of the engine block; logged
  once to the console and included in the review payload text.
- The engine block is everything from the `9. ENGINE` banner to the closing
  `</script>`, and the engine CSS is everything between the `3. ENGINE CSS`
  and `4. MOCKUP MARKUP` banners. Builds replace those blocks whole and never
  splice inside them. SKILL.md states this.
- The engine exposes `window.__walkthrough = { version, step, events: [] }`
  where events is an array of `{ t, type, step }` for: boot, loading-removed,
  card-voice, card-silent, play-requested, playing, play-rejected, ended,
  watchdog, step, hint-shown, hint-hidden. It exists for the test gate and
  costs nothing.

### Test gate

`scripts/check-playback.mjs <walkthrough.html>` opens the file in headless
Chromium through Playwright (resolved from the repo's node_modules, then from
~/.claude/skills/gstack/node_modules; the script says which it used and
fails with instructions if neither exists). It runs four scenarios and exits
non-zero on the first failure:

1. Normal: the loading line is present before the engine boots and gone
   after; after clicking `Play with voice`, a `playing` event arrives within
   2 s; across the first five steps no `step` event precedes the previous
   clip's `ended` or `watchdog` event.
2. Blocked audio: an init script makes HTMLMediaElement.prototype.play
   reject with NotAllowedError; after `Play with voice` the hint is visible,
   and steps 1 to 3 each last at least 2.5 s at speed 1.
3. Stuck clip: an init script makes play() resolve but suppresses `ended`;
   the watchdog releases step 1 within duration plus 5 s.
4. Silent: after `Read silently`, no play() is called and steps advance on
   the silent pacing.

The example walkthrough (example/expiring-quotes-walkthrough.html) gets a
clip array of three short silent MP3 data URIs so the gate has something to
play without any network or key.

## Docs

- SKILL.md: the controls table and the voice paragraph describe the sound
  card, the two flags, the hint and the engine contract; the per-step rule
  stays.
- reference/verifying.md: section 3 runs scripts/check-playback.mjs first.
- deliver-for-customer SKILL.md: "The page opens straight into the
  walkthrough, voice on" becomes "The page opens on the sound card";
  "Blocked sound" describes the hint as the fallback after the card. Nothing
  else in that skill changes.

## Testing the change itself

- node --check on the extracted engine script.
- scripts/check-playback.mjs on the example walkthrough, all four scenarios.
- A manual pass on a real Safari (Mac) and an iPhone, which the headless
  gate cannot cover: the voice starts on the tap, Pause and Play work,
  switching tabs and returning resumes the same step.

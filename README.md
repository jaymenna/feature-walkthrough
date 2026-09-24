# feature-walkthrough

A Claude Code skill that turns a codebase and a description of a feature into a
narrated, self-playing walkthrough of that feature — as if it already existed.

The output is one HTML file. No build step, no dependencies, no server, no network
calls. Send it to a customer and they double-click it.

[![The how-it-works walkthrough playing](example/how-it-works-preview.gif)](https://jaymenna.github.io/feature-walkthrough/how-it-works.html)

**[Watch it play, with sound →](https://jaymenna.github.io/feature-walkthrough/how-it-works.html)**
The skill explaining itself, made with itself. About ninety seconds.

## The problem it solves

A customer asks for a feature. You think you understood. You build it for three
weeks and find out you did not.

The usual defences are a written spec nobody reads to the end, or a static mockup
that shows what it looks like but not what it does. Neither reliably catches the
misunderstanding, because neither makes the customer *feel* the feature.

This makes the thing you would have built, before you build it — styled to look
like their actual application, playing itself, narrated a step at a time — and then
asks them, in the file, whether it is right.

An hour of work to find out you misheard, instead of three weeks.

## What it produces

A page that opens with a card saying "this is what we think we heard", then plays
itself:

- a caption appears, one idea at a time, and moves to whichever side of the
  highlighted area has room rather than covering the thing it describes
- a spotlight grows out of the caption onto the exact element being described,
  dimming everything else
- the screen actually moves — lists filter, panels open, settings cycle through real
  values and the numbers change while you watch
- **it reads itself aloud**, using a voice already installed on the viewer's
  machine, so the narration works with the network off like the rest of the file
- the viewer can pause, step, jump to any point, replay, change the speed
  (1×, 1.5×, 2×, 0.75×), turn the voice on or off, mute it, or set the volume
- at the end it asks: does this look right? Their answer comes back as copyable
  text, a downloadable file, a pre-filled email, or a message straight into your
  Slack — you set that up once and the file carries it

The screen is not a generic template. The skill reads the target codebase for its
real theme values, its real component shapes and its real domain vocabulary, so it
looks like the customer's own product and speaks in their own words.

### About the voice

The narration is spoken by the browser's own speech engine, so nothing is
embedded and nothing is fetched. What that means in practice:

| Where it opens | Voice |
| --- | --- |
| macOS, Windows | Works offline. Quality depends on the voices installed; an Enhanced or Premium voice sounds far better than the default compact one. |
| iPhone, Android, ChromeOS | Works. |
| Linux | Usually silent — desktop browsers there have no speech engine unless `speech-dispatcher` and `espeak` are installed. |

Browsers refuse to play audio until the viewer has interacted with the page, so
the walkthrough starts silent and the **Voice Is Off** button turns it on. That
press is also what unlocks audio on iPhone and Safari, which is why the button
begins speaking inside the tap itself.

## Install

Clone into your Claude Code skills directory:

```bash
git clone https://github.com/jaymenna/feature-walkthrough.git \
  ~/.claude/skills/feature-walkthrough
```

Or for one project only, clone it into that project's `.claude/skills/` instead.

Then in Claude Code:

```
/feature-walkthrough
```

It will ask you for two things: the path to the codebase, and what the feature
should do. That is all it needs.

## Companion skill: demo-pitch

A feature walkthrough asks whether the proposed behavior is right. The new
[demo-pitch skill](demo-pitch/SKILL.md) helps a viewer recognize a problem, see the
proposed solution, and understand why it matters. It recommends a concrete
situation/problem/outcome/proof/next-step outline, iterates on the pitch goals with
the user, and records agreement in `pitch-demo-brief.md` before production.

Keep independent pitch-demo and feature-demo artifacts and approvals. The pitch
skill includes [story guidance](demo-pitch/references/story-and-production.md),
[narration direction](demo-pitch/references/narration.md),
[research sources](demo-pitch/references/research.md), and a
[fictional worked brief](demo-pitch/examples/pitch-demo-brief.md).
Its optional JSON renderer makes an offline **planning storyboard**, not a product
demo or video. Voice generation and recording use the tools available in the
working project; no TTS service, video exporter or provider account is bundled.
For finished pitch production, the companion plans narration in the first version,
samples the selected voice before full generation, and keeps measured audio,
captions and scene timing synchronized. It reports listening limits explicitly.

### Install the companion or both skills

The original clone installation and `/feature-walkthrough` command above are
unchanged. **Cloning alone does not install the companion as a separate skill.**
To use only the new companion, copy this repository's `demo-pitch/`
folder into your agent's skills directory.

To export two independent folders with the parallel names `demo-features` and
`demo-pitch`, run from this repository with Python 3:

```bash
python scripts/package_skills.py --out ../demo-skills
```

Copy the selected output folder(s) into `~/.claude/skills/` for Claude Code, or
`~/.agents/skills/` for Codex. For a project, use `.claude/skills/` or
`.agents/skills/`, respectively. See [Codex's official skill discovery and metadata
documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).
The new pitch skill includes optional `agents/openai.yaml` UI metadata; the feature
export does not add vendor metadata to the original skill.

The packager does not install anything, requires output outside the checkout, and
refuses existing target folders. `demo-features` is an optional export name; it does not rename an existing
`feature-walkthrough` installation. Install one feature name to avoid duplicate
discovery. Use `--feature-name feature-walkthrough` to export the legacy name.

Examples after installing the exported folders:

```text
/demo-features — show the proposed request form and collect behavior feedback
/demo-pitch — show procurement coordinators how this concept addresses incomplete requests
```

Those are Claude Code invocations. In Codex, mention `$demo-features` or
`$demo-pitch`, or select the skill through the skill picker.

### Inspect the fictional planning example

Open [the SupplyLane storyboard](demo-pitch/examples/supplylane-storyboard.html)
offline, or regenerate it:

```bash
python demo-pitch/scripts/render_storyboard.py demo-pitch/examples/supplylane-storyboard.json /path/to/storyboard.html
python -m unittest discover -s scripts -p "test_*.py" -v
```

All SupplyLane product behavior is proposed, all data is fictional, and the example
contains no real approval record or claimed customer result. The renderer uses only
the Python standard library, escapes supplied markup and keeps evidence type and
data origin separate. It does not generate audio or interactive product screens.

## See it before you install anything

**[How it works](https://jaymenna.github.io/feature-walkthrough/how-it-works.html)**
— this skill, explained using this skill. A walkthrough of what actually happens
when you invoke it, start to finish. About ninety seconds.

![The example walkthrough, mid-play](example/screenshot.png)

**[A finished walkthrough](https://jaymenna.github.io/feature-walkthrough/example/expiring-quotes-walkthrough.html)**
— what the skill produces for a real feature: an alert system for an insurance
underwriting platform. About a minute. `example/README.md` explains why it is
built the way it is.

Both play themselves in the browser. Neither needs anything installed.

## What is in here

```
SKILL.md                              the skill Claude Code reads
how-it-works.html                     this skill, explained using this skill
template/walkthrough-template.html    the engine, with five slots to fill
reference/reading-the-codebase.md     extracting theme, components and vocabulary
reference/writing-the-tour.md         scripting a walkthrough people watch to the end
reference/verifying.md                confirming it works before you send it
reference/sharing-the-result.md       optional webhooks and hosting
example/                              a complete worked example
```

The template runs as-is with a placeholder screen, so you can open it and watch the
engine work before putting anything of your own into it.

## Using the engine without Claude

`template/walkthrough-template.html` is a normal HTML file. Everything marked YOURS
is yours to fill in by hand; everything marked ENGINE can be left alone. If you
would rather write the tour yourself, the template is a perfectly good starting
point on its own.

The interesting part of the engine is the spotlight. `#spot` has no background of
its own — a 9999-pixel box-shadow spread darkens the entire screen around it, so
whatever sits inside the hole stays fully lit and readable. The highlight is born at
the caption and grows out to the element being described, so the two read as one
gesture rather than two separate things happening.

## Design decisions worth knowing about

**One file, always.** No CDN links, no fetched fonts, no frameworks. It has to work
on a laptop with no internet, opened from a file path, years from now.

**Fake the data, never the vocabulary.** Invent the company names and the amounts.
Never invent what the product calls things. Getting a customer's own words wrong is
exactly what makes a mockup feel like it was made by someone who was not listening.

**Nothing is sent anywhere by default.** The review stays in the browser until the
reviewer presses Copy, Download or Email. An optional webhook exists for teams that
want reviews to arrive automatically, and it points at your infrastructure, not
anyone else's.

**It does not touch the codebase it reads.** This is a drawing of a feature, not an
implementation.

## Credit

The engine came out of a working process at Underwriters Technologies for getting
sign-off on feature requests before building them. It is published here because it
turned out to be useful and there is no reason to keep it.

## Licence

MIT. See [LICENSE](LICENSE).

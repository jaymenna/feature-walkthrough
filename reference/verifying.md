# Verifying the file before you hand it over

Never hand over a walkthrough you have not seen run. A broken one is worse than
none, because the customer's first impression of the feature is a blank page.

## 1. The JavaScript parses

The most common failure is a syntax error inside a tour step, which leaves the page
completely blank with nothing on screen to explain why.

Extract the script block and check it:

```bash
awk '/^<script>$/{f=1;next} /^<\/script>$/{f=0} f' walkthrough.html > /tmp/check.js
node --check /tmp/check.js
```

Silence means it parses. Anything else names the line.

This takes two seconds and catches most of what goes wrong.

## 2. It renders, and the spotlight lands correctly

Render it headlessly and look at the result:

```bash
timeout 40 "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1440,900 --virtual-time-budget=16000 \
  --screenshot=/tmp/shot.png --user-data-dir=/tmp/chrome-check \
  "file:///absolute/path/to/walkthrough.html"
```

On Linux use `google-chrome` or `chromium`. On Windows use the full path to
`chrome.exe`.

**Chrome will not exit on its own here, and that is expected.** The page has timers
running for the whole tour, so Chrome never decides the page is finished. That is
why the command is wrapped in `timeout`. A non-zero exit code from `timeout` is
normal — judge the result by whether the PNG was written, not by the exit code.

Vary `--virtual-time-budget` to land on different steps: roughly four seconds of
budget per step after the seven-second intro card.

Look at the screenshot and check:

- the screen looks like the customer's product, not like a generic template
- the caption is readable and the step counter is sensible
- the dimming is on, and the lit region is the thing the caption is talking about
- the transport bar is at the bottom with one dot per step

## 2b. It fits a phone, upright and sideways

Most reviewers open the link on a phone. Check a phone held sideways, a phone
held upright, a tablet, and a desktop. With Playwright:

```js
const { chromium, devices } = require('playwright');
for (const d of ['iPhone 14 landscape', 'iPhone 14', 'iPad Pro 11', null]) {
  const ctx = await browser.newContext(d ? devices[d] : { viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto('file:///absolute/path/to/walkthrough.html');
  // ...tap Show me, jump to a few steps, take screenshots
}
```

On every size, check:

- nothing scrolls sideways (`document.documentElement.scrollWidth` equals `innerWidth`)
- the whole mockup is on screen, and the spotlight lands on the right element
- the caption and the transport bar do not cover each other
- the intro card's Show me button is visible without scrolling
- a tap (not a click) on anything the tour opens still works

## 3. The things worth clicking through yourself

Open it in a real browser and confirm:

- the intro card appears, then hands off to the tour on its own
- Pause actually pauses, and Play resumes from where it stopped
- clicking a dot jumps to that step, and the step draws correctly when arrived at
  out of order — this is where `resetMockup()` gaps show up
- Replay returns the mockup to its opening state rather than replaying from wherever
  it happened to be
- the review panel opens at the end
- Send with nothing filled in shows the validation errors rather than doing nothing
- Copy, Download and Email all produce the review text

## 4. The self-contained check

The file has to work with no internet, from a file path, on someone else's laptop.

```bash
grep -oE 'src="https?://[^"]*|href="https?://[^"]*|@import[^;]*' walkthrough.html
```

Any hit is a dependency that will fail for the recipient. Inline it or remove it.

Fonts are the usual offender. A Google Fonts link works on your machine and turns
the customer's copy into Times New Roman.

## 5. Nothing private went in

Before sending a file to anyone outside your organisation:

```bash
grep -niE 'token|secret|api[_-]?key|password|bearer|@[a-z0-9.-]+\.(com|net|org)' walkthrough.html
```

Check every hit. The only credential this file should ever carry is a webhook URL
the user deliberately put there, and even that is worth a second thought before it
goes to a customer.

Also confirm the fake data really is fake. Real customer names, real amounts and
real people's names must not be in a file that is about to be emailed around.

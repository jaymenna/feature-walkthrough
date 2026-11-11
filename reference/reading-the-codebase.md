# Reading the codebase

**HARD RULE (Jay, 2026-11-11):** reading the theme is not enough. The screens in the
walkthrough are captured from the real app running from its source code (real DOM,
real CSS as written). Never hand-draw a screen from theme values. See the HARD RULE at
the top of SKILL.md for the capture steps. This page is for the vocabulary and for
knowing which screens and components to capture.

The walkthrough has to look like it was taken from the customer's own application.
That comes from reading their code, not from styling something that looks nice.

You are extracting three things, in this order.

---

## 1. The theme

Find where the real visual values live. In most projects this is one or two files.
Look in this order and stop when you find real values:

| Stack | Where to look |
|---|---|
| Tailwind | `tailwind.config.*` → `theme.extend.colors`, `fontFamily`, `borderRadius` |
| CSS variables | a `:root` or `:host` block, often in `index.css`, `global.css`, `variables.css`, `tokens.css` |
| Mantine | `theme.ts` / `theme.js` → `colors`, `primaryColor`, `defaultRadius`, `fontFamily` |
| Material UI | `createTheme(...)` → `palette`, `typography`, `shape.borderRadius` |
| Chakra | `extendTheme(...)` |
| styled-components | the object passed to `<ThemeProvider theme={...}>` |
| Bootstrap | a `_variables.scss` override file, or the `$primary` / `$body-color` overrides |
| Sass | `_variables.scss`, `_colors.scss`, `_theme.scss` |
| Design tokens | `tokens.json`, `design-tokens/`, a Style Dictionary config |

Search terms that find it when the file names do not:
`--primary`, `primaryColor`, `brandColor`, `$primary`, `colors:`, `palette:`,
`borderRadius`, `fontFamily`, `theme =`.

Pull out and write down the actual values:

- primary/brand colour, and its hover or dark variant
- body text colour, secondary text colour, muted/disabled text colour
- border colour, and any second lighter border colour
- page background, and the hover/zebra background
- semantic colours: success, warning, danger, info
- any status colours, and exactly which status each one belongs to
- font stack and base font size
- border radius
- shadow style, if the product uses one

**If you cannot find a theme file**, take the values off the rendered product
instead. Look at the most-used shared components — a Button, a Card, a Table — and
read the hex codes out of their styles. Say in your summary that you did this, and
which components you took them from.

**If there is genuinely no styling to read**, say so plainly to the user and ask
what the application looks like, rather than inventing a palette and hoping.

## 2. The component shapes

The theme gets the colours right. The component shapes get the *feel* right, and
people notice the feel before they notice the colours.

Find the shared UI components — usually `components/`, `ui/`, `shared/`, `common/`,
or a design-system package — and read how the product actually builds:

- **Tables and lists.** Are headers uppercase and letter-spaced, or sentence case?
  How tall is a row? Are there zebra stripes, row borders, or neither? Where does
  the row hover state show?
- **Status indicators.** Pills, badges, dots, or coloured text? Rounded fully or
  slightly? Filled with colour or outlined? Uppercase?
- **Navigation.** Sidebar or top bar? How wide? How is the active item marked?
- **Buttons.** Height, corner radius, weight of the label, filled versus outlined.
- **Modals and panels.** Do they overlay the centre, slide in from a side, or dock?
  How dark is the backdrop?
- **Density.** This one matters most. A dense internal tool and an airy consumer
  app can share a palette and still look nothing alike. Match the padding.

## 3. The vocabulary

This is the part that makes a customer say "they were listening", and the part
most mockups get wrong.

Find the domain model — schema files, migrations, type definitions, API
serialisers, form labels, translation files — and take the real words:

- What are the **entities** called? Policy, claim, matter, shipment, ticket, patient.
- What are the **fields** called, as the user sees them, not as the database
  spells them? `eff_dt` in the database might be "Effective date" on screen. Use
  the on-screen wording.
- What are the **statuses**, written exactly as they are displayed, including
  capitalisation? "BOUND AND ISSUED" is not "Bound".
- What are the **roles**? Underwriter, adjuster, dispatcher, case worker.
- What **abbreviations** does this industry use that an outsider would not know?

Good places to find the user-facing wording specifically: i18n/locale JSON files,
form label props, column header definitions, and enum-to-label maps.

---

## What to do with it

Write the theme values straight into the template's `:root` block. Build the mockup
CSS to match the component shapes. Populate the fake data with invented values
carried in real vocabulary.

**Invent the data. Never invent the words.**

Fake company names are good — they keep real customer data out of a file that is
about to be emailed around. Memorable, obviously-fictional names work best, because
nobody mistakes them for real records. Fake amounts, fake dates, fake reference
numbers, all fine.

But every column header, every status value, every role name, and every piece of
jargon must be the customer's own. That is the difference between a mockup that
reads as "we built you something" and one that reads as "we used a template".

---

## Before you build, say it back

Summarise what you found, naming the values:

> This is the Acme claims portal, a React and Mantine app. Primary is `#2f5fa0`
> with `#274f87` on hover, text is near-black on white with `#868e96` for muted,
> borders are `#dee2e6`, radius is 4px, system font stack at 14px. Tables use
> uppercase letter-spaced headers and 11px row padding — dense. Statuses render as
> filled pills in fully-rounded capsules, and the five values are OPEN, IN REVIEW,
> APPROVED, DENIED and CLOSED. You call the records "claims", the people who work
> them "adjusters", and the date that drives everything "date of loss".

If any of that is wrong, the user will correct it in one line, and you will not have
built the wrong thing.

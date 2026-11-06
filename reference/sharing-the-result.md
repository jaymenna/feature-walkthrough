# Getting the walkthrough in front of people

Do none of this unless the user asks. The default — one file, sent as an
attachment — works, needs no infrastructure, and cannot break.

## Default: just send the file

The output is a single HTML file with no dependencies. Email it, drop it in chat,
put it on a shared drive. The recipient double-clicks it and it plays.

This works offline, works on any operating system, works on a locked-down corporate
laptop, and will still work in five years.

The reviewer's answer comes back through whichever of these they prefer:

- **Copy** puts the review on their clipboard to paste wherever they like
- **Download** saves it as a text file
- **Email it** opens a pre-filled message, if `FEEDBACK_EMAIL` was set

Nothing leaves the page unless the reviewer presses one of those buttons.

## Optional: the answer comes back on its own

If the user wants the decision to arrive in the node's Slack channel without the
reviewer copying anything, host the page on try.undtec.com and set the relay
constants at the top of the file (template version 2):

```js
const FEEDBACK_ENDPOINT = 'https://try.undtec.com/mockups/api/feedback';
const FEEDBACK_KEY      = '<the relay key, from the try repo docs/SECURITY.md>';
const PAGE_PATH         = '/mockups/<customer>/<channel name>/index.html';
const WALKTHROUGH_URL   = 'https://try.undtec.com/mockups/<customer>/<channel name>/';
const NEXT_PROMPT       = 'Build <channel name> as approved';
const REVIEWER          = '<the node creator>';
const ASSIGNEES         = { '<name>': '<Slack user id>' };   // the channel's members, names and ids only
```

The relay (`opt/mockup-feedback` in the try repo) maps `PAGE_PATH` to the Slack
channel by the channel name in the path, and posts one message: the decision, the
reviewer, `Assigned to`, the walkthrough link, the comments, and `NEXT_PROMPT` in a
code block that the assignee pastes into Claude Code.

Four things to be straight with the user about:

1. **The key is in the file.** It is public by design: it only lets a page post text
   into a channel. Nothing moves a node or assigns anyone because of a relay post.
   The node creator's own Claude does that, with the creator's own key, after the
   creator confirms the decision.
2. **It never says Sent when nothing was sent.** The page waits at most 15 seconds.
   On a timeout, a network error or any answer that is not 2xx, the card says
   "Not posted to Slack" and shows the copy, download and email buttons.
3. **A repeat is posted once.** Every page load makes a `submission_id`; the relay
   remembers ids for 24 hours and answers 200 without a second post for a repeat.
4. **Fill `ASSIGNEES` from the channel's members.** A mention of someone who is not
   in the channel pings nobody. Names and Slack ids only; never emails on a public
   page.

## Optional: put it on a web address

Some reviewers will not open an HTML attachment, and some mail systems strip them.
A link avoids both problems.

It is one static file, so anything that serves static files will do. Free options
that need no server of your own:

- **GitHub Pages** — commit the file to a repository, enable Pages, link to it
- **Netlify Drop** — drag the file onto `app.netlify.com/drop`, get a URL
- **Cloudflare Pages** — same idea, connected to a repository
- **Any web host you already have** — copy the file in, it needs nothing but a
  static file server

Two cautions worth passing on:

- A public URL is public. Anyone with the link can see the feature you are
  proposing and the customer it is for. If that matters, use the attachment, or
  put the page behind whatever access control your host offers.
- Give the file a name nobody would guess if you are relying on obscurity, and
  remember that obscurity is not access control.

## What not to build

Resist building a service around this. The value is that it is one file that works
everywhere and depends on nothing. A hosting platform, a review database and a
notification pipeline is a different product, and it is the thing that stops people
from using this at all.

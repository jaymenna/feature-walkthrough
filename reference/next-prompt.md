# The Next step prompt (NEXT_PROMPT)

Jay, 2026-11-09: the box "For the AI" in the Slack post is NOT one sentence such as
"Build <node> as approved". It is the ENTIRE prompt followed by the ENTIRE test plan. The
person the node is assigned to pastes it into Claude Code and can work without asking anything.

Set `NEXT_PROMPT` in CONFIG to a template literal (backticks) that holds all of this, in order.
The relay posts up to 12,000 characters. Aim for 3,000 to 8,000. Slack cuts one message near
4,000 characters, so the relay posts a long prompt as several messages, each one a complete code
block (Part 1 of 3 ...). Keep paragraph breaks (blank lines) between sections so the cut falls
between sections. Put the TEST PLAN heading on its own line.

## Part 1: the build prompt

1. **Goal**: one sentence, plain English, in the words of the customer.
2. **Where**: node name and link, Slack channel, git branch (the existing branch of the node),
   repository, the walkthrough link.
3. **What to build**: numbered, specific, one behavior per line. Use the real names of screens,
   buttons, fields, files and functions that you read in the code. Say what already exists and
   what is missing (for example "core has no draft writer").
4. **What not to do**: not in scope; anything that must never happen (for example "never send an
   email, only save a draft").
5. **Open questions**: facts nobody has given yet, and who to ask. Say what to build in the
   meantime (a setting that is empty by default, a clear message to the user).
6. **Rules that apply**: the Edward rule codes the work touches, and the project's own rules.
7. **Process**: new worktree on the existing branch, follow the project CLAUDE.md, run the tests,
   commit (message starts with an imperative verb), push, open a pull request to main, stop at
   sandbox. Never touch live.

## Part 2: the test plan

A numbered list. Every item has: what to do, and the exact result expected. Cover:
- unit tests to write, and what each one asserts (include a test that proves the forbidden
  thing never happens);
- the main path end to end, with real screen names and the exact text expected;
- each failure path (missing setting, not signed in, nothing to attach) and the exact message;
- every provider, size or state the walkthrough showed;
- a regression item for the screen that was touched;
- the manual check on sandbox, step by step, with who does it and what they must see;
- button labels fit (UX-031) at 1440, 1280, 1024 and phone width, when buttons are added.

## Who reads the post

- The channel members read the top of the post: the decision, who has the node, the comments,
  the link. Never put an instruction for the AI there. The draft-email request is not in the post
  at all: it appears on the reviewer's own screen (see `buildDraftEmailPrompt`).
- The assignee's Claude reads the code block. Write it to the AI, in full sentences.

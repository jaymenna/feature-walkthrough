---
name: demo-pitch
description: Create a problem-and-solution product demo that persuades a buyer, investor, or stakeholder through visible proof and a clear next step. Use for demo pitches, product pitch videos, value-focused demos, or turning a feature tour into a compelling problem/solution story. Includes story selection, visual proof, expressive narration direction, and review. For feature behavior walkthroughs or design sign-off, use feature-walkthrough (or its demo-features export) instead.
---

# Demo pitch

Make the viewer recognize a problem, see a worthwhile outcome, and believe the demonstrated path can get them there. The product is evidence in the story. Feature coverage is not the goal.

## Keep the demo lanes separate

Use `demo-pitch` for this lane and `feature-walkthrough` for the existing feature lane (`demo-features` is an optional packaged name). Name this lane's brief **pitch-demo-brief.md**. Use matching pitch-demo names for its storyboard, script, HTML/video and review notes, or keep those files in a dedicated pitch-demo folder. The feature lane uses **feature-demo-brief.md** and feature-demo artifact names. Follow an existing user-selected directory layout; do not relocate or overwrite another lane's work merely to adopt a convention.

Treat brief agreement as **Gate 1**. Record its status and the user's explicit approval in the brief, then continue within that approved direction. Track each lane's brief, revisions and review status independently: approval of a pitch brief does not approve a feature demo or a finished video. Shared product evidence and visual assets are fine; keep lane-specific stories and outputs separate.

## Establish the brief

Use the conversation and supplied artifacts first. Identify whose product this is, the audience and their decision, concrete problem and current workaround, desired outcome, available product evidence, delivery format, approximate time budget, and next step. Record consequential assumptions. Present an unverified buyer problem as a hypothesis to test, not an observed fact; do not invent its frequency or duration to strengthen the opening. Requirements establish capabilities and constraints; they do not establish which problem should lead the pitch. Do not require a codebase when a working product, screenshots, or an adequately described concept is available.

For a finished demo pitch, plan narration with captions by default; honor an explicit silent, live-presenter, planning-only, or script-only request. Read [narration](references/narration.md) during briefing and check the available voice path before promising a finished narrated artifact. Professional audio belongs in the first delivered version, not a later enhancement. Include the voice choice, sample/listening plan, and any real capability limit in the brief.

Read available UI, theme, terminology, and relevant implementation before depicting them. Maintain a small claim ledger: claim, source, evidence type (observed / simulated / planned / measured), data provenance, limitation. A passing UI test proves UI behavior, not a functioning backend or customer outcome. An export action alone does not prove a particular field or audit entry exists in its output; inspect it. Use fictional data without implying customer endorsement. Keep source systems read-only unless changes are already authorized.

## Choose the story before building scenes

Read [story and production](references/story-and-production.md). Briefly consider alternative problem/solution angles and recommend the one best matched to this viewer's decision. Propose a filled-in outline using this research-informed default:

1. **Situation / story:** a brief moment the audience recognizes; who is trying to get what done? This can be part of the problem sentence, not a long anecdote.
2. **Problem and stakes:** what is difficult today, and why does it matter to this audience?
3. **Promise and early outcome:** what would improve? Show or describe the concrete useful result before taking the audience through setup.
4. **Demo as proof:** the shortest visible cause-and-effect path showing how the solution addresses that problem. Address a material doubt within the proof when useful.
5. **Payoff and call to action:** connect the result back to the original problem, then propose one relevant next step.

Fill the outline with actual candidate copy and proof moments; do not hand the user empty headings or a menu of product features. Recommend an angle and explain the main choice briefly. Adapt the shape to the audience and time budget rather than treating five parts as five mandatory slides.

Alongside the outline, make the proposed **pitch goals** explicit: who is watching; the one problem to own; what the viewer should understand or believe afterward; what visible evidence supports that belief; what action they should take; time/format and claim limits. State assumptions and invite corrections on these goals and the outline. Iterate until they are tight and agreed **before building detailed scenes, animation, or recording**. This is a story discussion, not a generic permission request.

Do not treat agreement on requirements, a feature walkthrough, or a prior unrelated pitch as agreement on this story. If the user has already endorsed the current pitch brief, continue without asking again. If they explicitly delegate the story choice and ask you to proceed without iteration, record that direction and the assumptions. Research, evidence inspection, and lightweight alternative outlines can continue while story feedback is pending; dependent production should wait. Record the agreed brief and what was cut. If adapting a tour, reorder and delete scenes; changing the introduction alone is insufficient.

Agreement means a clear endorsement of this framing or an instruction to proceed with it; silence, elapsed time, and agreement on skill names are not story agreement. If later feedback materially changes the audience, central problem, promise, or scope, revisit the brief before resuming dependent production. Keep pre-agreement work lightweight unless the user requested deeper research; avoid building enough speculative material that it anchors the discussion.

Start with a clear problem statement: who encounters what friction, in what situation, with what consequence. Then show a concrete desired result early. Demonstrate the smallest meaningful sequence that explains how the result happens. Address a material objection when it affects credibility. Close the original problem and give one relevant next step. Treat this as a flexible story shape, not a mandatory scene count or fixed duration.

For each proof beat specify: viewer question, visible action/change, evidence, spoken line, short screen headline, and resulting business meaning. A list of benefits, animated text, or an unexplained dashboard is not product proof. Shortcuts and time jumps must not imply nonexistent speed or skipped approvals.

For multiple roles, identify the primary and secondary customers and the value each receives. Follow one shared job across the handoff and establish whose view is on screen. Show the secondary customer's own benefit; do not depict them solely as someone completing work for the primary customer. Keep the primary problem central while making both outcomes visible. Put optional integrations or AI after core value unless they are the demonstrated source of that value. A fundraising demo proves product value; it does not substitute for market, traction, economics, or team evidence.

## Produce the requested artifact

For narrated work, select and assess a short voice sample after story agreement and before generating the full track or locking visual timings; follow [narration](references/narration.md). This is a production quality check, not an extra user-approval gate. Use [research](references/research.md) for rationale or alternative structures; it distinguishes expert advice from our production heuristics.

Create a compact brief, a storyboard with claim sources, and the requested demo. If the user requests only a skill, strategy, or script, do not expand that into an unsolicited full video. For an actual demo request, a script alone is not completion: build a working self-playing HTML demo or record the relevant product path, and export video when requested and the tools are available. Use existing app components or construct a faithful standalone representation; do not change the target app merely to film it.

Keep simulated/proposed behavior labeled throughout a simulation and in its spoken introduction. Label mixed real and simulated footage per segment. Do not introduce fictional implementation, automatic success, fabricated metrics, or fake testimonials for a more persuasive story. A future capability must sound like a proposal even in an audio-only excerpt.

Default HTML: local assets or self-contained, no external requests unless required and authorized, usable play/pause/replay/scene navigation, readable captions, and a relevant closing action. If it includes audio, start sound from an explicit viewer gesture, handle blocked playback, and retain a useful silent/caption mode. Do not inherit a feature sign-off form or an automatic email/webhook. If no CTA destination is known, use plain proposed-next-step text, not a dead button. Video: deliver a playable file plus accurate captions/transcript; disclose synthetic narration when applicable. Never substitute silent HTML for a requested narrated video without reporting the limitation.

The [fictional SupplyLane brief](examples/pitch-demo-brief.md) illustrates the story-agreement stage. After story agreement, the optional [storyboard format](assets/storyboard.example.json) and offline [renderer](scripts/render_storyboard.py) make a reviewable planning artifact. The renderer deliberately produces a **storyboard**, not a product demo or finished video. It has no TTS, recording, or product simulation. Populate specific visual direction and evidence; do not mistake rendered cards for completed proof.

## Review and verify

Use [review criteria](references/review.md). Obtain an independent critique when requested or required by the workspace; provide the brief and evidence, not instructions to agree. Resolve load-bearing findings yourself. Test the chosen story against a skeptical viewer: can they state the problem, the visible difference, why to believe it, and the next step?

Verify whatever you actually produced: visual readability, state continuity, accurate role/version labels, play/pause/replay and scene jumps for HTML. For every narrated format, including HTML, check full playback, audio/visual sync, pronunciation, caption accuracy and audible delivery. Review once muted and once audio-only where listening is available. Follow the narration guide's explicit fallback when it is not; successful decoding and an unmuted player do not prove professional delivery. Report what was tested and what remains unverified. Link the final artifacts and disclose implementation or production limitations succinctly.

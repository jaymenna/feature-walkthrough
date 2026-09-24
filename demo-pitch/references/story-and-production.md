# Story and production

## The default outline to propose

| Part | What the author proposes to the user | What makes it work |
| --- | --- | --- |
| Situation / story | A specific person, job and recognizable moment | Quickly establishes relevance; can fit in the problem sentence. |
| Problem and stakes | One clear problem and its practical consequence | Uses the audience's actual pain, without invented disaster or ROI. |
| Promise and early outcome | A concise improvement and a concrete result to glimpse | Gives the viewer a reason to watch the path rather than making them wait through setup. |
| Demo as proof | The few visible changes that explain how the result happens | Each action answers the original problem; meaningful doubt is answered with evidence. |
| Payoff and call to action | What this changes for the audience and one next step | Ends at the desired decision, not at the last menu item. |

This is the skill's synthesis of the cited practitioner guidance, not a universal formula. Recommend and fill in this outline before producing scenes. For a short pitch, combine situation/problem and payoff/CTA. For a technical audience, allow more proof. The story provides context for the problem; it must not delay a clear problem statement behind a long personal anecdote or company history.

Pair the outline with a small goals card: **audience; primary problem; desired belief or understanding; proof; desired action; runtime/format; voice and listening plan for narrated work; claim boundaries.** Iterate both with the user. Their feedback may change the angle or goal even when the product requirements remain unchanged. Record the agreed version, then build from it.

## A compact working brief

Save the pitch lane's brief as **pitch-demo-brief.md** and record Gate 1 as draft or approved, with the approval source/date when available. Keep feature-demo-brief.md and feature-demo production/review artifacts in their own lane. Approval and revision state belong to the specific lane and artifact; a brief approval is not final-media approval. Preserve existing directory choices and use distinct filenames when both lanes share a directory.

Capture audience, decision, situation, current workaround, consequence, desired outcome, differentiated mechanism, available evidence, scope limits, format/time budget, narration plan when applicable, and next step. One paragraph can be enough. Known context need not be reconfirmed.

Develop this with the user. Start with their business problem, recommend a short opening and proof sequence, and invite correction. Record the brief as draft until the user agrees with the story. Agreement on product requirements does not settle a pitch: a detailed audit requirement may be important implementation evidence while repeated back-and-forth over incomplete requests is the reason the buyer cares. Do not build a detailed storyboard or produce media first and use its polish to steer the user toward an unagreed angle.

If feedback changes the central problem, return to the brief and reconsider scene selection. Preserve previous candidates only as clearly superseded drafts. Resume production from the agreed story; do not repeatedly request agreement after it has already been given.

The one-sentence spine is: “For [person doing job], [problem] makes [consequence]; [approach] enables [specific outcome] through [demonstrable mechanism].” Rewrite into natural language before narration. A sentence full of abstract benefits is a signal to find a more concrete job.

Keep a claim ledger beside the storyboard. Cite an implementation path, observed UI action, approved requirement, provided data, or source artifact. Evidence labels:

- **Observed:** verified working behavior, with the limits of that observation.
- **Simulated:** reconstruction or staged workflow illustrating intended behavior.
- **Planned:** future behavior without present operational proof.
- **Measured:** a quantified result with its measurement source and conditions.

Staged data inside a working product does not automatically make the implementation simulated, but the data still needs an appropriate label. A simulation can demonstrate the proposed interaction; it cannot establish reliability, security, conversion lift, or time savings.

The storyboard records behavior in `evidence_type` and data origin separately in `data_provenance`. For example, a verified working queue can be `observed` with `data_provenance: fictional sandbox records`. State the observation's scope in `source`. An observed export action alone does not prove a particular field, audit entry, or security property appears in its output: inspect the output before using that detail as evidence.

## Build belief through a causal path

1. Make the problem recognizable without a company-history preamble.
2. Orient the viewer to a specific useful result. An early peek at the ending is fine; label a rewind when returning to earlier states.
3. Show the important transition that produces the result. Before → action → after must be visible. Skip typing and navigation that prove nothing, but preserve decisions and dependencies that matter.
4. Resolve the strongest relevant doubt with evidence. Do not run a laundry list of exception handling merely to appear thorough.
5. Return to the outcome and a next step this audience can take.

If a scene can be removed without weakening the viewer's understanding or belief, cut it or make it optional. If there are several jobs, select the primary one or offer separate paths. The same account, record, version, amounts, and time assumptions should persist through the story.

### Short pitches: 30–60 seconds

Use one problem, one visible change, and one next step. Combine setup with the action; let an existing proof beat answer the objection. Keep alternative roles and integrations only if they are essential to that single change. Planning fields do not all become spoken text.

Budget reading/visual holds before speech: for example, a 60-second slot with 15 seconds reserved for seeing the result leaves 45 seconds of speech, roughly 105 words at 140 words/minute. This is draft arithmetic, not a target pace for every speaker. If a read-through overruns, cut content before accelerating delivery. Measure the final take.

## Adapting a feature tour

Inventory existing scenes by the question they answer, not the menu they display. Choose the most persuasive artifact as the early outcome. Pull only the screens needed to explain its creation. Replace labels such as “dashboard” or “settings” with the viewer's question. Rewrite narration into spoken language. Preserve feature terminology where it is needed to operate or understand the UI.

Do not merely prepend a problem slide to the full original tour. A feature sign-off ending belongs to feature-walkthrough (or its demo-features export). A demo-pitch ending should match the buying or stakeholder decision. An internal concept pitch can still end in a specific design decision when that is the user's intended next step.

## Visual execution

For a real product, capture a rehearsed path with safe demo data. For a concept, construct a faithful simulation using known visual language. If screenshots are all that exist, identify the result as a screenshot-based demo; animated pointers must not imply verified interactions.

Keep one visual focal point per beat. Crop and enlarge important text rather than showing an unreadable whole desktop. Leave enough surrounding context to orient the viewer. Use cursor movement only to explain an action. Show resulting artifacts—such as a report or rendered document—when they are the promise, not merely a success toast claiming they exist.

For a video, record/render in sections that can be repaired; retain a timing manifest with speech, visual action, reveal point, and hold. Use measured narration length. Keep pauses long enough to read the evidence, and do not time-compress a wait into a false performance claim. Prepare a local backup recording for a live presentation when useful. Do not present the backup as a live operation.

For standalone HTML, use embedded/local resources, keyboard-accessible controls, reduced-motion support, and explicit scene state. Pause, replay, and jumping backward must cancel pending transitions so later scenes do not mutate the current one. Keep full captions or an accessible transcript separate from short design headlines.

## Optional AI chapter

Show the job the AI helps complete: input → scoped action → visible result or status. A chat transcript alone is weak proof. Label proposals and simulated tool output. Preserve authentication, review boundaries, pending jobs, and permissions. Do not imply a model's account grants access to another service or that advisory local checks are authoritative. Use AI as a second path into the demonstrated workflow when that is the product design.

## Deliverable scope

For planning: brief, claim ledger, storyboard, voice direction, and review findings. The bundled renderer supports this stage only.

For production: the requested playable demo/video, captions/transcript, and concise verification record. A planning artifact should never be reported as a finished narrated demo. If a production tool or voice account is unavailable, finish independent work and state precisely which output could not be produced.

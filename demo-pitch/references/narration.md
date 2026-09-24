# Narration that sounds like someone means it

Flatness can come from the script, performance, synthesis engine, or edit. Diagnose all four before changing a voice. A fixed-rate system voice reading caption text can be useful for timing, but a pitch also needs speech-written copy and directed delivery. No controlled voice comparison is implied by these examples.

## Choose the audio path before full production

Treat narration as part of the first finished pitch. During briefing, check the requested language, audience, runtime, available providers and credentials, and whether the production environment can actually listen to audio. After story agreement, generate a short representative sample before the full track or final animation timing. This is an internal quality check, not a mandatory voice-selection question when a suitable default and authorization already exist.

Match the voice path to the artifact. The root feature-walkthrough's browser speech is a sound choice for its portable, offline, single-file promise; quality depends on the viewer's installed voices. A rendered pitch intended to sound consistent across devices should use a suitable human recording or capable neural voice when authorized access exists. Basic system speech remains useful for timing drafts. Do not silently present a draft voice as professional narration.

If a suitable production path is unavailable, complete the script and independent visual work, state the specific missing capability, and label timing audio as a draft. Ask only for the missing access or choice needed to proceed; do not request secrets in chat or imply that paid service access is included.

## Write for one listener

Speak to the actual viewer in their vocabulary. Use contractions where natural, vary sentence length, and let each sentence advance the thought. Avoid reading button labels, numbered lists, or a breathless string of capabilities. Describe why a visible transition matters.

Keep these separate:

- **Headline:** short visual anchor; need not repeat the voice.
- **Speech:** exactly the words to say; no bracketed stage directions.
- **Delivery:** tone, emphasis, pronunciation, and pause/reveal cues.
- **Subtitles:** accurate representation of the final spoken track, not a headline copy.

Before: “The procurement coordinator can check the request completeness and manage its approval status.”

After, for a concept: “The delivery date is missing. In this design, the requester fixes it before sending. The coordinator gets a complete request to review.”

The second version gives a concrete event and consequence. It can support a small pause before the result, without pretending that a concept is running software.

## Direct a restrained performance

Example direction for the fictional SupplyLane concept:

> Speak to one experienced procurement coordinator. Warm, capable, conversational. Begin with recognition of repeated clarification work. Become more assured as the proposed handoff becomes clear. Emphasize “complete request” and “waiting for review,” not the product name. Hold on the corrected field and the pending state. Use clear sentence endings. Avoid an announcer voice or exaggerated drama.

Use an emotional progression rather than maximum energy throughout: recognition → curiosity → confidence → relief → invitation. Not every product or passage needs every emotion. In production notes, give concrete cues such as “hold on the version label after this sentence” instead of “make it more engaging.”

Separate editorial direction from controls actually sent to the engine. A `direction` field in a local file has no effect unless the provider accepts and receives it. With a voice/rate-only engine, achieve the intended delivery through voice choice, spoken phrasing, punctuation, and edited pauses; do not claim unsupported emotional or style control. Slowing a flat read or raising the bitrate alone does not make it professional.

Example pronunciation sheet: SupplyLane = “supply lane”; REQ-104 = “request one hundred four”; PDF = “P D F”; MCP = “M C P.” Prefer “your AI” to a new acronym when the protocol name adds no value. Verify names with the user or a reliable source if uncertain.

## Voice options and their limits

| Path | Use | Direction and limitation |
| --- | --- | --- |
| Human founder/operator or narrator | When natural ownership of the story matters | Record two takes of the same passage; coach pace and intent, preserve natural voice. Requires an actual recording. |
| Direction-capable neural TTS | Repeatable production and frequent script iteration | Audition with the actual passage; maintain voice/model/settings across scenes. Better expression is possible, not guaranteed. Requires authorized provider access. |
| Local system TTS | Offline drafts and timing checks | Use phrase grouping and supported pauses/rate controls. Do not promise actor-like delivery from a basic system voice. |

Provider notes checked September 12, 2026:

- [OpenAI TTS](https://developers.openai.com/api/docs/guides/text-to-speech) supports separate delivery instructions with appropriate models. Keep directions outside the input speech. The [speech API](https://developers.openai.com/api/reference/cli/resources/audio/subresources/speech/methods/create) notes instructions do not work with tts-1 or tts-1-hd. Disclose synthetic narration. Verify model availability and credentials before running.
- [ElevenLabs TTS](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech) supports audio tags with Eleven v3, which does not support SSML break tags. Other listed models have different pause support. Translate directions into supported controls and audition; do not insert tags blindly into another engine.

Provider controls and availability change. Check current official documentation at execution time. No provider is a required dependency of this skill. Do not interpret a Codex/Claude login as a speech-provider credential. Do not request secret keys in chat or upload private customer material for a generic audition.

## A practical audition and edit

Choose a 15–25 second passage containing the value statement, a role handoff or meaningful change, a product name or difficult term, and an outcome. Generate two plausible voice or delivery candidates with identical words when feasible. For a voice/rate-only engine, compare supported voices or settings rather than inventing style controls. An already accepted voice can remain the default, but spot-check it with the new script. These durations and styles are production starting points, not research-backed thresholds.

Listen for natural stress, clear names, conversational cadence, convincing pauses, and a stable speaker. Listen without looking at the screen. Score intelligibility and appropriateness before expressiveness. Keep a note of which take was heard and selected; do not claim an audition from text prompts alone.

Reject or repair a sample with robotic stress, a sales-announcer cadence, rushed phrases, unnatural acronym pronunciation, clipped endings or distracting pauses. Fix the words or change the voice before generating the full track; do not polish visuals around a known weak take.

If listening is unavailable, say so before representing the audio as reviewed. Use a previously user-accepted voice and settings when applicable, or the best supported candidate with a concise rationale. Generate the sample and continue authorized production rather than blocking unrelated work. Provide a playable sample or finished track for human listening, and mark **listening review pending**. Never equate samples generated, a successful decode, a waveform check, or `muted: false` with hearing the delivery. Using a neural voice alone does not pass the professional-audio quality check.

Generate complete thought groups rather than tiny sentence fragments that reset the voice. Match voice/settings between groups, and listen at the joins. Align the visual action with the relevant words and hold on the result. Prevent clipped endings and overlapping speech. Keep audio levels consistent without clipping; listen on ordinary speakers as well as headphones. Music is optional and should not compete with the explanation.

After editing, make subtitles from the actual final speech and verify them. Provider tags, pronunciation spellings, and unspoken directions do not belong in captions. Exact pauses are an editing task if the engine cannot reliably produce them.

## Keep the first version reproducible and synchronized

- Cache takes by spoken text, provider/model, voice, language and synthesis settings, not just scene number or filename. A script or voice change must invalidate the affected take. Keep failed or partial downloads out of the successful cache.
- Measure each finished take and build scene cues from those durations plus intentional reading holds. Use the media playback clock as the timeline authority where available. Do not retain old scene timings after a rewrite or stretch narration to fit an arbitrary animation.
- Keep a manifest of voice/settings, segment identity, measured speech boundaries and total duration. Derive captions, transcript and displayed runtime from that record. Check that every scene or phase has its intended audio and that captions reflect the final spoken take.
- Decode the final export, check level consistency and clipping, and listen to the full track and segment joins when possible. Preserve source quality and avoid repeated lossy re-encoding; a larger file or higher nominal bitrate cannot repair a weak source performance.
- Test the real delivery surface: start from its visible Play button with sound enabled, verify pause/resume, replay, seeking and closing, and provide a clear fallback if autoplay is blocked. Recheck the deployed artifact when publishing is within scope. Local playback does not prove the hosted page serves the new track.

Record which provider, voice and settings were used, why they were chosen, what was actually heard, what objective playback checks passed, and what remains unverified. Keep this short; it is evidence of the production decision, not a new approval ceremony.

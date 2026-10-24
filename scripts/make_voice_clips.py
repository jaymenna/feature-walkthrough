"""Make one ElevenLabs voice clip per tour step for a walkthrough page.

Usage:
    python scripts/make_voice_clips.py path/to/walkthrough.html [options]

The ElevenLabs key is read from the ELEVENLABS_API_KEY environment variable
and is never written anywhere. The script reads each step's `text` from the
page's TOUR, asks ElevenLabs for that sentence alone, and writes
voice/step-01.mp3, voice/step-02.mp3, ... beside the page. A step whose text
has not changed since the last run is not asked for again, so a fix to one
sentence costs one clip, not the whole tour.

With --update-html it also sets VOICE = 'elevenlabs' and VOICE_CLIPS in the
page. With --embed, VOICE_CLIPS holds the clips as data: URIs instead of
paths, so the page stays one file that plays with the network off.

Options:
    --voice-id ID        ElevenLabs voice (default: Eric, cjVigY5qzO86Huf0OWal)
    --model ID           ElevenLabs model (default: eleven_multilingual_v2)
    --out DIR            where the clips go (default: voice/ beside the page)
    --say TERM=SPOKEN    say TERM as SPOKEN in the audio only; repeatable
    --modkey WORD        what ${MODKEY} is read as (default: alt)
    --update-html        write VOICE and VOICE_CLIPS into the page
    --embed              with --update-html, embed the clips as data: URIs
"""
import argparse
import base64
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_VOICE = 'cjVigY5qzO86Huf0OWal'
DEFAULT_MODEL = 'eleven_multilingual_v2'
API = 'https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_64'
MANIFEST = 'clips.json'

TEXT_FIELD = re.compile(r"""\btext\s*:\s*(['"`])((?:\\.|(?!\1).)*)\1""", re.S)


def tour_texts(html):
    """Return the `text` of every TOUR step, in order."""
    start = html.find('const TOUR')
    if start < 0:
        raise ValueError('No "const TOUR" found in the page.')
    end = html.find('\n];', start)
    if end < 0:
        raise ValueError('The TOUR array in the page has no closing "];".')
    texts = []
    for quote, body in TEXT_FIELD.findall(html[start:end]):
        body = re.sub(r'\\(.)', r'\1', body)
        texts.append(re.sub(r'\s+', ' ', body).strip())
    if not texts:
        raise ValueError('The TOUR array in the page has no steps with text.')
    return texts


def spoken_text(text, say, modkey):
    """The sentence as it is sent to ElevenLabs. The caption keeps the real words."""
    text = text.replace('${MODKEY}', modkey)
    for term, spoken in say:
        text = re.sub(r'\b%s\b' % re.escape(term), spoken, text)
    return text


def clip_name(index):
    return 'step-%02d.mp3' % (index + 1)


def text_hash(spoken, voice, model):
    return hashlib.sha256(json.dumps([spoken, voice, model]).encode('utf-8')).hexdigest()


def elevenlabs_fetch(spoken, previous, following, voice, model, key):
    """Ask ElevenLabs for one sentence. previous_text and next_text let it
    keep the same tone from one clip to the next without reading them."""
    body = {'text': spoken, 'model_id': model}
    if previous:
        body['previous_text'] = previous
    if following:
        body['next_text'] = following
    req = urllib.request.Request(
        API.format(voice=voice), data=json.dumps(body).encode('utf-8'), method='POST',
        headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            return res.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')[:300]
        raise RuntimeError('ElevenLabs refused the clip (HTTP %d): %s' % (e.code, detail))


def make_clips(texts, out_dir, voice, model, say, modkey, fetch):
    """Write one clip per step into out_dir. Returns the clip paths in order."""
    out_dir.mkdir(exist_ok=True)
    manifest_path = out_dir / MANIFEST
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        manifest = {}
    spoken = [spoken_text(t, say, modkey) for t in texts]
    paths = []
    for i, line in enumerate(spoken):
        name = clip_name(i)
        path = out_dir / name
        digest = text_hash(line, voice, model)
        if manifest.get(name) == digest and path.is_file() and path.stat().st_size > 0:
            print('kept   %s  (text unchanged)' % name)
        else:
            audio = fetch(line, spoken[i - 1] if i > 0 else '',
                          spoken[i + 1] if i + 1 < len(spoken) else '')
            if not audio:
                raise RuntimeError('ElevenLabs sent an empty clip for step %d.' % (i + 1))
            tmp = path.with_name(name + '.part')
            tmp.write_bytes(audio)
            os.replace(tmp, path)
            manifest[name] = digest
            print('made   %s  %s' % (name, line[:60]))
        paths.append(path)
    tmp = manifest_path.with_name(MANIFEST + '.part')
    tmp.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding='utf-8')
    os.replace(tmp, manifest_path)
    return paths


def clip_entries(paths, page_dir, embed):
    if embed:
        return ['data:audio/mpeg;base64,' + base64.b64encode(p.read_bytes()).decode('ascii')
                for p in paths]
    return [os.path.relpath(p, page_dir).replace(os.sep, '/') for p in paths]


def update_html(html, entries):
    """Set VOICE to 'elevenlabs' and VOICE_CLIPS to the clip list."""
    voice_line = re.compile(r"^const VOICE = .*$", re.M)
    clips_line = re.compile(r"^const VOICE_CLIPS = \[.*?\];", re.M | re.S)
    if not voice_line.search(html) or not clips_line.search(html):
        raise ValueError('The page has no VOICE / VOICE_CLIPS lines. Build it from the '
                         'current template/walkthrough-template.html first.')
    listed = ',\n'.join('  ' + json.dumps(e) for e in entries)
    html = voice_line.sub(lambda m: "const VOICE = 'elevenlabs';", html, count=1)
    return clips_line.sub(lambda m: 'const VOICE_CLIPS = [\n%s\n];' % listed, html, count=1)


def parse_say(values):
    pairs = []
    for v in values:
        term, sep, spoken = v.partition('=')
        if not sep or not term.strip() or not spoken.strip():
            raise SystemExit('--say needs TERM=SPOKEN, for example --say "TRIA=Tree-uh"')
        pairs.append((term.strip(), spoken.strip()))
    return pairs


def main(argv=None):
    ap = argparse.ArgumentParser(description='Make one ElevenLabs clip per walkthrough step.')
    ap.add_argument('page')
    ap.add_argument('--voice-id', default=DEFAULT_VOICE)
    ap.add_argument('--model', default=DEFAULT_MODEL)
    ap.add_argument('--out')
    ap.add_argument('--say', action='append', default=[])
    ap.add_argument('--modkey', default='alt')
    ap.add_argument('--update-html', action='store_true')
    ap.add_argument('--embed', action='store_true')
    args = ap.parse_args(argv)

    page = Path(args.page).resolve()
    html = page.read_text(encoding='utf-8')
    texts = tour_texts(html)
    key = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not key:
        raise SystemExit('Set ELEVENLABS_API_KEY to your ElevenLabs key, then run this again.')
    out_dir = Path(args.out).resolve() if args.out else page.parent / 'voice'

    def fetch(spoken, previous, following):
        return elevenlabs_fetch(spoken, previous, following, args.voice_id, args.model, key)

    paths = make_clips(texts, out_dir, args.voice_id, args.model,
                       parse_say(args.say), args.modkey, fetch)
    if args.update_html:
        entries = clip_entries(paths, page.parent, args.embed)
        page.write_text(update_html(html, entries), encoding='utf-8')
        print('Updated %s: VOICE is elevenlabs, %d clips listed.' % (page.name, len(entries)))
    else:
        print('\nPut these two lines in the page, or run again with --update-html:')
        print("const VOICE = 'elevenlabs';")
        print('const VOICE_CLIPS = %s;' % json.dumps(clip_entries(paths, page.parent, False)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

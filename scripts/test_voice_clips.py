"""Check the per-step ElevenLabs clip maker without calling ElevenLabs."""
import importlib.util
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('voice_clips', ROOT / 'scripts/make_voice_clips.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
TEMPLATE = (ROOT / 'template/walkthrough-template.html').read_text(encoding='utf-8')


class TourTextTest(unittest.TestCase):
    def test_reads_every_template_step_in_order(self):
        texts = MODULE.tour_texts(TEMPLATE)
        self.assertEqual(len(texts), 4)
        self.assertEqual(texts[0], 'This is the record list as it works today.')
        self.assertTrue(texts[-1].endswith('Does this look right to you?'))

    def test_quotes_escapes_and_template_strings(self):
        page = ("const TOUR = [\n  { text:'It\\'s here.', run: async()=>{} },\n"
                '  { text:"Two  words", run: async()=>{} },\n'
                '  { text:`Hold ${MODKEY}`, run: async()=>{} },\n];')
        self.assertEqual(MODULE.tour_texts(page), ["It's here.", 'Two words', 'Hold ${MODKEY}'])

    def test_page_without_tour_is_refused(self):
        with self.assertRaises(ValueError):
            MODULE.tour_texts('<html></html>')


class SpokenTextTest(unittest.TestCase):
    def test_pronunciation_changes_the_audio_text_only(self):
        said = MODULE.spoken_text('TRIA applies, press ${MODKEY}.', [('TRIA', 'Tree-uh')], 'option')
        self.assertEqual(said, 'Tree-uh applies, press option.')

    def test_whole_words_only(self):
        self.assertEqual(MODULE.spoken_text('TRIAL', [('TRIA', 'Tree-uh')], 'alt'), 'TRIAL')


class MakeClipsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / 'voice'
        self.calls = []

    def tearDown(self):
        self.tmp.cleanup()

    def fetch(self, spoken, previous, following):
        self.calls.append((spoken, previous, following))
        return ('audio:' + spoken).encode('utf-8')

    def make(self, texts):
        return MODULE.make_clips(texts, self.out, 'v', 'm', [], 'alt', self.fetch)

    def test_one_clip_per_step_with_neighbours_for_tone(self):
        paths = self.make(['One.', 'Two.', 'Three.'])
        self.assertEqual([p.name for p in paths], ['step-01.mp3', 'step-02.mp3', 'step-03.mp3'])
        self.assertEqual(paths[1].read_bytes(), b'audio:Two.')
        self.assertEqual(self.calls[1], ('Two.', 'One.', 'Three.'))
        self.assertEqual(self.calls[0][1], '')
        self.assertEqual(self.calls[2][2], '')

    def test_unchanged_steps_are_not_asked_for_again(self):
        self.make(['One.', 'Two.'])
        self.calls.clear()
        self.make(['One.', 'Two, changed.'])
        self.assertEqual([c[0] for c in self.calls], ['Two, changed.'])

    def test_no_partial_files_left(self):
        self.make(['One.'])
        self.assertEqual(sorted(p.name for p in self.out.iterdir()), ['clips.json', 'step-01.mp3'])


class UpdateHtmlTest(unittest.TestCase):
    def test_sets_voice_and_clip_list(self):
        html = MODULE.update_html(TEMPLATE, ['voice/step-01.mp3', 'voice/step-02.mp3'])
        self.assertIn("const VOICE = 'elevenlabs';", html)
        self.assertIn('const VOICE_CLIPS = [\n  "voice/step-01.mp3",\n  "voice/step-02.mp3"\n];', html)
        self.assertEqual(MODULE.tour_texts(html), MODULE.tour_texts(TEMPLATE))

    def test_embed_gives_data_uris(self):
        with tempfile.TemporaryDirectory() as d:
            clip = Path(d) / 'step-01.mp3'
            clip.write_bytes(b'abc')
            self.assertEqual(MODULE.clip_entries([clip], Path(d), True),
                             ['data:audio/mpeg;base64,YWJj'])
            self.assertEqual(MODULE.clip_entries([clip], Path(d), False), ['step-01.mp3'])

    def test_old_page_without_voice_lines_is_refused(self):
        with self.assertRaises(ValueError):
            MODULE.update_html('const TOUR = [];', ['a.mp3'])


if __name__ == '__main__':
    unittest.main()

# Korean Conversation Review

A static, responsive study companion for Myongji Korean Conversation, following the visual style and browser-only structure of the Calculus Review app. Open `index.html`; no build, account, backend or API key is required.

## Study scope

Source: Seoul National University Korean Plus, Student’s Book 1A, in `.context/`.

The requested cutoff is **PDF pages 1–145**, which covers the complete Hangul booklet and units 1–4. PDF page 145 is **printed unit page 83**. The alphabet booklet uses separate printed numbering; using printed textbook page 145 would accidentally include later units.

The shared exercise bank contains **995 entries**: 468 unique vocabulary headwords, 288 unique sentences / expressions, all 40 Hangul letters, 19 consonant names, and 120 syllables from the book’s writing tables. Repeated vocabulary stays in each relevant chapter, so these unique counts do not add up to the entry count. It includes vocabulary glossaries, alphabet example words, sound-contrast options, final-consonant sorting words, classroom expressions, greetings, and chapter conversation / reading / writing examples. `coverage.json` lists chapter totals and referenced PDF pages. Every entry in `content.js` has its source page, meaning, category and image.

The study bank is explicitly transcribed rather than populated automatically from raw OCR. English meanings serve as practice cues. For long sentences and abstract terms, a relevant book illustration provides context and the English cue specifies the intended answer. Concrete vocabulary uses cropped book photographs / illustrations, countries use flags, and letter / syllable exercises use sound-name cues. Crops exclude printed answer labels.

## Exercises

- **Match word & photo:** four pairs per round; select either side first. Incorrect pairs flash red, clear after a short pause, and allow another attempt. Correct pairs fade and become disabled. Complete the pairs to unlock the next round.
- **Pronunciation review:** Hangul and meaning, Korean audio at normal or slow speed, then a self-reported review button. There is no microphone, recording, or pronunciation grading. Consonants play their Korean names; vowels play with silent initial ㅇ.
- **Write what you see:** picture + meaning cue, editable Hangul answer, retry feedback, optional answer hint, and a keyboard with all 40 letters. The keyboard composes syllables, compound vowels and final consonants. It supports insertion at the cursor, selected-text replacement, spaces, punctuation and component-level backspace. Isolated-letter questions automatically use literal-letter mode.

All three modes use **the same full bank**. Each chapter / content filter gets its own shuffled cycle. Every selected entry appears before that cycle repeats; finishing starts an explicitly requested new shuffle. Small final matching rounds are supported. The study collection includes search, chapter counts, the complete alphabet chart, and source-page links.

## Audio availability

Audio uses the browser’s Web Speech API and a voice whose language is Korean (`ko-KR`). A Korean text-to-speech voice must be available on the device. If none is available, the app tells the learner to add Korean speech in device language settings; it does not silently play an English voice. Some browsers obtain voices online. No audio files or service credentials are bundled.

For reliable playback across phones, tablets and computers, generate one Korean MP3 per study item with a licensed TTS voice and place the files in `audio/`. The current player still uses browser speech synthesis, so these assets and player integration must be added before playback is device-independent. GitHub Pages cannot run server-side TTS, and a provider API key must never be placed in public JavaScript.

Browser tests cover the missing-voice path and validate configured language / speed using a mocked speech engine; audible native Korean speech was not verified in the headless environment.

## Progress and answers

Queues, completed matching pairs, filters and practice counts are stored locally under `korean-review-v1`. Words have deterministic IDs derived from chapter, category and Korean text. Unfinished matching rounds resume after a reload. Typing fields start empty when leaving / reopening writing practice; mastery persists. Hint-assisted writing advances the cycle but does not count as independently recalled mastery. Writing accepts differences in spacing and ordinary sentence punctuation while requiring the Korean text itself to match. Storage failures do not prevent practice.

## Run / host

Open `index.html` directly, or from this directory run:

```sh
python -m http.server 8001
```

Visit `http://localhost:8001/`. The static application files are `index.html`, `styles.css`, `content.js`, `hangul.js`, `app.js`, `assets/`, and `.nojekyll`. Routes use URL hashes and assets use relative paths, so project-path hosting such as GitHub Pages needs no server rewrite rules.

### GitHub Pages

The workflow in `.github/workflows/deploy.yml` publishes the app whenever `main` is updated. Create a GitHub repository with this project folder as its root, push the `main` branch, then open **Settings → Pages** and set **Source** to **GitHub Actions**. The deployment appears in the repository’s **Actions** tab. The workflow stages only the browser files; it does not publish `.context/`, temporary files, or development scripts. Source page references remain visible on the hosted site, while links to the local textbook PDF are shown only when running on the local machine.

Source links point to the existing PDF in `.context/`, currently ignored by Git. The exercises work without distributing the full PDF; source links require that PDF to be present at the same relative path in the served folder.

## Validation

```sh
node test.cjs
node browser-test.cjs
node edge-case-test.cjs
```

`test.cjs` needs only Node: it checks unique IDs, page bounds, image files, all course strings’ Hangul decomposition / composition round trips, cursor operations and answer normalization. Browser tests use Playwright (the bundled Codex runtime here) and installed Chrome; adapt the dependency location if using another machine. Screenshots and OCR / rendered-book intermediates are ignored under `tmp/`.

Browser checks cover matching errors and retries, disabled successful pairs, saved round restoration, non-repeating rounds, writing retry / hints, the Hangul keyboard, Korean audio configuration / fallback, collection search, final partial rounds / cycle completion, and mobile layouts at 390px. They use an isolated browser profile and do not change the learner’s browser progress.

## Content maintenance

`build-content.py` is the transcription / crop source. To regenerate its source page images, render only the first 145 PDF pages to `tmp/page-001.jpg` etc. with Poppler:

```sh
pdftoppm -f 1 -l 145 -scale-to 1700 -jpeg -jpegopt quality=85 BOOK.pdf tmp/page
python build-content.py
```

The source book and generated page images are needed only for maintenance. `ocr.cjs` / `ocr-parallel.cjs` were development extraction helpers, not runtime dependencies. Runtime content and imagery are already bundled.

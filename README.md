# Korean Conversation Review

A responsive Korean study companion for Myongji University’s Korean Conversation class. It runs entirely in the browser and can be hosted on GitHub Pages without a build step, backend, account, or API key.

Made by: Guilherme "Boler" Lopes de Carvalho.

## Study experience

- **Homepage:** introduces the review app and links to matching, pronunciation, and writing practice.
- **Match word & photo:** match Hangul vocabulary from the professor’s assigned pages to related pictures in four-pair rounds. Incorrect pairs show visual feedback and can be tried again; correct pairs fade and become disabled. Complete a round to continue.
- **Pronunciation review:** practice the dialogue lines and guided role-play from the assigned speaking activities. Each card shows Hangul and its meaning and plays Korean audio at normal or slow speed. This is listening practice; the app does not use a microphone or grade pronunciation. A voice setup guide covers Windows, macOS, Android, and iPhone/iPad.
- **Write what you see:** identify a picture from its English meaning cue and enter the matching vocabulary in Hangul. The on-screen keyboard composes syllables, compound vowels, and final consonants. It supports cursor insertion, selected-text replacement, spaces, punctuation, and component-level backspace.
- **Exam-focused cycles:** Match and Write share the vocabulary from the assigned glossary pages; Pronunciation uses dialogue practice from the four assigned speaking pages. Each unit filter gets a shuffled cycle, and every item in the selected set appears before the cycle repeats. Completing a cycle lets the learner explicitly start a new shuffle. Small final matching rounds are supported.
- **Study collection:** search the exam vocabulary and dialogue lines, browse unit counts, and see each item’s book page.
- **Progress and answers:** queues, completed matching pairs, filters, and practice counts save locally under `korean-review-v1`. Unfinished matching rounds resume after reload. Writing fields reopen empty while mastery progress remains saved. Hint-assisted answers advance the cycle without counting as independent recall. Answers accept spacing and ordinary sentence punctuation differences while requiring the Korean text to match. Storage failures do not prevent practice.

## Course material and coverage

The app is based on *Seoul National University Korean Plus, Student’s Book 1A*.

The app follows the professor’s midterm guidance: written-test vocabulary from book pages **28–29, 38–39, 44–45, 54–55, 61, 70–71, and 76–77**; pronunciation review from the speaking activities on pages **25, 41, 57, and 73**. The app contains 93 vocabulary entries from those glossary pages and 36 dialogue and guided role-play lines from the speaking activities. The written test has 50 questions drawn from the assigned vocabulary pages.

English meanings provide writing and listening cues. Each vocabulary item uses a related image, and matching follows the Hangul text shown in the book. The library shows the selected vocabulary and speaking lines grouped by unit.

## Audio

Playback uses the browser’s Web Speech API and a Korean (`ko-KR`) text-to-speech voice available on the device. If no Korean voice is available, the app explains how to add one in the device’s speech settings. It does not silently substitute an English voice. Some browsers obtain voices online.

GitHub Pages cannot run server-side text-to-speech. For consistent playback across devices, licensed Korean MP3 files would need to be bundled in `audio/` and connected to the player; the current app does not include audio files or provider credentials. Browser tests check the missing-voice fallback and voice-language / speed configuration with a mocked speech engine; native audible Korean speech was not verified in the headless test environment.

## Run locally

Open `index.html` directly for a quick look, or serve the project directory for consistent browser storage behavior:

```sh
python -m http.server 8001
```

Visit `http://localhost:8001/`. No installation or build is required. All application logic, study content, and images are bundled locally. Hash routes and relative asset paths also work when the app is hosted under a GitHub Pages project path.

## Publish with GitHub Pages

The workflow in `.github/workflows/deploy.yml` publishes the static app whenever `main` is updated. Push this project with its files at the repository root, then open **Settings → Pages** and set **Source** to **GitHub Actions**. The deployment status and published link appear in the repository’s **Actions** tab.

The workflow stages `index.html`, `styles.css`, `content.js`, `hangul.js`, `app.js`, `assets/`, `.nojekyll`, and `audio/` if present. Temporary files and development scripts are not included in the published site.

## Files and maintenance

| File | Purpose |
| --- | --- |
| `index.html` | Static page shell and script loading |
| `styles.css` | Responsive layout, typography, exercise and feedback styles |
| `content.js` | Study entries, meanings, categories, and image references |
| `hangul.js` | Hangul composition, keyboard editing, and answer normalization |
| `app.js` | Hash routing, exercise cycles, speech, local progress, and rendering |
| `assets/` | Book image crops, illustrations, and country flags used in exercises |
| `coverage.json` | Chapter totals |

`build-content.py` is the transcription and image-crop source. Its source images and OCR helpers are only needed for content maintenance; runtime content and imagery are already bundled.

`ocr.cjs` and `ocr-parallel.cjs` were development extraction helpers, not runtime dependencies.

## Verification

Run the content and front-end checks with Node.js:

```sh
node test.cjs
node browser-test.cjs
node edge-case-test.cjs
```

`test.cjs` checks the selected vocabulary and speaking scope, unique vocabulary images, asset files, Hangul decomposition and composition round trips, cursor operations, and answer normalization. Browser tests use Playwright and an installed Chrome browser; the bundled Codex runtime is used in this development environment.

The browser checks also confirm that every assigned vocabulary image loads, including the SVG illustrations, and cover matching errors and retries, disabled successful pairs, saved round restoration, non-repeating rounds, writing retries and hints, the Hangul keyboard, Korean audio configuration and fallback, collection search, final partial rounds, cycle completion, and mobile layouts at 390px. They use an isolated browser profile and do not change the learner’s saved progress. Screenshots and OCR / rendered-book intermediates are ignored under `tmp/`.

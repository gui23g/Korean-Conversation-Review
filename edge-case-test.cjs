const { chromium } = require('C:/Users/Inteli/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const { pathToFileURL } = require('url');
const path = require('path');
const assert = require('assert');

const base = pathToFileURL(path.join(__dirname, 'index.html')).href;
(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await page.addInitScript(() => {
    window.played = [];
    window.SpeechSynthesisUtterance = class { constructor(text) { this.text = text; } };
    Object.defineProperty(window, 'speechSynthesis', { value: {
      getVoices: () => [{ lang: 'ko-KR', name: 'Test Korean', localService: true }],
      addEventListener() {}, cancel() {},
      speak(utterance) {
        played.push({ text: utterance.text, lang: utterance.lang, rate: utterance.rate, voice: utterance.voice.lang });
        utterance.onstart?.();
        utterance.onend?.();
      }
    } });
  });

  await page.goto(base);
  await page.evaluate(() => {
    const q = COURSE.items.filter(item => item.kind === 'word' && COURSE.midtermScope.vocabularyPages.includes(item.bookPage) && !COURSE.midtermScope.vocabularyExclusions.includes(item.ko)).map(item => item.id);
    localStorage.setItem('korean-review-v1', JSON.stringify({
      sessions: { 'match:all:all': { queue: q, at: q.length - 2, solved: [], cycle: 1 } },
      mastery: {}, filter: { group: 'all', kind: 'all' }
    }));
  });
  await page.reload();
  await page.goto(base + '#/match');
  assert.equal(await page.locator('[data-side=photo]').count(), 2, 'Final matching round supports two items');
  const ids = await page.locator('[data-side=photo]').evaluateAll(buttons => buttons.map(button => button.dataset.id));
  for (const id of ids) {
    await page.locator(`[data-side=word][data-id="${id}"]`).click();
    await page.locator(`[data-side=photo][data-id="${id}"]`).click();
  }
  await page.locator('#next').click();
  assert((await page.locator('.complete').innerText()).includes('93'));
  await page.locator('#restart').click();
  assert((await page.locator('.session-head').innerText()).includes('Cycle 2'));

  await page.goto(base + '#/write');
  const target = await page.evaluate(() => {
    const state = JSON.parse(localStorage.getItem('korean-review-v1'));
    const session = state.sessions['write:all:all'];
    return COURSE.items.find(item => item.id === session.queue[session.at]);
  });
  assert(target.kind === 'word' && [28, 29, 38, 39, 44, 45, 54, 55, 61, 70, 71, 76, 77].includes(target.bookPage));
  await page.locator('#reveal').click();
  await page.locator('#answer').fill(target.ko);
  await page.locator('button[type=submit]').click();
  assert(await page.locator('#next').isEnabled());
  assert.equal(await page.evaluate(() => Object.keys(JSON.parse(localStorage.getItem('korean-review-v1')).mastery.write || {}).length), 0, 'Hinted answers do not count as independent recall');
  await page.locator('#next').click();
  await page.locator('#clear').click();
  for (const key of ['ㅎ', 'ㅏ', 'ㄴ', 'ㄱ', 'ㅡ', 'ㄹ']) await page.locator(`[data-key="${key}"]`).click();
  assert.equal(await page.locator('#answer').inputValue(), '한글');
  await page.locator('#backspace').click();
  assert.equal(await page.locator('#answer').inputValue(), '한그');

  await page.goto(base + '#/pronunciation');
  const phrase = await page.evaluate(() => {
    const state = JSON.parse(localStorage.getItem('korean-review-v1'));
    const session = state.sessions['pronunciation:all:all'];
    return COURSE.items.find(item => item.id === session.queue[session.at]).ko;
  });
  await page.locator('#listen').click();
  await page.locator('#slow').click();
  const played = await page.evaluate(() => window.played);
  assert.deepEqual(played.map(item => item.lang), ['ko-KR', 'ko-KR']);
  assert.deepEqual(played.map(item => item.rate), [1, .65]);
  assert.deepEqual(played.map(item => item.text), [phrase, phrase]);

  await page.evaluate(() => {
    const vocabulary = COURSE.items.filter(item => item.kind === 'word' && COURSE.midtermScope.vocabularyPages.includes(item.bookPage) && !COURSE.midtermScope.vocabularyExclusions.includes(item.ko));
    const longest = [...vocabulary].sort((a, b) => b.en.length - a.en.length);
    const q = [...longest.map(item => item.id), ...vocabulary.filter(item => !longest.slice(0, 4).some(first => first.id === item.id)).map(item => item.id)];
    const state = JSON.parse(localStorage.getItem('korean-review-v1'));
    state.filter = { group: 'all', kind: 'all' };
    state.sessions['match:all:all'] = { queue: q, at: 0, solved: [], cycle: 1 };
    localStorage.setItem('korean-review-v1', JSON.stringify(state));
  });
  await page.reload();
  await page.goto(base + '#/match');
  await page.screenshot({ path: __dirname + '/tmp/match-long-mobile.png', fullPage: true });
  const clipping = await page.locator('.tile').evaluateAll(buttons => buttons.filter(button => button.scrollHeight > button.clientHeight + 2).map(button => button.innerText));
  assert.deepEqual(clipping, [], 'Long cues should not clip on mobile');
  console.log('Edge cases passed: final two-pair round, full vocabulary cycle, shuffled restart, hint mastery, Hangul keyboard, Korean dialogue TTS / speed, longest mobile prompts.');
  await browser.close();
})();

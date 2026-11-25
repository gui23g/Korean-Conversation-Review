const { chromium } = require('C:/Users/Inteli/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const { pathToFileURL } = require('url');
const path = require('path');
const assert = require('assert');

const base = pathToFileURL(path.join(__dirname, 'index.html')).href;
(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1050 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));

  await page.goto(base);
  await page.screenshot({ path: __dirname + '/tmp/home-desktop.png', fullPage: true });
  assert.equal(await page.locator('.mode-card').count(), 3);
  assert((await page.locator('.scope-note').innerText()).includes('pages 86, 92–93'));
  assert((await page.locator('.exam-tag').innerText()).includes('FINALS'));
  const missingImages = await page.evaluate(async () => {
    const selected = COURSE.finalVocabulary;
    const sources = [...new Set(selected.map(item => item.image))];
    const failures = await Promise.all(sources.map(src => new Promise(resolve => {
      const image = new Image();
      image.onload = () => resolve(null);
      image.onerror = () => resolve(src);
      image.src = src;
    })));
    return failures.filter(Boolean);
  });
  assert.deepEqual(missingImages, [], 'All 100 Finals illustrations load');

  await page.goto(base + '#/match');
  assert((await page.locator('.session-head').innerText()).includes('100 items'));
  const photos = await page.locator('[data-side=photo]').evaluateAll(buttons => buttons.map(button => button.dataset.id));
  assert.equal(await page.evaluate(ids => ids.every(id => {
    const item = COURSE.items.find(entry => entry.id === id);
    return item.kind === 'word' && item.id.startsWith('final-') && COURSE.finalScope.vocabularyPages.includes(item.bookPage);
  }), photos), true, 'Match contains only Finals vocabulary');
  const wrong = photos.find(id => id !== photos[0]);
  await page.locator(`[data-side=photo][data-id=${photos[0]}]`).click();
  await page.locator(`[data-side=word][data-id=${wrong}]`).click();
  assert((await page.locator('#feedback').innerText()).includes('try again'));
  await page.waitForTimeout(700);
  for (const id of photos) {
    await page.locator(`[data-side=photo][data-id=${id}]`).click();
    await page.locator(`[data-side=word][data-id=${id}]`).click();
    assert(await page.locator(`[data-side=photo][data-id=${id}]`).isDisabled());
  }
  assert(await page.locator('#next').isEnabled());
  assert.deepEqual(await page.locator('.tile img').evaluateAll(images => images.filter(image => !image.naturalWidth).map(image => image.src)), []);
  await page.screenshot({ path: __dirname + '/tmp/match-desktop.png', fullPage: true });
  await page.reload();
  assert.equal(await page.locator('.tile.solved').count(), 8);
  await page.locator('#next').click();
  const nextPhotos = await page.locator('[data-side=photo]').evaluateAll(buttons => buttons.map(button => button.dataset.id));
  assert(!nextPhotos.some(id => photos.includes(id)));

  await page.goto(base + '#/write');
  await page.locator('#answer').fill('wrong');
  await page.locator('button[type=submit]').click();
  assert.equal(await page.locator('#answer').inputValue(), 'wrong');
  assert(await page.locator('#next').isDisabled());
  const expected = await page.evaluate(() => {
    const state = JSON.parse(localStorage.getItem('korean-review-v1'));
    const item = COURSE.items.find(entry => entry.id === state.sessions['write:all:all'].queue[state.sessions['write:all:all'].at]);
      return { ko: item.ko, inScope: item.kind === 'word' && item.id.startsWith('final-') && COURSE.finalScope.vocabularyPages.includes(item.bookPage) };
  });
  assert(expected.inScope, 'Write contains only assigned vocabulary');
  await page.locator('#answer').fill(expected.ko);
  await page.locator('button[type=submit]').click();
  assert(await page.locator('#next').isEnabled());
  await page.locator('#next').click();
  await page.locator('#clear').click();
  for (const key of ['ㅎ', 'ㅏ', 'ㄴ', 'ㄱ', 'ㅡ', 'ㄹ']) await page.locator(`[data-key="${key}"]`).click();
  assert.equal(await page.locator('#answer').inputValue(), '한글');
  await page.locator('#backspace').click();
  assert.equal(await page.locator('#answer').inputValue(), '한그');
  await page.screenshot({ path: __dirname + '/tmp/write-desktop.png', fullPage: true });

  await page.goto(base + '#/pronunciation');
  assert((await page.locator('.session-head').innerText()).includes('36 items'));
  const speechScope = await page.evaluate(() => {
    const state = JSON.parse(localStorage.getItem('korean-review-v1'));
    const session = state.sessions['pronunciation:all:all'];
    return session.queue.every(id => {
      const item = COURSE.items.find(entry => entry.id === id);
      return item.kind === 'phrase' && COURSE.midtermScope.speakingPages.includes(item.bookPage);
    });
  });
  assert(speechScope, 'Pronunciation contains only the assigned speaking activities');
  await page.locator('#listen').click();
  await page.waitForTimeout(200);
  assert((await page.locator('#audio-status').innerText()).length > 0);
  assert.equal(await page.locator('.voice-guide-card').count(), 4);
  assert.deepEqual(await page.locator('.voice-guide-card h3').allTextContents(), ['Windows 10 / 11', 'Mac', 'Android', 'iPhone / iPad']);
  await page.locator('.voice-guide summary').click();
  assert(await page.locator('.voice-guide').evaluate(details => details.open));
  await page.screenshot({ path: __dirname + '/tmp/listen-desktop.png', fullPage: true });

  await page.goto(base + '#/library');
  assert.equal(await page.locator('.coverage-table tbody tr').count(), 8);
  await page.locator('#search').fill('우산');
  assert.equal(await page.locator('.collection-card').count(), 0, 'Out-of-scope vocabulary is absent');
  await page.locator('#search').fill('등산하다');
  assert.equal(await page.locator('.collection-card').count(), 1);
  assert((await page.locator('.collection-card').innerText()).includes('Book p. 109'));
  await page.locator('#search').fill('어서 오세요.');
  assert.equal(await page.locator('.collection-card').count(), 1, 'The old speaking review remains available in the collection');

  await page.setViewportSize({ width: 390, height: 844 });
  for (const route of ['', 'match', 'write', 'pronunciation', 'library']) {
    await page.goto(base + '#/' + route);
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), route + ' overflow');
    await page.screenshot({ path: __dirname + '/tmp/' + (route || 'home') + '-mobile.png', fullPage: true });
  }
  assert.deepEqual(errors, []);
  console.log('Browser tests passed: professor-selected page coverage / matching feedback / writing / pronunciation / library / 390px layouts.');
  await browser.close();
})();

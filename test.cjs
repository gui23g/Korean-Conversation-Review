const fs = require('fs');
const path = require('path');
const vm = require('vm');
const Hangul = require('./hangul.js');
const assert = require('assert');

const context = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(__dirname, 'content.js'), 'utf8'), context);
const course = context.window.COURSE;
const items = course.items;
assert.equal(new Set(items.map(item => item.id)).size, items.length, 'IDs are unique');
for (const item of items) {
  assert(item.page >= 1 && item.page <= 145, item.ko);
  assert(fs.existsSync(path.join(__dirname, item.image)), item.image);
  assert.equal(Hangul.compose(Hangul.decompose(item.ko)), item.ko, item.ko);
}

const vocabularyPages = new Set(course.midtermScope.vocabularyPages);
const speakingPages = new Set(course.midtermScope.speakingPages);
const vocabularyExclusions = new Set(course.midtermScope.vocabularyExclusions || []);
const examVocabulary = items.filter(item => item.kind === 'word' && vocabularyPages.has(item.bookPage) && !vocabularyExclusions.has(item.ko));
const examSpeaking = items.filter(item => item.kind === 'phrase' && speakingPages.has(item.bookPage));
assert.equal(examVocabulary.length, 93, 'All vocabulary entries on the assigned glossary pages are included');
assert.equal(new Set(examVocabulary.map(item => item.ko)).size, 93, 'Written practice contains only unique vocabulary');
assert.equal(new Set(examVocabulary.map(item => item.image)).size, 93, 'Every vocabulary prompt has a distinct visual cue');
assert.equal(examSpeaking.length, 36, 'Speaking practice includes dialogue lines and guided country role-play from the assigned pages');
assert(examVocabulary.every(item => item.group !== 'hangul'));
assert(examSpeaking.every(item => item.bookPage !== undefined));
assert(!examVocabulary.some(item => item.ko === '자다'), 'Vocabulary stays within the selected printed glossary entries');
assert(!examSpeaking.some(item => item.ko === '저는 프랑스 사람이에요.'), 'Do not include a phrase from an unassigned speaking page');
for (const phrase of ['안녕하세요?', '반가워요.', '어서 오세요.', '네. 오렌지 주스하고 딸기 주스가 있어요.']) {
  assert(examSpeaking.some(item => item.ko === phrase), `Missing speaking line: ${phrase}`);
}
assert.equal(examSpeaking.filter(item => item.practiceType === 'roleplay').length, 12);
assert.equal(items.filter(item => item.kind === 'letter').length, 40);

for (const [raw, expected] of [
  ['ㅎㅏㄴㄱㅡㄹ', '한글'],
  ['ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ', '안녕하세요'],
  ['ㄱㅏㅂㅅㅇㅣ', '값이'],
  ['ㄱㅗㅏㄴㅊㅏㄹ', '관찰'],
  ['ㅇㅣㄹㄱㅇㅓㅇㅛ', '읽어요'],
  ['ㅎㅗㅏㅅㅣㄹ', '화실']
]) assert.equal(Hangul.compose(raw), expected);
assert.equal(Hangul.backspace('한', 1, 1).value, '하');
assert.equal(Hangul.backspace('화', 1, 1).value, '호');
assert.equal(Hangul.insert('한글', 1, 2, 'ㄱ').value, '한ㄱ');
assert.equal(Hangul.normalize('안녕하세요?'), '안녕하세요');
console.log('Midterm scope, content references, Hangul round trips, composition, cursor edits and normalization passed.');

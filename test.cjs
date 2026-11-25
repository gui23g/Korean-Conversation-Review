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
  assert(item.page >= 1 && item.page <= 197, item.ko);
  assert(fs.existsSync(path.join(__dirname, item.image)), item.image);
  assert.equal(Hangul.compose(Hangul.decompose(item.ko)), item.ko, item.ko);
}

const midtermPages = new Set(course.midtermScope.vocabularyPages);
const speakingPages = new Set(course.midtermScope.speakingPages);
const vocabularyExclusions = new Set(course.midtermScope.vocabularyExclusions || []);
const midtermVocabulary = items.filter(item => item.kind === 'word' && midtermPages.has(item.bookPage) && !vocabularyExclusions.has(item.ko));
const examSpeaking = items.filter(item => item.kind === 'phrase' && speakingPages.has(item.bookPage));
const finalPages = new Set(course.finalScope.vocabularyPages);
const finalVocabulary = items.filter(item => item.id.startsWith('final-'));
assert.equal(course.finalScope.pdfPageOffset, 62);
assert.equal(135 + course.finalScope.pdfPageOffset, 197, 'Printed page 135 maps to PDF page 197');
assert.equal(finalVocabulary.length, 100, 'Every listed Finals glossary entry is included');
assert.equal(new Set(finalVocabulary.map(item => item.ko)).size, 100, 'Finals vocabulary contains no duplicate Hangul answers');
assert.equal(new Set(finalVocabulary.map(item => item.image)).size, 100, 'Every Finals word has a distinct visual cue');
assert(finalVocabulary.every(item => finalPages.has(item.bookPage) && item.group >= 5 && item.group <= 8));
assert(finalVocabulary.every(item => item.page === item.bookPage + 62));
assert(!finalVocabulary.some(item => item.kind === 'phrase'), 'Finals Match and Write contain words only');
const finalCounts = Object.fromEntries(course.finalScope.vocabularyPages.map(page => [page, finalVocabulary.filter(item => item.bookPage === page).length]));
assert.deepEqual(JSON.parse(JSON.stringify(finalCounts)), { 86: 10, 92: 6, 93: 21, 102: 12, 103: 7, 109: 7, 118: 8, 119: 6, 124: 4, 125: 6, 134: 8, 135: 5 });
assert(!finalVocabulary.some(item => item.bookPage === 197 || item.group === '1'), 'Speaking pages are not included in the Finals vocabulary bank');
assert.equal(midtermVocabulary.length, 93, 'The previous midterm vocabulary remains in the source collection');
assert.equal(examSpeaking.length, 36, 'Speaking practice includes dialogue lines and guided country role-play from the assigned pages');
assert(examSpeaking.every(item => item.bookPage !== undefined));
assert(!midtermVocabulary.some(item => item.ko === '자다'), 'Midterm vocabulary stays within its selected printed glossary entries');
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
console.log('Finals page scope and 100-word coverage, midterm speaking scope, assets, Hangul round trips, cursor edits and normalization passed.');

// Rebuild the small, word-specific illustrations used by Finals Match and Write.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = __dirname;
const context = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(root, 'content.js'), 'utf8'), context);
const items = context.window.COURSE.finalVocabulary;
const colors = { 5: ['#f8eadc', '#f2d5c0'], 6: ['#e8f1e6', '#c7dbce'], 7: ['#f4eadf', '#e7d0bc'], 8: ['#e7f0f3', '#c9dfe6'] };

function escapeXml(value) {
  return String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' })[char]);
}

function illustration(item) {
  const [background, accent] = colors[item.group] || colors[5];
  const content = item.visualType === 'number'
    ? `<text x="180" y="177" text-anchor="middle" class="number">${escapeXml(item.icon)}</text>`
    : item.visualType === 'calendar'
      ? `<g class="calendar"><rect x="70" y="45" width="220" height="190" rx="20"/><path d="M70 86h220"/><path d="M120 35v30M240 35v30"/><path d="M104 114h8m32 0h8m32 0h8m32 0h8m32 0h8M104 145h8m32 0h8m32 0h8m32 0h8m32 0h8M104 176h8m32 0h8m32 0h8m32 0h8m32 0h8"/><text x="180" y="160" text-anchor="middle" class="calendar-word">${escapeXml(item.icon)}</text></g>`
      : `<text x="180" y="170" text-anchor="middle" class="emoji">${escapeXml(item.icon)}</text>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 260" role="img" aria-label="Illustration for ${escapeXml(item.en)}">
  <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="${background}"/><stop offset="1" stop-color="${accent}"/></linearGradient></defs>
  <rect width="360" height="260" rx="28" fill="url(#bg)"/>
  <circle cx="314" cy="43" r="20" fill="#fff" opacity=".35"/><circle cx="44" cy="216" r="28" fill="#fff" opacity=".28"/>
  <rect x="48" y="32" width="264" height="196" rx="25" fill="#fffdf8" opacity=".86"/>
  ${content}
  <path d="M142 205h76" stroke="${accent}" stroke-width="8" stroke-linecap="round" opacity=".8"/>
  <style>.emoji{font-family:'Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji',sans-serif;font-size:100px}.number{font-family:Arial,sans-serif;font-size:84px;font-weight:700;fill:#31534b}.calendar rect{fill:#fff;stroke:#67867d;stroke-width:6}.calendar path{fill:none;stroke:#67867d;stroke-width:6;stroke-linecap:round}.calendar-word{font-family:Arial,sans-serif;font-size:32px;font-weight:700;fill:#31534b}</style>
</svg>`;
}

for (const item of items) {
  const destination = path.join(root, item.image);
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.writeFileSync(destination, illustration(item), 'utf8');
}
console.log(`Generated ${items.length} Finals illustrations.`);

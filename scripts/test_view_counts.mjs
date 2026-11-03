import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { runInNewContext } from 'node:vm';

const layout = await readFile(new URL('../src/layouts/ArticleLayout.astro', import.meta.url), 'utf8');
const scripts = [...layout.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length, 1);

function counter(baseline, initial = '') {
  const current = { textContent: initial };
  const total = { dataset: { legacyViews: String(baseline) }, textContent: String(baseline) };
  let onChange;
  runInNewContext(scripts[0][1], {
    document: {
      getElementById(id) {
        return { busuanzi_value_page_pv: current, 'article-view-count': total }[id] ?? null;
      },
    },
    MutationObserver: class {
      constructor(callback) { onChange = callback; }
      observe(target) { assert.equal(target, current); }
    },
  });
  assert.equal(typeof onChange, 'function');
  return {
    total,
    update(value) {
      current.textContent = value;
      onChange();
    },
  };
}

const newPost = counter(0);
assert.equal(newPost.total.textContent, '0');
newPost.update('7');
assert.equal(newPost.total.textContent, '7');

const oldPost = counter(10345);
oldPost.update('7');
assert.equal(oldPost.total.textContent, '10352');
oldPost.update('7');
assert.equal(oldPost.total.textContent, '10352');
oldPost.update('8');
assert.equal(oldPost.total.textContent, '10353');

for (const invalid of ['', '   ', 'invalid', '-1', '1.5', '1e3', '9007199254740992']) {
  oldPost.update(invalid);
  assert.equal(oldPost.total.textContent, '10353', `Ignore invalid PV: ${JSON.stringify(invalid)}`);
}
oldPost.update('0');
assert.equal(oldPost.total.textContent, '10345');

assert.equal(counter(10345, '7').total.textContent, '10352');
assert.equal(counter(Number.MAX_SAFE_INTEGER, '1').total.textContent, String(Number.MAX_SAFE_INTEGER));

import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import worker from '../dist/server/index.js';

const dist = new URL('../dist/', import.meta.url);
const env = {
  ASSETS: {
    async fetch(request) {
      const pathname = decodeURIComponent(new URL(request.url).pathname).replace(/^\/+/, '');
      try {
        const body = await readFile(new URL(pathname, dist));
        return new Response(body, { status: 200 });
      } catch {
        return new Response('Not found', { status: 404 });
      }
    },
  },
};

const home = await worker.fetch(new Request('https://example.com/'), env);
assert.equal(home.status, 200);
assert.match(await home.text(), /To1in/);

const about = await worker.fetch(new Request('https://example.com/about-to1in/'), env);
assert.equal(about.status, 200);
assert.match(await about.text(), /你好，我是 To1in/);

const robots = await worker.fetch(new Request('https://example.com/robots.txt'), env);
assert.equal(robots.status, 200);

const missing = await worker.fetch(new Request('https://example.com/not-found/'), env);
assert.equal(missing.status, 404);
assert.match(await missing.text(), /404/);

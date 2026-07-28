import { mkdir, writeFile } from 'node:fs/promises';

const outputDirectory = new URL('../dist/server/', import.meta.url);
const worker = `export default {
  async fetch(request, env) {
    if (!env.ASSETS) {
      return new Response('Static assets binding is unavailable.', { status: 500 });
    }
    return env.ASSETS.fetch(request);
  },
};
`;

await mkdir(outputDirectory, { recursive: true });
await writeFile(new URL('index.js', outputDirectory), worker, 'utf8');

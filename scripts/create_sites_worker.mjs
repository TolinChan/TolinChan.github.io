import { mkdir, writeFile } from 'node:fs/promises';

const outputDirectory = new URL('../dist/server/', import.meta.url);
const worker = `function assetRequest(request, pathname) {
  const url = new URL(request.url);
  url.pathname = pathname;
  return new Request(url, request);
}

export default {
  async fetch(request, env) {
    if (!env.ASSETS) {
      return new Response('Static assets binding is unavailable.', { status: 500 });
    }

    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method not allowed.', {
        status: 405,
        headers: { Allow: 'GET, HEAD' },
      });
    }

    const url = new URL(request.url);
    const candidates = [url.pathname];
    if (url.pathname.endsWith('/')) {
      candidates.push(\`\${url.pathname}index.html\`);
    } else if (!url.pathname.split('/').pop()?.includes('.')) {
      candidates.push(\`\${url.pathname}/index.html\`);
    }

    for (const pathname of candidates) {
      const response = await env.ASSETS.fetch(assetRequest(request, pathname));
      if (response.status !== 404) return response;
    }

    const fallback = await env.ASSETS.fetch(assetRequest(request, '/404.html'));
    return new Response(fallback.body, {
      status: 404,
      headers: fallback.headers,
    });
  },
};
`;

await mkdir(outputDirectory, { recursive: true });
await writeFile(new URL('index.js', outputDirectory), worker, 'utf8');

import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeRaw from 'rehype-raw';
import rehypePrettyCode from 'rehype-pretty-code';

export default defineConfig({
  site: 'https://blog.tolinchan.xyz',
  output: 'static',
  trailingSlash: 'always',
  integrations: [sitemap()],
  markdown: {
    syntaxHighlight: false,
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [
        rehypeRaw,
        rehypeKatex,
        [rehypePrettyCode, {
          theme: {
            dark: 'github-dark',
            light: 'github-light',
          },
          keepBackground: false,
        }],
      ],
    }),
  },
});

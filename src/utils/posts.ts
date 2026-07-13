import type { CollectionEntry } from 'astro:content';

export type BlogPost = CollectionEntry<'blog'>;

export function sortPosts(posts: BlogPost[]) {
  return [...posts].sort(
    (a, b) => b.data.publishedAt.getTime() - a.data.publishedAt.getTime(),
  );
}

export function formatDate(date: Date) {
  return new Intl.DateTimeFormat('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date);
}

export function termSlug(value: string) {
  return value
    .normalize('NFKC')
    .trim()
    .toLocaleLowerCase('zh-CN')
    .replace(/\s+/g, '-')
    .replace(/[\\/?#%]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function termHref(kind: 'category' | 'tag', value: string) {
  return `/${kind}/${encodeURIComponent(termSlug(value))}/`;
}

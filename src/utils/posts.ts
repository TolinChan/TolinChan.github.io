import type { CollectionEntry } from 'astro:content';

export type BlogPost = CollectionEntry<'blog'>;

const categoryAliases: Record<string, string> = {
  BUUexp: 'CTF',
  Blockchain: '区块链安全',
  Lattice: '格密码',
  'Paper study': '论文阅读',
  wp: 'CTF',
  对称加密: '对称密码',
  未分类: '随笔',
};

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

export function normalizeCategory(value: string) {
  return categoryAliases[value] || value;
}

export function getPostCategories(post: BlogPost) {
  return [...new Set(post.data.categories.map(normalizeCategory))];
}

export function getPostDescription(post: BlogPost, maxLength = 112) {
  let description = (post.data.description || '这篇文章暂时没有摘要。')
    .replace(/^markDown\d+\s*/i, '')
    .replace(/\s+/g, ' ')
    .trim();

  if (description.startsWith(post.data.title)) {
    description = description.slice(post.data.title.length).trim();
  }
  description = description.replace(/^wp\s+/i, '').trim();

  const characters = Array.from(description);
  if (characters.length <= maxLength) return description;

  const shortened = characters.slice(0, maxLength).join('');
  const sentenceEnd = Math.max(
    shortened.lastIndexOf('。'),
    shortened.lastIndexOf('！'),
    shortened.lastIndexOf('？'),
  );
  return `${sentenceEnd >= maxLength * 0.65 ? shortened.slice(0, sentenceEnd + 1) : shortened}…`;
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

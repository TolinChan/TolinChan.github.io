import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { sortPosts } from '../utils/posts';

export async function GET(context) {
  const posts = sortPosts(await getCollection('blog', ({ data }) => !data.draft));
  return rss({
    title: "To1in's Blog",
    description: '密码学、安全与技术随笔。',
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.publishedAt,
      link: post.data.route,
      categories: [...post.data.categories, ...post.data.tags],
    })),
    customData: '<language>zh-CN</language>',
  });
}

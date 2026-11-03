# To1in's Blog

从 WordPress 备份迁移而来的 Astro 静态博客，部署目标为 GitHub Pages 与
`blog.tolinchan.xyz`。

## 本地开发

在 PowerShell 中使用 `npm.cmd`，避免系统执行策略拦截 `npm.ps1`：

```powershell
npm.cmd install
npm.cmd run migrate
npm.cmd run dev
```

构建与验收：

```powershell
npm.cmd run build
npm.cmd run verify
```

## 新文章

在 `src/content/blog` 新建 Markdown 文件，frontmatter 需符合
`src/content.config.ts`。WordPress 原始备份必须保留在本仓库之外。

## Giscus

GitHub 仓库开启 Discussions、安装 [Giscus GitHub App](https://github.com/apps/giscus)
并创建 `Blog Comments` 分类后，将仓库 ID 与分类 ID 写入 GitHub Actions 的
Variables：

- `PUBLIC_GISCUS_REPO_ID`
- `PUBLIC_GISCUS_CATEGORY_ID`

本仓库已经配置上述两个 Variables。若以后更换仓库或 Discussion 分类，可在
[Giscus 配置页](https://giscus.app/zh-CN)取得新的 ID；更新 Variables 后重新
运行 Pages 工作流即可应用新配置。

## 文章阅读量

文章标题下使用[不蒜子](https://busuanzi.ibruce.info/)显示当前页面的累计
阅读次数（PV），刷新也会计数，不代表独立访客人数。新增 PV 由第三方服务保存，
无需本地数据库或密钥；浏览器会向该服务发送访问请求，包含页面地址。

计数异步加载，服务不可用或被拦截时隐藏阅读量，不影响正文。域名或文章路径
变化可能使新计数分开，本地预览数字不代表正式站。

显示总数 = `src/data/legacy-views.json` 中按 `legacyId` 匹配的旧站基数 +
不蒜子返回的新 PV。已从 2025-07-05 的 WordPress WXR 备份提取 42 篇文章的
`views` 元数据，合计 398,377 次，并与同日 SQL 备份逐篇核对一致。新文章基数为 0。
这份数据是固定快照，不会随页面访问或重新构建累加；备份后到新站启用统计前的
旧站访问量不在其中。原始备份仍保留在仓库之外。

## 自定义域名切换

先在 `https://TolinChan.github.io` 验收部署，再按以下顺序切换：

1. 在 GitHub 验证 `tolinchan.xyz`，并在 Pages 设置中添加
   `blog.tolinchan.xyz`。
2. 将 DNSPod 中 `blog` 的旧 A 记录替换为指向
   `tolinchan.github.io` 的 CNAME。
3. DNS 生效且站点正常后启用 Enforce HTTPS。

切换完成前保留旧 A 记录；若新站异常且旧服务器仍可用，恢复旧 A 记录。

不要把数据库、WordPress 整站包、WXR、`.env` 或旧站凭据提交到仓库。

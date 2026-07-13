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

GitHub 仓库开启 Discussions 并创建 `Blog Comments` 分类后，将仓库 ID 与
分类 ID 写入 GitHub Actions 的 Variables：

- `PUBLIC_GISCUS_REPO_ID`
- `PUBLIC_GISCUS_CATEGORY_ID`

不要把数据库、WordPress 整站包、WXR、`.env` 或旧站凭据提交到仓库。

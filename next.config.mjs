// NEXT_EXPORT=1 → 纯静态导出（GitHub Pages）；默认 → 常规 next start
// NEXT_PUBLIC_BASE_PATH → Pages 子路径（如 /luniverse），运行时资源引用见 lib/base-path.ts
const isStatic = process.env.NEXT_EXPORT === '1'
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || ''

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  basePath,
  ...(isStatic ? { output: 'export', trailingSlash: true } : {}),
}

export default nextConfig

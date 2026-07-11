// public/ 下资源的运行时引用前缀（next.config 的 basePath 不会自动加到 fetch/loader URL 上）
export const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? ''

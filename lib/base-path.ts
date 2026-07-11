// public/ 下资源的运行时引用前缀（next.config 的 basePath 不会自动加到 fetch/loader URL 上）
export const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? ''

// 把各种来源的路径归一成 rooms.ts 的键：剥 basePath 前缀 + 剥尾斜杠。
// Pages 静态导出（trailingSlash）给 "/studio/"，window.location 给 "/luniverse/studio/"，
// 本地 next start 给 "/studio"——不归一会 fallback 到大厅（相机不飞的隐性 bug）。
export function normalizeRoute(pathname: string): string {
  let p = pathname
  if (BASE_PATH && p.startsWith(BASE_PATH)) p = p.slice(BASE_PATH.length)
  if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1)
  return p || '/'
}

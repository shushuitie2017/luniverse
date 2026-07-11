import type { Metadata } from 'next'
import './globals.css'
import { ClientShell } from '@/components/ClientShell'

export const metadata: Metadata = {
  title: 'Luniverse — 单世界·相机即路由',
  description:
    '全站共享一个微缩 3D 世界：切换路由 = 相机沿贝塞尔弧线飞到那个房间，滚动 = 推轨。Next.js + React Three Fiber + Lenis + Blender 烘焙管线。',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body>
        <ClientShell>{children}</ClientShell>
      </body>
    </html>
  )
}

'use client'

import { useEffect, type ReactNode } from 'react'
import { usePathname } from 'next/navigation'
import Lenis from 'lenis'
import gsap from 'gsap'
import { frame } from '@/lib/frame'
import { normalizeRoute } from '@/lib/base-path'
import { useStore } from '@/lib/store'
import { WebGLCanvas } from '@/webgl/Canvas'
import { Nav } from '@/components/Nav'

// 配方 1（M0 考古笔记）：摘掉 GSAP 自己的 rAF，挂到统一脉搏上
let gsapWired = false
function wireGsap() {
  if (gsapWired) return
  gsapWired = true
  gsap.ticker.lagSmoothing(0)
  gsap.ticker.remove(gsap.updateRoot)
  frame.add((time) => gsap.updateRoot(time / 1000), 0)
}

export function ClientShell({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const setRoute = useStore((s) => s.setRoute)
  const setLenis = useStore((s) => s.setLenis)
  const setScrollProgress = useStore((s) => s.setScrollProgress)

  useEffect(() => {
    wireGsap()
    const lenis = new Lenis({ lerp: 0.125, autoRaf: false })
    const off = frame.add((time) => lenis.raf(time), 1)
    lenis.on('scroll', (e: Lenis) => {
      setScrollProgress(Number.isFinite(e.progress) ? e.progress : 0)
    })
    setLenis(lenis)
    return () => {
      off()
      lenis.destroy()
      setLenis(null)
    }
  }, [setLenis, setScrollProgress])

  useEffect(() => {
    setRoute(normalizeRoute(pathname))
    // 换房间：滚动立即归零，新房间从驻留机位开始
    const lenis = useStore.getState().lenis
    lenis?.scrollTo(0, { immediate: true })
    useStore.getState().setScrollProgress(0)
  }, [pathname, setRoute])

  return (
    <>
      <WebGLCanvas />
      <Nav />
      <main className="content">{children}</main>
    </>
  )
}

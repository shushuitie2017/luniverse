import { create } from 'zustand'
import type Lenis from 'lenis'

interface AppState {
  lenis: Lenis | null
  setLenis: (lenis: Lenis | null) => void
  // 当前路由（由 DOM 侧写入，Canvas 内的 CameraRig 消费——绕开 R3F 跨 reconciler 的 context 断裂）
  route: string
  setRoute: (route: string) => void
  // 当前页滚动进度 0..1（Lenis progress），驱动房间内的相机推轨
  scrollProgress: number
  setScrollProgress: (p: number) => void
}

export const useStore = create<AppState>((set) => ({
  lenis: null,
  setLenis: (lenis) => set({ lenis }),
  route: '/',
  setRoute: (route) => set({ route }),
  scrollProgress: 0,
  setScrollProgress: (scrollProgress) => set({ scrollProgress }),
}))

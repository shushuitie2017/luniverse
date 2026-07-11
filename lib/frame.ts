// 统一 rAF 脉搏（tempus 的极简平替）——全站唯一的 requestAnimationFrame。
// Lenis / GSAP / R3F 全部作为订阅者挂在这里，priority 越小越先执行。
type FrameCallback = (time: number, delta: number) => void

type Sub = { cb: FrameCallback; priority: number }

class FrameLoop {
  private subs: Sub[] = []
  private running = false
  private last = 0

  add(cb: FrameCallback, priority = 0) {
    this.subs.push({ cb, priority })
    this.subs.sort((a, b) => a.priority - b.priority)
    this.start()
    return () => this.remove(cb)
  }

  remove(cb: FrameCallback) {
    this.subs = this.subs.filter((s) => s.cb !== cb)
  }

  private start() {
    if (this.running || typeof window === 'undefined') return
    this.running = true
    const tick = (time: number) => {
      const delta = this.last ? time - this.last : 0
      this.last = time
      for (const s of this.subs) s.cb(time, delta)
      requestAnimationFrame(tick)
    }
    requestAnimationFrame(tick)
  }
}

export const frame = new FrameLoop()

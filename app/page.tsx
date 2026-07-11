import type { CSSProperties } from 'react'

export default function LobbyPage() {
  return (
    <div style={{ '--accent': '#e2543e' } as CSSProperties}>
      <section className="section">
        <div className="block">
          <div className="eyebrow mono">Room 01 · Lobby</div>
          <h1>大厅</h1>
          <p>
            全站共享同一个微缩世界。你现在看到的是大厅——点上方导航去别的房间，
            注意页面不会白屏跳转，而是相机飞过去。
          </p>
        </div>
      </section>
      <section className="section right">
        <div className="block">
          <h2>往下滚，相机在推轨</h2>
          <p>
            Lenis 滚动进度直接驱动相机向房间中心推近。DOM 文字与 WebGL
            相机吃的是同一个滚动值——这就是 M0 考古里的统一帧循环在工作。
          </p>
        </div>
      </section>
      <section className="section">
        <div className="block">
          <h2>浏览器前进/后退 = 倒放运镜</h2>
          <p>路由状态与相机位姿绑定，历史记录导航同样触发飞行，试试看。</p>
        </div>
      </section>
    </div>
  )
}

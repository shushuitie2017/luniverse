import type { CSSProperties } from 'react'

export default function LifePage() {
  return (
    <div style={{ '--accent': '#e8a33d' } as CSSProperties}>
      <section className="section">
        <div className="block">
          <div className="eyebrow mono">Room 03 · Life</div>
          <h1>生活</h1>
          <p>
            世界西侧的房间。直接把 /life 这个 URL 发给别人，
            对方打开时相机会硬切到这里——深链接直达，不放多余的开场动画。
          </p>
        </div>
      </section>
      <section className="section right">
        <div className="block">
          <h2>滚动进度是每个房间自己的</h2>
          <p>换房间时滚动归零，推轨从驻留机位重新开始，房间之间互不污染。</p>
        </div>
      </section>
      <section className="section">
        <div className="block">
          <h2>下一步</h2>
          <p>SK-09 camera-as-router 的可移植模块，就从这套灰盒里蒸馏。</p>
        </div>
      </section>
    </div>
  )
}

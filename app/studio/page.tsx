import type { CSSProperties } from 'react'

export default function StudioPage() {
  return (
    <div style={{ '--accent': '#3fa8a0' } as CSSProperties}>
      <section className="section">
        <div className="block">
          <div className="eyebrow mono">Room 02 · Studio</div>
          <h1>工坊</h1>
          <p>
            这是世界东侧的房间。刚才那段飞行是一条二次贝塞尔弧线——中点自动抬升，
            相机「越过世界」而不是直线穿墙。
          </p>
        </div>
      </section>
      <section className="section right">
        <div className="block">
          <h2>飞行中断也不跳变</h2>
          <p>
            飞到一半就点别的房间试试：运镜从当前实际位姿续飞，
            而不是先瞬移回起点。
          </p>
        </div>
      </section>
      <section className="section">
        <div className="block">
          <h2>灰盒的意义</h2>
          <p>先证明骨架成立，再谈质感。M2 会把其中一个房间换成烘焙资产。</p>
        </div>
      </section>
    </div>
  )
}

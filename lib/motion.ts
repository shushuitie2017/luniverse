// 运动语言令牌（motion language tokens）——全站动效的唯一出处。
// 原则：微交互 ≤200ms 走 CSS；编排/运镜走 GSAP；两边都只从这里取值。
// CSS 侧对应变量见 globals.css 的 :root（--ease-luni / --dur-*），两处数值必须一致。
export const MOTION = {
  ease: {
    // 站点签名曲线：快出缓收
    cssLuni: 'cubic-bezier(0.32, 0, 0.15, 1)',
    gsapFlight: 'power2.inOut', // 相机飞行：对称进出
  },
  dur: {
    fast: 0.2, // hover / 按钮反馈
    base: 0.4, // 元素状态切换
    slow: 0.8, // 进出场 reveal
    flight: 1.8, // 相机跨房间飞行
  },
} as const

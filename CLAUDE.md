# Luniverse — 单世界·相机即路由

全站共享一个 3D 世界，路由切换 = 相机运镜。Next.js 15 + R3F 9 + Lenis + GSAP + zustand，pnpm。

## 现状

- **M1 ✅** 灰盒三联动实测：3 路由 = 3 段贝塞尔弧线运镜、滚动推轨、前进后退倒放、深链接硬切、60fps
- **M2 ✅** 大厅换成烘焙房间「蓝猫工坊」：Blender headless 烘焙 → WebP 压缩 240KB；Lighthouse 四项全 100
- **M3 待办** studio/life 两房间按 M2 管线量产 + 微交互运动语言令牌

## 运行

```
pnpm install
pnpm dev      # http://localhost:3012
pnpm build && pnpm start          # 常规服务
NEXT_EXPORT=1 NEXT_PUBLIC_BASE_PATH=/luniverse pnpm build   # GitHub Pages 静态导出 → out/
```

## 架构

- `lib/frame.ts` — 统一 rAF 脉搏。**全站只有这一个 requestAnimationFrame**；GSAP(priority 0)、Lenis(1)、R3F advance(2) 都是订阅者。新动画源必须挂这里，禁止自开 rAF。
- `components/ClientShell.tsx` — GSAP ticker 摘除+接线、Lenis 初始化（lerp 0.125, autoRaf:false）、路由→zustand。
- `lib/store.ts` — zustand：`route` / `scrollProgress` / `lenis`。**路由由 DOM 侧写入 store，Canvas 内组件从 store 读**——绕开 R3F 跨 reconciler 的 next context 断裂，别在 Canvas 子树里调 next/navigation hooks。
- `lib/rooms.ts` — 世界地图：每条路由一个房间（center/camera/dolly/accent）。加新房间 = 加一条记录 + 一个 page。
- `webgl/CameraRig.tsx` — 相机即路由核心：路由变化 → GSAP 补间 t → 二次贝塞尔弧线（中点自动抬升）；滚动进度 → camera↔dolly 推轨；飞行中断从当前实际位姿续飞；深链接首帧硬切。
- `webgl/World.tsx` / `webgl/BakedRoom.tsx` — 场景与烘焙房间装配（GLB 材质运行时换 MeshBasicMaterial unlit）。
- `lib/base-path.ts` — public/ 资源的 basePath 前缀（Pages 子路径部署用）。

## 烘焙管线

`tools/bake_workshop.py` 一个脚本完成建模→烘焙→导出：
`blender -b -P tools/bake_workshop.py -- tools/out` → `pnpm dlx @gltf-transform/cli webp tools/out/workshop-raw.glb public/models/workshop.glb`
- 全部件 join 成单 mesh + Smart UV Project 一张图集；Cycles COMBINED 把灯光/发光体全烤进去；导出前换单一烘焙材质
- 灯光调参经验：暗色主题下 fill AREA 460 + world 0.85 + 桌面补 POINT 90 才够读；220/0.5 会死黑
- 贴图压缩暂用 WebP；KTX2 需装 KTX-Software，M3 再说

## 约束

- 包管理 pnpm（禁 npm）；端口 3012。
- DOM 文字永远留在 DOM（SEO 红线），WebGL 只做视觉。
- `.content` 默认 pointer-events:none，需要交互的文字块用 `.block`（已恢复 auto）。
- 部署：GitHub Actions（`.github/workflows/deploy.yml`）静态导出推 Pages，CI pnpm 版本须与锁文件对齐（当前 8）。

// Luniverse 世界地图：全站共享一个 3D 世界，每条路由对应世界中的一个「房间」。
// 路由切换 = 相机在房间之间飞行（camera-as-router）。
export interface Room {
  path: string
  name: string
  nameEn: string
  center: [number, number, number] // 房间中心（lookAt 目标基准）
  camera: [number, number, number] // 相机驻留位（scroll=0 时）
  dolly: [number, number, number] // scroll=1 时相机推到的位置
  accent: string
}

export const ROOMS: Room[] = [
  {
    path: '/',
    name: '大厅',
    nameEn: 'LOBBY',
    center: [0, 1.2, 0],
    camera: [0, 3.4, 10],
    dolly: [0, 1.8, 5.5],
    accent: '#e2543e',
  },
  {
    path: '/studio',
    name: '工坊',
    nameEn: 'STUDIO',
    center: [18, 1.2, -2],
    camera: [18, 3.4, 8],
    dolly: [15.5, 2.0, 3.5],
    accent: '#3fa8a0',
  },
  {
    path: '/life',
    name: '生活',
    nameEn: 'LIFE',
    center: [-18, 1.2, -2],
    camera: [-18, 3.4, 8],
    dolly: [-15.5, 2.0, 3.5],
    accent: '#e8a33d',
  },
]

export function roomByPath(path: string): Room {
  return ROOMS.find((r) => r.path === path) ?? ROOMS[0]
}

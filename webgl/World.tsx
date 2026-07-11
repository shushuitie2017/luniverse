'use client'

import { Suspense } from 'react'
import { ROOMS } from '@/lib/rooms'
import { BASE_PATH } from '@/lib/base-path'
import { BakedRoom } from './BakedRoom'

// 灰盒世界：三个房间共享一个连续地面，先证明骨架成立，再谈质感（M2 换烘焙资产）
function GreyBoxRoom({
  center,
  accent,
}: {
  center: [number, number, number]
  accent: string
}) {
  const [cx, , cz] = center
  return (
    <group position={[cx, 0, cz]}>
      {/* 房间地台 */}
      <mesh position={[0, -0.05, 0]} receiveShadow>
        <boxGeometry args={[12, 0.1, 12]} />
        <meshStandardMaterial color="#2a2e36" />
      </mesh>
      {/* 后墙 + 侧墙 */}
      <mesh position={[0, 2, -5.8]}>
        <boxGeometry args={[12, 4.2, 0.3]} />
        <meshStandardMaterial color="#333842" />
      </mesh>
      <mesh position={[-5.8, 2, 0]}>
        <boxGeometry args={[0.3, 4.2, 12]} />
        <meshStandardMaterial color="#30343d" />
      </mesh>
      {/* 陈设灰盒 */}
      <mesh position={[-2.2, 0.75, -1.5]} castShadow>
        <boxGeometry args={[1.5, 1.5, 1.5]} />
        <meshStandardMaterial color={accent} />
      </mesh>
      <mesh position={[1.8, 0.5, 0.8]} castShadow>
        <cylinderGeometry args={[0.7, 0.7, 1, 24]} />
        <meshStandardMaterial color="#7d828c" />
      </mesh>
      <mesh position={[0.2, 1.4, -3.2]} castShadow>
        <coneGeometry args={[0.8, 1.8, 4]} />
        <meshStandardMaterial color="#5a5f6a" />
      </mesh>
      {/* 房间信标：漂浮的强调色小球 */}
      <mesh position={[0, 3.2, 0]}>
        <sphereGeometry args={[0.35, 24, 24]} />
        <meshStandardMaterial
          color={accent}
          emissive={accent}
          emissiveIntensity={0.6}
        />
      </mesh>
    </group>
  )
}

export function World() {
  return (
    <>
      <color attach="background" args={['#14171c']} />
      <fog attach="fog" args={['#14171c', 30, 90]} />
      <ambientLight intensity={0.5} />
      <directionalLight position={[8, 14, 6]} intensity={1.4} />
      {/* 连续大地面：三个房间同属一个世界 */}
      <mesh position={[0, -0.12, 0]}>
        <boxGeometry args={[64, 0.1, 36]} />
        <meshStandardMaterial color="#1d2027" />
      </mesh>
      {/* 房间之间的连廊地砖 */}
      <mesh position={[9, -0.02, 0]}>
        <boxGeometry args={[6, 0.06, 2.4]} />
        <meshStandardMaterial color="#262a32" />
      </mesh>
      <mesh position={[-9, -0.02, 0]}>
        <boxGeometry args={[6, 0.06, 2.4]} />
        <meshStandardMaterial color="#262a32" />
      </mesh>
      {/* 大厅 = 烘焙房间（M2 首航），加载期间回退灰盒 */}
      <Suspense
        fallback={
          <GreyBoxRoom center={ROOMS[0].center} accent={ROOMS[0].accent} />
        }
      >
        <BakedRoom url={`${BASE_PATH}/models/workshop.glb`} position={ROOMS[0].center.map((v, i) => (i === 1 ? 0 : v)) as [number, number, number]} />
      </Suspense>
      {ROOMS.slice(1).map((room) => (
        <GreyBoxRoom key={room.path} center={room.center} accent={room.accent} />
      ))}
    </>
  )
}

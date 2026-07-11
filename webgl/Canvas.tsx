'use client'

import { Canvas, advance } from '@react-three/fiber'
import { useEffect } from 'react'
import { frame } from '@/lib/frame'
import { World } from './World'
import { CameraRig } from './CameraRig'

// 配方 1：R3F 不自转，frameloop="never"，由统一脉搏手动推帧
export function WebGLCanvas() {
  useEffect(() => frame.add((time) => advance(time / 1000), 2), [])

  return (
    <div className="canvas-wrap">
      <Canvas
        frameloop="never"
        dpr={[1, 2]}
        gl={{ antialias: true, powerPreference: 'high-performance' }}
        camera={{ fov: 45, near: 0.1, far: 300, position: [0, 3.4, 10] }}
      >
        <CameraRig />
        <World />
      </Canvas>
    </div>
  )
}

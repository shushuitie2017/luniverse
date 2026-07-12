'use client'

import { useFrame, useThree } from '@react-three/fiber'
import { useEffect, useRef } from 'react'
import * as THREE from 'three'
import gsap from 'gsap'
import { useStore } from '@/lib/store'
import { normalizeRoute } from '@/lib/base-path'
import { MOTION } from '@/lib/motion'
import { roomByPath, type Room } from '@/lib/rooms'

const easeScroll = (p: number) => p * p * (3 - 2 * p) // smoothstep

function scrollPose(room: Room, p: number, pos: THREE.Vector3) {
  const e = easeScroll(p)
  pos.set(
    room.camera[0] + (room.dolly[0] - room.camera[0]) * e,
    room.camera[1] + (room.dolly[1] - room.camera[1]) * e,
    room.camera[2] + (room.dolly[2] - room.camera[2]) * e
  )
}

// 相机即路由：路由切换 = 贝塞尔弧线飞行到目标房间；房间内滚动 = 推轨。
// 飞行中被打断时，捕获当前实际位姿作为新起点，连按导航也不跳变。
export function CameraRig() {
  const camera = useThree((s) => s.camera)

  const rig = useRef({
    toRoom: roomByPath(
      normalizeRoute(typeof window !== 'undefined' ? window.location.pathname : '/')
    ),
    fromPos: new THREE.Vector3(),
    fromLook: new THREE.Vector3(),
    curPos: new THREE.Vector3(),
    curLook: new THREE.Vector3(),
    ctrl: new THREE.Vector3(),
    t: 1, // 1 = 已抵达
  })
  const tween = useRef<gsap.core.Tween | null>(null)
  const tmpTarget = useRef(new THREE.Vector3())

  // 深链接：首帧直接硬切到 URL 对应房间（无飞行）
  useEffect(() => {
    const r = rig.current
    scrollPose(r.toRoom, 0, r.curPos)
    r.curLook.set(...r.toRoom.center)
    camera.position.copy(r.curPos)
    camera.lookAt(r.curLook)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // 订阅路由变化 → 启动飞行
  useEffect(() => {
    const unsub = useStore.subscribe((state, prev) => {
      if (state.route === prev.route) return
      const to = roomByPath(state.route)
      const r = rig.current
      if (to.path === r.toRoom.path) return
      // 从当前实际位姿起飞（支持中断续飞）
      r.fromPos.copy(r.curPos)
      r.fromLook.copy(r.curLook)
      r.toRoom = to
      r.t = 0
      tween.current?.kill()
      tween.current = gsap.to(r, {
        t: 1,
        duration: MOTION.dur.flight,
        ease: MOTION.ease.gsapFlight,
        overwrite: true,
      })
    })
    return unsub
  }, [])

  useFrame((_, __) => {
    const r = rig.current
    const p = useStore.getState().scrollProgress
    const target = tmpTarget.current
    scrollPose(r.toRoom, r.t < 1 ? 0 : p, target)

    if (r.t < 1) {
      // 二次贝塞尔：中点抬升，飞行有"越过世界"的弧度
      r.ctrl.addVectors(r.fromPos, target).multiplyScalar(0.5)
      const lift = THREE.MathUtils.clamp(r.fromPos.distanceTo(target) * 0.35, 1.5, 9)
      r.ctrl.y += lift
      const t = r.t
      const s = 1 - t
      r.curPos.set(
        s * s * r.fromPos.x + 2 * s * t * r.ctrl.x + t * t * target.x,
        s * s * r.fromPos.y + 2 * s * t * r.ctrl.y + t * t * target.y,
        s * s * r.fromPos.z + 2 * s * t * r.ctrl.z + t * t * target.z
      )
      r.curLook.lerpVectors(r.fromLook, new THREE.Vector3(...r.toRoom.center), t)
    } else {
      r.curPos.copy(target)
      r.curLook.set(...r.toRoom.center)
    }

    camera.position.copy(r.curPos)
    camera.lookAt(r.curLook)
  })

  return null
}

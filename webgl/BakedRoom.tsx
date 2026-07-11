'use client'

import { useLoader } from '@react-three/fiber'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import * as THREE from 'three'
import { useMemo } from 'react'

// 烘焙房间：光照全部烤进贴图，运行时换成 unlit 材质（MeshBasicMaterial），
// 浏览器端不算光——这就是「离线渲染质感搬进浏览器」路线（M0 配方 / SK-10）。
export function BakedRoom({
  url,
  position,
}: {
  url: string
  position: [number, number, number]
}) {
  const gltf = useLoader(GLTFLoader, url)

  const scene = useMemo(() => {
    const s = gltf.scene
    s.traverse((o) => {
      if (o instanceof THREE.Mesh) {
        const old = o.material as THREE.MeshStandardMaterial
        if (old?.map) {
          old.map.anisotropy = 8
          o.material = new THREE.MeshBasicMaterial({ map: old.map })
          old.dispose()
        }
      }
    })
    return s
  }, [gltf])

  return <primitive object={scene} position={position} />
}

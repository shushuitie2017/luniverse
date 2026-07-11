'use client'

import type { CSSProperties } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { ROOMS } from '@/lib/rooms'

export function Nav() {
  const pathname = usePathname()
  return (
    <header className="nav">
      <span className="nav-logo mono">LUNIVERSE · 灰盒</span>
      <nav className="nav-links">
        {ROOMS.map((room) => (
          <Link
            key={room.path}
            href={room.path}
            className={pathname === room.path ? 'active' : ''}
            style={{ '--accent': room.accent } as CSSProperties}
          >
            <i className="dot" />
            {room.name}
            <span className="mono en">{room.nameEn}</span>
          </Link>
        ))}
      </nav>
    </header>
  )
}

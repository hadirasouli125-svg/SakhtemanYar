import { NextResponse } from 'next/server'
import { cookies } from 'next/headers'

const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://okizneyesdwiundvadpe.supabase.co/functions/v1/api_gateway'
const COOKIE = 'sy_session'
const ROLE_COOKIE = 'sy_role'

export async function GET() {
  const store = await cookies()
  const token = store.get(COOKIE)?.value || ''
  const role = store.get(ROLE_COOKIE)?.value || ''
  return NextResponse.json({ authenticated: Boolean(token), role: role === 'resident' ? 'resident' : role === 'manager' ? 'manager' : '' })
}

export async function POST(req: Request) {
  try {
    const input = await req.json()
    const action = String(input?.action || '')
    const store = await cookies()
    const token = store.get(COOKIE)?.value || ''
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    if (token) headers.Authorization = `Bearer ${token}`

    const response = await fetch(API, {
      method: 'POST',
      headers,
      body: JSON.stringify(input),
      cache: 'no-store',
    })
    const data = await response.json().catch(() => ({}))
    if (!response.ok || data?.error) {
      return NextResponse.json(data?.error ? { error: data.error } : data, { status: response.status || 500 })
    }

    const out = NextResponse.json(data)
    if (action === 'login_manager' || action === 'login_resident') {
      const session = data?.access_token || data?.session || ''
      if (session) {
        out.cookies.set(COOKIE, session, {
          httpOnly: true,
          secure: process.env.NODE_ENV === 'production',
          sameSite: 'lax',
          path: '/',
          maxAge: 60 * 60 * 24 * 7,
        })
        out.cookies.set(ROLE_COOKIE, action === 'login_resident' ? 'resident' : 'manager', {
          httpOnly: true,
          secure: process.env.NODE_ENV === 'production',
          sameSite: 'lax',
          path: '/',
          maxAge: 60 * 60 * 24 * 7,
        })
      }
    } else if (action === 'logout') {
      out.cookies.set(COOKIE, '', { httpOnly: true, secure: process.env.NODE_ENV === 'production', sameSite: 'lax', path: '/', maxAge: 0 })
      out.cookies.set(ROLE_COOKIE, '', { httpOnly: true, secure: process.env.NODE_ENV === 'production', sameSite: 'lax', path: '/', maxAge: 0 })
    }
    return out
  } catch {
    return NextResponse.json({ error: 'خطای سرور' }, { status: 500 })
  }
}

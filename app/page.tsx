'use client'
import { useState } from 'react'

export default function Home() {
  const [signedIn, setSignedIn] = useState(false)
  return <main className="shell"><section className="auth card"><div className="logo">SY</div><h1>ساختمان‌یار</h1><p className="muted">مدیریت هوشمند ساختمان</p>{signedIn ? <><div className="success">داشبورد آماده است</div><div className="grid"><div className="card stat"><span>موجودی صندوق</span><b>۰</b></div><div className="card stat"><span>بدهی کل</span><b>۰</b></div><div className="card stat"><span>پرداخت ماه</span><b>۰</b></div><div className="card stat"><span>تعمیرات</span><b>۰</b></div></div><button className="btn primary wide" onClick={()=>setSignedIn(false)}>خروج</button></> : <><input className="input" placeholder="شماره موبایل"/><input className="input" type="password" placeholder="رمز عبور"/><button className="btn primary wide" onClick={()=>setSignedIn(true)}>ورود</button><button className="btn secondary wide">ساخت مدیر اولیه</button></>}</section></main>
}
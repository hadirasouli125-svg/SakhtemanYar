'use client'

import { useEffect, useState } from 'react'

function jalali(value: string) {
  if (!value) return '-'
  const m = value.match(/(\d{4})-(\d{2})-(\d{2})/)
  if (!m) return value
  const gy=Number(m[1]),gm=Number(m[2]),gd=Number(m[3]); const gdm=[0,31,59,90,120,151,181,212,243,273,304,334]
  let days=365*(gy-1600)+Math.floor((gy-1603)/4)-Math.floor((gy-1599)/100)+Math.floor((gy-1599)/400)+gd+gdm[gm-1]
  if(gm>2&&((gy%4===0&&gy%100!==0)||gy%400===0))days++
  let jDays=days-79; let jy=979+33*Math.floor(jDays/12053); let d=jDays%12053; jy+=4*Math.floor(d/1461); d%=1461
  if(d>365){jy+=Math.floor((d-1)/365);d=(d-1)%365}
  const jm=d<186?1+Math.floor(d/31):7+Math.floor((d-186)/30),jday=1+(d<186?d%31:(d-186)%30)
  return `${jy}/${String(jm).padStart(2,'0')}/${String(jday).padStart(2,'0')}`
}

async function call(action: string, body: Record<string, any> = {}) {
  const r = await fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action,...body})})
  const j=await r.json().catch(()=>({})); if(!r.ok||j.error) throw new Error(j.error||'خطای سرور'); return j
}

export default function Home(){
 const [username,setUsername]=useState(''),[password,setPassword]=useState(''),[role,setRole]=useState<'manager'|'resident'>('manager'),[token,setToken]=useState('session'),[data,setData]=useState<any>({}),[loading,setLoading]=useState(false),[error,setError]=useState(''),[register,setRegister]=useState(false),[building,setBuilding]=useState(''),[address,setAddress]=useState(''),[confirm,setConfirm]=useState('')
 useEffect(()=>{(async()=>{try{const r=await fetch('/api/session',{cache:'no-store'});const s=await r.json();if(s.authenticated&&s.role){setRole(s.role);await load(s.role)}else setToken('')}catch{setToken('')}})()},[])
 async function load(r=role){setLoading(true);setError('');try{const j=await call(r==='manager'?'manager_dashboard':'resident_dashboard');setData(j)}catch(e:any){setError(e.message||'خطا در دریافت اطلاعات')}finally{setLoading(false)}}
 async function login(){setLoading(true);setError('');try{await call(role==='manager'?'login_manager':'login_resident',{username:username.trim(),password});setToken('session');await load(role)}catch(e:any){setError(e.message||'ورود ناموفق بود')}finally{setLoading(false)}}
 async function createManager(){if(!username.trim()||!password||password!==confirm||!building.trim()){setError('نام کاربری، رمز، تکرار رمز و نام ساختمان را کامل کنید');return}setLoading(true);setError('');try{await call('register_manager',{username:username.trim(),password,building_name:building.trim(),building_address:address.trim()});setRegister(false);setConfirm('');setError('ثبت با موفقیت انجام شد؛ اکنون وارد شوید')}catch(e:any){setError(e.message||'ثبت ساختمان ناموفق بود')}finally{setLoading(false)}}
 async function logout(){try{await call('logout')}catch{}setToken('');setData({})}
 if(!token)return <main className="shell"><section className="auth card"><div className="logo">SY</div><h1>ساختمان‌یار</h1><p className="muted">مدیریت هوشمند ساختمان</p>{register?<><input className="input" placeholder="نام کاربری مدیر" value={username} onChange={e=>setUsername(e.target.value)}/><input className="input" placeholder="نام ساختمان" value={building} onChange={e=>setBuilding(e.target.value)}/><input className="input" placeholder="آدرس ساختمان" value={address} onChange={e=>setAddress(e.target.value)}/><input className="input" type="password" placeholder="رمز عبور" value={password} onChange={e=>setPassword(e.target.value)}/><input className="input" type="password" placeholder="تکرار رمز عبور" value={confirm} onChange={e=>setConfirm(e.target.value)}/><button className="btn primary wide" disabled={loading} onClick={createManager}>{loading?'در حال ثبت...':'ثبت ساختمان و مدیر'}</button><button className="btn secondary wide" onClick={()=>setRegister(false)}>بازگشت</button></>:<><input className="input" placeholder="نام کاربری" value={username} onChange={e=>setUsername(e.target.value)}/><input className="input" type="password" placeholder="رمز عبور" value={password} onChange={e=>setPassword(e.target.value)}/><div className="tabs"><button className={role==='manager'?'tab active':'tab'} onClick={()=>setRole('manager')}>مدیر ساختمان</button><button className={role==='resident'?'tab active':'tab'} onClick={()=>setRole('resident')}>ساکن</button></div><button className="btn primary wide" disabled={loading} onClick={login}>{loading?'در حال ورود...':'ورود امن'}</button><button className="btn secondary wide" onClick={()=>setRegister(true)}>ساخت مدیر اولیه</button></>} {error&&<div className="msg">{error}</div>}</section></main>
 return <main className="shell"><section className="card"><div className="hero"><h1>داشبورد ساختمان‌یار</h1><p className="muted">{role==='manager'?'مدیریت ساختمان و امور مالی':'وضعیت واحد و پرداخت‌های من'}</p></div><div className="grid"><div className="card stat"><span>موجودی صندوق</span><b>{Number(data.cashbox?.balance??data.fund?.balance??0).toLocaleString('fa-IR')}</b></div><div className="card stat"><span>بدهی</span><b>{Number(data.balance??data.me?.balance??0).toLocaleString('fa-IR')}</b></div><div className="card stat"><span>دریافتی</span><b>{Number(data.cashbox?.cash_in??data.fund?.total_paid??0).toLocaleString('fa-IR')}</b></div><div className="card stat"><span>هزینه ثبت‌شده</span><b>{Number(data.cashbox?.cash_out??0).toLocaleString('fa-IR')}</b></div></div>{data.subscription_expires_at&&<div className="item">پایان اشتراک: {jalali(data.subscription_expires_at)}</div>}{error&&<div className="msg">{error}</div>}<button className="btn primary wide" disabled={loading} onClick={()=>load()}>{loading?'در حال دریافت...':'به‌روزرسانی'}</button><button className="btn secondary wide" onClick={logout}>خروج</button></section></main>
}

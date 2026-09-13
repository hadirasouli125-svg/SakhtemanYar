from pathlib import Path

p = Path('app/page.tsx')
s = p.read_text(encoding='utf-8')
s = s.replace("const API = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://okizneyesdwiundvadpe.supabase.co/functions/v1/api_gateway'\n\n", "")
s = s.replace("async function call(action: string, body: Record<string, any> = {}, token = '') {\n  const r = await fetch(API,{method:'POST',headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},body:JSON.stringify({action,...body})})\n", "async function call(action: string, body: Record<string, any> = {}) {\n  const r = await fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action,...body})})\n")
s = s.replace("[username,setUsername]=useState(''),[password,setPassword]=useState(''),[role,setRole]=useState<'manager'|'resident'>('manager'),[token,setToken]=useState(''),", "[username,setUsername]=useState(''),[password,setPassword]=useState(''),[role,setRole]=useState<'manager'|'resident'>('manager'),[token,setToken]=useState('session'),")
s = s.replace(" useEffect(()=>{const t=localStorage.getItem('sy_session'),r=localStorage.getItem('sy_role') as any;if(t&&r){setToken(t);setRole(r);load(t,r)}},[])\n async function load(t=token,r=role){", " useEffect(()=>{(async()=>{try{const r=await fetch('/api/session',{cache:'no-store'});const s=await r.json();if(s.authenticated&&s.role){setRole(s.role);await load(s.role)}else setToken('')}catch{setToken('')}})()},[])\n async function load(r=role){")
s = s.replace(",{},t);setData(j)", ");setData(j)")
s = s.replace("function logout(){localStorage.removeItem('sy_session');localStorage.removeItem('sy_role');setToken('');setData({})}", "async function logout(){try{await call('logout')}catch{}setToken('');setData({})}")
p.write_text(s, encoding='utf-8')

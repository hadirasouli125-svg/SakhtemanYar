from pathlib import Path
p=Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s=p.read_text(encoding='utf-8')
add=[]
if 'void setBusy(boolean v)' not in s:
    add.append('''void setBusy(boolean v){if(busyBar!=null)busyBar.setVisibility(v?View.VISIBLE:View.GONE);if(root!=null){java.util.ArrayDeque<View> q=new java.util.ArrayDeque<>();q.add(root);while(!q.isEmpty()){View x=q.remove();if(x instanceof Button)x.setEnabled(!v);if(x instanceof ViewGroup){ViewGroup g=(ViewGroup)x;for(int i=0;i<g.getChildCount();i++)q.add(g.getChildAt(i));}}}}''')
if 'String friendly(Exception e)' not in s:
    add.append('''String friendly(Exception e){String m=e==null?"":String.valueOf(e.getMessage());if(m.contains("UnknownHost")||m.contains("internet")||m.contains("اینترنت"))return "اینترنت در دسترس نیست";if(m.contains("timeout")||m.contains("Timeout"))return "ارتباط با سرور زمان‌بر شد. دوباره تلاش کنید.";return m.isEmpty()?"خطایی رخ داد. دوباره تلاش کنید.":m;}''')
if add:
    pos=s.rfind('\n}')
    s=s[:pos]+'\n    '+'\n    '.join(add)+s[pos:]
p.write_text(s,encoding='utf-8')
print('V18 helper fix2 applied')

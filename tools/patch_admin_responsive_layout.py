from pathlib import Path

p = Path('app/src/main/java/com/sakhtemanyar/AdminActivity.java')
s = p.read_text(encoding='utf-8')

# Make master-admin cards content-driven instead of relying on fixed outer heights.
repls = [
    ('body.addView(h,new LinearLayout.LayoutParams(-1,dp(112)));body.addView(gap(15));',
     'body.addView(h,new LinearLayout.LayoutParams(-1,-2));body.addView(gap(15));'),
    ('body.addView(x,new LinearLayout.LayoutParams(-1,dp(74)));body.addView(gap(9));',
     'body.addView(x,new LinearLayout.LayoutParams(-1,-2));body.addView(gap(10));'),
    ('body.addView(box,new LinearLayout.LayoutParams(-1,dp(142)));body.addView(gap(10));',
     'body.addView(box,new LinearLayout.LayoutParams(-1,-2));body.addView(gap(10));'),
    ('body.addView(x,new LinearLayout.LayoutParams(-1,dp(135)));body.addView(gap(9));',
     'body.addView(x,new LinearLayout.LayoutParams(-1,-2));body.addView(gap(10));'),
    ('body.addView(x,new LinearLayout.LayoutParams(-1,dp(165)));body.addView(gap(9));',
     'body.addView(x,new LinearLayout.LayoutParams(-1,-2));body.addView(gap(10));'),
    ('body.addView(x,new LinearLayout.LayoutParams(-1,dp(72)));body.addView(gap(8));',
     'body.addView(x,new LinearLayout.LayoutParams(-1,-2));body.addView(gap(8));'),
    ('body.addView(x,new LinearLayout.LayoutParams(-1,dp(78)));body.addView(gap(8));',
     'body.addView(x,new LinearLayout.LayoutParams(-1,-2));body.addView(gap(8));'),
]
for old, new in repls:
    if old in s:
        s = s.replace(old, new, 1)

# Responsive card internals: children can grow with wrapped Persian text.
old = '''void card(String h,String sub,String icon,int c,View.OnClickListener l){LinearLayout x=new LinearLayout(this);x.setGravity(Gravity.CENTER_VERTICAL);x.setPadding(dp(10),dp(5),dp(8),dp(5));x.setBackground(bg(white,19));TextView i=tv(icon,25,c);i.setGravity(Gravity.CENTER);x.addView(i,new LinearLayout.LayoutParams(dp(55),dp(64)));LinearLayout tx=new LinearLayout(this);tx.setOrientation(LinearLayout.VERTICAL);TextView a=tv(h,15,dark);a.setTypeface(Typeface.DEFAULT,Typeface.BOLD);tx.addView(a);tx.addView(tv(sub,11,muted));x.addView(tx,new LinearLayout.LayoutParams(0,dp(64),1));x.addView(tv("‹",25,muted),new LinearLayout.LayoutParams(dp(34),dp(64)));x.setOnClickListener(l);body.addView(x,new LinearLayout.LayoutParams(-1,-2));body.addView(gap(10));}'''
new = '''void card(String h,String sub,String icon,int c,View.OnClickListener l){LinearLayout x=new LinearLayout(this);x.setGravity(Gravity.CENTER_VERTICAL);x.setPadding(dp(10),dp(8),dp(8),dp(8));x.setBackground(bg(white,19));TextView i=tv(icon,25,c);i.setGravity(Gravity.CENTER);i.setMinHeight(dp(64));x.addView(i,new LinearLayout.LayoutParams(dp(55),-2));LinearLayout tx=new LinearLayout(this);tx.setOrientation(LinearLayout.VERTICAL);tx.setGravity(Gravity.CENTER_VERTICAL);tx.setMinimumHeight(dp(64));TextView a=tv(h,15,dark);a.setTypeface(Typeface.DEFAULT,Typeface.BOLD);tx.addView(a,new LinearLayout.LayoutParams(-1,-2));TextView d=tv(sub,11,muted);tx.addView(d,new LinearLayout.LayoutParams(-1,-2));x.addView(tx,new LinearLayout.LayoutParams(0,-2,1));TextView arrow=tv("‹",25,muted);arrow.setGravity(Gravity.CENTER);arrow.setMinHeight(dp(64));x.addView(arrow,new LinearLayout.LayoutParams(dp(34),-2));x.setOnClickListener(l);body.addView(x,new LinearLayout.LayoutParams(-1,-2));body.addView(gap(10));}'''
if old in s:
    s = s.replace(old, new, 1)

# Make variable-height list cards explicitly wrap content while preserving comfortable minimum controls.
s = s.replace('body.addView(box,new LinearLayout.LayoutParams(-1,-2));', 'body.addView(box,new LinearLayout.LayoutParams(-1,-2));', 1)

p.write_text(s, encoding='utf-8')
print('Responsive admin layout patch applied')

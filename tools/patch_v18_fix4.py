from pathlib import Path

for name in ['MainActivity.java','AdminActivity.java']:
    p=Path('app/src/main/java/com/sakhtemanyar')/name
    s=p.read_text(encoding='utf-8')
    if 'import ir.sakhtemanyar.app.BuildConfig;' not in s:
        s=s.replace('package com.sakhtemanyar;','package com.sakhtemanyar;\nimport ir.sakhtemanyar.app.BuildConfig;',1)
    if 'scrollWrap(View v)' not in s:
        marker='int dp(float n)'
        helper='''    View scrollWrap(View v){
        ScrollView sv=new ScrollView(this);
        sv.setFillViewport(true);
        sv.setPadding(0,dp(2),0,dp(2));
        sv.addView(v,new ScrollView.LayoutParams(-1,-2));
        return sv;
    }
'''
        idx=s.find(marker)
        if idx>=0:
            line_start=s.rfind('\n',0,idx)+1
            s=s[:line_start]+helper+s[line_start:]
    s=s.replace('.setView(l)', '.setView(scrollWrap(l))')
    p.write_text(s,encoding='utf-8')
print('V18 final hardening applied')

from pathlib import Path

for name in ['MainActivity.java','AdminActivity.java']:
 p=Path('app/src/main/java/com/sakhtemanyar')/name
 s=p.read_text(encoding='utf-8')
 if 'import ir.sakhtemanyar.app.BuildConfig;' not in s:
  s=s.replace('package com.sakhtemanyar;','package com.sakhtemanyar;\nimport ir.sakhtemanyar.app.BuildConfig;',1)
 if 'View scrollWrap(View v)' not in s:
  marker='    int dp(float n)'
  helper='''    View scrollWrap(View v){\n        ScrollView sv=new ScrollView(this);\n        sv.setFillViewport(true);\n        sv.setPadding(0,dp(2),0,dp(2));\n        sv.addView(v,new ScrollView.LayoutParams(-1,-2));\n        return sv;\n    }\n'''
  s=s.replace(marker,helper+marker,1)
 s=s.replace('.setView(l)', '.setView(scrollWrap(l))')
 p.write_text(s,encoding='utf-8')
print('V18 final hardening applied')

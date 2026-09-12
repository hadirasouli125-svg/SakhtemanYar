from pathlib import Path
for name in ['MainActivity.java','AdminActivity.java']:
 p=Path('app/src/main/java/com/sakhtemanyar')/name
 s=p.read_text(encoding='utf-8')
 if 'import ir.sakhtemanyar.app.BuildConfig;' not in s:
  if name=='MainActivity.java': s=s.replace('package com.sakhtemanyar;','package com.sakhtemanyar;\nimport ir.sakhtemanyar.app.BuildConfig;',1)
  else: s=s.replace('package com.sakhtemanyar;','package com.sakhtemanyar;\nimport ir.sakhtemanyar.app.BuildConfig;',1)
 p.write_text(s,encoding='utf-8')
print('V18 BuildConfig import fixed')

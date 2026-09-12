from pathlib import Path
p=Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s=p.read_text(encoding='utf-8')
s=s.replace('formatToman(amount)', 'amount+" ریال"')
s=s.replace('formatToman(x.optString("amount","0"))', 'x.optString("amount","0")+" ریال"')
p.write_text(s,encoding='utf-8')
print('v6 compile compatibility patch applied')

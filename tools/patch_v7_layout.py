from pathlib import Path
p=Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s=p.read_text(encoding='utf-8')

def replace_once(old,new):
    global s
    if old in s:
        s=s.replace(old,new,1)

replace_once('content.addView(x,new LinearLayout.LayoutParams(-1,dp(70)));content.addView(gap(8));', 'LinearLayout.LayoutParams ilp=new LinearLayout.LayoutParams(-1,-2);ilp.setMargins(0,0,0,dp(9));x.setMinimumHeight(dp(92));content.addView(x,ilp);')
replace_once('content.addView(c,new LinearLayout.LayoutParams(-1,dp(145)));content.addView(gap(9));', 'LinearLayout.LayoutParams ulp=new LinearLayout.LayoutParams(-1,-2);ulp.setMargins(0,0,0,dp(12));c.setMinimumHeight(dp(178));content.addView(c,ulp);')
replace_once('content.addView(c,new LinearLayout.LayoutParams(-1,dp("pending".equals(x.optString("status"))?170:125)));content.addView(gap(9));', 'LinearLayout.LayoutParams plp=new LinearLayout.LayoutParams(-1,-2);plp.setMargins(0,0,0,dp(9));c.setMinimumHeight("pending".equals(x.optString("status"))?170:125);content.addView(c,plp);')
old='money(x.optDouble("amount_rial"))+"  •  "+JalaliDate.format(x.optString("created_at"))'
new='money(x.optDouble("amount_rial"))+"  •  تاریخ: "+JalaliDate.format(x.optString("charge_date",x.optString("due_date",x.optString("created_at"))))'
replace_once(old,new)
p.write_text(s,encoding='utf-8')
print('v7 layout/date rendering patch applied')

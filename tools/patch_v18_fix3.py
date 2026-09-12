from pathlib import Path

main=Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
admin=Path('app/src/main/java/com/sakhtemanyar/AdminActivity.java')
gradle=Path('app/build.gradle')

for p in (main,admin):
    s=p.read_text(encoding='utf-8')
    s=s.replace('static final String API="https://okizneyesdwiundvadpe.supabase.co/functions/v1/api_gateway";','static final String API=BuildConfig.API_BASE_URL;')
    p.write_text(s,encoding='utf-8')

g=gradle.read_text(encoding='utf-8')
if 'buildConfigField "String", "API_BASE_URL"' not in g:
    marker="versionName '1.0.0' }"
    g=g.replace(marker,"versionName '1.0.0'; buildConfigField 'String', 'API_BASE_URL', '\"https://okizneyesdwiundvadpe.supabase.co/functions/v1/api_gateway\"' }",1)
if 'buildFeatures { buildConfig true }' not in g:
    g=g.replace('android { namespace', 'android { buildFeatures { buildConfig true }; namespace',1)
gradle.write_text(g,encoding='utf-8')

s=admin.read_text(encoding='utf-8')
needle='EditText n=in("نام طرح"),d=in("مدت به روز"),p=in("مبلغ به ریال"),m=in("حداکثر واحد");'
if needle in s and 'Switch active=new Switch(this)' not in s:
    s=s.replace(needle,needle+'Switch active=new Switch(this);active.setText("فعال");if(x!=null)active.setChecked(x.optBoolean("active",true));',1)
s=s.replace('for(EditText e:new EditText[]{n,d,p,m}){l.addView(e,new LinearLayout.LayoutParams(-1,dp(52)));l.addView(gap(7));}', 'for(EditText e:new EditText[]{n,d,p,m}){l.addView(e,new LinearLayout.LayoutParams(-1,dp(52)));l.addView(gap(7));}l.addView(active,new LinearLayout.LayoutParams(-1,dp(48)));',1)
s=s.replace('b.put("plan_id",x.optString("id"));post(b,session);', 'b.put("plan_id",x.optString("id"));b.put("active",active.isChecked());post(b,session);',1)
admin.write_text(s,encoding='utf-8')
print('V18 fix3 applied')

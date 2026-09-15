from pathlib import Path

P=Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s=P.read_text(encoding='utf-8')

def replace_method(src,name,new):
    marker='void '+name+'('
    start=src.find(marker)
    if start<0:
        raise SystemExit('method not found: '+name)
    brace=src.find('{',start)
    depth=0
    for i in range(brace,len(src)):
        if src[i]=='{': depth+=1
        elif src[i]=='}':
            depth-=1
            if depth==0:
                return src[:start]+new+src[i+1:]
    raise SystemExit('unterminated method: '+name)

new_residents='''void residents(){frame("ساکنین",true);managerDrawer();section("مدیریت ساکنین","مدیر ساختمان می‌تواند مشخصات ساکن را ویرایش یا ساکن قبلی را حذف کند");call("list_residents",j->{JSONArray a=j.optJSONArray("data");if(a==null||a.length()==0){empty("هنوز ساکنی ثبت نشده است");return;}for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(14),dp(12),dp(14),dp(12));c.setBackground(box(white,18));c.addView(tv(x.optString("full_name","ساکن بدون نام"),17,navy));c.addView(tv("نام کاربری: "+x.optString("username","-")+" • تلفن: "+x.optString("phone","-"),13,muted));c.addView(tv("وضعیت: "+(x.optBoolean("active",true)?"فعال":"غیرفعال"),12,x.optBoolean("active",true)?green:red));LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);Button e=btn("ویرایش",blue),d=btn("حذف ساکن",red);LinearLayout.LayoutParams ep=new LinearLayout.LayoutParams(0,dp(46),1);ep.setMargins(0,0,dp(4),0);LinearLayout.LayoutParams dp0=new LinearLayout.LayoutParams(0,dp(46),1);dp0.setMargins(dp(4),0,0,0);row.addView(e,ep);row.addView(d,dp0);c.addView(row);e.setOnClickListener(v->residentEditDialog(x));d.setOnClickListener(v->new AlertDialog.Builder(this).setTitle("حذف ساکن").setMessage("آیا از حذف این ساکن اطمینان دارید؟").setNegativeButton("لغو",null).setPositiveButton("حذف",(q,w)->call("delete_resident",new JSONObject().put("resident_id",x.optString("id")),z->{toast("ساکن حذف شد");residents();})).show());content.addView(c,new LinearLayout.LayoutParams(-1,-2));content.addView(gap(10));}});}'''

new_edit='''void residentEditDialog(JSONObject x){EditText name=input("نام و نام خانوادگی"),phone=input("شماره تلفن"),pass=input("رمز جدید (اختیاری)");name.setText(x.optString("full_name",""));phone.setText(x.optString("phone",""));pass.setInputType(129);LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.addView(name,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));l.addView(phone,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));l.addView(pass,new LinearLayout.LayoutParams(-1,dp(54)));AlertDialog d=new AlertDialog.Builder(this).setTitle("ویرایش ساکن").setView(dialogScroll(l)).setNegativeButton("لغو",null).setPositiveButton("ذخیره",(q,w)->{JSONObject b=new JSONObject().put("resident_id",x.optString("id")).put("full_name",name.getText().toString().trim()).put("phone",phone.getText().toString().trim());String p=pass.getText().toString();if(!p.isEmpty())b.put("password",p);call("update_resident",b,z->{toast("اطلاعات ساکن ویرایش شد");residents();});}).create();d.setOnShowListener(q->{Window win=d.getWindow();if(win!=null){win.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);win.setLayout((int)(getResources().getDisplayMetrics().widthPixels*.94f),WindowManager.LayoutParams.WRAP_CONTENT);}});d.show();}'''

s=replace_method(s,'residents',new_residents)
s=replace_method(s,'residentEditDialog',new_edit)
P.write_text(s,encoding='utf-8')
print('resident management patch applied')

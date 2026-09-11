from pathlib import Path

p = Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s = p.read_text(encoding='utf-8')

if 'import android.util.Base64;' not in s:
    s = s.replace('import android.widget.*;\n', 'import android.widget.*;\nimport android.util.Base64;\n')
old_fields='LinearLayout root,content,drawer; String session="",role=""; final ArrayDeque<String> history=new ArrayDeque<>();'
new_fields=old_fields+'\n    int uploadTarget=0; Button receiptButton; String receiptData="";'
s=s.replace(old_fields,new_fields,1)
old_destroy='@Override protected void onDestroy(){io.shutdownNow();super.onDestroy();}'
new_destroy='''@Override protected void onDestroy(){io.shutdownNow();super.onDestroy();}
    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){super.onActivityResult(requestCode,resultCode,data);if(requestCode==901&&resultCode==RESULT_OK&&data!=null&&data.getData()!=null){try{InputStream in=getContentResolver().openInputStream(data.getData());Bitmap b=BitmapFactory.decodeStream(in);if(in!=null)in.close();if(b==null)throw new Exception("image");int max=900,w=b.getWidth(),h=b.getHeight();if(Math.max(w,h)>max){float sc=Math.min((float)max/w,(float)max/h);b=Bitmap.createScaledBitmap(b,Math.max(1,(int)(w*sc)),Math.max(1,(int)(h*sc)),true);}ByteArrayOutputStream out=new ByteArrayOutputStream();b.compress(Bitmap.CompressFormat.JPEG,78,out);receiptData="data:image/jpeg;base64,"+Base64.encodeToString(out.toByteArray(),Base64.NO_WRAP);if(receiptButton!=null)receiptButton.setText("✓ فیش/عکس انتخاب شد");toast("عکس انتخاب شد");}catch(Exception e){toast("انتخاب عکس انجام نشد");}}}'''
s=s.replace(old_destroy,new_destroy,1)
# Improve all action cards, especially unit account activation.
s=s.replace('content.addView(x,new LinearLayout.LayoutParams(-1,dp(70)));content.addView(gap(8));','content.addView(x,new LinearLayout.LayoutParams(-1,dp(82)));content.addView(gap(12));',1)
s=s.replace('x.addView(i,new LinearLayout.LayoutParams(dp(55),dp(58)));','x.addView(i,new LinearLayout.LayoutParams(dp(62),dp(64)));',1)
s=s.replace('x.addView(tx,new LinearLayout.LayoutParams(0,dp(58),1));x.addView(tv("‹",25,muted),new LinearLayout.LayoutParams(dp(31),dp(58)));','x.addView(tx,new LinearLayout.LayoutParams(0,dp(64),1));x.addView(tv("‹",25,muted),new LinearLayout.LayoutParams(dp(36),dp(64)));',1)

start=s.index('    void chargeDialog(){'); end=s.index('    void repairs(){',start)
new_charge='''    void chargeDialog(){
        call("dashboard",j->{final JSONArray units=j.optJSONArray("units");final EditText t=input("عنوان شارژ / هزینه"),a=input("مبلغ به تومان"),d=input("توضیحات");final Spinner target=new Spinner(this);final ArrayList<String> labels=new ArrayList<>(),ids=new ArrayList<>();labels.add("کل ساختمان");ids.add("");if(units!=null)for(int i=0;i<units.length();i++){JSONObject u=units.optJSONObject(i);if(u!=null){labels.add("واحد "+u.optString("unit_no","-"));ids.add(u.optString("id",""));}}target.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,labels));receiptData="";receiptButton=btn("＋ آپلود عکس / فیش هزینه",gold);LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(dp(10),0,dp(10),0);l.addView(tv("اختصاص هزینه به",12,muted),new LinearLayout.LayoutParams(-1,dp(32)));l.addView(target,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(7));for(EditText e:new EditText[]{t,a,d}){l.addView(e,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(7));}l.addView(receiptButton,new LinearLayout.LayoutParams(-1,dp(50)));receiptButton.setOnClickListener(v->{uploadTarget=1;pickImage();});new AlertDialog.Builder(this).setTitle("ثبت شارژ یا هزینه").setView(l).setNegativeButton("لغو",null).setPositiveButton("ثبت",(x,w)->{long rial=Math.max(0,parseMoney(a.getText().toString())*10);String unitId=ids.get(target.getSelectedItemPosition());callObj(new JSONObject().put("action","add_charge").put("title",t.getText().toString().trim()).put("amount_rial",rial).put("description",d.getText().toString().trim()).put("unit_id",unitId.isEmpty()?JSONObject.NULL:unitId).put("allocation_method",unitId.isEmpty()?"per_unit":"unit_specific").put("receipt_url",receiptData),z->{receiptData="";receiptButton=null;toast("هزینه ثبت شد");charges();});}).show();});
    }
'''
s=s[:start]+new_charge+s[end:]

start=s.index('    void repairs(){'); end=s.index('    void payments(){',start)
new_repairs='''    void repairs(){
        frame("تعمیرات",true);managerDrawer();section("تعمیرات ساختمان","ثبت تعمیر همراه با عکس فاکتور یا مستندات");Button add=btn("＋ ثبت تعمیر جدید",red);content.addView(add,new LinearLayout.LayoutParams(-1,dp(54)));content.addView(gap(12));add.setOnClickListener(v->{final EditText t=input("عنوان تعمیر"),a=input("مبلغ به تومان"),d=input("توضیحات");receiptData="";receiptButton=btn("＋ آپلود عکس / فیش تعمیرات",red);LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(dp(10),0,dp(10),0);for(EditText e:new EditText[]{t,a,d}){l.addView(e,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));}l.addView(receiptButton,new LinearLayout.LayoutParams(-1,dp(50)));receiptButton.setOnClickListener(q->{uploadTarget=3;pickImage();});new AlertDialog.Builder(this).setTitle("ثبت تعمیرات").setView(l).setNegativeButton("لغو",null).setPositiveButton("ثبت",(q,w)->{long rial=Math.max(0,parseMoney(a.getText().toString())*10);callObj(new JSONObject().put("action","add_repair").put("title",t.getText().toString().trim()).put("amount_rial",rial).put("description",d.getText().toString().trim()).put("receipt_url",receiptData),z->{receiptData="";receiptButton=null;toast("تعمیر ثبت شد");repairs();});}).show();});call("dashboard",j->{JSONArray r=j.optJSONArray("repairs");if(r==null||r.length()==0){empty("هنوز تعمیراتی ثبت نشده است");return;}for(int i=0;i<r.length();i++){JSONObject x=r.optJSONObject(i);if(x==null)continue;String title=x.optString("title","تعمیر"),amount=x.optString("amount_rial",x.optString("amount","0")),receipt=x.optString("receipt_url","");item(title,"مبلغ: "+formatToman(amount)+(receipt.isEmpty()?"":"  •  📎 فیش/عکس پیوست دارد"));}});
    }
'''
s=s[:start]+new_repairs+s[end:]

start=s.index('    void payments(){'); end=s.index('    void plans(){',start)
new_payments='''    void payments(){
        frame("پرداخت‌ها",true);managerDrawer();section("ثبت و بررسی پرداخت‌ها","پرداخت ساکن را به واحد درست ثبت کنید و فیش را بررسی کنید");Button add=btn("＋ ثبت پرداخت برای ساکن",green);content.addView(add,new LinearLayout.LayoutParams(-1,dp(54)));content.addView(gap(12));add.setOnClickListener(v->{call("dashboard",j->{JSONArray units=j.optJSONArray("units");ArrayList<String> labels=new ArrayList<>(),ids=new ArrayList<>();if(units!=null)for(int i=0;i<units.length();i++){JSONObject u=units.optJSONObject(i);if(u!=null){labels.add("واحد "+u.optString("unit_no","-"));ids.add(u.optString("id",""));}}final Spinner unit=new Spinner(this);unit.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,labels));final EditText a=input("مبلغ پرداخت به تومان"),n=input("توضیحات / شماره پیگیری");receiptData="";receiptButton=btn("＋ آپلود عکس / فیش پرداخت",green);LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(dp(10),0,dp(10),0);l.addView(tv("انتخاب واحد ساکن",12,muted),new LinearLayout.LayoutParams(-1,dp(30)));l.addView(unit,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));l.addView(a,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));l.addView(n,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));l.addView(receiptButton,new LinearLayout.LayoutParams(-1,dp(50)));receiptButton.setOnClickListener(q->{uploadTarget=2;pickImage();});new AlertDialog.Builder(this).setTitle("ثبت پرداخت برای ساکن").setView(l).setNegativeButton("لغو",null).setPositiveButton("ثبت",(q,w)->{if(ids.isEmpty()){toast("هیچ واحدی برای ثبت پرداخت وجود ندارد");return;}long rial=Math.max(0,parseMoney(a.getText().toString())*10);callObj(new JSONObject().put("action","add_payment").put("unit_id",ids.get(unit.getSelectedItemPosition())).put("amount_rial",rial).put("note",n.getText().toString().trim()).put("receipt_url",receiptData),z->{receiptData="";receiptButton=null;toast("پرداخت با موفقیت ثبت شد");payments();});}).show();});});
        call("dashboard",j->{JSONArray p=j.optJSONArray("payments");if(p==null||p.length()==0){empty("هنوز پرداختی ثبت نشده است");return;}for(int i=0;i<p.length();i++){JSONObject x=p.optJSONObject(i);if(x==null)continue;String st=x.optString("status","pending"),label=st.equals("approved")?"تأیید شده":st.equals("rejected")?"رد شده":"در انتظار بررسی",receipt=x.optString("receipt_url","");item("پرداخت واحد "+x.optString("unit_id","-"),"مبلغ: "+formatToman(x.optString("amount","0"))+" • "+label+(receipt.isEmpty()?"":" • 📎 فیش پیوست دارد"));}}
    }
'''
s=s[:start]+new_payments+s[end:]

# Shared picker helper keeps all three upload buttons consistent.
if 'void pickImage()' not in s:
    marker='    void logout(){session="";role="";history.clear();showLogin();}\n'
    helper='    void pickImage(){Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);i.setType("image/*");startActivityForResult(i,901);}\n'
    if marker in s:s=s.replace(marker,marker+helper,1)

# Resident payment: no unit id is required; API derives it from the resident session.
start=s.index('    void residentPay(){'); end=s.index('    void adminHome(){',start)
new_res='''    void residentPay(){frame("ثبت پرداخت",true);residentDrawer();section("ثبت پرداخت جدید","فیش پرداخت را همراه مبلغ برای تأیید مدیر ارسال کنید");EditText a=input("مبلغ پرداخت به تومان"),n=input("توضیحات / شماره پیگیری");content.addView(a,new LinearLayout.LayoutParams(-1,dp(56)));content.addView(gap(9));content.addView(n,new LinearLayout.LayoutParams(-1,dp(56)));content.addView(gap(10));receiptData="";receiptButton=btn("＋ آپلود عکس / فیش پرداخت",green);content.addView(receiptButton,new LinearLayout.LayoutParams(-1,dp(52)));content.addView(gap(12));Button b=btn("ثبت پرداخت برای بررسی مدیر",green);content.addView(b,new LinearLayout.LayoutParams(-1,dp(55)));receiptButton.setOnClickListener(v->{uploadTarget=2;pickImage();});b.setOnClickListener(v->{long rial=Math.max(0,parseMoney(a.getText().toString())*10);if(rial<=0){toast("مبلغ پرداخت را وارد کنید");return;}callObj(new JSONObject().put("action","add_payment").put("amount_rial",rial).put("note",n.getText().toString().trim()).put("receipt_url",receiptData),z->{toast("پرداخت و فیش برای بررسی مدیر ارسال شد");receiptData="";receiptButton=null;residentHome();});});}
'''
s=s[:start]+new_res+s[end:]

p.write_text(s,encoding='utf-8')
print('patched payment, charge, repair receipt flows and spacing')

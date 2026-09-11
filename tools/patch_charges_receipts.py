from pathlib import Path

p = Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s = p.read_text(encoding='utf-8')

if 'import android.util.Base64;' not in s:
    s = s.replace('import android.widget.*;\n', 'import android.widget.*;\nimport android.util.Base64;\n')

old_fields = 'LinearLayout root,content,drawer; String session="",role=""; final ArrayDeque<String> history=new ArrayDeque<>();'
new_fields = old_fields + '\n    int uploadTarget=0; Button receiptButton; String receiptData="";'
s = s.replace(old_fields, new_fields)

old_destroy = '@Override protected void onDestroy(){io.shutdownNow();super.onDestroy();}'
new_destroy = '''@Override protected void onDestroy(){io.shutdownNow();super.onDestroy();}
    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){super.onActivityResult(requestCode,resultCode,data);if(requestCode==901&&resultCode==RESULT_OK&&data!=null&&data.getData()!=null){try{InputStream in=getContentResolver().openInputStream(data.getData());Bitmap b=BitmapFactory.decodeStream(in);if(in!=null)in.close();if(b==null)throw new Exception("تصویر قابل خواندن نیست");int max=900,w=b.getWidth(),h=b.getHeight();if(Math.max(w,h)>max){float sc=Math.min((float)max/w,(float)max/h);b=Bitmap.createScaledBitmap(b,Math.max(1,(int)(w*sc)),Math.max(1,(int)(h*sc)),true);}ByteArrayOutputStream out=new ByteArrayOutputStream();b.compress(Bitmap.CompressFormat.JPEG,78,out);receiptData="data:image/jpeg;base64,"+Base64.encodeToString(out.toByteArray(),Base64.NO_WRAP);if(receiptButton!=null)receiptButton.setText("✓ فیش/عکس انتخاب شد");toast("عکس فیش انتخاب شد");}catch(Exception e){toast("انتخاب عکس انجام نشد");}}}'''
s = s.replace(old_destroy, new_destroy)

start = s.index('    void chargeDialog(){')
end = s.index('    void repairs(){', start)
new_charge = '''    void chargeDialog(){
        call("dashboard",j->{
            final JSONArray units=j.optJSONArray("units");
            final EditText t=input("عنوان شارژ / هزینه"),a=input("مبلغ به تومان"),d=input("توضیحات");
            final Spinner target=new Spinner(this); final ArrayList<String> labels=new ArrayList<>(); final ArrayList<String> ids=new ArrayList<>();
            labels.add("کل ساختمان"); ids.add("");
            if(units!=null)for(int i=0;i<units.length();i++){JSONObject u=units.optJSONObject(i);if(u!=null){labels.add("واحد "+u.optString("unit_no","-"));ids.add(u.optString("id",""));}}
            ArrayAdapter<String> adapter=new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,labels);target.setAdapter(adapter);
            receiptData=""; receiptButton=btn("＋ آپلود عکس / فیش هزینه",gold);
            LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(dp(10),0,dp(10),0);
            l.addView(tv("اختصاص هزینه به",12,muted),new LinearLayout.LayoutParams(-1,dp(32)));l.addView(target,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(7));
            for(EditText e:new EditText[]{t,a,d}){l.addView(e,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(7));}
            l.addView(receiptButton,new LinearLayout.LayoutParams(-1,dp(50))); receiptButton.setOnClickListener(v->{uploadTarget=1;Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);i.setType("image/*");startActivityForResult(i,901);});
            new AlertDialog.Builder(this).setTitle("ثبت شارژ یا هزینه").setView(l).setNegativeButton("لغو",null).setPositiveButton("ثبت",(x,w)->{long rial=Math.max(0,parseMoney(a.getText().toString())*10);String unitId=ids.get(target.getSelectedItemPosition());callObj(new JSONObject().put("action","add_charge").put("title",t.getText().toString()).put("amount_rial",rial).put("description",d.getText().toString()).put("unit_id",unitId.isEmpty()?JSONObject.NULL:unitId).put("allocation_method",unitId.isEmpty()?"per_unit":"unit_specific").put("receipt_url",receiptData),z->{receiptData="";receiptButton=null;toast("هزینه ثبت شد");charges();});}).show();
        });
    }
'''
s = s[:start] + new_charge + s[end:]

start = s.index('    void residentPay(){')
end = s.index('    void adminHome(){', start)
new_pay = '''    void residentPay(){
        frame("ثبت پرداخت",true);residentDrawer();section("ثبت پرداخت جدید","فیش پرداخت را هم می‌توانید همراه مبلغ ارسال کنید");
        EditText a=input("مبلغ پرداخت به تومان"),n=input("توضیحات / شماره پیگیری");content.addView(a,new LinearLayout.LayoutParams(-1,dp(56)));content.addView(gap(9));content.addView(n,new LinearLayout.LayoutParams(-1,dp(56)));content.addView(gap(10));
        receiptData="";receiptButton=btn("＋ آپلود عکس / فیش پرداخت",green);content.addView(receiptButton,new LinearLayout.LayoutParams(-1,dp(52)));content.addView(gap(12));
        Button b=btn("ثبت پرداخت برای بررسی",green);content.addView(b,new LinearLayout.LayoutParams(-1,dp(55)));
        receiptButton.setOnClickListener(v->{uploadTarget=2;Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);i.setType("image/*");startActivityForResult(i,901);});
        b.setOnClickListener(v->{long rial=Math.max(0,parseMoney(a.getText().toString())*10);callObj(new JSONObject().put("action","add_payment").put("amount_rial",rial).put("note",n.getText().toString()).put("receipt_url",receiptData),z->{toast("پرداخت ثبت شد و فیش برای مدیر ارسال شد");receiptData="";receiptButton=null;residentHome();});});
    }
'''
s = s[:start] + new_pay + s[end:]

p.write_text(s, encoding='utf-8')
print('patched charges and receipts')

from pathlib import Path

p = Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s = p.read_text(encoding='utf-8')

if 'import android.util.Base64;' not in s:
    s = s.replace('import android.widget.*;\n', 'import android.widget.*;\nimport android.util.Base64;\n')

old_fields = 'LinearLayout root,content,drawer; String session="",role=""; final ArrayDeque<String> history=new ArrayDeque<>();'
new_fields = old_fields + '\n    int uploadTarget=0; Button receiptButton; String receiptData="";'
s = s.replace(old_fields, new_fields, 1)

old_destroy = '@Override protected void onDestroy(){io.shutdownNow();super.onDestroy();}'
new_destroy = '''@Override protected void onDestroy(){io.shutdownNow();super.onDestroy();}
    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){super.onActivityResult(requestCode,resultCode,data);if(requestCode==901&&resultCode==RESULT_OK&&data!=null&&data.getData()!=null){try{InputStream in=getContentResolver().openInputStream(data.getData());Bitmap b=BitmapFactory.decodeStream(in);if(in!=null)in.close();if(b==null)throw new Exception("image");int max=900,w=b.getWidth(),h=b.getHeight();if(Math.max(w,h)>max){float sc=Math.min((float)max/w,(float)max/h);b=Bitmap.createScaledBitmap(b,Math.max(1,(int)(w*sc)),Math.max(1,(int)(h*sc)),true);}ByteArrayOutputStream out=new ByteArrayOutputStream();b.compress(Bitmap.CompressFormat.JPEG,78,out);receiptData="data:image/jpeg;base64,"+Base64.encodeToString(out.toByteArray(),Base64.NO_WRAP);if(receiptButton!=null)receiptButton.setText("✓ فیش/عکس انتخاب شد");toast("عکس انتخاب شد");}catch(Exception e){toast("انتخاب عکس انجام نشد");}}}'''
s = s.replace(old_destroy, new_destroy, 1)

# Give action cards more breathing room so the icon and account controls do not collide.
old_action = 'content.addView(x,new LinearLayout.LayoutParams(-1,dp(70)));content.addView(gap(8));'
new_action = 'content.addView(x,new LinearLayout.LayoutParams(-1,dp(82)));content.addView(gap(12));'
s = s.replace(old_action, new_action, 1)
old_icon = 'x.addView(i,new LinearLayout.LayoutParams(dp(55),dp(58)));'
new_icon = 'x.addView(i,new LinearLayout.LayoutParams(dp(62),dp(64)));'
s = s.replace(old_icon, new_icon, 1)
old_tx = 'x.addView(tx,new LinearLayout.LayoutParams(0,dp(58),1));x.addView(tv("‹",25,muted),new LinearLayout.LayoutParams(dp(31),dp(58)));'
new_tx = 'x.addView(tx,new LinearLayout.LayoutParams(0,dp(64),1));x.addView(tv("‹",25,muted),new LinearLayout.LayoutParams(dp(36),dp(64)));'
s = s.replace(old_tx, new_tx, 1)

# Charge form with building-wide or unit-specific target and receipt upload.
start = s.index('    void chargeDialog(){')
end = s.index('    void repairs(){', start)
new_charge = '''    void chargeDialog(){
        call("dashboard",j->{
            final JSONArray units=j.optJSONArray("units");
            final EditText t=input("عنوان شارژ / هزینه"),a=input("مبلغ به تومان"),d=input("توضیحات");
            final Spinner target=new Spinner(this); final ArrayList<String> labels=new ArrayList<>(); final ArrayList<String> ids=new ArrayList<>();
            labels.add("کل ساختمان"); ids.add("");
            if(units!=null)for(int i=0;i<units.length();i++){JSONObject u=units.optJSONObject(i);if(u!=null){labels.add("واحد "+u.optString("unit_no","-"));ids.add(u.optString("id",""));}}
            target.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,labels));
            receiptData="";receiptButton=btn("＋ آپلود عکس / فیش هزینه",gold);
            LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(dp(10),0,dp(10),0);
            l.addView(tv("اختصاص هزینه به",12,muted),new LinearLayout.LayoutParams(-1,dp(32)));l.addView(target,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(7));
            for(EditText e:new EditText[]{t,a,d}){l.addView(e,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(7));}
            l.addView(receiptButton,new LinearLayout.LayoutParams(-1,dp(50)));receiptButton.setOnClickListener(v->{uploadTarget=1;Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);i.setType("image/*");startActivityForResult(i,901);});
            new AlertDialog.Builder(this).setTitle("ثبت شارژ یا هزینه").setView(l).setNegativeButton("لغو",null).setPositiveButton("ثبت",(x,w)->{long rial=Math.max(0,parseMoney(a.getText().toString())*10);String unitId=ids.get(target.getSelectedItemPosition());callObj(new JSONObject().put("action","add_charge").put("title",t.getText().toString().trim()).put("amount_rial",rial).put("description",d.getText().toString().trim()).put("unit_id",unitId.isEmpty()?JSONObject.NULL:unitId).put("allocation_method",unitId.isEmpty()?"per_unit":"unit_specific").put("receipt_url",receiptData),z->{receiptData="";receiptButton=null;toast("هزینه ثبت شد");charges();});}).show();
        });
    }
'''
s=s[:start]+new_charge+s[end:]

# Repair form with receipt/photo upload. The manager can keep the evidence attached to the repair record.
start=s.index('    void repairs(){')
end=s.index('    void plans(){',start)
new_repairs='''    void repairs(){
        frame("تعمیرات",true);managerDrawer();section("تعمیرات ساختمان","ثبت هزینه تعمیر همراه با عکس فاکتور یا مستندات");
        Button add=btn("＋ ثبت تعمیر جدید",red);content.addView(add,new LinearLayout.LayoutParams(-1,dp(54)));content.addView(gap(12));
        add.setOnClickListener(v->{final EditText t=input("عنوان تعمیر"),a=input("مبلغ به تومان"),d=input("توضیحات");receiptData="";receiptButton=btn("＋ آپلود عکس / فیش تعمیرات",red);LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(dp(10),0,dp(10),0);for(EditText e:new EditText[]{t,a,d}){l.addView(e,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));}l.addView(receiptButton,new LinearLayout.LayoutParams(-1,dp(50)));receiptButton.setOnClickListener(q->{uploadTarget=3;Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);i.setType("image/*");startActivityForResult(i,901);});new AlertDialog.Builder(this).setTitle("ثبت تعمیرات").setView(l).setNegativeButton("لغو",null).setPositiveButton("ثبت",(q,w)->{long rial=Math.max(0,parseMoney(a.getText().toString())*10);callObj(new JSONObject().put("action","add_repair").put("title",t.getText().toString().trim()).put("amount_rial",rial).put("description",d.getText().toString().trim()).put("receipt_url",receiptData),z->{receiptData="";receiptButton=null;toast("تعمیر ثبت شد");repairs();});}).show();});
        call("dashboard",j->{JSONArray r=j.optJSONArray("repairs");if(r==null||r.length()==0){empty("هنوز تعمیراتی ثبت نشده است");return;}for(int i=0;i<r.length();i++){JSONObject x=r.optJSONObject(i);if(x==null)continue;String title=x.optString("title","تعمیر");String amount=x.optString("amount_rial",x.optString("amount","0"));String receipt=x.optString("receipt_url","");item(title,"مبلغ: "+formatToman(amount)+(receipt.isEmpty()?"":"  •  📎 فیش/عکس پیوست دارد"));}});
    }
'''
s=s[:start]+new_repairs+s[end:]

p.write_text(s,encoding='utf-8')
print('patched charges, repairs, receipts and spacing')

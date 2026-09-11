from pathlib import Path
p=Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s=p.read_text(encoding='utf-8')
s=s.replace('formatToman(amount)', 'amount + " ریال"')
start=s.find('    void payments(){')
end=s.find('    void plans(){',start)
if start<0 or end<0: raise SystemExit('payment boundaries not found')
method='''    void payments(){
        frame("پرداخت‌ها",true); managerDrawer(); section("ثبت و بررسی پرداخت‌ها","پرداخت ساکن را به واحد درست ثبت کنید و فیش را بررسی کنید");
        Button add=btn("＋ ثبت پرداخت برای ساکن",green); content.addView(add,new LinearLayout.LayoutParams(-1,dp(54))); content.addView(gap(12));
        add.setOnClickListener(v->{
            call("dashboard",j->{
                JSONArray units=j.optJSONArray("units"); ArrayList<String> labels=new ArrayList<>(),ids=new ArrayList<>();
                if(units!=null)for(int i=0;i<units.length();i++){JSONObject u=units.optJSONObject(i);if(u!=null){labels.add("واحد "+u.optString("unit_no","-"));ids.add(u.optString("id",""));}}
                if(ids.isEmpty()){toast("هیچ واحدی برای ثبت پرداخت وجود ندارد");return;}
                Spinner unit=new Spinner(this); unit.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_spinner_dropdown_item,labels));
                EditText a=input("مبلغ پرداخت به تومان"),n=input("توضیحات / شماره پیگیری"); receiptData=""; receiptButton=btn("＋ آپلود عکس / فیش پرداخت",green);
                LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(dp(10),0,dp(10),0);
                l.addView(tv("انتخاب واحد ساکن",12,muted),new LinearLayout.LayoutParams(-1,dp(30))); l.addView(unit,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));
                l.addView(a,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));l.addView(n,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));l.addView(receiptButton,new LinearLayout.LayoutParams(-1,dp(50)));
                receiptButton.setOnClickListener(q->{uploadTarget=2;pickImage();});
                new AlertDialog.Builder(this).setTitle("ثبت پرداخت برای ساکن").setView(l).setNegativeButton("لغو",null).setPositiveButton("ثبت",(q,w)->{
                    long rial=Math.max(0,parseMoney(a.getText().toString())*10);if(rial<=0){toast("مبلغ پرداخت را وارد کنید");return;}
                    try{callObj(new JSONObject().put("action","add_payment").put("unit_id",ids.get(unit.getSelectedItemPosition())).put("amount_rial",rial).put("note",n.getText().toString().trim()).put("receipt_url",receiptData),z->{receiptData="";receiptButton=null;toast("پرداخت با موفقیت ثبت شد و در انتظار تأیید است");payments();});}catch(Exception e){toast("ثبت پرداخت ناموفق بود");}
                }).show();
            });
        });
        call("dashboard",j->{JSONArray p=j.optJSONArray("payments");if(p==null||p.length()==0){empty("هنوز پرداختی ثبت نشده است");return;}for(int i=0;i<p.length();i++){JSONObject x=p.optJSONObject(i);if(x==null)continue;String st=x.optString("status","pending");String label=st.equals("approved")?"تأیید شده":st.equals("rejected")?"رد شده":"در انتظار بررسی";String receipt=x.optString("receipt_url","");item("پرداخت واحد "+x.optString("unit_id","-"),"مبلغ: "+x.optString("amount","0")+" ریال • "+label+(receipt.isEmpty()?"":" • 📎 فیش پیوست دارد"));}});
    }
'''
s=s[:start]+method+s[end:]
p.write_text(s,encoding='utf-8')
print('payment screen finalized')

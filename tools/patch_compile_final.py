from pathlib import Path
import re

p = Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s = p.read_text(encoding='utf-8')

if 'void financeManagerItem(JSONObject x,boolean charge)' not in s:
    marker = '\n    void residentHome(){'
    method = r'''
    void financeManagerItem(JSONObject x,boolean charge){
        LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(15),dp(12),dp(15),dp(12));c.setBackground(box(white,18));
        String title=x.optString("title",charge?"شارژ / هزینه":"تعمیر");
        double amount=x.optDouble(charge?"amount_rial":"amount");
        c.addView(tv(title,16,navy),new LinearLayout.LayoutParams(-1,dp(34)));
        c.addView(tv("مبلغ: "+financeMoney(amount)+"  •  "+financeDate(x.optString(charge?"charge_date":"repair_date",x.optString("created_at"))),12,muted),new LinearLayout.LayoutParams(-1,dp(32)));
        LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);
        Button detail=btn("جزئیات",blue), receipt=btn("مشاهده فیش",gold);
        row.addView(detail,new LinearLayout.LayoutParams(0,dp(45),1));row.addView(receipt,new LinearLayout.LayoutParams(0,dp(45),1));c.addView(row);
        detail.setOnClickListener(v->{String d=x.optString("description","");new AlertDialog.Builder(this).setTitle(title).setMessage("مبلغ: "+financeMoney(amount)+"\n\n"+d).setPositiveButton("بستن",null).show();});
        receipt.setOnClickListener(v->showReceipt(x.optString("receipt_url","")));
        content.addView(c,new LinearLayout.LayoutParams(-1,-2));content.addView(gap(9));
    }
    void pickImage(){
        Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);i.setType("image/*");startActivityForResult(i,702);
    }
'''
    if marker in s:
        s=s.replace(marker,method+marker,1)
    else:
        pos=s.rfind('\n}')
        s=s[:pos]+method+s[pos:]

# Extend the subscription callback so legacy finance image selection also works.
old = r'@Override protected void onActivityResult\(int requestCode,int resultCode,Intent data\)\{.*?\n\s*\}'
m = re.search(old,s,re.S)
if m and 'requestCode==702' not in m.group(0):
    new = r'''@Override protected void onActivityResult(int requestCode,int resultCode,Intent data){
        super.onActivityResult(requestCode,resultCode,data);
        if(resultCode!=RESULT_OK||data==null||data.getData()==null)return;
        Uri u=data.getData();
        if(requestCode==702){
            io.submit(()->{try{InputStream in=getContentResolver().openInputStream(u);ByteArrayOutputStream out=new ByteArrayOutputStream();byte[] buf=new byte[8192];int n,total=0;while((n=in.read(buf))!=-1){total+=n;if(total>8*1024*1024)throw new Exception("حجم تصویر بیشتر از ۸ مگابایت است");out.write(buf,0,n);}in.close();String mime=getContentResolver().getType(u);if(mime==null)mime="image/jpeg";receiptData="data:"+mime+";base64,"+Base64.encodeToString(out.toByteArray(),Base64.NO_WRAP);runOnUiThread(()->{if(receiptButton!=null)receiptButton.setText("✓ فیش / تصویر انتخاب شد");toast("فایل انتخاب شد");});}catch(Exception e){runOnUiThread(()->toast(e.getMessage()==null?"خطا در انتخاب تصویر":e.getMessage()));}});return;
        }
        if(requestCode!=701)return;
        io.submit(()->{try{InputStream in=getContentResolver().openInputStream(u);ByteArrayOutputStream out=new ByteArrayOutputStream();byte[] buf=new byte[8192];int n,total=0;while((n=in.read(buf))!=-1){total+=n;if(total>10*1024*1024)throw new Exception("حجم فیش بیشتر از ۱۰ مگابایت است");out.write(buf,0,n);}in.close();String mime=getContentResolver().getType(u);if(mime==null)mime="application/octet-stream";JSONObject q=new JSONObject().put("action","upload_receipt").put("request_id",pendingRequestId).put("mime_type",mime).put("file_base64",Base64.encodeToString(out.toByteArray(),Base64.NO_WRAP));JSONObject j=new JSONObject(post(q,session));if(j.has("error"))throw new Exception(j.getString("error"));runOnUiThread(()->toast("فیش با موفقیت ارسال شد؛ درخواست در انتظار تأیید مدیرکل است"));}catch(Exception e){runOnUiThread(()->toast(e.getMessage()==null?"خطا در ارسال فیش":e.getMessage()));}});
    }'''
    s=s[:m.start()]+new+s[m.end():]

p.write_text(s,encoding='utf-8')
print('final compile compatibility patch applied')

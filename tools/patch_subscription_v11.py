from pathlib import Path
import re

MAIN = Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
ADMIN = Path('app/src/main/java/com/sakhtemanyar/AdminActivity.java')
GATEWAY = 'https://okizneyesdwiundvadpe.supabase.co/functions/v1/api_gateway'

m = MAIN.read_text(encoding='utf-8')
m = m.replace('import android.content.*;\n', 'import android.content.*;\nimport android.net.Uri;\nimport android.util.Base64;\n')
m = m.replace('static final String API="https://okizneyesdwiundvadpe.supabase.co/functions/v1/api";', f'static final String API="{GATEWAY}";')
m = m.replace('LinearLayout root,content,drawer; String session="",role="";', 'LinearLayout root,content,drawer; String session="",role=""; String pendingRequestId="";')

start = m.index('    void plans(){')
end = m.index('    void residentHome(){', start)
new_plans = r'''    void plans(){frame("اشتراک سامانه",true);managerDrawer();section("طرح‌های اشتراک","اشتراک فقط بعد از تأیید مدیرکل فعال می‌شود");loadSubscriptionStatus();call("list_plans",j->{JSONArray a=j.optJSONArray("data");if(a==null||a.length()==0){empty("در حال حاضر طرح فعالی وجود ندارد");return;}for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x!=null)planCard(x);}});}
    void loadSubscriptionStatus(){call("subscription_status",j->{String st=j.optString("status",j.optString("subscription_status","-"));String end=j.optString("ends_at",j.optString("expires_at","-"));int c="active".equalsIgnoreCase(st)||"trial".equalsIgnoreCase(st)?green:red;item("وضعیت فعلی اشتراک",statusFa(st)+"  •  پایان: "+end);});}
    void planCard(JSONObject x){LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(16),dp(13),dp(16),dp(13));c.setBackground(grad(Color.WHITE,Color.rgb(248,251,252),20));TextView h=tv(x.optString("name","طرح"),18,navy);h.setTypeface(Typeface.DEFAULT,Typeface.BOLD);c.addView(h);long price=Math.round(x.optDouble("price_rial"));int days=x.optInt("duration_days");c.addView(tv(money(price)+"  •  "+days+" روز",13,teal));Button b=btn(price>0?"خرید و ثبت درخواست":"فعال‌سازی طرح رایگان",teal);c.addView(b,new LinearLayout.LayoutParams(-1,dp(47)));b.setOnClickListener(v->requestPlan(x));content.addView(c,new LinearLayout.LayoutParams(-1,dp(130)));content.addView(gap(9));}
    void requestPlan(JSONObject x){io.submit(()->{try{JSONObject q=new JSONObject().put("action","request_subscription").put("plan_id",x.optString("id"));JSONObject j=new JSONObject(post(q,session));if(j.has("error"))throw new Exception(j.getString("error"));pendingRequestId=j.optString("request_id",j.optString("id",""));long price=Math.round(x.optDouble("price_rial"));runOnUiThread(()->{if(price>0&& !pendingRequestId.isEmpty()) chooseReceipt();else toast("درخواست اشتراک ثبت شد و در انتظار تأیید مدیرکل است");});}catch(Exception e){runOnUiThread(()->toast(e.getMessage()==null?"خطا در ثبت درخواست":e.getMessage()));}});}
    void chooseReceipt(){new AlertDialog.Builder(this).setTitle("ارسال فیش پرداخت").setMessage("برای تکمیل درخواست اشتراک، تصویر یا PDF فیش بانکی را انتخاب کنید.").setNegativeButton("بعداً",null).setPositiveButton("انتخاب فیش",(d,w)->pickReceipt()).show();}
    void pickReceipt(){Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);i.setType("*/*");i.putExtra(Intent.EXTRA_MIME_TYPES,new String[]{"image/jpeg","image/png","image/webp","application/pdf"});startActivityForResult(i,701);}
    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){super.onActivityResult(requestCode,resultCode,data);if(requestCode!=701||resultCode!=RESULT_OK||data==null||data.getData()==null)return;Uri u=data.getData();io.submit(()->{try{java.io.InputStream in=getContentResolver().openInputStream(u);java.io.ByteArrayOutputStream out=new java.io.ByteArrayOutputStream();byte[] buf=new byte[8192];int n,total=0;while((n=in.read(buf))!=-1){total+=n;if(total>10*1024*1024)throw new Exception("حجم فیش بیشتر از ۱۰ مگابایت است");out.write(buf,0,n);}in.close();String mime=getContentResolver().getType(u);if(mime==null)mime="application/octet-stream";JSONObject q=new JSONObject().put("action","upload_receipt").put("request_id",pendingRequestId).put("mime_type",mime).put("file_base64",Base64.encodeToString(out.toByteArray(),Base64.NO_WRAP));JSONObject j=new JSONObject(post(q,session));if(j.has("error"))throw new Exception(j.getString("error"));runOnUiThread(()->toast("فیش با موفقیت ارسال شد؛ درخواست در انتظار تأیید مدیرکل است"));}catch(Exception e){runOnUiThread(()->toast(e.getMessage()==null?"خطا در ارسال فیش":e.getMessage()));}});}
'''
m = m[:start] + new_plans + m[end:]
MAIN.write_text(m, encoding='utf-8')

a = ADMIN.read_text(encoding='utf-8')
a = a.replace('static final String API="https://okizneyesdwiundvadpe.supabase.co/functions/v1/api";', f'static final String API="{GATEWAY}";')
# Replace request cards with receipt viewing support while keeping existing approval flow.
old = 'x.addView(tv("طرح: "+safe(q.optString("subscription_plans")),12,teal));x.addView(tv("وضعیت: "+safe(status),13,"pending".equals(status)?gold:green));if("pending".equals(status)){'
new = 'x.addView(tv("طرح: "+safe(q.optString("subscription_plans")),12,teal));x.addView(tv("مبلغ: "+money(q.optDouble("amount_rial")),12,dark));x.addView(tv("وضعیت: "+safe(status),13,"pending".equals(status)?gold:green));if(q.optString("receipt_path","").length()>0){Button rv=btn("مشاهده فیش پرداخت",teal);x.addView(rv,new LinearLayout.LayoutParams(-1,dp(46)));rv.setOnClickListener(v->viewReceipt(id));}if("pending".equals(status)){'
a = a.replace(old, new)
# Replace finance with platform finance.
fs=a.index('    void finance(){')
fe=a.index('    void audit(){', fs)
new_fin = r'''    void finance(){base("مالی سامانه");title("درآمد اشتراک‌ها");call("admin_finance",j->{JSONArray a=j.optJSONArray("transactions");if(a==null||a.length()==0){empty("تراکنش اشتراکی ثبت نشده است");return;}for(int i=0;i<a.length();i++){JSONObject q=a.optJSONObject(i);if(q==null)continue;String st=q.optString("status");int c="confirmed".equals(st)?green:"rejected".equals(st)?red:gold;item("اشتراک • "+money(q.optDouble("amount_rial")),"وضعیت: "+safe(st)+"  •  ساختمان: "+safe(q.optString("building_id"))+"  •  شروع: "+safe(q.optString("period_start"))+"  •  پایان: "+safe(q.optString("period_end")));}});}
    void viewReceipt(String id){io.submit(()->{try{JSONObject j=new JSONObject(post(new JSONObject().put("action","admin_get_receipt").put("request_id",id),session));String url=j.optString("signed_url","");if(url.isEmpty())throw new Exception("فیش در دسترس نیست");runOnUiThread(()->{try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(url)));}catch(Exception e){toast("امکان باز کردن فیش وجود ندارد");}});}catch(Exception e){runOnUiThread(()->toast(e.getMessage()));}});}
'''
a=a[:fs]+new_fin+a[fe:]
a=a.replace('import android.os.*;\n', 'import android.os.*;\nimport android.content.*;\nimport android.net.Uri;\n')
ADMIN.write_text(a, encoding='utf-8')
print('subscription v11 patch applied')

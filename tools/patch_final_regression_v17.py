from pathlib import Path
import re

MAIN=Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
ADMIN=Path('app/src/main/java/com/sakhtemanyar/AdminActivity.java')

def replace_method(src,name,new):
    marker='    void '+name+'('
    start=src.find(marker)
    if start<0:
        return src
    brace=src.find('{',start)
    depth=0
    end=-1
    for i in range(brace,len(src)):
        if src[i]=='{': depth+=1
        elif src[i]=='}':
            depth-=1
            if depth==0:
                end=i+1
                break
    if end<0:return src
    return src[:start]+new+src[end:]

s=MAIN.read_text(encoding='utf-8')
# Make every keyboard/dialog screen resize instead of drawing over content.
s=s.replace('void frame(String title,boolean inner){screenToken++;', 'void frame(String title,boolean inner){getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);screenToken++;',1)
if 'ScrollView dialogScroll(' not in s:
    anchor='    void drawerHead(String title,String sub,int accent){'
    helper='    View dialogScroll(View v){ScrollView sv=new ScrollView(this);sv.setFillViewport(true);sv.setPadding(0,dp(4),0,dp(4));sv.addView(v,new ScrollView.LayoutParams(-1,-2));return sv;}\n'
    s=s.replace(anchor,helper+anchor,1)
s=s.replace('.setView(l).setNegativeButton', '.setView(dialogScroll(l)).setNegativeButton')
s=s.replace('.setView(l).setNegativeButton', '.setView(dialogScroll(l)).setNegativeButton')

# Manager subscription page: always show active/trial/pending state and dates.
new_plans='''    void plans(){frame("اشتراک سامانه",true);managerDrawer();section("وضعیت اشتراک ساختمان","وضعیت، تاریخ شروع و تاریخ پایان باید همیشه برای مدیر قابل مشاهده باشد");call("subscription_status",j->{String st=j.optString("status",j.optString("subscription_status","expired"));String start=j.optString("starts_at","-");String end=j.optString("ends_at",j.optString("expires_at","-"));int c=("active".equalsIgnoreCase(st)||"trial".equalsIgnoreCase(st))?green:red;item("اشتراک فعلی",statusFa(st));item("شروع اشتراک",start);item("پایان اشتراک",end);});call("my_requests",j->{JSONArray r=j.optJSONArray("data");if(r!=null&&r.length()>0){section("درخواست‌های من","آخرین درخواست و وضعیت فیش پرداخت");for(int i=0;i<r.length();i++){JSONObject q=r.optJSONObject(i);if(q==null)continue;String st=q.optString("status","pending");String plan=q.optJSONObject("subscription_plans")!=null?q.optJSONObject("subscription_plans").optString("name","طرح"):"طرح";item(plan,statusFa(st)+"  •  "+(q.optString("receipt_path","").isEmpty()?"فیش ثبت نشده":"فیش ثبت شده"));}}});section("طرح‌های قابل خرید","خرید جدید پس از تأیید مدیرکل فعال می‌شود");call("list_plans",j->{JSONArray a=j.optJSONArray("data");if(a==null||a.length()==0){empty("در حال حاضر طرح فعالی وجود ندارد");return;}for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x!=null)planCard(x);}});}'''
s=replace_method(s,'plans',new_plans)

# Manager dashboard subscription summary.
old='void managerHome(){frame("داشبورد مدیر",false);managerDrawer();hero("داشبورد ساختمان","امروز: "+JalaliDate.now()+"  •  همه تاریخ‌ها شمسی نمایش داده می‌شوند",teal);loadDashboard();}'
new='void managerHome(){frame("داشبورد مدیر",false);managerDrawer();hero("داشبورد ساختمان","امروز: "+JalaliDate.now()+"  •  همه تاریخ‌ها شمسی نمایش داده می‌شوند",teal);call("subscription_status",j->{String st=j.optString("status","expired"),end=j.optString("ends_at",j.optString("expires_at","-"));stat("اشتراک ساختمان",statusFa(st)+"  •  تا "+end,("active".equalsIgnoreCase(st)||"trial".equalsIgnoreCase(st))?green:red);});loadDashboard();}'
s=s.replace(old,new,1)

# Master-admin buildings: show subscription end date explicitly.
new_admin_buildings='''    void adminBuildings(){frame("مدیریت ساختمان‌ها",true);adminDrawer();section("ساختمان‌های ثبت‌شده","وضعیت و تاریخ پایان اشتراک هر ساختمان");call("admin_dashboard",j->{JSONArray a=j.optJSONArray("buildings");if(a==null||a.length()==0){empty("ساختمانی وجود ندارد");return;}for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;String st=x.optString("subscription_status","expired"),end=x.optString("subscription_expires_at","-");item(x.optString("name","بدون نام"),"وضعیت: "+statusFa(st)+"  •  پایان اشتراک: "+end);}});}'''
s=replace_method(s,'adminBuildings',new_admin_buildings)

# Master-admin requests: receipt button, amount, building, status and approve/reject.
new_admin_plans='''    void adminPlans(){frame("مدیریت اشتراک‌ها",true);adminDrawer();section("طرح‌ها و درخواست‌ها","فیش پرداخت و وضعیت هر درخواست باید در همین صفحه قابل بررسی باشد");call("admin_dashboard",j->{JSONArray a=j.optJSONArray("plans");if(a!=null)for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x!=null)item(x.optString("name","طرح"),money(x.optDouble("price_rial"))+"  •  "+x.optInt("duration_days")+" روز");}JSONArray r=j.optJSONArray("requests");if(r==null||r.length()==0){empty("درخواستی وجود ندارد");return;}section("درخواست‌های اشتراک","جدیدترین درخواست‌ها");for(int i=0;i<r.length();i++){JSONObject q=r.optJSONObject(i);if(q==null)continue;subscriptionRequestCard(q);}});}'''
s=replace_method(s,'adminPlans',new_admin_plans)
if 'void subscriptionRequestCard(JSONObject q)' not in s:
    anchor='    void adminSettings(){'
    helper='''    void subscriptionRequestCard(JSONObject q){LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(15),dp(12),dp(15),dp(12));c.setBackground(box(white,19));String st=q.optString("status","pending");c.addView(tv("درخواست اشتراک",16,navy));c.addView(tv("ساختمان: "+q.optString("building_id","-"),12,muted));c.addView(tv("مبلغ: "+money(q.optDouble("amount_rial")),12,teal));c.addView(tv("وضعیت: "+statusFa(st),13,statusColor(st)));if(!q.optString("receipt_path","").isEmpty()){Button rv=btn("مشاهده فیش پرداخت",blue);c.addView(rv,new LinearLayout.LayoutParams(-1,dp(48)));rv.setOnClickListener(v->viewReceipt(q.optString("id")));}if("pending".equals(st)){LinearLayout row=new LinearLayout(this);Button ok=btn("تأیید و فعال‌سازی",green),no=btn("رد درخواست",red);row.addView(ok,new LinearLayout.LayoutParams(0,dp(48),1));row.addView(no,new LinearLayout.LayoutParams(0,dp(48),1));c.addView(row);ok.setOnClickListener(v->subscription(q.optString("id"),"approved"));no.setOnClickListener(v->subscription(q.optString("id"),"rejected"));}content.addView(c,new LinearLayout.LayoutParams(-1,-2));content.addView(gap(9));}\n    void viewReceipt(String id){io.submit(()->{try{JSONObject j=new JSONObject(post(new JSONObject().put("action","admin_get_receipt").put("request_id",id),session));String url=j.optString("signed_url",j.optString("url",""));if(url.isEmpty())throw new Exception("فیش در دسترس نیست");runOnUiThread(()->{try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(url)));}catch(Exception e){toast("امکان باز کردن فیش وجود ندارد");}});}catch(Exception e){runOnUiThread(()->toast(e.getMessage()==null?"خطا در دریافت فیش":e.getMessage()));}});}\n'''
    s=s.replace(anchor,helper+anchor,1)

MAIN.write_text(s,encoding='utf-8')

# AdminActivity: make its dialogs scrollable and card heights content-driven.
a=ADMIN.read_text(encoding='utf-8')
a=a.replace('import android.graphics.drawable.GradientDrawable;','import android.graphics.drawable.GradientDrawable;\nimport android.content.*;\nimport android.net.Uri;',1)
if 'View dialogScroll(' not in a:
    a=a.replace('    void base(String title){','    View dialogScroll(View v){ScrollView sv=new ScrollView(this);sv.setFillViewport(true);sv.setPadding(0,dp(4),0,dp(4));sv.addView(v,new ScrollView.LayoutParams(-1,-2));return sv;}\n    void base(String title){',1)
a=a.replace('.setView(l).setNegativeButton','.setView(dialogScroll(l)).setNegativeButton')
a=a.replace('.setView(l).setNegativeButton','.setView(dialogScroll(l)).setNegativeButton')
# Receipt visibility in the independent admin panel too.
if 'void viewReceipt(String id)' not in a:
    a=a.replace('    void subscription(String id,String status){', '    void viewReceipt(String id){io.submit(()->{try{JSONObject j=new JSONObject(post(new JSONObject().put("action","admin_get_receipt").put("request_id",id),session));String url=j.optString("signed_url",j.optString("url",""));if(url.isEmpty())throw new Exception("فیش در دسترس نیست");runOnUiThread(()->{try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(url)));}catch(Exception e){toast("امکان باز کردن فیش وجود ندارد");}});}catch(Exception e){runOnUiThread(()->toast(e.getMessage()==null?"خطا در دریافت فیش":e.getMessage()));}});}\n    void subscription(String id,String status){',1)
# Add receipt button to the request card before the pending action.
needle='x.addView(tv("وضعیت: "+safe(status),13,"pending".equals(status)?gold:green));if("pending".equals(status)){'
repl='x.addView(tv("وضعیت: "+safe(status),13,"pending".equals(status)?gold:green));if(q.optString("receipt_path","").length()>0){Button rv=btn("مشاهده فیش پرداخت",teal);x.addView(rv,new LinearLayout.LayoutParams(-1,dp(46)));rv.setOnClickListener(v->viewReceipt(id));}if("pending".equals(status)){'
a=a.replace(needle,repl,1)
ADMIN.write_text(a,encoding='utf-8')
print('Final regression/UI/subscription patch applied')

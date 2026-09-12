from pathlib import Path
import re

p = Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s = p.read_text(encoding='utf-8')

# The subscription patch can remove the finance helper while leaving calls to it.
# Use a broad signature check so formatting differences cannot skip the repair.
if 'void financeManagerItem(' not in s:
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
'''
    # Insert directly before the final class brace. This is independent of
    # the order/formatting of the other generated methods.
    pos = s.rfind('\n}')
    if pos < 0:
        raise SystemExit('MainActivity class closing brace not found')
    s = s[:pos] + method + s[pos:]

# Finance receipt picker. Keep it separate from the subscription picker (701).
if 'void pickImage()' not in s:
    method = r'''
    void pickImage(){
        Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);
        i.addCategory(Intent.CATEGORY_OPENABLE);
        i.setType("image/*");
        startActivityForResult(i,702);
    }
'''
    pos = s.rfind('\n}')
    if pos < 0:
        raise SystemExit('MainActivity class closing brace not found')
    s = s[:pos] + method + s[pos:]

# Do not replace the existing subscription callback here. The compile blocker
# in this build is the missing finance helper; the existing callback remains
# responsible for request 701 and later patches can add 702 handling safely.
p.write_text(s,encoding='utf-8')
print('final compile compatibility patch applied')

from pathlib import Path
p=Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s=p.read_text(encoding='utf-8')
today='new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).format(new java.util.Date())'

def once(old,new):
    global s
    if old in s and new not in s:
        s=s.replace(old,new,1)

once('final EditText t=input("عنوان شارژ / هزینه"),a=input("مبلغ به تومان"),d=input("توضیحات");','final EditText t=input("عنوان شارژ / هزینه"),a=input("مبلغ به تومان"),d=input("توضیحات"),date=input("تاریخ هزینه (YYYY-MM-DD)");date.setText('+today+');')
idx=s.find('final EditText t=input("عنوان شارژ / هزینه"),a=input("مبلغ به تومان"),d=input("توضیحات"),date=')
if idx>=0:
    pos=s.find('for(EditText e:new EditText[]{t,a,d})',idx)
    if pos>=0:s=s[:pos]+s[pos:].replace('for(EditText e:new EditText[]{t,a,d})','for(EditText e:new EditText[]{t,a,d,date})',1)
    pos=s.find('.put("description",d.getText().toString().trim()).put("unit_id",unitId.isEmpty()?JSONObject.NULL:unitId)',idx)
    if pos>=0:s=s[:pos]+s[pos:].replace('.put("description",d.getText().toString().trim()).put("unit_id",unitId.isEmpty()?JSONObject.NULL:unitId)', '.put("description",d.getText().toString().trim()).put("due_date",date.getText().toString().trim()).put("unit_id",unitId.isEmpty()?JSONObject.NULL:unitId)',1)

once('final EditText t=input("عنوان تعمیر"),a=input("مبلغ به تومان"),d=input("توضیحات");','final EditText t=input("عنوان تعمیر"),a=input("مبلغ به تومان"),d=input("توضیحات"),date=input("تاریخ تعمیر (YYYY-MM-DD)");date.setText('+today+');')
idx=s.find('final EditText t=input("عنوان تعمیر"),a=input("مبلغ به تومان"),d=input("توضیحات"),date=')
if idx>=0:
    pos=s.find('for(EditText e:new EditText[]{t,a,d})',idx)
    if pos>=0:s=s[:pos]+s[pos:].replace('for(EditText e:new EditText[]{t,a,d})','for(EditText e:new EditText[]{t,a,d,date})',1)
    pos=s.find('.put("description",d.getText().toString().trim()).put("receipt_url",receiptData)',idx)
    if pos>=0:s=s[:pos]+s[pos:].replace('.put("description",d.getText().toString().trim()).put("receipt_url",receiptData)', '.put("description",d.getText().toString().trim()).put("repair_date",date.getText().toString().trim()).put("receipt_url",receiptData)',1)

# Manager payment date
once('EditText a=input("مبلغ پرداخت به تومان"),n=input("توضیحات / شماره پیگیری");','EditText a=input("مبلغ پرداخت به تومان"),n=input("توضیحات / شماره پیگیری"),date=input("تاریخ پرداخت (YYYY-MM-DD)");date.setText('+today+');')
idx=s.find('EditText a=input("مبلغ پرداخت به تومان"),n=input("توضیحات / شماره پیگیری"),date=')
if idx>=0:
    pos=s.find('l.addView(n,new LinearLayout.LayoutParams(-1,dp(54)));',idx)
    if pos>=0:s=s[:pos]+s[pos:].replace('l.addView(n,new LinearLayout.LayoutParams(-1,dp(54)));','l.addView(n,new LinearLayout.LayoutParams(-1,dp(54)));l.addView(gap(8));l.addView(date,new LinearLayout.LayoutParams(-1,dp(54)));',1)
    pos=s.find('.put("note",n.getText().toString().trim()).put("receipt_url",receiptData)',idx)
    if pos>=0:s=s[:pos]+s[pos:].replace('.put("note",n.getText().toString().trim()).put("receipt_url",receiptData)', '.put("paid_at",date.getText().toString().trim()).put("note",n.getText().toString().trim()).put("receipt_url",receiptData)',1)

# Resident payment date, scoped to the residentPay method only.
start=s.find('void residentPay(){')
if start>=0:
    end=s.find('\n    void ',start+10)
    if end<0:end=s.find('\n}',start)
    if end<0:end=len(s)
    resident=s[start:end]
    if 'date=input("تاریخ پرداخت (YYYY-MM-DD)")' not in resident:
        resident=resident.replace('EditText a=input("مبلغ پرداخت به تومان"),n=input("توضیحات / شماره پیگیری");','EditText a=input("مبلغ پرداخت به تومان"),n=input("توضیحات / شماره پیگیری"),date=input("تاریخ پرداخت (YYYY-MM-DD)");date.setText('+today+');',1)
    if 'content.addView(date,new LinearLayout.LayoutParams(-1,dp(56)));' not in resident:
        resident=resident.replace('content.addView(n,new LinearLayout.LayoutParams(-1,dp(56)));','content.addView(n,new LinearLayout.LayoutParams(-1,dp(56)));content.addView(gap(9));content.addView(date,new LinearLayout.LayoutParams(-1,dp(56)));',1)
    if '.put("paid_at",date.getText().toString().trim())' not in resident:
        resident=resident.replace('.put("note",n.getText().toString().trim()).put("receipt_url",receiptData)', '.put("paid_at",date.getText().toString().trim()).put("note",n.getText().toString().trim()).put("receipt_url",receiptData)',1)
    s=s[:start]+resident+s[end:]

p.write_text(s,encoding='utf-8')
print('v4 dates applied safely')
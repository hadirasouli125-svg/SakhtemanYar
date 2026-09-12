from pathlib import Path
p=Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s=p.read_text(encoding='utf-8')
start=s.index('    void residentItemDetail(')
end=s.index('    void residentPaymentCard(',start)
fixed='''    void residentItemDetail(JSONObject x,boolean charge){StringBuilder q=new StringBuilder();q.append("مبلغ سهم شما: ").append(financeMoney(x.optJSONObject("my_allocation")!=null?x.optJSONObject("my_allocation").optDouble("allocated_amount_rial"):0));q.append(" | تاریخ: ").append(financeDate(x.optString(charge?"charge_date":"repair_date",x.optString("created_at"))));q.append(" | ").append(x.optString("description","بدون توضیحات"));new AlertDialog.Builder(this).setTitle(x.optString("title")).setMessage(q.toString()).setPositiveButton("بستن",null).show();}\n'''
s=s[:start]+fixed+s[end:]
p.write_text(s,encoding='utf-8')
print('finance detail escaping fixed')

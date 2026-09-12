from pathlib import Path
p=Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s=p.read_text(encoding='utf-8')
s=s.replace('ok.setOnClickListener(v->subscription(q.optString("id"),"approved"));no.setOnClickListener(v->subscription(q.optString("id"),"rejected"));', 'ok.setOnClickListener(v->callObj(new JSONObject().put("action","admin_subscription_action").put("request_id",q.optString("id")).put("status","approved"),z->adminHome()));no.setOnClickListener(v->callObj(new JSONObject().put("action","admin_subscription_action").put("request_id",q.optString("id")).put("status","rejected"),z->adminHome()));')
p.write_text(s,encoding='utf-8')
print('V17 compile fix applied')

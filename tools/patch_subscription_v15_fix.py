from pathlib import Path

p = Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s = p.read_text(encoding='utf-8')

# subscription_api returns the request object under "request".
# V14 was looking for a top-level request_id, leaving the receipt upload without an ID.
old = 'pendingRequestId=j.optString("request_id",j.optString("id",""));'
new = 'JSONObject rq=j.optJSONObject("request"); pendingRequestId=rq!=null?rq.optString("id",""):j.optString("request_id",j.optString("id",""));'
s = s.replace(old, new)

# Keep the receipt MIME picker compatible with Android providers.
s = s.replace('i.setType("*/*");i.putExtra(Intent.EXTRA_MIME_TYPES,new String[]{"image/jpeg","image/png","image/webp","application/pdf"});', 'i.setType("application/pdf");i.putExtra(Intent.EXTRA_MIME_TYPES,new String[]{"image/jpeg","image/png","image/webp","application/pdf"});')

p.write_text(s, encoding='utf-8')
print('subscription V15 fix applied')

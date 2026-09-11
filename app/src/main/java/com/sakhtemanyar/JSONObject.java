package com.sakhtemanyar;

public class JSONObject {
    private final org.json.JSONObject value;

    public JSONObject() { value = new org.json.JSONObject(); }
    public JSONObject(String json) throws org.json.JSONException { value = new org.json.JSONObject(json); }
    public JSONObject(org.json.JSONObject object) { value = object == null ? new org.json.JSONObject() : object; }

    public JSONObject put(String key, Object val) {
        try { value.put(key, val); } catch (org.json.JSONException ignored) {}
        return this;
    }
    public boolean has(String key) { return value.has(key); }
    public String getString(String key) throws org.json.JSONException { return value.getString(key); }
    public String optString(String key) { return value.optString(key); }
    public String optString(String key, String fallback) { return value.optString(key, fallback); }
    public int optInt(String key) { return value.optInt(key); }
    public double optDouble(String key) { return value.optDouble(key); }
    public boolean optBoolean(String key) { return value.optBoolean(key); }
    public JSONArray optJSONArray(String key) {
        org.json.JSONArray a = value.optJSONArray(key);
        return a == null ? null : new JSONArray(a);
    }
    public JSONObject optJSONObject(String key) {
        org.json.JSONObject a = value.optJSONObject(key);
        return a == null ? null : new JSONObject(a);
    }
    @Override public String toString() { return value.toString(); }
}

package com.sakhtemanyar;

public class JSONArray extends org.json.JSONArray {
    public JSONArray() { super(); }
    public JSONArray(String source) throws org.json.JSONException { super(source); }
    @Override public JSONObject optJSONObject(int index) { org.json.JSONObject o = super.optJSONObject(index); if (o == null) return null; if (o instanceof JSONObject) return (JSONObject)o; try { return new JSONObject(o.toString()); } catch (org.json.JSONException e) { return null; } }
}

package com.sakhtemanyar;

import java.util.List;

public class JSONArray extends org.json.JSONArray {
    public JSONArray() { super(); }
    public JSONArray(String source) throws org.json.JSONException { super(source); }
    public JSONArray(List<?> values) { super(); if(values!=null) for(Object v:values) put(v); }
    @Override public JSONObject optJSONObject(int index) { org.json.JSONObject o = super.optJSONObject(index); if (o == null) return null; if (o instanceof JSONObject) return (JSONObject)o; try { return new JSONObject(o.toString()); } catch (org.json.JSONException e) { return null; } }
}

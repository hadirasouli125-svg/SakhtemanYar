package com.sakhtemanyar;

public class JSONObject extends org.json.JSONObject {
    public JSONObject() { super(); }
    public JSONObject(String source) throws org.json.JSONException { super(source); }
    @Override public JSONObject put(String name, Object value) throws org.json.JSONException { super.put(name, value); return this; }
    @Override public JSONObject put(String name, boolean value) throws org.json.JSONException { super.put(name, value); return this; }
    @Override public JSONObject put(String name, double value) throws org.json.JSONException { super.put(name, value); return this; }
    @Override public JSONObject put(String name, int value) throws org.json.JSONException { super.put(name, value); return this; }
    @Override public JSONObject put(String name, long value) throws org.json.JSONException { super.put(name, value); return this; }
    @Override public JSONObject optJSONObject(String name) { org.json.JSONObject o = super.optJSONObject(name); return wrap(o); }
    private static JSONObject wrap(org.json.JSONObject o) { if (o == null) return null; if (o instanceof JSONObject) return (JSONObject)o; try { return new JSONObject(o.toString()); } catch (org.json.JSONException e) { return null; } }
}

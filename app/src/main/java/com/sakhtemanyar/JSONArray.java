package com.sakhtemanyar;

public class JSONArray {
    private final org.json.JSONArray value;
    public JSONArray(org.json.JSONArray value) { this.value = value; }
    public int length() { return value == null ? 0 : value.length(); }
    public JSONObject optJSONObject(int index) {
        if (value == null) return null;
        org.json.JSONObject child = value.optJSONObject(index);
        if (child == null) return null;
        try { return new JSONObject(child.toString()); }
        catch (org.json.JSONException e) { return null; }
    }
}

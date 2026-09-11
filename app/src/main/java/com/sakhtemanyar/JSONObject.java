package com.sakhtemanyar;

public class JSONObject extends org.json.JSONObject {
    public JSONObject() { super(); }
    public JSONObject(String source) throws org.json.JSONException { super(source); }
    @Override public JSONObject put(String name, Object value) { try { super.put(name, value); return this; } catch (org.json.JSONException e) { throw new IllegalArgumentException(e); } }
    @Override public JSONObject put(String name, boolean value) { try { super.put(name, value); return this; } catch (org.json.JSONException e) { throw new IllegalArgumentException(e); } }
    @Override public JSONObject put(String name, double value) { try { super.put(name, value); return this; } catch (org.json.JSONException e) { throw new IllegalArgumentException(e); } }
    @Override public JSONObject put(String name, int value) { try { super.put(name, value); return this; } catch (org.json.JSONException e) { throw new IllegalArgumentException(e); } }
    @Override public JSONObject put(String name, long value) { try { super.put(name, value); return this; } catch (org.json.JSONException e) { throw new IllegalArgumentException(e); } }
    @Override public JSONObject optJSONObject(String name) { org.json.JSONObject o = super.optJSONObject(name); return wrap(o); }
    @Override public JSONArray optJSONArray(String name) { org.json.JSONArray a = super.optJSONArray(name); return wrap(a); }
    private static JSONObject wrap(org.json.JSONObject o) { if (o == null) return null; if (o instanceof JSONObject) return (JSONObject)o; try { return new JSONObject(o.toString()); } catch (org.json.JSONException e) { return null; } }
    private static JSONArray wrap(org.json.JSONArray a) { if (a == null) return null; if (a instanceof JSONArray) return (JSONArray)a; try { return new JSONArray(a.toString()); } catch (org.json.JSONException e) { return null; } }
}

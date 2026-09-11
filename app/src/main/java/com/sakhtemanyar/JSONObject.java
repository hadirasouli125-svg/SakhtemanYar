package com.sakhtemanyar;

import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class JSONObject {
    private final org.json.JSONObject value;
    private static final Pattern ISO_DATE = Pattern.compile("^(\\d{4})-(\\d{2})-(\\d{2})(?:[T ](\\d{2}):(\\d{2})(?::(\\d{2}))?.*)?$");

    public JSONObject() { value = new org.json.JSONObject(); }
    public JSONObject(String json) throws org.json.JSONException { value = new org.json.JSONObject(json); }
    public JSONObject(org.json.JSONObject object) { value = object == null ? new org.json.JSONObject() : object; }

    public JSONObject put(String key, Object val) {
        try { value.put(key, val); } catch (org.json.JSONException ignored) {}
        return this;
    }
    public boolean has(String key) { return value.has(key); }
    public String getString(String key) throws org.json.JSONException { return value.getString(key); }
    public String optString(String key) { return displayDate(value.optString(key)); }
    public String optString(String key, String fallback) { return displayDate(value.optString(key, fallback)); }
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

    private static String displayDate(String s) {
        if (s == null || s.length() < 10) return s;
        Matcher m = ISO_DATE.matcher(s);
        if (!m.matches()) return s;
        try {
            int gy = Integer.parseInt(m.group(1));
            int gm = Integer.parseInt(m.group(2));
            int gd = Integer.parseInt(m.group(3));
            int[] j = gregorianToJalali(gy, gm, gd);
            String out = String.format(java.util.Locale.US, "%04d/%02d/%02d", j[0], j[1], j[2]);
            if (m.group(4) != null) out += " " + m.group(4) + ":" + m.group(5) + (m.group(6) == null ? "" : ":" + m.group(6));
            return out;
        } catch (Exception ignored) { return s; }
    }

    private static int[] gregorianToJalali(int gy, int gm, int gd) {
        int[] gdm = {0,31,28,31,30,31,30,31,31,30,31,30,31};
        int gy2 = gy - 1600, gm2 = gm - 1, gd2 = gd - 1;
        int gdn = 365 * gy2 + (gy2 + 3) / 4 - (gy2 + 99) / 100 + (gy2 + 399) / 400;
        for (int i = 0; i < gm2; i++) gdn += gdm[i + 1];
        if (gm2 > 1 && ((gy % 4 == 0 && gy % 100 != 0) || gy % 400 == 0)) gdn++;
        gdn += gd2;
        int jdn = gdn - 79;
        int jnp = jdn / 12053;
        int jdn2 = jdn % 12053;
        int jy = 979 + 33 * jnp + 4 * (jdn2 / 1461);
        jdn2 %= 1461;
        if (jdn2 >= 366) { jy += (jdn2 - 1) / 365; jdn2 = (jdn2 - 1) % 365; }
        int jm = jdn2 < 186 ? 1 + jdn2 / 31 : 7 + (jdn2 - 186) / 30;
        int jd = 1 + (jdn2 < 186 ? jdn2 % 31 : (jdn2 - 186) % 30);
        return new int[]{jy, jm, jd};
    }
}

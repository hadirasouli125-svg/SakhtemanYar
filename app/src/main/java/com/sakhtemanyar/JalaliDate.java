package com.sakhtemanyar;

import java.util.Calendar;
import java.util.Locale;

public final class JalaliDate {
    private JalaliDate() {}

    public static String now() {
        return format(Calendar.getInstance());
    }

    public static String format(Calendar g) {
        int gy = g.get(Calendar.YEAR);
        int gm = g.get(Calendar.MONTH) + 1;
        int gd = g.get(Calendar.DAY_OF_MONTH);
        int[] j = toJalali(gy, gm, gd);
        return String.format(Locale.US, "%04d/%02d/%02d", j[0], j[1], j[2]);
    }

    public static String format(String iso) {
        if (iso == null || iso.length() < 10) return iso == null ? "" : iso;
        try {
            int y = Integer.parseInt(iso.substring(0, 4));
            int m = Integer.parseInt(iso.substring(5, 7));
            int d = Integer.parseInt(iso.substring(8, 10));
            int[] j = toJalali(y, m, d);
            return String.format(Locale.US, "%04d/%02d/%02d", j[0], j[1], j[2]);
        } catch (Exception e) {
            return iso;
        }
    }

    private static int[] toJalali(int gy, int gm, int gd) {
        int[] gdm = {0,31,28,31,30,31,30,31,31,30,31,30,31};
        int gy2 = gy - (gm > 2 ? 0 : 1);
        int days = 355666 + 365 * gy2 + (gy2 + 3) / 4 - (gy2 + 99) / 100 + (gy2 + 399) / 400 + gd;
        for (int i = 1; i < gm; i++) days += gdm[i];
        int jy = -1595 + 33 * (days / 12053);
        days %= 12053;
        jy += 4 * (days / 1461);
        days %= 1461;
        if (days > 365) {
            jy += (days - 1) / 365;
            days = (days - 1) % 365;
        }
        int jm = days < 186 ? 1 + days / 31 : 7 + (days - 186) / 30;
        int jd = 1 + (days < 186 ? days % 31 : (days - 186) % 30);
        return new int[]{jy, jm, jd};
    }
}

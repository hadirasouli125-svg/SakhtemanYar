package com.sakhtemanyar;

import java.util.Calendar;
import java.util.Locale;

public final class JalaliDate {
    private JalaliDate() {}
    public static String now(){return format(Calendar.getInstance());}
    public static String format(Calendar g){int gy=g.get(Calendar.YEAR),gm=g.get(Calendar.MONTH)+1,gd=g.get(Calendar.DAY_OF_MONTH);int[] j=toJalali(gy,gm,gd);return String.format(Locale.US,"%04d/%02d/%02d",j[0],j[1],j[2]);}
    public static String format(String iso){if(iso==null||iso.length()<10)return iso==null?"":iso;try{int y=Integer.parseInt(iso.substring(0,4)),m=Integer.parseInt(iso.substring(5,7)),d=Integer.parseInt(iso.substring(8,10));int[] j=toJalali(y,m,d);return String.format(Locale.US,"%04d/%02d/%02d",j[0],j[1],j[2]);}catch(Exception e){return iso;}}
    public static String toGregorianIso(String jalali){try{String v=jalali.trim().replace('-','/');String[] p=v.split("/");if(p.length!=3)return "";int jy=Integer.parseInt(p[0]),jm=Integer.parseInt(p[1]),jd=Integer.parseInt(p[2]);int[] g=toGregorian(jy,jm,jd);return String.format(Locale.US,"%04d-%02d-%02d",g[0],g[1],g[2]);}catch(Exception e){return "";}}
    private static int[] toGregorian(int jy,int jm,int jd){int jy2=jy-979;int days=365*jy2+(jy2/33)*8+((jy2%33+3)/4);for(int i=1;i<jm;i++)days+=i<=6?31:30;days+=jd-1;int gy=1600+400*(days/146097);days%=146097;boolean leap=true;if(days>=36525){days--;gy+=100*(days/36524);days%=36524;if(days>=365)days++;}gy+=4*(days/1461);days%=1461;if(days>=366){leap=false;days--;gy+=days/365;days%=365;}int[] md={31,28+(leap?1:0),31,30,31,30,31,31,30,31,30,31};int gm=1;while(gm<=12&&days>=md[gm-1]){days-=md[gm-1];gm++;}return new int[]{gy,gm,days+1};}
    private static int[] toJalali(int gy,int gm,int gd){int[] gdm={0,31,28,31,30,31,30,31,31,30,31,30,31};int gy2=gy-(gm>2?0:1);int days=355666+365*gy2+(gy2+3)/4-(gy2+99)/100+(gy2+399)/400+gd;for(int i=1;i<gm;i++)days+=gdm[i];int jy=-1595+33*(days/12053);days%=12053;jy+=4*(days/1461);days%=1461;if(days>365){jy+=(days-1)/365;days=(days-1)%365;}int jm=days<186?1+days/31:7+(days-186)/30;int jd=1+(days<186?days%31:(days-186)%30);return new int[]{jy,jm,jd};}
}

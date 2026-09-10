package ir.sakhtemanyar.app;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.graphics.Typeface;
import android.view.Gravity;
import android.view.View;
import android.widget.*;

public class MainActivity extends Activity {
    LinearLayout root;
    int teal = Color.rgb(15,118,110);
    int ink = Color.rgb(15,23,42);

    @Override public void onCreate(Bundle b) {
        super.onCreate(b);
        showLogin();
    }

    TextView text(String s, int size, boolean bold) {
        TextView t = new TextView(this); t.setText(s); t.setTextSize(size); t.setTextColor(ink);
        t.setGravity(Gravity.RIGHT); t.setTypeface(Typeface.DEFAULT, bold ? Typeface.BOLD : Typeface.NORMAL);
        t.setPadding(0, 8, 0, 8); return t;
    }
    EditText input(String hint, boolean password) {
        EditText e = new EditText(this); e.setHint(hint); e.setTextSize(16); e.setGravity(Gravity.RIGHT);
        e.setSingleLine(true); e.setPadding(24, 12, 24, 12);
        if(password) e.setInputType(0x81); return e;
    }
    Button button(String label) {
        Button b = new Button(this); b.setText(label); b.setTextSize(15); b.setTextColor(Color.WHITE); b.setAllCaps(false);
        b.setBackgroundColor(teal); return b;
    }
    void base(String title, String subtitle) {
        root = new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL); root.setGravity(Gravity.TOP|Gravity.RIGHT);
        root.setPadding(28, 42, 28, 28); root.setBackgroundColor(Color.rgb(248,250,252)); root.setLayoutDirection(View.LAYOUT_DIRECTION_RTL);
        TextView h=text(title,30,true); h.setTextColor(teal); root.addView(h);
        root.addView(text(subtitle,15,false)); setContentView(root);
    }
    void showLogin() {
        base("ساختمان‌یار", "مدیریت ساده، شفاف و امن ساختمان");
        EditText user=input("نام کاربری",false), pass=input("رمز عبور",true); root.addView(user); root.addView(pass);
        Button login=button("ورود به سامانه"); LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,60); lp.setMargins(0,24,0,12); root.addView(login,lp);
        Button register=button("ثبت مدیر اولیه"); root.addView(register);
        root.addView(text("نسخه اولیه: تأیید ایمیلی فعال نیست",13,false));
        login.setOnClickListener(v -> showDashboard("مدیر ساختمان"));
        register.setOnClickListener(v -> showRegister());
    }
    void showRegister() {
        base("ثبت مدیر اولیه", "ساختمان خود را ایجاد کنید و دوره آزمایشی را شروع کنید");
        EditText u=input("نام کاربری",false), p=input("رمز عبور",true), p2=input("تکرار رمز عبور",true);
        root.addView(u); root.addView(p); root.addView(p2);
        Button create=button("ثبت مدیر و شروع دوره آزمایشی"); LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,64); lp.setMargins(0,24,0,12); root.addView(create,lp);
        Button back=button("بازگشت به ورود"); root.addView(back);
        create.setOnClickListener(v -> { if(u.length()==0 || p.length()<4 || !p.getText().toString().equals(p2.getText().toString())) { Toast.makeText(this,"اطلاعات ورود را بررسی کنید",Toast.LENGTH_SHORT).show(); return; } showDashboard("مدیر ساختمان"); });
        back.setOnClickListener(v -> showLogin());
    }
    void showDashboard(String role) {
        base("داشبورد مدیر", "دوره آزمایشی فعال است • تنظیمات اشتراک از پنل مدیرکل کنترل می‌شود");
        String[] cards={"شارژ ماه جاری\n۰ تومان","بدهی واحدها\n۰ تومان","هزینه تعمیرات\n۰ تومان","موجودی صندوق\n۰ تومان"};
        for(String c:cards){ TextView tv=text(c,19,true); tv.setBackgroundColor(Color.WHITE); tv.setPadding(24,22,24,22); LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,82); p.setMargins(0,8,0,8); root.addView(tv,p); }
        Button units=button("مدیریت واحدها و ساکنان"); root.addView(units); Button costs=button("شارژ، هزینه‌ها و تعمیرات"); root.addView(costs); Button reports=button("گزارش مالی و گردش حساب"); root.addView(reports);
    }
}

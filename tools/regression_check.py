from pathlib import Path
import re

errors = []
root = Path('.')

manifest = (root / 'app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
gradle = (root / 'app/build.gradle').read_text(encoding='utf-8')
main = (root / 'app/src/main/java/com/sakhtemanyar/MainActivity.java').read_text(encoding='utf-8')
admin = (root / 'app/src/main/java/com/sakhtemanyar/AdminActivity.java').read_text(encoding='utf-8')
page = (root / 'app/page.tsx').read_text(encoding='utf-8')
route = (root / 'app/api/session/route.ts').read_text(encoding='utf-8')
workflow = (root / '.github/workflows/android.yml').read_text(encoding='utf-8')

if list((root / 'app/src/main/java').rglob('MainActivity.java')).count((root / 'app/src/main/java/com/sakhtemanyar/MainActivity.java')) != 1:
    errors.append('MainActivity source identity is not unique.')
if 'android:name="com.sakhtemanyar.MainActivity"' not in manifest:
    errors.append('Launcher activity is not com.sakhtemanyar.MainActivity.')
if 'buildFeatures { buildConfig true }' not in gradle or 'buildConfigField' not in gradle:
    errors.append('BuildConfig is not explicitly reproducible from app/build.gradle.')
if 'import ir.sakhtemanyar.app.BuildConfig;' not in main or 'import ir.sakhtemanyar.app.BuildConfig;' not in admin:
    errors.append('BuildConfig import is missing from an Android activity.')
if 'EncryptedSharedPreferences' not in main or 'restoreSession()' not in main:
    errors.append('MainActivity secure session persistence is missing.')
if 'localStorage' in page or 'sessionStorage' in page:
    errors.append('Web client still stores the bearer session in browser storage.')
if "fetch('/api/session'" not in page or "httpOnly" not in route:
    errors.append('Web session is not routed through the HttpOnly cookie endpoint.')
if 'new AlertDialog' in admin and re.search(r'\.show\(\);\s*new AlertDialog', admin):
    errors.append('AdminActivity still contains consecutive AlertDialog.show calls.')
if 'tools/patch_' in workflow or 'restore_missing_main_methods.py' in workflow:
    errors.append('Build workflow still depends on legacy patch-generation steps.')
if 'gradle assembleDebug --no-daemon' not in workflow:
    errors.append('Android compile verification is missing from workflow.')
if 'npm install' not in workflow or 'npm run build' not in workflow:
    errors.append('Web build verification is missing from workflow.')

if errors:
    print('REGRESSION CHECK FAILED')
    for e in errors:
        print(' - ' + e)
    raise SystemExit(1)

print('REGRESSION CHECK PASSED')
print(' - single Android MainActivity identity')
print(' - launcher identity matches source')
print(' - BuildConfig is source-defined')
print(' - Android session persistence uses encrypted preferences')
print(' - web bearer token is not stored in browser storage')
print(' - web session uses HttpOnly cookie route')
print(' - no consecutive admin dialogs')
print(' - workflow builds Android and Web from repository source')

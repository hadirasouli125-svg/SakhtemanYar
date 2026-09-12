from pathlib import Path
import re

p = Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')
s = p.read_text(encoding='utf-8')

# Remove any pre-existing receipt picker callback injected by an earlier patch.
pattern = r'\n\s*@Override\s+protected\s+void\s+onActivityResult\s*\(\s*int\s+requestCode\s*,\s*int\s+resultCode\s*,\s*Intent\s+data\s*\)\s*\{.*?\n\s*\}\s*\n(?=\s*(?:void|@Override|private|protected|public|\}))'
s, n = re.subn(pattern, '\n', s, count=1, flags=re.S)

# If the previous callback is formatted on one line and not caught above, remove it by method signature + balanced braces.
if n == 0:
    sig = 'protected void onActivityResult(int requestCode,int resultCode,Intent data)'
    pos = s.find(sig)
    if pos >= 0:
        start = s.rfind('@Override', 0, pos)
        brace = s.find('{', pos)
        if start >= 0 and brace >= 0:
            depth = 0
            end = -1
            for i in range(brace, len(s)):
                if s[i] == '{': depth += 1
                elif s[i] == '}':
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            if end > 0:
                s = s[:start] + s[end:]

p.write_text(s, encoding='utf-8')
print('duplicate onActivityResult callback removed')

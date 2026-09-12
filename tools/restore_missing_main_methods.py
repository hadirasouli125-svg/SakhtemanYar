from pathlib import Path
import re
import subprocess

TARGET = Path('app/src/main/java/com/sakhtemanyar/MainActivity.java')


def top_level_methods(src):
    methods = {}
    # Match method declarations, then use balanced braces to capture the full method.
    pat = re.compile(r'(?m)^\s*(?:@Override\s*)?(?:public|protected|private|static|final|synchronized|native|abstract|strictfp|\s)+[\w<>\[\], ?]+\s+(\w+)\s*\([^;{}]*\)\s*\{')
    for m in pat.finditer(src):
        name = m.group(1)
        brace = src.find('{', m.start(), m.end())
        depth = 0
        end = None
        for i in range(brace, len(src)):
            ch = src[i]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end:
            methods.setdefault(name, src[m.start():end])
    return methods


def current_method_names(src):
    return set(top_level_methods(src).keys())

original = subprocess.check_output(
    ['git', 'show', 'HEAD:app/src/main/java/com/sakhtemanyar/MainActivity.java'],
    text=True,
    encoding='utf-8'
)
current = TARGET.read_text(encoding='utf-8')
orig_methods = top_level_methods(original)
cur_names = current_method_names(current)

# Only restore methods that are completely missing. Existing patched methods win.
missing = [name for name in orig_methods if name not in cur_names and name not in {'plans'}]
if missing:
    insert_at = current.rfind('\n}')
    if insert_at < 0:
        raise SystemExit('Could not locate MainActivity class closing brace')
    blocks = '\n\n' + '\n\n'.join(orig_methods[n].rstrip() for n in missing) + '\n'
    current = current[:insert_at] + blocks + current[insert_at:]
    TARGET.write_text(current, encoding='utf-8')

print('MainActivity restore check: missing methods restored =', len(missing))
if missing:
    print('Restored:', ', '.join(missing))
else:
    print('No missing original methods detected')

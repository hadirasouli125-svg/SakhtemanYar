from pathlib import Path
import re

FILES = [
    Path('app/src/main/java/com/sakhtemanyar/MainActivity.java'),
    Path('app/src/main/java/com/sakhtemanyar/AdminActivity.java'),
]

# Make vertical content containers/cards size themselves from their children.
# Keep explicit sizes for top bars, buttons and drawer rows; target content/card additions only.
for p in FILES:
    s = p.read_text(encoding='utf-8')

    # Any view added directly to the scrolling content/body with a fixed vertical size
    # is allowed to measure itself. This removes the source of text clipping/overlap.
    s = re.sub(
        r'(content\.addView\([^;\n]*?new LinearLayout\.LayoutParams\(-1,)dp\(\d+\)\)',
        r'\1-2)', s
    )
    s = re.sub(
        r'(body\.addView\([^;\n]*?new LinearLayout\.LayoutParams\(-1,)dp\(\d+\)\)',
        r'\1-2)', s
    )

    # Card internals: text blocks must grow for long Persian text instead of overlapping.
    s = re.sub(
        r'new LinearLayout\.LayoutParams\(0,dp\((?:58|64|70|72|76|78|84|92|101|108|112|125|130|135|142|145|165)\),1\)',
        'new LinearLayout.LayoutParams(0,-2,1)', s
    )

    # Common card/action rows where the whole row was fixed-height.
    s = re.sub(
        r'(content\.addView\([^;\n]*?new LinearLayout\.LayoutParams\(-1,)dp\((?:70|74|78|84|92|108|112|125|130|135|142|145|165)\)\)',
        r'\1-2)', s
    )
    s = re.sub(
        r'(body\.addView\([^;\n]*?new LinearLayout\.LayoutParams\(-1,)dp\((?:74|78|92|135|142|165)\)\)',
        r'\1-2)', s
    )

    p.write_text(s, encoding='utf-8')

print('Responsive content/card sizing patch applied to manager, resident and master-admin panels.')

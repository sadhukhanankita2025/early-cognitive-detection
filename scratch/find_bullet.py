from pathlib import Path
text = Path('app.py').read_text(encoding='utf-8')
for i, line in enumerate(text.splitlines(), 1):
    if '•' in line:
        print(i, repr(line))

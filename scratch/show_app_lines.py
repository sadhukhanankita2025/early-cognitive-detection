from pathlib import Path
lines = Path('app.py').read_text(encoding='utf-8').splitlines()
for i in range(560, 586):
    print(f'{i+1}: {lines[i]}')

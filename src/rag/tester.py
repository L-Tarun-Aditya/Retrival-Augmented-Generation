from pathlib import Path
p=Path('.')
newpath = p/'src'/'rag'
print(newpath)
resolved_path = p.resolve()
print(resolved_path)
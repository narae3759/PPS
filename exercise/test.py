from pathlib import Path 

p = Path(__file__)
print(f"현재 위치: {p}")
print(f"부모 위치: {p.parent}")
print(f"다른 폴더 위치: {p.parent / 'pages'}")
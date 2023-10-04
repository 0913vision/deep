with open('ip.txt', 'r') as f:
    lines = f.readlines()

with open('ip.txt', 'w') as f:
    for idx, line in enumerate(lines, 1):
        line = line.strip()  # 라인의 앞뒤 공백 제거
        f.write(f"{line} worker{idx}\n")

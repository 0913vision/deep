def normalize_ratio(a, b, c):
    """비율을 총합이 1이 되도록 조정하는 함수"""
    total = a + b + c
    return a / total, b / total, c / total

def compute_average_ratio(samples):
    """주어진 표본들에 대해 평균 비율을 계산하는 함수"""
    normalized_samples = [normalize_ratio(a, b, c) for a, b, c in samples]

    avg_a = sum(a for a, _, _ in normalized_samples) / len(samples)
    avg_b = sum(b for _, b, _ in normalized_samples) / len(samples)
    avg_c = sum(c for _, _, c in normalized_samples) / len(samples)

    return avg_a, avg_b, avg_c

# 표본
samples = [
    (155, 23, 11),
    (532, 146, 90),
    (787, 293, 158)
]

avg_a, avg_b, avg_c = compute_average_ratio(samples)
print(f"평균 비율: {1/avg_a:.4f}:{1/avg_b:.4}:{1/avg_c:.4}")

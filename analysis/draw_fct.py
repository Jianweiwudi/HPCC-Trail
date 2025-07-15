import numpy as np
import matplotlib.pyplot as plt

file_path = r"fct_result.txt"

# 读取算法名称
with open(file_path, "r") as f:
    lines = f.readlines()
algo_names = lines[0].strip().split()
data_lines = lines[1:]

sizes = []
results = []  # 每行为[[avg1, mid1, pct1], [avg2, mid2, pct2], ...]

for line in data_lines:
    parts = line.strip().split()
    if len(parts) < 1 + 3 * len(algo_names):
        continue
    # 跳过空行或无效行
    try:
        size = int(parts[0])
    except ValueError:
        continue
    if size < 1000000:
        sizes.append(size)
        algos = []
        idx = 1
        for _ in algo_names:
            # 跳过多余的空字段
            while idx < len(parts) and parts[idx] == '':
                idx += 1
            if idx + 2 < len(parts):
                algos.append([float(parts[idx]), float(parts[idx+1]), float(parts[idx+2])])
                idx += 3
        results.append(algos)

sizes = np.array(sizes)
results = np.array(results)  # shape: (N, algo_num, 3)
metrics = ['avg fct slowdown', '95-pct fct slowdown', '99-pct fct slowdown']

for metric_idx, metric in enumerate(metrics):
    plt.figure()
    for algo_idx, algo in enumerate(algo_names):
        plt.plot(sizes, results[:, algo_idx, metric_idx], label=algo)
    plt.xlabel('Flow Size')
    plt.ylabel(metric)
    plt.title(f'{metric}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{metric.replace(" ", "_")}_10G_NPFC.png')
    # plt.show()

print("绘图完成，图片已保存。")
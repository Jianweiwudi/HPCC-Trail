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

# ... 保持前面数据读取部分不变 ...

# ... 保持前面数据读取部分不变 ...

sizes = np.array(sizes)
results = np.array(results)  # shape: (N, algo_num, 3)
metrics = ['avg', '95-pct', '99-pct']

plt.figure(figsize=(10, 6))
bar_width = 0.8 / len(algo_names)
x = np.arange(len(metrics))

# 计算每个算法在所有流量下各指标的均值
means = results.mean(axis=0)  # shape: (algo_num, 3)

for i, algo in enumerate(algo_names):
    plt.bar(x + i * bar_width, means[i], width=bar_width, label=algo)

plt.xlabel('FCT slowdown metric')
plt.ylabel('FCT slowdown')
plt.title('FCT slowdown (avg, 95-pct, 99-pct) for each Algorithm')
plt.xticks(x + bar_width * (len(algo_names) - 1) / 2, metrics)
plt.legend()
plt.tight_layout()
plt.savefig('FCT_slowdown_metrics_hist_10G_NPFC.png')
# plt.show()

print("绘图完成，图片已保存。")
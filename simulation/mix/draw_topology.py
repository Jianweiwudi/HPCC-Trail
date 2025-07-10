import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def read_fat_tree_file(filename):
    nodes = []
    switches = []
    edges = []
    with open(filename, 'r') as f:
        # 读取第一行
        line = f.readline().split()
        total_nodes = int(line[0])
        switch_nodes = int(line[1])
        total_links = int(line[2])
        
        # 读取交换机节点列表
        switches = list(map(int, f.readline().split()))
        
        # 读取所有链路，跳过空行
        for _ in range(total_links):
            line = f.readline().strip()
            if not line:  # 跳过空行
                continue
            parts = line.split()
            if len(parts) < 2:  # 确保有足够的元素
                continue
            src = int(parts[0])
            dst = int(parts[1])
            edges.append((src, dst))
    
    # 创建节点列表
    nodes = list(range(total_nodes))
    return nodes, switches, edges

def assign_levels(nodes, switches, edges):
    # 手动分配层级（基于胖树结构知识）
    level = {}
    
    # 主机节点（0-63）在第0层
    for i in range(64):
        level[i] = 0
    
    # 边缘交换机（64-91）在第1层
    for i in range(64, 92):
        level[i] = 1
    
    # 汇聚交换机（72-83, 92-99）在第2层
    for i in range(72, 84):
        level[i] = 2
    for i in range(92, 100):
        level[i] = 2
    
    # 核心交换机（80-83, 100-103）在第3层
    for i in range(80, 84):
        level[i] = 3
    for i in range(100, 104):
        level[i] = 3
    
    # 顶级核心交换机（104-105）在第4层
    level[104] = 4
    level[105] = 4
    
    return level

def plot_fat_tree(nodes, switches, edges, level_dict):
    G = nx.Graph()
    
    # 添加所有节点
    G.add_nodes_from(nodes)
    
    # 添加所有边
    G.add_edges_from(edges)
    
    # 为节点分配位置（按层级）
    pos = {}
    level_groups = {}
    
    # 按层级分组节点
    for node, lvl in level_dict.items():
        if lvl not in level_groups:
            level_groups[lvl] = []
        level_groups[lvl].append(node)
    
    # 为每个层级分配位置
    max_nodes = max(len(level_groups[lvl]) for lvl in level_groups)
    for lvl, nodes_in_level in level_groups.items():
        nodes_in_level.sort()
        num_nodes = len(nodes_in_level)
        y = lvl * 2  # 层级决定Y坐标
        
        # 在X轴上均匀分布节点
        for i, node in enumerate(nodes_in_level):
            # 居中布局，考虑最大节点数保持比例
            x = (i - num_nodes/2) * (max_nodes / max(1, num_nodes))
            pos[node] = (x, y)
    
    # 绘制节点
    host_nodes = [n for n in nodes if n not in switches]
    switch_nodes = switches
    
    plt.figure(figsize=(18, 10))
    
    # 绘制主机节点（小圆点）
    nx.draw_networkx_nodes(G, pos, nodelist=host_nodes, 
                           node_color='skyblue', node_size=50, 
                           alpha=0.7, label='Hosts')
    
    # 绘制交换机节点（大方块）
    nx.draw_networkx_nodes(G, pos, nodelist=switch_nodes, 
                           node_color='lightgreen', node_size=200, 
                           node_shape='s', alpha=0.8, label='Switches')
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, edgelist=edges, 
                           width=0.8, alpha=0.3, edge_color='gray')
    
    # 添加标签（只显示交换机）
    switch_labels = {}
    for node in switches:
        # 只标记关键交换机（避免过于拥挤）
        if level_dict[node] >= 2 or node in [64, 84, 104, 105]:
            switch_labels[node] = node
    
    nx.draw_networkx_labels(G, pos, labels=switch_labels, 
                            font_size=8, font_weight='bold')
    
    # 添加图例和标题
    plt.legend(loc='upper right', scatterpoints=1)
    plt.title("Fat Tree Topology Visualization", fontsize=14)
    
    # 添加层级标记
    for lvl in sorted(level_groups.keys()):
        y_pos = lvl * 2
        plt.text(-max_nodes/2 - 1, y_pos, f"Layer {lvl}", 
                fontsize=10, ha='right', va='center')
    
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# 主程序
if __name__ == "__main__":
    filename = "fat_tree_DCI.txt"
    try:
        nodes, switches, edges = read_fat_tree_file(filename)
        level_dict = assign_levels(nodes, switches, edges)
        
        print(f"Total nodes: {len(nodes)}")
        print(f"Switches: {len(switches)}")
        print(f"Edges: {len(edges)}")
        
        # 打印层级分布
        from collections import defaultdict
        level_dist = defaultdict(list)
        for node, lvl in level_dict.items():
            level_dist[lvl].append(node)
        
        for lvl in sorted(level_dist.keys()):
            print(f"Layer {lvl}: {len(level_dist[lvl])} nodes")
        
        plot_fat_tree(nodes, switches, edges, level_dict)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
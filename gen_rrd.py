import rerun as rr
import numpy as np
import math

# 1. 初始化
rr.init("retail_demo_offline", spawn=False)

print("💾 开始生成数据... (预计生成 500 帧)")

# 2. 生成数据
for i in range(500):
    # 时间轴：每帧 0.01s
    time_sim = i * 0.01
    
    # 【关键修正】指定时间轴名字为 "step_count"
    rr.set_time(timeline="step_count", sequence=i)
    
    # 模拟数据 A: 正弦波曲线
    sin_val = math.sin(time_sim * 5)
    # 注意：新版要求标量用 Scalars 列表包装
    rr.log("sensors/motor_curve", rr.Scalars([sin_val]))
    
    # 模拟数据 B: 随机噪点图 (模拟相机)
    # 224x224 RGB
    random_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    rr.log("sensors/camera_image", rr.Image(random_img))
    
    # 打印进度条
    if i % 50 == 0:
        print(f"   进度: {i}/500...", end="\r")

print("\n✅ 数据生成完毕！")

# 3. 保存文件
output_file = "retail_demo.rrd"
rr.save(output_file)
print(f"💾 文件已保存至: {output_file}")
print("   (请在 Mac 终端使用 'docker cp' 命令将其拷出查看)")
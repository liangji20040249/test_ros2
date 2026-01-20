import h5py
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# 1. 读取脏数据
filename = "raw_data.h5"
with h5py.File(filename, 'r') as f:
    t_cam = f['camera/timestamp'][:]
    t_motor = f['motor/timestamp'][:]
    motor_pos = f['motor/position'][:]

print("📊 数据加载完毕，开始对齐...")

# 2. 核心算法：构建插值函数
# kind='linear' 线性插值，对于 500Hz 的密集数据足够了
# fill_value="extrapolate" 允许外推 (处理边缘微小的时间差)
interpolator = interp1d(t_motor, motor_pos, kind='linear', fill_value="extrapolate")

# 3. 执行对齐
# 问：在相机拍照的那些时刻 (t_cam)，电机位置应该是多少？
aligned_motor_pos = interpolator(t_cam)

# 4. 验证与可视化 (架构师必须眼见为实)
# 我们画出前 2 秒的数据对比
plt.figure(figsize=(10, 6))

# 画原始高频电机数据 (灰色细线)
plt.plot(t_motor, motor_pos, 'k-', alpha=0.3, label='Raw Motor (500Hz)')

# 画对齐后的数据 (红色圆点)
# 这些点应该完美落在灰色曲线上
plt.plot(t_cam, aligned_motor_pos, 'ro', label='Aligned to Camera (30Hz)')

plt.xlim(0, 2)
plt.title("Data Alignment Verification")
plt.xlabel("Time (s)")
plt.ylabel("Joint Position")
plt.legend()
plt.grid(True)

# 保存图片到本地查看
plt.savefig("alignment_result.png")
print("✅ 对齐完成！结果图已保存为 alignment_result.png")

# (可选) 保存为训练用的 clean_data.h5 ...
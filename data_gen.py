import numpy as np
import h5py
import os

# 1. 模拟参数
DURATION = 10.0 # 采集 10 秒
CAM_FPS = 30    # 相机 30Hz (低频)
MOTOR_FPS = 500 # 电机 500Hz (高频)

# 2. 生成时间戳 (模拟不同步)
# 相机时间戳：从 0 开始，每 0.033s 一帧，加一点点随机抖动
t_cam = np.arange(0, DURATION, 1/CAM_FPS)
t_cam += np.random.normal(0, 0.002, size=len(t_cam)) # 2ms 抖动

# 电机时间戳：从 0.005s 开始 (比相机晚启动)，每 0.002s 一帧
t_motor = np.arange(0.005, DURATION, 1/MOTOR_FPS)

# 3. 生成数据 (模拟一个正弦波运动)
# 假设机器人做了一个正弦摆动：position = sin(2 * pi * t)
# 我们生成"真实"的电机数据
motor_pos = np.sin(2 * np.pi * 0.5 * t_motor) # 0.5Hz 的正弦波

# 模拟相机数据 (这里只存占位符，假设图像里拍到了对应的位置)
# 在真实世界里，这是 jpg 图片；这里我们只存时间戳
cam_data_placeholder = np.zeros((len(t_cam), 224, 224, 3), dtype=np.uint8)

# 4. 存入 HDF5 (模拟 LeRobot/Mobile Aloha 格式)
filename = "raw_data.h5"
with h5py.File(filename, 'w') as f:
    # 存相机
    g_cam = f.create_group('camera')
    g_cam.create_dataset('timestamp', data=t_cam)
    g_cam.create_dataset('image', data=cam_data_placeholder)
    
    # 存电机
    g_motor = f.create_group('motor')
    g_motor.create_dataset('timestamp', data=t_motor)
    g_motor.create_dataset('position', data=motor_pos)

print(f"✅ 生成脏数据: {filename}")
print(f"   相机帧数: {len(t_cam)}, 电机帧数: {len(t_motor)}")
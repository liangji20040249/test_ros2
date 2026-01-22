import h5py
import rerun as rr
import numpy as np
import time

# ==========================================
# 1. 初始化与启动 Web Server
# ==========================================
# 初始化 Recording
rr.init("retail_demo", spawn=False)

# 启动 Web Viewer
# 注意：v0.28+ 移除了 bind_addr，直接指定 web_port
print("🚀 正在启动 Rerun Web Server...")
#rr.serve_web_viewer(web_port=9876, open_browser=False)
rr.serve_web_viewer(web_port=9876, open_browser=False)

print("🌐 请在浏览器访问: http://localhost:9876")

# ==========================================
# 2. 读取数据
# ==========================================
filename = "raw_data.h5"
print(f"📂 读取文件: {filename}")
f = h5py.File(filename, 'r')

t_cam = f['camera/timestamp'][:]
# 模拟彩色噪点图 (H, W, C)
images = np.random.randint(0, 255, (len(t_cam), 224, 224, 3), dtype=np.uint8)

t_motor = f['motor/timestamp'][:]
motor_pos = f['motor/position'][:]

# ==========================================
# 3. 数据流回放 (适配 v0.28+ API)
# ==========================================
print("▶️ 开始回放数据流...")

cam_idx = 0
motor_idx = 0
max_time = max(t_cam[-1], t_motor[-1])

# 为了演示流畅，我们按 0.005s 的步长进行循环
for current_time in np.arange(0, max_time, 0.005):
    
    # --- 关键修复 1: 时间轴设置 ---
    # Rerun 新版对 seconds/nanos 参数支持不稳定
    # 我们采用最稳妥的 "sequence" (序列号) 方式
    # 将时间(秒) * 1000，把 "毫秒" 当作 "步数" 传进去
    # 这样在时间轴上，1000步 = 1秒
    ms_time = int(current_time * 1000)
    rr.set_time(timeline="stable_time_ms", sequence=ms_time)
    
    # --- 关键修复 2: 电机数据 ---
    while motor_idx < len(t_motor) and t_motor[motor_idx] <= current_time:
        pos = motor_pos[motor_idx]
        
        # v0.28+ 移除了 Scalar(单数)，必须用 Scalars(复数)
        # 即使是一个数，也要由列表包裹: [pos]
        rr.log("motor/position", rr.Scalars([pos]))
        
        motor_idx += 1
        
    # --- 关键修复 3: 相机数据 ---
    while cam_idx < len(t_cam) and t_cam[cam_idx] <= current_time:
        img = images[cam_idx]
        
        # Image API 保持相对稳定，直接传入 numpy array
        rr.log("camera/image", rr.Image(img))
        
        cam_idx += 1
        
    # 稍微控制一下发送速度，模拟真实回放 (可选)
    # time.sleep(0.001)

print("✅ 数据发送完毕！请在浏览器查看。")

# 保持脚本运行，否则 Web Server 会断开
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("退出...")
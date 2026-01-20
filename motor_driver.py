import time
import rclpy
from rclpy.lifecycle import Node, State, TransitionCallbackReturn
from std_msgs.msg import String

class MotorDriver(Node):
    def __init__(self):
        super().__init__('motor_driver_lifecycle')
        self.pub = None
        self.timer = None
        print("[System] 驱动程序已启动，等待配置 (Unconfigured)...")

    # 1. 配置阶段 (on_configure)
    def on_configure(self, state: State) -> TransitionCallbackReturn:
        print("[Lifecycle] 正在配置... (模拟连接CAN总线)")
        self.pub = self.create_lifecycle_publisher(String, 'motor_status', 10)
        print("[Lifecycle] 配置完成，进入 Inactive 状态")
        return TransitionCallbackReturn.SUCCESS

    # 2. 激活阶段 (on_activate)
    def on_activate(self, state: State) -> TransitionCallbackReturn:
        print("[Lifecycle] 正在激活... (电机上电)")
        super().on_activate(state)
        # 创建定时器，每秒发一次
        self.timer = self.create_timer(1.0, self.publish_status)
        return TransitionCallbackReturn.SUCCESS

    # 3. 停用阶段 (on_deactivate)
    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        print("[Lifecycle] 正在停用... (电机下电)")
        if self.timer:
            self.timer.cancel()
            self.destroy_timer(self.timer)
        super().on_deactivate(state)
        return TransitionCallbackReturn.SUCCESS

    # 4. 清理阶段 (on_cleanup)
    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        print("[Lifecycle] 正在清理... (断开连接)")
        self.destroy_publisher(self.pub)
        return TransitionCallbackReturn.SUCCESS

    def publish_status(self):
        msg = String()
        msg.data = f"Motor Running... Time: {time.time():.2f}"
        self.pub.publish(msg)
        print(f"📤 发送: {msg.data}")

def main():
    rclpy.init()
    node = MotorDriver()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

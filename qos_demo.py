import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

class QoSDemoNode(Node):
    def __init__(self, mode='publisher'):
        super().__init__('qos_demo_node')
        self.mode = mode

        # ================= QoS 策略定义 =================
        
        # 策略 A: "控制指令" (Reliable - 可靠)
        # 类似于 TCP：发出去的包，对方必须收到 ACK，否则重发。
        # 适用：急停、目标点、状态切换
        qos_control = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )

        # 策略 B: "传感器流" (Best Effort - 尽力而为)
        # 类似于 UDP：发出去就不管了。如果网络堵了，这就丢包。
        # 适用：雷达、图像、高频关节数据
        qos_sensor = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        # ================= 业务逻辑 =================

        if self.mode == 'publisher':
            # 创建发布者
            self.pub_cmd = self.create_publisher(String, 'robot_cmd', qos_control)
            self.pub_stream = self.create_publisher(Int32, 'sensor_stream', qos_sensor)
            
            self.timer = self.create_timer(0.5, self.publish_data)
            self.counter = 0
            print("[Publisher] 开始发送数据...")

        elif self.mode == 'subscriber':
            # 创建订阅者
            self.sub_cmd = self.create_subscription(
                String, 'robot_cmd', self.cmd_callback, qos_control)
            
            # 注意：订阅者的 QoS 必须兼容发布者！
            # 如果发布者是 Best Effort，订阅者必须也是 Best Effort。
            self.sub_stream = self.create_subscription(
                Int32, 'sensor_stream', self.stream_callback, qos_sensor)
            
            print("[Subscriber] 开始监听数据...")

    def publish_data(self):
        self.counter += 1
        
        # 1. 发送关键指令
        cmd_msg = String()
        cmd_msg.data = f"CMD_SEQ_{self.counter} (不可丢)"
        self.pub_cmd.publish(cmd_msg)
        
        # 2. 发送传感器流 (模拟)
        stream_msg = Int32()
        stream_msg.data = self.counter
        self.pub_stream.publish(stream_msg)
        
        print(f"📤 发出: {cmd_msg.data} | 传感器帧: {stream_msg.data}")

    def cmd_callback(self, msg):
        print(f"   ✅ [指令通道] 收到: {msg.data}")

    def stream_callback(self, msg):
        print(f"   🌊 [数据通道] 收到帧: {msg.data}")

def main():
    import sys
    rclpy.init()
    
    # 根据命令行参数决定是发还是收
    # 运行方式: python3 qos_demo.py pub  或者  python3 qos_demo.py sub
    mode = 'publisher'
    if len(sys.argv) > 1 and sys.argv[1] == 'sub':
        mode = 'subscriber'
        
    node = QoSDemoNode(mode)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

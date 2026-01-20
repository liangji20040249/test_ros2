from launch import LaunchDescription
from launch.actions import ExecuteProcess, LogInfo, TimerAction
from launch.substitutions import FindExecutable

def generate_launch_description():
    
    # 1. 定义核心路径 (Docker 内部路径)
    workspace_path = '/root/workspace/test_ros2'
    
    # 2. 定义要启动的节点
    
    # 节点 A: 电机驱动 (Lifecycle Node)
    motor_node = ExecuteProcess(
        cmd=['python3', '-u',f'{workspace_path}/motor_driver.py'],
        output='screen',
        name='motor_process'
    )
    
    # 节点 B: 业务逻辑 (QoS Demo Publisher)
    business_node = ExecuteProcess(
        cmd=['python3', '-u',f'{workspace_path}/qos_demo.py', 'pub'],
        output='screen',
        name='business_process'
    )

    # 3. 定义生命周期管理指令 (The Orchestrator)
    # 架构师思维：我们不手动敲命令，而是让脚本按时间轴自动触发
    
    # 动作：配置 (Configure)
    configure_cmd = ExecuteProcess(
        cmd=['ros2', 'lifecycle', 'set', '/motor_driver_lifecycle', 'configure'],
        output='screen'
    )

    # 动作：激活 (Activate)
    activate_cmd = ExecuteProcess(
        cmd=['ros2', 'lifecycle', 'set', '/motor_driver_lifecycle', 'activate'],
        output='screen'
    )

    # 4. 组装启动流程 (Timeline)
    return LaunchDescription([
        LogInfo(msg="[System] 零售机器人系统正在启动..."),
        
        # 立即启动两个节点
        motor_node,
        business_node,
        
        # 延时 3秒 后，执行配置 (模拟硬件自检时间)
        TimerAction(
            period=3.0,
            actions=[
                LogInfo(msg="[Orchestrator] 正在配置电机驱动..."),
                configure_cmd
            ]
        ),
        
        # 再延时 2秒 (总计5秒) 后，执行激活 (模拟系统就绪)
        TimerAction(
            period=5.0,
            actions=[
                LogInfo(msg="[Orchestrator] 系统就绪，激活电机输出！"),
                activate_cmd
            ]
        )
    ])

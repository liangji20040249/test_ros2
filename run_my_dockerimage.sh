docker run -it --name ros2_dev \
    --network host \
    --ipc host \
    -v ~/Documents/robot_workspace:/root/workspace \
    my_robot_env:v1.0

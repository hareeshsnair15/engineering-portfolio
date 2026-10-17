import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, LifecycleNode
import lifecycle_msgs.msg

def generate_launch_description():
    # Package directories
    trolley_slam_share = get_package_share_directory('trolley_slam')
    ydlidar_driver_share = get_package_share_directory('ydlidar_ros2_driver')
    slam_toolbox_share = get_package_share_directory('slam_toolbox')

    # Launch Configurations
    params_file = LaunchConfiguration('params_file')
    slam_params_file = LaunchConfiguration('slam_params_file')
    open_rviz = LaunchConfiguration('open_rviz')

    # Declare launch arguments
    declare_params_file = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(ydlidar_driver_share, 'params', 'X2.yaml'),
        description='Path to the ROS2 parameters file for YDLidar X2'
    )

    declare_slam_params_file = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(trolley_slam_share, 'config', 'mapper_params_online_async.yaml'),
        description='Path to the slam_toolbox parameters file'
    )

    declare_open_rviz = DeclareLaunchArgument(
        'open_rviz',
        default_value='true',
        description='Whether to launch RViz2 for visualization'
    )

    # 1. Include trolley description (URDF, state publishers)
    trolley_description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(trolley_slam_share, 'launch', 'trolley_description.launch.py')
        )
    )

    # 2. Launch YDLidar X2 driver node (as a LifecycleNode)
    ydlidar_driver_node = LifecycleNode(
        package='ydlidar_ros2_driver',
        executable='ydlidar_ros2_driver_node',
        name='ydlidar_ros2_driver_node',
        output='screen',
        emulate_tty=True,
        parameters=[params_file],
        namespace='/'
    )

    # 3. Automatic transition of YDLidar LifecycleNode trigger
    # Wait for node to start, then configure and activate it
    lifecycle_trigger = ExecuteProcess(
        cmd=['bash', '-c', 
             'sleep 2 && ros2 lifecycle set /ydlidar_ros2_driver_node configure && ros2 lifecycle set /ydlidar_ros2_driver_node activate'],
        output='screen'
    )

    # 4. Dummy transform publisher for odom -> base_footprint (for lidar SLAM mapping without wheel encoders)
    dummy_odom_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_pub_odom',
        arguments=['0', '0', '0', '0', '0', '0', '1', 'odom', 'base_footprint'],
        output='screen'
    )

    # 5. Parallel launch of slam_toolbox in online_async mode
    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_toolbox_share, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'slam_params_file': slam_params_file,
            'use_sim_time': 'false'
        }.items()
    )

    # 6. Launch RViz2 configured with SLAM visualization (if display is present)
    from launch.conditions import IfCondition
    rviz_config = os.path.join(trolley_slam_share, 'config', 'trolley.rviz')
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen',
        condition=IfCondition(open_rviz)
    )

    return LaunchDescription([
        declare_params_file,
        declare_slam_params_file,
        declare_open_rviz,
        trolley_description_launch,
        ydlidar_driver_node,
        lifecycle_trigger,
        dummy_odom_tf_node,
        slam_toolbox_launch,
        rviz2_node
    ])

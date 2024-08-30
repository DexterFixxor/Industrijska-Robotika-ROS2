import os
import pathlib
import yaml
import launch
from launch.substitutions.path_join_substitution import PathJoinSubstitution
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.urdf_spawner import URDFSpawner, get_webots_driver_node  
from webots_ros2_driver.webots_controller import WebotsController
from webots_ros2_driver.webots_launcher import WebotsLauncher
from launch.event_handlers.on_process_start import OnProcessStart
from launch.event_handlers.on_process_io import OnProcessIO

def generate_launch_description():
    package_dir = get_package_share_directory("webots_ros2_panda")
    robot_description_path = os.path.join(package_dir, 'resource', 'panda.urdf')
    ros2_control_params = os.path.join(package_dir, 'config', 'ros2_controllers.yaml')

    panda_robot_driver = WebotsController(
        robot_name="Panda",
        parameters=[
            {'robot_description': robot_description_path},
            {'use_sim_time': True},
            {'set_robot_state_publisher': False},
            ros2_control_params
        ],
    )
 
    with open(robot_description_path, 'r') as infp:
        robot_desc = infp.read()

    spawn_robot = URDFSpawner(
        name='panda',
        urdf_path=robot_description_path,
        robot_description=robot_desc
    )
    

    controller_manager_timeout = ['--controller-manager-timeout', '100']
    controller_manager_prefix = 'python.exe' if os.name == 'nt' else ''
    trajectory_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        prefix=controller_manager_prefix,
        arguments=['panda_arm_controller', '-c', 'controller_manager'] + controller_manager_timeout,
        parameters=[{"use_sim_time": True}]
    )
    
    gripper_trajectory_controller = Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        prefix=controller_manager_prefix,
        arguments=['hand_controller', '-c', 'controller_manager'] + controller_manager_timeout,
        parameters=[{"use_sim_time": True}]
    )


    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        prefix=controller_manager_prefix,
        arguments=['joint_state_broadcaster', '-c', 'controller_manager'] + controller_manager_timeout,
        parameters=[{"use_sim_time": True}]
    )
    

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True
        }],
        arguments=[robot_description_path]
    )
    
        # Static TF
    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "world", "base_link"],
    )
    
    return LaunchDescription([
        
        #spawn_robot,
        panda_robot_driver,
        robot_state_publisher,
        static_tf,
        
        trajectory_controller_spawner,
        gripper_trajectory_controller,
        joint_state_broadcaster_spawner,

         # Kill all the nodes when the driver node is shut down
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=panda_robot_driver,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        ),
        
    ])

# ros2 action send_goal panda_arm_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{
#   trajectory: {
#     joint_names: [panda_joint1, panda_joint2, panda_joint3, panda_joint4, panda_joint5, panda_joint6, panda_joint7],                     
#     points: [
#       { positions: [0.1, -0.7853981633974483, 0, -2.356194490192345, 0, 1.5707963267948966, 0.7853981633974483], time_from_start: { sec: 5, nanosec: 500 } },
#       { positions: [-0.5, -0.7853981633974483, 0, -2.356194490192345, 0, 1.5707963267948966, 0.7853981633974483], time_from_start: { sec: 15, nanosec: 500 } },
#       { positions: [0.1, -0.7853981633974483, 0, -2.356194490192345, 0, 1.5707963267948966, 0.7853981633974483], time_from_start: { sec: 25, nanosec: 500 } }
#     ]
#   },
#   goal_tolerance: [
#     { name: panda_joint1, position: 0.0 },
#     { name: panda_joint2, position: -0.7853981633974483 },
#     { name: panda_joint3, position: 0.0 },
#     { name: panda_joint4, position: -2.356194490192345 },
#     { name: panda_joint5, position: 0.0 },
#     { name: panda_joint6, position: 1.5707963267948966 }, 
#     { name: panda_joint7, position: 0.7853981633974483 }, 
#     { name: panda_finger::left, position: 0.1 }, 
#     { name: panda_finger::right, position: 0.1 },
#   ]
# }"

# ros2 action send_goal panda_hand_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{
#   trajectory: {
#     joint_names: [panda_finger::left, panda_finger::right],                     
#     points: [
#       { positions: [0.04, 0.04], time_from_start: { sec: 5, nanosec: 500 } },
#       { positions: [0.0, 0.0], time_from_start: { sec: 15, nanosec: 500 } },
#       { positions: [0.04, 0.04], time_from_start: { sec: 25, nanosec: 500 } }
#     ]
#   }
# }"


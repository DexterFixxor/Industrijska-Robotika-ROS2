import os
import pathlib
import yaml
from launch.actions import IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory, get_packages_with_prefixes


PACKAGE_NAME = 'webots_ros2_panda'
USE_SIM_TIME = True

def generate_launch_description():
    launch_description_nodes = []
    package_dir = get_package_share_directory(PACKAGE_NAME)

    def load_file(filename):
        return pathlib.Path(os.path.join(package_dir, 'resource', filename)).read_text()

    def load_yaml(filename):
        return yaml.safe_load(load_file(filename))
    
    
    launch_description_nodes.append(
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(package_dir, 'launch', 'robot_nodes.py'))
            )
        )
    
    # Configuration
    urdf_path = os.path.join(package_dir, 'resource', 'panda.urdf')
    srdf_path = os.path.join(package_dir, 'config', 'panda.srdf')
    kinematics_config = os.path.join(package_dir, 'config', 'kinematics.yaml')

    description = {'robot_description': load_file(urdf_path)}
    description_semantic = {'robot_description_semantic': load_file(srdf_path)}
    description_kinematics = {'robot_description_kinematics': load_yaml(kinematics_config)}
    sim_time = {'use_sim_time': USE_SIM_TIME}
    
    # Rviz node
    rviz_config_file = os.path.join(package_dir, 'config', 'moveit.rviz')
    
    launch_description_nodes.append(
            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                arguments=['-d', rviz_config_file],
                parameters=[
                    description,
                    description_semantic,
                    description_kinematics,
                    sim_time
                ],
            )
        )
    
     # MoveIt2 node
     
    movegroup_config = os.path.join(package_dir, 'config', 'moveit_movegroup.yaml')
    moveit_controllers_config = os.path.join(package_dir, 'config', 'moveit_controllers.yaml')

    movegroup = {'move_group': load_yaml(movegroup_config)}
    moveit_controllers = {
            'moveit_controller_manager': 'moveit_simple_controller_manager/MoveItSimpleControllerManager',
            'moveit_simple_controller_manager': load_yaml(moveit_controllers_config)
        }

    launch_description_nodes.append(
            Node(
                package='moveit_ros_move_group',
                executable='move_group',
                output='screen',
                parameters=[
                    description,
                    description_semantic,
                    description_kinematics,
                    moveit_controllers,
                    movegroup,
                    sim_time
                ]
            )
        )

    return LaunchDescription(launch_description_nodes)

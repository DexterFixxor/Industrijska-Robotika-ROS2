
import launch
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions.path_join_substitution import PathJoinSubstitution
from webots_ros2_driver.webots_launcher import WebotsLauncher


def generate_launch_description():
    
    package_dir = get_package_share_directory('webots_ros2_panda')
    world = LaunchConfiguration('world')

    # Starts Webots
    webots = WebotsLauncher(world=PathJoinSubstitution([package_dir, 'worlds', world]) ,ros2_supervisor=True)

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='empty.wbt',
            description='Choose one of the world files from `/webots_ros2_panda/worlds` directory'
        ),
        webots,
        webots._supervisor,
        # This action will kill all nodes once the Webots simulation has exited
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    node_list = []
    
    node1 = Node(
        executable="my_node",
        package="my_package",
        name="Proba1",
        namespace="ns1"
    )
    
    node2= Node(
        executable="my_node",
        package="my_package",
        name="Proba2",
        namespace="ns2"
    )
    
    node_list = [ node1, node2]
    
    return LaunchDescription(node_list)

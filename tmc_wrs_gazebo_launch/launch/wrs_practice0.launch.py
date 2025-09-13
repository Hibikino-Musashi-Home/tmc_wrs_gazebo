#!/usr/bin/env python3
# -*-encoding:UTF-8-*-

# Auther: Tomoaki Fujino (Hibikino-Musashi@Home)

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchContext, LaunchDescription

from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from hsrb_launch_utils.hsrb_launch_utils import declare_launch_arguments


def declare_arguments():
    declared_arguments: list = declare_launch_arguments()

    declared_arguments.append(DeclareLaunchArgument("highrtf", default_value="false"))
    declared_arguments.append(DeclareLaunchArgument("seed", default_value="1"))
    declared_arguments.append(
        DeclareLaunchArgument(
            "world_suffix",
            default_value="",
            condition=UnlessCondition(LaunchConfiguration("fast_physics")),
        ),
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "world_suffix",
            default_value="_fast",
            condition=IfCondition(LaunchConfiguration("fast_physics")),
        ),
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "world_suffix2",
            default_value="",
            condition=UnlessCondition(LaunchConfiguration("highrtf")),
        ),
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "world_suffix2",
            default_value="_highrtf",
            condition=IfCondition(LaunchConfiguration("highrtf")),
        ),
    )

    # Default comment out --------------------------------------------------------

    # declared_arguments.append(
    #     DeclareLaunchArgument(
    #         "use_camera_control",
    #         default_value="false",
    #         description="Whether to launch tidy camera controller",
    #     ),
    # )

    # ----------------------------------------------------------------------------

    return declared_arguments


def generate_launch_description():
    args = {}
    for arg in declare_arguments():
        args[arg.name] = LaunchConfiguration(arg.name)

    hsrb_gazebo_common_path = os.path.join(
        get_package_share_directory("hsrb_gazebo_launch"),
        "launch/include/hsrb_gazebo_common.launch.py",
    )

    # Default comment out --------------------------------------------------------

    # common_path = os.path.join(
    #     get_package_share_directory("common_launch_dir"),
    #     "launch/common.launch.py",
    # )

    # ----------------------------------------------------------------------------

    tmc_wrs_gazebo_worlds_dir = get_package_share_directory("tmc_wrs_gazebo_worlds")

    # Static launch_arguments are defined here.
    launch_arg_info = {
        "map": os.path.join(
            get_package_share_directory("tmc_wrs_gazebo_worlds"),
            "maps/wrs2020/map.yaml",
        ),
        "robot_pos_x": "-2.1",
        "robot_pos_y": "1.2",
        "robot_pos_z": "0.0",
        "robot_rpy_Y": "-1.57",
    }

    hsrb_gazebo_common = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(hsrb_gazebo_common_path),
        launch_arguments={
            **launch_arg_info,
            **{
                "world_name": os.path.join(
                    tmc_wrs_gazebo_worlds_dir,
                    "worlds/wrs2020.world",
                ),
            },
        }.items(),
        condition=UnlessCondition(LaunchConfiguration("fast_physics")),
    )

    hsrb_gazebo_common_fast = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(hsrb_gazebo_common_path),
        launch_arguments={
            **launch_arg_info,
            **{
                "world_name": os.path.join(
                    tmc_wrs_gazebo_worlds_dir,
                    "worlds/wrs2020_fast_highrtf.world",
                ),
            },
        }.items(),
        condition=IfCondition(LaunchConfiguration("fast_physics")),
    )

    bridge_spawn_entity_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="bridge_spawn_entity",
        output="screen",
        arguments=[
            "/world/default/create@ros_gz_interfaces/srv/SpawnEntity",
            "/world/default/remove@ros_gz_interfaces/srv/DeleteEntity",
            "/world/default/set_pose@ros_gz_interfaces/srv/SetEntityPose",
        ],
        remappings=[
            ("/world/default/create", "/spawn_entity"),
            ("/world/default/remove", "/delete_entity"),
            ("/world/default/set_pose", "/set_entity_pose"),
        ],
    )

    spawn_objects = Node(
        package="tmc_wrs_gazebo_worlds",
        executable="spawn_objects",
        name="spawn_objects",
        arguments=["--seed", LaunchConfiguration("seed")],
        output="screen",
    )

    # Default comment out --------------------------------------------------------

    # camera_controller_node = Node(
    #     package="hsrb_gazebo_task_evaluators",
    #     executable="hhcc_tidy_camera_controller",
    #     name="camera_controller",
    #     output="screen",
    #     condition=IfCondition(LaunchConfiguration("use_camera_control")),
    # )

    # toys_in_trofase_detector_node = (
    #     Node(
    #         package="hsrb_gazebo_task_evaluators",
    #         executable="object_in_box_detector",
    #         name="toys_in_trofase_detector",
    #         output="screen",
    #         parameters=[
    #             {"box_name": "trofase"},
    #             {"box_size": [0.35, 0.21, 0.25]},
    #             {"box_pose": [0, 0, 0.125]},
    #             {"object_names": ["toy*"]},
    #         ],
    #     ),
    # )

    # dishes_in_sink_detector_node = (
    #     Node(
    #         package="hsrb_gazebo_task_evaluators",
    #         executable="object_in_box_detector",
    #         name="dishes_in_sink_detector",
    #         output="screen",
    #         parameters=[
    #             {"box_name": "sink::dishwasher_link"},
    #             {"box_size": [0.47, 0.36, 0.32]},
    #             {"box_pose": [-0.315, 0, 0.31]},
    #             {"object_names": ["dish*"]},
    #             {"target_axes": [0, 1, 0]},
    #             {"allow_degree": 45},
    #             {"both_direction": 1},
    #         ],
    #     ),
    # )

    # teacups_in_sink_detector_node = (
    #     Node(
    #         package="hsrb_gazebo_task_evaluators",
    #         executable="object_in_box_detector",
    #         name="teacups_in_sink_detector",
    #         output="screen",
    #         parameters=[
    #             {"box_name": "sink::dishwasher_link"},
    #             {"box_size": [0.47, 0.36, 0.32]},
    #             {"box_pose": [-0.315, 0, 0.31]},
    #             {"object_names": ["teacup*"]},
    #             {"target_axes": [0, 0, -1]},
    #         ],
    #     ),
    # )

    # cellphone_in_wagon_detector_node = (
    #     Node(
    #         package="hsrb_gazebo_task_evaluators",
    #         executable="object_in_box_detector",
    #         name="cellphone_in_wagon_detector",
    #         output="screen",
    #         parameters=[
    #             {"box_name": "wagon::top_center_drawer_link"},
    #             {"box_size": [0.40, 0.456, 0.30]},
    #             {"box_pose": [-0.2, 0.608, 0.9]},
    #             {"object_names": ["cellphone"]},
    #             {"object_axes": [1, 0, 0]},
    #             {"target_axes": [1, 0, 0]},
    #             {"both_direction": 1},
    #             {"target_position": [-0.2, 0.608, 0.757]},
    #         ],
    #     ),
    # )

    # remocon_in_wagon_detector_node = (
    #     Node(
    #         package="hsrb_gazebo_task_evaluators",
    #         executable="object_in_box_detector",
    #         name="remocon_in_wagon_detector",
    #         output="screen",
    #         parameters=[
    #             {"box_name": "wagon::top_center_drawer_link"},
    #             {"box_size": [0.40, 0.456, 0.30]},
    #             {"box_pose": [-0.2, 0.608, 0.9]},
    #             {"object_names": ["remocon"]},
    #             {"object_axes": [1, 0, 0]},
    #             {"target_axes": [1, 0, 0]},
    #             {"both_direction": 1},
    #             {"target_position": [-0.2, 0.508, 0.757]},
    #         ],
    #     ),
    # )

    # stapler_in_wagon_detector_node = Node(
    #     package="hsrb_gazebo_task_evaluators",
    #     executable="object_in_box_detector",
    #     name="stapler_in_wagon_detector",
    #     output="screen",
    #     parameters=[
    #         {"box_name": "wagon::top_center_drawer_link"},
    #         {"box_size": [0.40, 0.456, 0.30]},
    #         {"box_pose": [-0.2, 0.608, 0.9]},
    #         {"object_names": ["stapler"]},
    #         {"object_axes": [0, 1, 0]},
    #         {"target_axes": [1, 0, 0]},
    #         {"both_direction": 1},
    #         {"target_position": [-0.2, 0.708, 0.757]},
    #     ],
    # )

    # ----------------------------------------------------------------------------

    return LaunchDescription(
        declare_arguments()
        + [
            hsrb_gazebo_common,
            hsrb_gazebo_common_fast,
            bridge_spawn_entity_node,
            spawn_objects,
        ]
    )

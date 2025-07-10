#!/usr/bin/env python3
# -*-encoding:UTF-8-*-

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription

from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def declare_arguments():
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "score_bag",
            default_value=os.path.join(
                get_package_share_directory("hsrb_wrs_gazebo_launch"),
                "score/score",
                description="Save path for score bag",
            ),
        ),
    )

    return declared_arguments


def generate_launch_description():

    # Node(
    #     package="hsrb_gazebo_task_evaluators",
    #     executable="undesired_contact_detector",
    #     name="undesired_contact_detector",
    #     output="screen",
    #     parameters=[
    #         {"target_model_name": "hsrb"},
    #         {"except_model_names": ["gplane", "block*"]}
    #     ]
    # ),

    hsrb_gazebo_task_evaluators_node = Node(
        package="hsrb_gazebo_task_evaluators",
        executable="hhcc_score_counter",
        name="hhcc_score_counter",
        output="screen",
        parameters=[
            {"per_cleaned_object": 100},
            {"collision_per_second": -1},
        ],
    )

    ros2_bag_record_cmd = ExecuteProcess(
        cmd=[
            "ros2",
            "bag",
            "record",
            "-o",
            LaunchConfiguration('score_bag'),
        ],
        name="record_score",
        output="screen",
    )

    # Node(
    #     package='hsrb_gazebo_task_evaluators',
    #     executable='record_gazebo_stat',
    #     name='record_gazebo_stat',
    #     output='screen',
    #     arguments=['gazebo-stat.log']
    # ),

    return LaunchDescription(
        declare_arguments()
        + [
            hsrb_gazebo_task_evaluators_node,
            ros2_bag_record_cmd,
        ],
    )

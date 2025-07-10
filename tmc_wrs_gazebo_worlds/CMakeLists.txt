cmake_minimum_required(VERSION 3.8)
project(tmc_wrs_gazebo_worlds)

###############################################################################
# Compiler settings
###############################################################################
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

###############################################################################
# Dependencies
###############################################################################
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)   # <-- For Python package install
find_package(xacro REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)

###############################################################################
# Python helpers
###############################################################################
# Install the entire Python package under src/${PROJECT_NAME}
ament_python_install_package(${PROJECT_NAME})

# Stand‑alone executable scripts (ROS 2 entry‑points via ros2 run)
install(PROGRAMS
  scripts/spawn_object.py
  DESTINATION lib/${PROJECT_NAME}
)

###############################################################################
# World generation (unchanged)
###############################################################################
file(GLOB _world_xacros "${PROJECT_SOURCE_DIR}/worlds/*.world.xacro")
file(GLOB_RECURSE _component_xacros "${PROJECT_SOURCE_DIR}/worlds/include/*.xacro")

if(ROS1)
  set(_cmd_xacro_start "${CATKIN_DEVEL_PREFIX}/env.sh rosrun xacro xacro")
  set(_cmd_xacro_end "")
else()
  set(_cmd_xacro_start "/opt/ros/$ENV{ROS_DISTRO}/bin/xacro")
  set(_cmd_xacro_end "")
endif()

# Generate world files from each *.world.xacro files.
foreach(_xacro ${_world_xacros})
  get_filename_component(_dir ${_xacro} PATH)
  get_filename_component(_name ${_xacro} NAME_WE)

  set(_default_world ${_dir}/${_name}.world)
  set(_default_highrtf_world ${_dir}/${_name}_highrtf.world)
  set(_fast_world ${_dir}/${_name}_fast.world)
  set(_fast_highrtf_world ${_dir}/${_name}_fast_highrtf.world)
  set(_default_knob_world ${_dir}/${_name}_knob.world)
  set(_default_highrtf_knob_world ${_dir}/${_name}_highrtf_knob.world)
  set(_fast_knob_world ${_dir}/${_name}_fast_knob.world)
  set(_fast_highrtf_knob_world ${_dir}/${_name}_fast_highrtf_knob.world)

  add_custom_command(
    OUTPUT ${_default_world}
    DEPENDS ${_xacro} ${_component_xacros}
    COMMAND xacro ${_xacro} fast_physics:=false highrtf:=false trofast_knob:=false > ${_default_world})
  add_custom_command(
    OUTPUT ${_default_highrtf_world}
    DEPENDS ${_xacro} ${_component_xacros}
    COMMAND xacro ${_xacro} fast_physics:=false highrtf:=true trofast_knob:=false > ${_default_highrtf_world})
  add_custom_command(
    OUTPUT ${_fast_world}
    DEPENDS ${_xacro} ${_component_xacros}
    COMMAND xacro ${_xacro} fast_physics:=true highrtf:=false trofast_knob:=false > ${_fast_world})
  add_custom_command(
    OUTPUT ${_fast_highrtf_world}
    DEPENDS ${_xacro} ${_component_xacros}
    COMMAND xacro ${_xacro} fast_physics:=true highrtf:=true trofast_knob:=false > ${_fast_highrtf_world})

  add_custom_command(
    OUTPUT ${_default_knob_world}
    DEPENDS ${_xacro} ${_component_xacros}
    COMMAND xacro ${_xacro} fast_physics:=false highrtf:=false trofast_knob:=true > ${_default_knob_world})
  add_custom_command(
    OUTPUT ${_default_highrtf_knob_world}
    DEPENDS ${_xacro} ${_component_xacros}
    COMMAND xacro ${_xacro} fast_physics:=false highrtf:=true trofast_knob:=true > ${_default_highrtf_knob_world})
  add_custom_command(
    OUTPUT ${_fast_knob_world}
    DEPENDS ${_xacro} ${_component_xacros}
    COMMAND xacro ${_xacro} fast_physics:=true highrtf:=false trofast_knob:=true > ${_fast_knob_world})
  add_custom_command(
    OUTPUT ${_fast_highrtf_knob_world}
    DEPENDS ${_xacro} ${_component_xacros}
    COMMAND xacro ${_xacro} fast_physics:=true highrtf:=true trofast_knob:=true > ${_fast_highrtf_knob_world})

  add_custom_target(${PROJECT_NAME}_${_name}_gen_default_world ALL DEPENDS ${_default_world})
  add_custom_target(${PROJECT_NAME}_${_name}_gen_default_highrtf_world ALL DEPENDS ${_default_highrtf_world})
  add_custom_target(${PROJECT_NAME}_${_name}_gen_fast_world ALL DEPENDS ${_fast_world})
  add_custom_target(${PROJECT_NAME}_${_name}_gen_fast_highrtf_world ALL DEPENDS ${_fast_highrtf_world})
  add_custom_target(${PROJECT_NAME}_${_name}_gen_default_knob_world ALL DEPENDS ${_default_knob_world})
  add_custom_target(${PROJECT_NAME}_${_name}_gen_default_highrtf_knob_world ALL DEPENDS ${_default_highrtf_knob_world})
  add_custom_target(${PROJECT_NAME}_${_name}_gen_fast_knob_world ALL DEPENDS ${_fast_knob_world})
  add_custom_target(${PROJECT_NAME}_${_name}_gen_fast_highrtf_knob_world ALL DEPENDS ${_fast_highrtf_knob_world})
endforeach()

###############################################################################
# Runtime resources
###############################################################################
install(
  DIRECTORY models
  DESTINATION share/${PROJECT_NAME})

install(
  DIRECTORY worlds
  DESTINATION share/${PROJECT_NAME}
  FILES_MATCHING PATTERN "*.world"
  PATTERN "include" EXCLUDE)

###############################################################################

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/env-hooks/${PROJECT_NAME}.dsv.in")

ament_package()

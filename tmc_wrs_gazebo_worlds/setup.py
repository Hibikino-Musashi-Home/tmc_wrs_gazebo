from setuptools import setup

package_name = "tmc_wrs_gazebo_worlds"

setup(
    name=package_name,
    version="1.0.0",
    packages=[package_name],
    package_dir={"": "src"},
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="HSR Support",
    maintainer_email="xr-hsr-support@mail.toyota.co.jp",
    description="WRS Gazebo world Python support",
    license="BSD 3-clause Clear License",
    entry_points={
        "console_scripts": [
            "spawn_objects = tmc_wrs_gazebo_worlds.spawn_objects:main",
        ],
    },
)

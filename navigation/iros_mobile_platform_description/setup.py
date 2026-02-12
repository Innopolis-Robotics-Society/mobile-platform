from setuptools import find_packages, setup
import os
from glob import glob

package_name = "iros_mobile_platform_description"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            "share/" + package_name + "/launch",
            glob(os.path.join("launch", "*.launch.py")),
        ),
        (
            os.path.join("share", package_name, "description"),
            glob(os.path.join("description", "*xacro")),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="vscode",
    maintainer_email="e.shlomov@innopolis.university",
    description="Package with iros_mobile_platform robot description",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "odom_publisher = description.odom_publisher:main",
            "cmd_to_odom = description.cmd_to_odom:main",
	],
    },
)

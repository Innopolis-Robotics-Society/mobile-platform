from setuptools import find_packages, setup
import os
from glob import glob

package_name = "path_planner"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "maps"), glob("maps/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="rizo",
    maintainer_email="m.maribjonov@innopilis.university",
    description="TODO: Package description",
    license="TODO: License declaration",
    entry_points={
        "console_scripts": [],
    },
)

from setuptools import find_packages, setup
import os
from glob import glob


package_name = "overlord100_simulation"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            glob(os.path.join("launch", "*")),
        ),
        (
            os.path.join("share", package_name, "description"),
            glob(os.path.join("description", "*xacro")),
        ),
        (
            os.path.join("share", package_name, "worlds"),
            glob(os.path.join("worlds", "*")),
        ),
        (
            os.path.join("share", package_name, "models"),
            glob(os.path.join("models", "*")),
        ),
        (
            os.path.join("share", package_name, "rviz"),
            glob("rviz/simulator.rviz"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Overlord100_simulation_team",
    maintainer_email="e.shlomov@innopolis.university",
    description="This package contains data for simulating the Overlord 100 mobile platform, but third-party products can also be launched through launch options",
    license="MIT",
    tests_require=["pytest", "unittest"],
    entry_points={
        "console_scripts": ["converter = overlord100_simulation.converter:main"],
    },
)

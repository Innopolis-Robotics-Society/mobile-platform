import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'iros_mobile_platform_database'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools', 'pymongo', 'pyyaml', 'Pillow'],
    zip_safe=True,
    maintainer='dom-iva',
    maintainer_email='i.domrachev@innopolis.university',
    description='A ROS2 package to manage maps, points, and routes in a MongoDB database.',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'database_node = iros_mobile_platform_database.database_node:main',
            'database_test = iros_mobile_platform_database.database_test_client:main',
        ],
    },
)

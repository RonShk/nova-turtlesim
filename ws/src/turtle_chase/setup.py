import os
from glob import glob
from setuptools import setup

package_name = 'turtle_chase'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # This line is what makes `ros2 launch` able to find them:
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ron Shaked',
    maintainer_email='ronshaked07@gmail.com',
    description='Turtlesim chase demo for Nova UTD onboarding',
    license='MIT',
    entry_points={
        'console_scripts': [
            'mode_node = turtle_chase.mode_node:main',
            'chase_node = turtle_chase.chase_node:main',
            'mouse_node = turtle_chase.mouse_node:main',
        ],
    },
)
